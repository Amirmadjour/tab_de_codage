import pandas as pd
import time
import traceback
from .bennebi_imputation.bennebi_logic import WaterQualityOptimizerLogic

# Paramètres par défaut pour l'API (réduits pour des tests plus rapides)
DEFAULT_SCA_ITERATIONS_API = 3 
DEFAULT_SCA_STRATEGIES_API = 2
DEFAULT_GWO_WOLVES_API = 5
DEFAULT_GWO_ITERATIONS_API = 5 # Réduit par rapport à l'original (10-15)

def bennebi_pipeline_main(df_original: pd.DataFrame,
                          target_column_name: str = 'Potability', # Assurez-vous que c'est le nom correct
                          num_sca_iterations=DEFAULT_SCA_ITERATIONS_API,
                          num_sca_strategies_per_iter=DEFAULT_SCA_STRATEGIES_API,
                          num_gwo_wolves=DEFAULT_GWO_WOLVES_API,
                          num_gwo_iterations=DEFAULT_GWO_ITERATIONS_API):
    overall_start_time = time.time()
    
    if df_original.shape[1] < 2:
        raise ValueError("Le DataFrame doit avoir au moins deux colonnes.")
    if target_column_name not in df_original.columns:
        # Essayer de deviner si c'est la dernière colonne si non spécifié et non 'Potability'
        if target_column_name == 'Potability' and target_column_name not in df_original.columns:
            actual_target_column_name = df_original.columns[-1]
            # print(f"Avertissement: Colonne cible '{target_column_name}' non trouvée. Utilisation de la dernière colonne '{actual_target_column_name}' à la place.")
        else: # Si une autre colonne cible était spécifiée mais non trouvée
             raise ValueError(f"Colonne cible '{target_column_name}' non trouvée dans le DataFrame.")
    else:
        actual_target_column_name = target_column_name


    # Vérifier si des NaN existent avant de lancer l'imputation
    # Le code de Bennebi gère l'imputation même s'il n'y a pas de NaN (SimpleImputer fonctionnera)
    # mais le pipeline est conçu pour l'imputation.
    # if not df_original.isnull().values.any():
    #     # ... (gestion du cas sans NaN si nécessaire, pour l'instant on laisse le pipeline tourner)

    try:
        optimizer = WaterQualityOptimizerLogic(input_dataframe=df_original.copy(), 
                                               target_column_name=actual_target_column_name)
        
        optimization_results = optimizer.optimize_pipeline(
            num_sca_iterations=num_sca_iterations,
            num_sca_strategies_per_iter=num_sca_strategies_per_iter,
            num_gwo_wolves_param=num_gwo_wolves,
            num_gwo_iterations_param=num_gwo_iterations
        )

        if "error" in optimization_results:
            return {
                "message": optimization_results["error"],
                "duree": f"{(time.time() - overall_start_time):.2f}s"
            }

        # Préparer la réponse pour l'API
        best_solution_info = optimization_results["best_solution_found"]
        
        response_data = {
            "message": "Pipeline d'optimisation de Bennebi terminé.",
            "best_imputation_strategy": best_solution_info['imputation_strategy_details'],
            "best_selected_feature_names": best_solution_info['selected_feature_names'],
            "best_accuracy_knn": optimization_results["best_overall_accuracy_knn"],
            # Le dataset retourné est déjà celui avec les features sélectionnées et la cible
            "dataset_imputed_selected_features": optimization_results["final_imputed_table_selected_features_json"],
            "original_missing_mask": df_original.isnull().values.tolist(), # Pour la coloration dans le frontend
            "duree": f"{(time.time() - overall_start_time):.2f}s",
            # "all_tried_solutions_details": optimization_results["all_tried_solutions_details"] # Peut être trop volumineux pour l'API
        }
        return response_data

    except Exception as e:
        # print(f"Erreur dans bennebi_pipeline_main: {e}")
        # print(traceback.format_exc())
        raise e