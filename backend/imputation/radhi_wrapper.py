import pandas as pd
import time
import traceback
from .radhi_imputation.radhi_logic import sca_gwo_hybrid_logic

# Paramètres par défaut pour l'API (peuvent être surchargés par la requête)
DEFAULT_RADHI_SCA_EPOCH = 10
DEFAULT_RADHI_SCA_POPSIZE = 15
DEFAULT_RADHI_GWO_EPOCH = 8
DEFAULT_RADHI_GWO_POPSIZE = 10
DEFAULT_RADHI_TESTINGSET_RATIO = 0.2

def radhi_sca_gwo_pipeline_main(
    df_original: pd.DataFrame,
    target_col_idx: int = -1, # Par défaut, dernière colonne
    sca_epoch_val: int = DEFAULT_RADHI_SCA_EPOCH,
    sca_popsize_val: int = DEFAULT_RADHI_SCA_POPSIZE,
    gwo_epoch_val: int = DEFAULT_RADHI_GWO_EPOCH,
    gwo_popsize_val: int = DEFAULT_RADHI_GWO_POPSIZE,
    test_ratio: float = DEFAULT_RADHI_TESTINGSET_RATIO
    ):
    
    overall_start_time = time.time()
    
    if df_original.empty:
        raise ValueError("Le DataFrame fourni est vide.")
    if not (0 < test_ratio < 1):
        raise ValueError("testingset_ratio doit être entre 0 et 1 (exclus).")

    try:
        imputed_df, results_dict = sca_gwo_hybrid_logic(
            input_df=df_original.copy(),
            target_column_index=target_col_idx,
            testingset_ratio=test_ratio,
            sca_epoch=sca_epoch_val,
            sca_popsize=sca_popsize_val,
            gwo_epoch_param=gwo_epoch_val,
            gwo_popsize_param=gwo_popsize_val
        )

        duree_sec = time.time() - overall_start_time

        # Préparer la réponse pour l'API
        response_data = {
            "message": results_dict.get("message", "Pipeline Radhi SCA-GWO terminé."),
            "dataset_imputed": imputed_df.to_json(orient="split"),
            "final_accuracy_knn": results_dict.get("final_accuracy"),
            "original_missing_mask": df_original.isnull().values.tolist(), # Pour la coloration
            "duree": f"{duree_sec:.2f}s",
            # Optionnel: retourner les données d'évolution si le frontend les gère
            # "sca_evolution": results_dict.get("sca_accuracy_evolution"),
            # "gwo_evolution": results_dict.get("gwo_accuracy_evolution_per_sca_solution"),
        }
        if "Aucune valeur manquante" in response_data["message"]:
            response_data["final_accuracy_knn"] = 1.0 # Ou une autre valeur pour indiquer "non applicable"

        return response_data

    except Exception as e:
        # print(f"Erreur dans radhi_sca_gwo_pipeline_main (wrapper): {e}")
        # print(traceback.format_exc())
        raise e # Relancer pour que la vue Django la gère
