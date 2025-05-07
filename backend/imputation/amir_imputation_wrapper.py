from mealpy import FloatVar, BinaryVar, SCA, GWO
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import time
import traceback

# Paramètres par défaut pour les algorithmes (peuvent être réduits pour des tests plus rapides)
DEFAULT_EPOCH_SCA = 10  # Réduit par rapport à l'original pour des tests plus rapides
DEFAULT_POP_SCA = 10
DEFAULT_EPOCH_GWO = 5
DEFAULT_POP_GWO = 5

def amir_sca_gwo_impute_main(df_original: pd.DataFrame, 
                             epoch_sca=DEFAULT_EPOCH_SCA, pop_sca=DEFAULT_POP_SCA, 
                             epoch_gwo=DEFAULT_EPOCH_GWO, pop_gwo=DEFAULT_POP_GWO):
    start_time = time.time()
    
    if df_original.shape[1] < 2:
        raise ValueError("Le DataFrame doit avoir au moins deux colonnes (une feature, une cible).")

    data_np = df_original.to_numpy()
    # Supposons que la dernière colonne est la cible, les autres sont des features
    features_original_np = data_np[:, :-1].copy()
    target_np = data_np[:, -1]
    
    original_feature_columns = df_original.columns[:-1].tolist()
    original_target_column = df_original.columns[-1]

    nan_indices_in_features = np.argwhere(np.isnan(features_original_np))

    if len(nan_indices_in_features) == 0:
        duree = time.time() - start_time
        return {
            'dataset_imputed': df_original.to_json(orient='split'),
            'missing_mask': df_original.isnull().values.tolist(),
            'accuracy': 1.0, # Ou None, car aucune imputation n'a été évaluée de cette manière
            'metrics': {"message": "Aucune valeur NaN trouvée dans les features."},
            'duree': f"{duree:.2f}s",
            'selected_features_mask': [True] * features_original_np.shape[1] # Toutes features sélectionnées
        }

    complete_rows_mask = ~np.isnan(features_original_np).any(axis=1)
    
    if not np.any(complete_rows_mask):
        raise ValueError("Aucune ligne complète trouvée dans les features pour ajuster le scaler ou le modèle KNN.")

    scaler = StandardScaler()
    scaler.fit(features_original_np[complete_rows_mask])
    
    # Bornes pour l'optimisation SCA (sur les valeurs non normalisées des NaN)
    lb_feat_unscaled = np.nanmin(features_original_np[complete_rows_mask], axis=0)
    ub_feat_unscaled = np.nanmax(features_original_np[complete_rows_mask], axis=0)

    for i in range(len(lb_feat_unscaled)):
        if lb_feat_unscaled[i] == ub_feat_unscaled[i]: # Gérer les features constantes
            lb_feat_unscaled[i] -= (abs(lb_feat_unscaled[i] * 0.01) + 1e-6) if lb_feat_unscaled[i] != 0 else -1e-6
            ub_feat_unscaled[i] += (abs(ub_feat_unscaled[i] * 0.01) + 1e-6) if ub_feat_unscaled[i] != 0 else 1e-6
        if lb_feat_unscaled[i] > ub_feat_unscaled[i]: # Sanity check
             lb_feat_unscaled[i], ub_feat_unscaled[i] = ub_feat_unscaled[i], lb_feat_unscaled[i]


    lb_sca_opt_values = [lb_feat_unscaled[c_idx] for r, c_idx in nan_indices_in_features]
    ub_sca_opt_values = [ub_feat_unscaled[c_idx] for r, c_idx in nan_indices_in_features]

    if not lb_sca_opt_values: # Devrait être couvert par len(nan_indices_in_features) == 0
        raise ValueError("Problème lors de la dérivation des bornes pour les valeurs d'imputation.")
    for i in range(len(lb_sca_opt_values)):
        if lb_sca_opt_values[i] > ub_sca_opt_values[i]:
             lb_sca_opt_values[i], ub_sca_opt_values[i] = ub_sca_opt_values[i], lb_sca_opt_values[i]


    # Fonction de fitness pour SCA (qui exécute GWO en interne)
    # `imputation_solution_unscaled` sont les valeurs proposées par SCA pour les NaN (non normalisées)
    def sca_fitness_function(imputation_solution_unscaled):
        current_imputed_features_unscaled = features_original_np.copy()
        for i, (r, c_idx) in enumerate(nan_indices_in_features):
            current_imputed_features_unscaled[r, c_idx] = imputation_solution_unscaled[i]

        try:
            scaled_features_for_gwo = scaler.transform(current_imputed_features_unscaled)
        except Exception:
            return 1.0 # Pénaliser si la normalisation échoue

        # Fonction de fitness pour GWO (sélection de features)
        # `feature_mask_binary` est le masque binaire des features proposées par GWO
        def gwo_fitness_function(feature_mask_binary):
            feature_mask_binary = np.round(feature_mask_binary).astype(int)
            
            if np.sum(feature_mask_binary) == 0:
                return 1.0 # Pénaliser si aucune feature n'est sélectionnée
            
            selected_features_for_knn = scaled_features_for_gwo[:, feature_mask_binary == 1]

            if selected_features_for_knn.shape[0] < 2 or selected_features_for_knn.shape[1] == 0:
                return 1.0

            min_samples_knn = min(5, selected_features_for_knn.shape[0])
            if min_samples_knn == 0: return 1.0
            
            # Stratification pour train_test_split si possible
            unique_targets, counts = np.unique(target_np, return_counts=True)
            min_class_count = counts.min() if len(counts) > 0 else 0
            
            stratify_gwo = None
            test_size_gwo = 0.2

            if len(unique_targets) > 1 and min_class_count >= 2 : # Condition pour la stratification (au moins 2 échantillons par classe)
                # Vérifier si le test_size est compatible avec la plus petite classe
                if int(min_class_count * test_size_gwo) >=1 and int(min_class_count * (1-test_size_gwo)) >=1 :
                    stratify_gwo = target_np

            try:
                X_train, X_test, y_train, y_test = train_test_split(
                    selected_features_for_knn, target_np, test_size=test_size_gwo, random_state=42, stratify=stratify_gwo
                )
            except ValueError: # Si la stratification échoue malgré tout
                 X_train, X_test, y_train, y_test = train_test_split(
                    selected_features_for_knn, target_np, test_size=test_size_gwo, random_state=42
                )

            if X_train.shape[0] == 0 or X_test.shape[0] == 0 or X_train.shape[1] == 0:
                return 1.0
            
            n_neighbors_actual = min(min_samples_knn, X_train.shape[0])
            if n_neighbors_actual == 0: return 1.0

            model_knn = KNeighborsClassifier(n_neighbors=n_neighbors_actual)
            model_knn.fit(X_train, y_train)
            predictions = model_knn.predict(X_test)
            acc = accuracy_score(y_test, predictions)
            return 1 - acc # GWO minimise le taux d'erreur

        gwo_problem = {
            "bounds": BinaryVar(n_vars=features_original_np.shape[1]),
            "minmax": "min",
            "obj_func": gwo_fitness_function,
            "verbose": False,
        }
        gwo_model = GWO.OriginalGWO(epoch=epoch_gwo, pop_size=pop_gwo)
        gwo_result = gwo_model.solve(gwo_problem)
        return gwo_result.target.fitness # Retourne (1 - accuracy_knn)

    sca_problem = {
        "bounds": FloatVar(lb=lb_sca_opt_values, ub=ub_sca_opt_values),
        "minmax": "min", # SCA minimise (1 - accuracy_knn de GWO)
        "obj_func": sca_fitness_function,
        "verbose": False,
    }
    sca_model = SCA.DevSCA(epoch=epoch_sca, pop_size=pop_sca) # DevSCA comme dans le script original
    sca_result = sca_model.solve(sca_problem)

    final_imputed_values_unscaled = sca_result.solution
    
    final_features_imputed_unscaled_np = features_original_np.copy()
    for i, (r, c_idx) in enumerate(nan_indices_in_features):
        final_features_imputed_unscaled_np[r, c_idx] = final_imputed_values_unscaled[i]

    df_imputed_features = pd.DataFrame(final_features_imputed_unscaled_np, columns=original_feature_columns)
    df_imputed_target = pd.DataFrame(target_np.reshape(-1,1), columns=[original_target_column]) # Assurer 2D pour concat
    df_final_imputed = pd.concat([df_imputed_features, df_imputed_target], axis=1)
    
    final_accuracy = 1 - sca_result.target.fitness

    # Pour obtenir le masque de features final, il faudrait ré-exécuter GWO avec les meilleures valeurs imputées
    # Pour simplifier, nous ne retournons pas un masque spécifique ici, ou nous retournons un masque par défaut.
    # Alternative: stocker le meilleur masque trouvé pendant les appels à sca_fitness_function.
    # Pour l'instant, on ne retourne pas de masque de feature spécifique.
    
    duree_total = time.time() - start_time

    return {
        'dataset_imputed': df_final_imputed.to_json(orient='split'),
        'missing_mask': df_original.isnull().values.tolist(),
        'accuracy': final_accuracy,
        'metrics': {
            "final_sca_objective_value": sca_result.target.fitness,
        },
        'duree': f"{duree_total:.2f}s",
        # 'selected_features_mask': "Non implémenté dans cette version du wrapper" 
    }