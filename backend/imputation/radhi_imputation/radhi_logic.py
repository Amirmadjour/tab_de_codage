import numpy as np
import pandas as pd
from mealpy import FloatVar, SCA, GWO
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
# import matplotlib.pyplot as plt # Désactivé pour l'API
# from matplotlib.ticker import MaxNLocator # Désactivé pour l'API
import os
import time

def sca_gwo_hybrid_logic(
    input_df: pd.DataFrame, 
    target_column_index: int = -1, # Par défaut, la dernière colonne
    testingset_ratio: float = 0.2, 
    sca_epoch: int = 10, # Réduit pour l'API (original 50)
    sca_popsize: int = 15, # Réduit pour l'API (original 30)
    gwo_epoch_param: int = 8, # Réduit pour l'API (original 40)
    gwo_popsize_param: int = 10, # Réduit pour l'API (original 20)
    # save_plots_param: bool = False, # Forcé à False pour l'API
    # output_dir_param: str = "temp_radhi_plots" # Non utilisé si save_plots_param est False
    ):
    
    # if save_plots_param and not os.path.exists(output_dir_param):
    #     os.makedirs(output_dir_param) # Non nécessaire pour l'API
    
    original_df_columns = input_df.columns.tolist()
    data_np = input_df.values.copy() # Travailler sur une copie
    
    scaler = StandardScaler()
    
    if target_column_index == -1:
        target_column_idx_actual = data_np.shape[1] - 1
    else:
        target_column_idx_actual = target_column_index
        if not (0 <= target_column_idx_actual < data_np.shape[1]):
            raise ValueError(f"Invalid target_column_index: {target_column_idx_actual}")

    feature_indices = [i for i in range(data_np.shape[1]) if i != target_column_idx_actual]
    
    if not feature_indices:
        raise ValueError("No feature columns found after excluding the target column.")

    features_np = data_np[:, feature_indices].astype(float) # Assurer le type float pour les features
    target_np = data_np[:, target_column_idx_actual]
    
    # Mise à l'échelle des features
    # Doit être fait avant l'identification des NaN si on veut imputer sur l'échelle normalisée
    # Cependant, le code original normalise, PUIS trouve les NaN, ce qui est inhabituel.
    # Pour "garder la même logique", on suit cela.
    # Mais il est plus courant d'imputer PUIS de normaliser, ou de normaliser les non-NaN, imputer, puis re-normaliser.
    
    # Le code original normalise toutes les features, y compris celles avec NaN, ce qui peut être problématique.
    # scaler.fit(features_np) # Fit sur toutes les features (peut être influencé par les NaN si SimpleImputer n'est pas utilisé avant)
    # features_np_scaled = scaler.transform(features_np)
    
    # Alternative plus robuste: fit scaler sur les données non-NaN uniquement
    temp_features_for_scaling = features_np.copy()
    nan_mask_for_scaling_fit = ~np.isnan(temp_features_for_scaling)
    if np.any(nan_mask_for_scaling_fit.sum(axis=0) == 0): # Si une colonne est entièrement NaN
         raise ValueError("Une colonne de feature est entièrement NaN, impossible de normaliser.")

    # Fit le scaler sur les valeurs non-NaN de chaque colonne
    # Pour simplifier et suivre l'esprit original, on va normaliser après avoir identifié les NaN
    # et séparé les données, comme dans le script original.
    # Cette approche est conservée pour adhérer à la demande "garder la même logique".

    # --- Logique originale de gestion des NaN et de la normalisation ---
    nan_indices_list = []
    for col_idx_in_features_np in range(features_np.shape[1]):
        for row_idx in np.argwhere(np.isnan(features_np[:, col_idx_in_features_np])).flatten():
            nan_indices_list.append((row_idx, col_idx_in_features_np))
    
    nan_n_count = len(nan_indices_list)
    
    if nan_n_count == 0:
        # print("Aucune valeur manquante à imputer (logique Radhi).")
        # Retourner le DataFrame original non modifié et une accuracy de 1 (ou N/A)
        return input_df.copy(), {
            "final_accuracy": 1.0, # Ou None, ou un message
            "message": "Aucune valeur manquante trouvée.",
            "sca_accuracy_evolution": [],
            "gwo_accuracy_evolution_per_sca_solution": {}
        }

    # Normaliser les features APRÈS avoir identifié les NaN (comme dans le script original)
    # Cela signifie que les NaN sont ignorés par fit, mais transform les transformera en NaN.
    scaler.fit(features_np[~np.isnan(features_np).any(axis=1)]) # Fit sur les lignes sans NaN
    features_np_scaled = scaler.transform(features_np) # Transform toutes les lignes

    # Ré-identifier les NaN sur les données normalisées (car transform peut les préserver)
    nan_indices_list_scaled = []
    for col_idx in range(features_np_scaled.shape[1]):
        for row_idx in np.argwhere(np.isnan(features_np_scaled[:, col_idx])).flatten():
            nan_indices_list_scaled.append((row_idx, col_idx))
    
    # Utiliser les indices NaN des données normalisées pour l'imputation
    current_nan_indices_for_imputation = np.array(nan_indices_list_scaled)
    current_nan_n_for_imputation = len(current_nan_indices_for_imputation)

    if current_nan_n_for_imputation == 0: # Si la normalisation a éliminé les NaN (improbable avec StandardScaler)
        df_imputed_final = input_df.copy() # Retourner l'original car rien n'a été imputé
        # Reconstruire le DataFrame avec les features normalisées (mais non imputées) et la cible
        # df_imputed_final.iloc[:, feature_indices] = scaler.inverse_transform(features_np_scaled) # Inverse transform si besoin
        return df_imputed_final, {
             "final_accuracy": 1.0, "message": "Aucun NaN après normalisation (inattendu).",
             "sca_accuracy_evolution": [], "gwo_accuracy_evolution_per_sca_solution": {}
        }

    # Séparer les données avec et sans NaN (basé sur les features normalisées)
    rows_with_nan_mask_scaled = np.isnan(features_np_scaled).any(axis=1)
    features_without_nan_scaled = features_np_scaled[~rows_with_nan_mask_scaled].copy()
    target_for_rows_without_nan = target_np[~rows_with_nan_mask_scaled]

    if features_without_nan_scaled.shape[0] < 2 or len(np.unique(target_for_rows_without_nan)) < 2 :
        raise ValueError("Pas assez de données sans NaN ou de classes cibles pour entraîner KNN.")

    # Définir les bornes pour l'optimisation (basées sur les min/max des features normalisées sans NaN)
    lb_val = np.min(features_without_nan_scaled) if features_without_nan_scaled.size > 0 else -1
    ub_val = np.max(features_without_nan_scaled) if features_without_nan_scaled.size > 0 else 1
    lower_bounds = (lb_val,) * current_nan_n_for_imputation
    upper_bounds = (ub_val,) * current_nan_n_for_imputation
    
    # Préparer les données pour l'entraînement KNN (utilisé dans les fonctions objectif)
    X_train_knn, X_test_knn, y_train_knn, y_test_knn = train_test_split(
        features_without_nan_scaled, target_for_rows_without_nan, 
        test_size=testingset_ratio, random_state=42, stratify=target_for_rows_without_nan
    )
    
    if X_train_knn.shape[0] == 0:
        raise ValueError("X_train pour KNN est vide après le split.")

    knn_model = KNeighborsClassifier(n_neighbors=min(5, X_train_knn.shape[0]))
    knn_model.fit(X_train_knn, y_train_knn)
    
    # Variables pour stocker les accuracies (pour l'API, on ne les utilisera pas pour les plots)
    sca_solutions_details = [] # Liste de (solution_vector, accuracy, f1_score)
    sca_all_iteration_accuracies = [] # Accuracies à chaque éval de la fonction objectif SCA
    gwo_all_iteration_accuracies_per_sca = {} # Dict: {sca_solution_id: [gwo_iter_accuracies]}

    # --- Fonction objectif pour SCA ---
    def sca_objective_function_mealpy(solution_vector):
        features_temp_imputed_scaled = features_np_scaled.copy()
        for k_idx, (r_idx, c_idx) in enumerate(current_nan_indices_for_imputation):
            features_temp_imputed_scaled[r_idx, c_idx] = solution_vector[k_idx]
        
        # Évaluer sur les lignes qui avaient des NaN + le X_test_knn (qui n'a pas de NaN)
        # Ceci est la logique originale de Radhi.
        features_for_eval_nan_rows = features_temp_imputed_scaled[rows_with_nan_mask_scaled, :]
        target_for_eval_nan_rows = target_np[rows_with_nan_mask_scaled]

        if features_for_eval_nan_rows.shape[0] > 0:
            X_eval_combined = np.concatenate((features_for_eval_nan_rows, X_test_knn), axis=0)
            y_eval_combined = np.concatenate((target_for_eval_nan_rows, y_test_knn), axis=0)
        else: # Si par hasard toutes les lignes avaient des NaN (improbable si features_without_nan_scaled n'était pas vide)
            X_eval_combined = X_test_knn
            y_eval_combined = y_test_knn

        if X_eval_combined.shape[0] == 0: return 1.0 # Fitness maximale si pas de données à évaluer

        y_pred_eval = knn_model.predict(X_eval_combined)
        acc_eval = accuracy_score(y_eval_combined, y_pred_eval)
        f1_eval = f1_score(y_eval_combined, y_pred_eval, zero_division=0)
        
        sca_solutions_details.append((solution_vector, acc_eval, f1_eval))
        sca_all_iteration_accuracies.append(acc_eval)
        
        return 1 - acc_eval # mealpy minimise, donc 1 - accuracy

    # --- Exécution de SCA ---
    problem_sca = {
        "bounds": FloatVar(lb=lower_bounds, ub=upper_bounds, name="vars"),
        "minmax": "min",
        "obj_func": sca_objective_function_mealpy
    }
    model_sca_instance = SCA.DevSCA(epoch=sca_epoch, pop_size=sca_popsize)
    model_sca_instance.solve(problem_sca) # g_best_sca n'est pas directement utilisé ensuite pour GWO dans le code original
    
    # Trier les solutions SCA et prendre les top N (original: top 3)
    sca_solutions_details.sort(key=lambda x: x[1], reverse=True) # Trier par accuracy (décroissant)
    top_n_sca_solutions_for_gwo = sca_solutions_details[:min(3, len(sca_solutions_details))]
    
    best_overall_gwo_solution_vector = None
    best_overall_gwo_fitness = float('inf') # (1 - accuracy)

    # --- Appliquer GWO sur chaque top solution SCA ---
    for sca_idx, (sca_sol_vector, sca_acc, _) in enumerate(top_n_sca_solutions_for_gwo):
        gwo_solution_id_str = f"sca_sol_{sca_idx+1}"
        gwo_all_iteration_accuracies_per_sca[gwo_solution_id_str] = []

        # Fonction objectif pour GWO (wrapper autour de la logique d'évaluation)
        def gwo_objective_function_mealpy_wrapper(gwo_solution_vector):
            # GWO optimise les mêmes valeurs NaN que SCA
            features_gwo_imputed_scaled = features_np_scaled.copy()
            for k_idx, (r_idx, c_idx) in enumerate(current_nan_indices_for_imputation):
                features_gwo_imputed_scaled[r_idx, c_idx] = gwo_solution_vector[k_idx]

            features_for_gwo_eval_nan_rows = features_gwo_imputed_scaled[rows_with_nan_mask_scaled, :]
            target_for_gwo_eval_nan_rows = target_np[rows_with_nan_mask_scaled]
            
            if features_for_gwo_eval_nan_rows.shape[0] > 0:
                X_gwo_eval_combined = np.concatenate((features_for_gwo_eval_nan_rows, X_test_knn), axis=0)
                y_gwo_eval_combined = np.concatenate((target_for_gwo_eval_nan_rows, y_test_knn), axis=0)
            else:
                X_gwo_eval_combined = X_test_knn
                y_gwo_eval_combined = y_test_knn

            if X_gwo_eval_combined.shape[0] == 0: return 1.0

            y_pred_gwo_eval = knn_model.predict(X_gwo_eval_combined)
            acc_gwo_eval = accuracy_score(y_gwo_eval_combined, y_pred_gwo_eval)
            
            gwo_all_iteration_accuracies_per_sca[gwo_solution_id_str].append(acc_gwo_eval)
            return 1 - acc_gwo_eval

        problem_gwo = {
            # GWO optimise les mêmes valeurs que SCA, donc les bornes sont les mêmes.
            # Le vecteur solution initial pour GWO est implicitement géré par mealpy.
            # Le code original ne semble pas passer explicitement sca_sol_vector comme point de départ à GWO.
            # GWO redémarre l'optimisation des valeurs NaN.
            "bounds": FloatVar(lb=lower_bounds, ub=upper_bounds, name="vars_gwo"),
            "minmax": "min",
            "obj_func": gwo_objective_function_mealpy_wrapper
        }
        model_gwo_instance = GWO.OriginalGWO(epoch=gwo_epoch_param, pop_size=gwo_popsize_param)
        g_best_gwo_result = model_gwo_instance.solve(problem_gwo)
        
        if g_best_gwo_result.target.fitness < best_overall_gwo_fitness:
            best_overall_gwo_fitness = g_best_gwo_result.target.fitness
            best_overall_gwo_solution_vector = g_best_gwo_result.solution
    
    if best_overall_gwo_solution_vector is None:
        # Fallback: si GWO n'a rien produit (ou si top_n_sca_solutions était vide)
        # Utiliser la meilleure solution SCA directement
        if top_n_sca_solutions_for_gwo:
            best_overall_gwo_solution_vector = top_n_sca_solutions_for_gwo[0][0] # Le vecteur solution
            best_overall_gwo_fitness = 1 - top_n_sca_solutions_for_gwo[0][1] # 1 - accuracy
        elif sca_solutions_details: # Si SCA a tourné mais top_n était vide pour une raison
             best_overall_gwo_solution_vector = sca_solutions_details[0][0]
             best_overall_gwo_fitness = 1 - sca_solutions_details[0][1]
        else: # Aucune solution du tout
            # Retourner le DataFrame original avec un message d'erreur/avertissement
            return input_df.copy(), {
                "final_accuracy": 0.0, 
                "message": "Aucune solution d'imputation n'a pu être trouvée.",
                "sca_accuracy_evolution": sca_all_iteration_accuracies,
                "gwo_accuracy_evolution_per_sca_solution": gwo_all_iteration_accuracies_per_sca
            }

    # Construire le DataFrame final imputé avec la meilleure solution GWO
    features_final_imputed_scaled = features_np_scaled.copy()
    for k_idx, (r_idx, c_idx) in enumerate(current_nan_indices_for_imputation):
        features_final_imputed_scaled[r_idx, c_idx] = best_overall_gwo_solution_vector[k_idx]
    
    # Inverse-transformer les features pour les remettre à l'échelle originale
    features_final_imputed_original_scale = scaler.inverse_transform(features_final_imputed_scaled)
    
    df_imputed_final = input_df.copy()
    # Mettre à jour uniquement les valeurs qui étaient NaN dans le DataFrame original
    # en utilisant les valeurs imputées et dénormalisées.
    # `nan_indices_list` contient les (row, col_in_original_features_np) des NaN initiaux.
    for k_final, (original_row_idx, original_col_idx_in_features) in enumerate(nan_indices_list):
        # `best_overall_gwo_solution_vector[k_final]` est la valeur imputée normalisée.
        # Il faut la dé-normaliser. Mais c'est plus simple de prendre de `features_final_imputed_original_scale`.
        # La k-ième valeur imputée dans `best_overall_gwo_solution_vector` correspond au k-ième NaN identifié.
        # `current_nan_indices_for_imputation` donne (row, col_in_scaled_features) pour ces valeurs.
        # On a besoin de mapper cela aux colonnes originales du DataFrame.
        
        # Plus simple: reconstruire la partie feature du df_imputed_final
        df_imputed_final.iloc[:, feature_indices] = features_final_imputed_original_scale

    final_accuracy_achieved = 1 - best_overall_gwo_fitness

    # Les plots ne sont pas générés ici pour l'API.
    # Les données d'évolution sont retournées si le frontend veut les plotter.
    
    return df_imputed_final, {
        "final_accuracy": final_accuracy_achieved,
        "message": "Imputation Radhi SCA-GWO terminée.",
        "sca_accuracy_evolution": sca_all_iteration_accuracies, # Peut être long
        "gwo_accuracy_evolution_per_sca_solution": gwo_all_iteration_accuracies_per_sca # Peut être volumineux
    }