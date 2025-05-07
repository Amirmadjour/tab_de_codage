import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, f1_score

# MODIFIÉ: Accepte un DataFrame et un index de colonne cible
def load_and_prepare_data(input_df: pd.DataFrame, target_column_index: int):
    """Charge les données DEPUIS UN DATAFRAME, identifie les NaN et prépare les indices."""
    data_full = input_df.values

    if not (0 <= target_column_index < data_full.shape[1]):
        raise ValueError(f"L'index de la colonne cible {target_column_index} est hors limites pour un DataFrame de {data_full.shape[1]} colonnes.")

    all_indices = np.arange(data_full.shape[1])
    feature_indices = np.delete(all_indices, target_column_index)
    features = data_full[:, feature_indices].copy()
    target = data_full[:, target_column_index]

    nan_indices_in_features = np.array([
        (row, col)
        for col in range(features.shape[1])
        for row in np.argwhere(np.isnan(features[:, col])).flatten()
    ])
    nan_n = len(nan_indices_in_features)

    if nan_n == 0:
        raise ValueError("Aucune valeur NaN trouvée dans les features du dataset.")

    scaler = StandardScaler()
    features_no_nan_rows_mask = ~np.isnan(features).any(axis=1)

    if not np.any(features_no_nan_rows_mask):
        if features.shape[0] > 0:
            scaler.fit(features) # Fitter sur tout si aucune ligne complète
        else:
            raise ValueError("Le tableau des features est vide, impossible d'ajuster le scaler.")
    else:
        scaler.fit(features[features_no_nan_rows_mask])

    features_scaled = scaler.transform(features) # Les NaN restent NaN

    nan_indices_scaled = np.array([
        (row, col)
        for col in range(features_scaled.shape[1])
        for row in np.argwhere(np.isnan(features_scaled[:, col])).flatten()
    ])

    nan_mask_for_knn_data = np.isnan(features_scaled).any(axis=1)
    features_complete_scaled_for_knn = features_scaled[~nan_mask_for_knn_data]
    target_complete_for_knn = target[~nan_mask_for_knn_data]

    if len(features_complete_scaled_for_knn) < 2 or len(np.unique(target_complete_for_knn)) < 2:
        min_samples_for_split = 2 * (len(np.unique(target_complete_for_knn)) if len(np.unique(target_complete_for_knn)) > 1 else 2) # k * n_classes for StratifiedShuffleSplit
        if len(features_complete_scaled_for_knn) < min_samples_for_split :
             raise ValueError(f"Pas assez de données complètes ({len(features_complete_scaled_for_knn)} lignes) ou de classes ({len(np.unique(target_complete_for_knn))}) pour entraîner le modèle KNN pour l'évaluation de la fitness. Nécessite au moins {min_samples_for_split} échantillons complets.")


    stratify_option = target_complete_for_knn if len(np.unique(target_complete_for_knn)) > 1 else None
    X_train_knn, X_test_knn, y_train_knn, y_test_knn = train_test_split(
        features_complete_scaled_for_knn, target_complete_for_knn, test_size=0.2, random_state=42, stratify=stratify_option
    )

    if len(X_train_knn) == 0:
        raise ValueError("L'ensemble d'entraînement KNN est vide. Impossible d'entraîner le modèle KNN.")
    
    knn = KNeighborsClassifier(n_neighbors=min(5, len(X_train_knn))) # Assurer n_neighbors <= n_samples
    knn.fit(X_train_knn, y_train_knn)

    lb_val = np.nanmin(features_complete_scaled_for_knn) if features_complete_scaled_for_knn.size > 0 else -1.0
    ub_val = np.nanmax(features_complete_scaled_for_knn) if features_complete_scaled_for_knn.size > 0 else 1.0
    
    if lb_val == ub_val:
        lb_val -= 1e-6
        ub_val += 1e-6


    problem_info = {
        "features_scaled": features_scaled,
        "target": target,
        "nan_indices_scaled": nan_indices_scaled,
        "original_indices_nan": np.where(nan_mask_for_knn_data)[0],
        "X_test_knn": X_test_knn,
        "y_test_knn": y_test_knn,
        "knn_model": knn,
        "lower_bound": lb_val,
        "upper_bound": ub_val,
        "dim": nan_n,
        "scaler": scaler,
        "feature_indices": feature_indices,
        "target_column_index": target_column_index
    }
    return problem_info

def calculate_fitness(solution, problem_info):
    """Calcule la fitness (1 - accuracy) pour une solution donnée."""
    features_imputed = problem_info["features_scaled"].copy()
    nan_indices = problem_info["nan_indices_scaled"]
    dim = problem_info["dim"]

    if len(solution) != dim:
         # print(f"Avertissement: Taille de solution ({len(solution)}) != Dimension attendue ({dim}). Ajustement...")
         if len(solution) > dim:
             solution = solution[:dim]
         else:
             solution = np.pad(solution, (0, dim - len(solution)), 'constant', constant_values=np.mean(solution) if len(solution) > 0 else 0)


    for k, (row, col) in enumerate(nan_indices):
        features_imputed[row, col] = solution[k]
    
    # Données à prédire : celles qui étaient NaN (maintenant imputées) + l'ensemble de test KNN existant
    # Les features imputées correspondant aux lignes NaN originales
    imputed_features_for_nan_rows = features_imputed[problem_info["original_indices_nan"], :]
    
    # Concaténer avec X_test_knn (qui vient de lignes complètes)
    # S'assurer qu'il y a des données à concaténer
    if imputed_features_for_nan_rows.shape[0] > 0 and problem_info["X_test_knn"].shape[0] > 0:
        X_combined_test = np.concatenate((imputed_features_for_nan_rows, problem_info["X_test_knn"]), axis=0)
        y_combined_test = np.concatenate((problem_info["target"][problem_info["original_indices_nan"]], problem_info["y_test_knn"]), axis=0)
    elif imputed_features_for_nan_rows.shape[0] > 0: # Seulement des lignes imputées à tester
        X_combined_test = imputed_features_for_nan_rows
        y_combined_test = problem_info["target"][problem_info["original_indices_nan"]]
    elif problem_info["X_test_knn"].shape[0] > 0: # Seulement X_test_knn (pas de NaN à imputer, ce cas est géré avant)
        X_combined_test = problem_info["X_test_knn"]
        y_combined_test = problem_info["y_test_knn"]
    else: # Aucune donnée de test, ne devrait pas arriver si KNN a été entraîné
        return 1.0 # Pire fitness

    if X_combined_test.shape[0] == 0: # Si toujours pas de données de test
        return 1.0

    y_pred = problem_info["knn_model"].predict(X_combined_test)
    acc = accuracy_score(y_combined_test, y_pred)
    return 1 - acc