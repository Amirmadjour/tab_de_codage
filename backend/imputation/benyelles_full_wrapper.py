import pandas as pd
import time
import os
import shutil
import traceback
from .anes_imputation.benyelles_original_logic import run_original_anes_pipeline

# Default parameters for the API call (can be overridden if you add request params)
# These are from the original anes_code.py main() or typical values
DEFAULT_ORIG_SCA_N_AGENTS = 7
DEFAULT_ORIG_SCA_MAX_ITER = 10 # Reduced from 20/50 for API speed
DEFAULT_ORIG_GWO_N_WOLVES = 10
DEFAULT_ORIG_GWO_MAX_ITER = 10 # Reduced from 20/30 for API speed
DEFAULT_ORIG_MLP_MAX_ITER = 50 # Reduced from 200 for API speed
DEFAULT_ORIG_RANDOM_SEED = 42

def benyelles_original_pipeline_main(df_original: pd.DataFrame,
                                     sca_n_agents=DEFAULT_ORIG_SCA_N_AGENTS,
                                     sca_max_iter=DEFAULT_ORIG_SCA_MAX_ITER,
                                     gwo_n_wolves=DEFAULT_ORIG_GWO_N_WOLVES,
                                     gwo_max_iter=DEFAULT_ORIG_GWO_MAX_ITER,
                                     mlp_max_iter=DEFAULT_ORIG_MLP_MAX_ITER,
                                     random_seed=DEFAULT_ORIG_RANDOM_SEED):
    start_time_wrapper = time.time()
    
    if df_original.shape[1] < 2:
        raise ValueError("Le DataFrame doit avoir au moins deux colonnes (une feature, une cible).")

    target_column_name = df_original.columns[-1] # Assume last column is target

    # Define a unique temporary directory for this run
    # It will be created inside 'backend/imputation/anes_imputation/'
    base_temp_dir_path = os.path.join(os.path.dirname(__file__), "anes_imputation", "temp_original_solutions")
    # Potentially add a timestamp or UUID for truly unique concurrent runs, but for now, simple path
    # run_specific_temp_dir = os.path.join(base_temp_dir_path, f"run_{int(time.time())}")
    # For simplicity, the logic script will create and use 'temp_original_solutions' directly if passed base_temp_dir_path
    # The logic script's save_solutions will handle os.makedirs(temp_storage_dir, exist_ok=True)

    if not df_original.isnull().values.any():
        duree_wrapper = time.time() - start_time_wrapper
        return {
            'message': "Aucune valeur NaN trouvée dans le dataset original. Pipeline Original de Benyelles non exécuté intensivement.",
            'dataset_imputed': df_original.to_json(orient='split'), # Return original
            'missing_mask': df_original.isnull().values.tolist(),
            'accuracy_type': "N/A",
            'accuracy_value': 1.0, # Or None
            'selected_features_info': {"selected_feature_names": df_original.columns[:-1].tolist(), "num_selected_features": len(df_original.columns[:-1])},
            'duree': f"{duree_wrapper:.2f}s"
        }
        
    try:
        # The logic function will handle creation of its specific temp sub-directory if needed,
        # or use temp_storage_dir directly.
        # The save_solutions_to_temp_files in the logic script now takes the full path.
        results = run_original_anes_pipeline(
            input_df=df_original.copy(),
            target_column_name=target_column_name,
            temp_storage_dir=base_temp_dir_path, # Pass the base directory for temp files
            sca_n_agents_param=sca_n_agents,
            sca_max_iter_param=sca_max_iter,
            gwo_n_wolves_param=gwo_n_wolves,
            gwo_max_iter_param=gwo_max_iter,
            mlp_max_iter_param=mlp_max_iter,
            random_seed_param=random_seed
        )
        
        best_imputed_df_obj = results["best_imputed_dataframe"]
        
        response_data = {
            'message': results.get("message", "Pipeline Original de Benyelles terminé."),
            'dataset_imputed': best_imputed_df_obj.to_json(orient="split"),
            'missing_mask': results["original_missing_mask_list"],
            'accuracy_type': "MLP Accuracy (GWO selected features, Original Logic)",
            'accuracy_value': results["final_mlp_accuracy"],
            'selected_features_info': {
                "selected_feature_names": results["selected_feature_names"],
                "num_selected_features": len(results["selected_feature_names"])
            },
            'duree': f"{results['execution_time_sec']:.2f}s"
        }
        return response_data

    except Exception as e:
        # print(f"Erreur dans benyelles_original_pipeline_main (wrapper): {e}")
        # print(traceback.format_exc())
        raise e # Relancer pour que la vue Django la gère
    finally:
        # Cleanup the base temporary directory
        if os.path.exists(base_temp_dir_path):
            try:
                shutil.rmtree(base_temp_dir_path)
                # print(f"Nettoyage du dossier temporaire: {base_temp_dir_path}")
            except Exception as e_clean:
                print(f"Échec du nettoyage du dossier temporaire {base_temp_dir_path}: {e_clean}")
