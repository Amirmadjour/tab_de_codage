#### main.py
# Assurez-vous que les fonctions sont importées correctement
from data_handler import load_and_prepare_data
from sca_hybrid import run_hybrid_sca_gwo_from_scratch

if __name__ == "__main__":
    # Paramètres
    CSV_PATH = '../SCA-GWO-Imputation/water_potability.csv' # Chemin vers le fichier CSV
    SCA_POP_SIZE = 10  # Taille de population SCA (petite à cause du coût)
    SCA_EPOCHS = 5     # Époques SCA (peu à cause du coût)
    GWO_POP_SIZE = 5   # Taille de population GWO interne (très petite)
    GWO_EPOCHS = 5     # Époques GWO interne (très peu)

    print("1. Chargement et préparation des données...")
    try:
        problem_info = load_and_prepare_data(CSV_PATH)
        print(f"   Nombre de valeurs manquantes à imputer (Dimension): {problem_info['dim']}")
        print(f"   Bornes pour l'optimisation: [{problem_info['lower_bound']:.4f}, {problem_info['upper_bound']:.4f}]")
    except ValueError as e:
        print(f"Erreur: {e}")
        exit()
    except FileNotFoundError:
        print(f"Erreur: Le fichier {CSV_PATH} n'a pas été trouvé.")
        exit()

    print("\n2. Démarrage de l'optimisation hybride SCA-GWO (depuis zéro)...")
    print(f"   Paramètres SCA: Pop={SCA_POP_SIZE}, Epochs={SCA_EPOCHS}")
    print(f"   Paramètres GWO interne: Pop={GWO_POP_SIZE}, Epochs={GWO_EPOCHS}")
    print("   ATTENTION: Ce processus peut être très long !")

    best_solution, best_fitness = run_hybrid_sca_gwo_from_scratch(
        problem_info,
        sca_pop_size=SCA_POP_SIZE,
        sca_epochs=SCA_EPOCHS,
        gwo_pop_size=GWO_POP_SIZE,
        gwo_epochs=GWO_EPOCHS
    )

    print("\n--- Optimisation Terminée ---")
    print(f"Meilleure Fitness (1 - Accuracy) trouvée: {best_fitness}")
    # L'accuracy correspondante est 1 - best_fitness
    print(f"Meilleure Accuracy KNN estimée: {1 - best_fitness}")
    # print(f"Meilleure Solution (valeurs imputées): {best_solution}") # Peut être très long à afficher

    # Ici, vous pouvez utiliser 'best_solution' pour imputer le dataset final
    # et potentiellement appliquer la transformation inverse du scaler.