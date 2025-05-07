import pandas as pd
import numpy as np
import time
# Assurez-vous que le chemin d'importation est correct par rapport à la structure de votre projet
from .salah_imputation.data_handler import load_and_prepare_data
from .salah_imputation.sca_hybrid import run_hybrid_sca_gwo_from_scratch

# Paramètres par défaut (peuvent être rendus configurables via l'API si nécessaire)
SCA_POP_SIZE_DEFAULT = 10
SCA_EPOCHS_DEFAULT = 5
GWO_POP_SIZE_DEFAULT = 5
GWO_EPOCHS_DEFAULT = 5

def salah_hybrid_impute_main(df_original: pd.DataFrame, target_column_name: str = None):
    start_time = time.time()
    df = df_original.copy()

    if target_column_name is None:
        # Par défaut, la dernière colonne est la cible
        target_column_index = df.shape[1] - 1
        # target_column_name = df.columns[target_column_index] # Non utilisé directement par la suite
    else:
        if target_column_name not in df.columns:
            raise ValueError(f"La colonne cible '{target_column_name}' n'a pas été trouvée dans le DataFrame.")
        target_column_index = df.columns.get_loc(target_column_name)

    try:
        problem_info = load_and_prepare_data(df, target_column_index=target_column_index)
    except ValueError as e:
        if "Aucune valeur NaN trouvée" in str(e):
            duree = time.time() - start_time
            return {
                'metrics': {},
                'dataset_imputed': df_original.to_json(orient='split'),
                'missing_mask': df_original.isnull().values.tolist(),
                'overall_metrics': {},
                'fitness_mse': None,
                'accuracy': 1.0,
                'duree': f"{duree:.2f}s",
                'message': 'Aucune valeur NaN trouvée dans le dataset. Données originales retournées.'
            }
        else:
            raise e

    best_solution_values, best_fitness = run_hybrid_sca_gwo_from_scratch(
        problem_info,
        sca_pop_size=SCA_POP_SIZE_DEFAULT,
        sca_epochs=SCA_EPOCHS_DEFAULT,
        gwo_pop_size=GWO_POP_SIZE_DEFAULT,
        gwo_epochs=GWO_EPOCHS_DEFAULT
    )

    features_scaled_imputed = problem_info["features_scaled"].copy()
    nan_indices_scaled = problem_info["nan_indices_scaled"]

    # S'assurer que best_solution_values a la bonne dimension
    if len(best_solution_values) != problem_info["dim"]:
        # Cette situation est normalement gérée dans calculate_fitness si la solution est passée directement
        # Ici, best_solution_values vient de best_pos de l'optimiseur, qui devrait être correct.
        # Si un décalage se produit, il faut le traiter (par ex. padding/troncature)
        # print(f"Alerte: len(best_solution_values)={len(best_solution_values)} != problem_info['dim']={problem_info['dim']}")
        if len(best_solution_values) > problem_info["dim"]:
            best_solution_values = best_solution_values[:problem_info["dim"]]
        else:
            best_solution_values = np.pad(best_solution_values, (0, problem_info["dim"] - len(best_solution_values)), 'mean')


    for k, (row, col) in enumerate(nan_indices_scaled):
        features_scaled_imputed[row, col] = best_solution_values[k]

    scaler = problem_info["scaler"]
    features_imputed_unscaled = scaler.inverse_transform(features_scaled_imputed)

    df_imputed = df.copy()
    # Reconstruire le DataFrame avec les features imputées
    # feature_indices stocke les indices des colonnes de features dans le df original
    original_feature_column_names = df.columns[problem_info["feature_indices"]]
    
    df_imputed_features_part = pd.DataFrame(features_imputed_unscaled, columns=original_feature_column_names, index=df.index)

    for col_name in original_feature_column_names:
        df_imputed[col_name] = df_imputed_features_part[col_name]


    accuracy = 1 - best_fitness
    duree = time.time() - start_time
    missing_mask_original = df_original.isnull().values.tolist()

    imputed_data_dict = {
        'metrics': {"knn_accuracy_on_test_split": accuracy},
        'dataset_imputed': df_imputed.to_json(orient='split'),
        'missing_mask': missing_mask_original,
        'overall_metrics': {"final_objective_value (1-accuracy)": best_fitness},
        'fitness_mse': None,
        'accuracy': accuracy,
        'duree': f"{duree:.2f}s"
    }
    return imputed_data_dict