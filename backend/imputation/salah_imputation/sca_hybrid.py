#### sca_hybrid.py
import numpy as np
import random
import math
# Assurez-vous que les fonctions GWO et de fitness sont accessibles
from .gwo import run_gwo_from_scratch # Utilise le gwo.py modifié
from .data_handler import calculate_fitness # Bien que non utilisé directement ici, importé par gwo.py

def sca_objective_wrapper(solution, problem_info, gwo_pop_size, gwo_epochs):
    """Fonction objectif pour SCA qui appelle GWO pour affiner. (INCHANGÉ CONCEPTUELLEMENT)"""
    # print(f"SCA candidate -> Running inner GWO...") # Peut être commenté pour moins de verbosité
    initial_gwo_pop = [solution.copy()]
    dim = problem_info["dim"]
    lb = problem_info["lower_bound"]
    ub = problem_info["upper_bound"]
    # Créer le reste de la population GWO initiale aléatoirement
    for _ in range(gwo_pop_size - 1):
        initial_gwo_pop.append(np.random.uniform(lb, ub, dim))

    # Exécuter GWO pour affiner (utilise maintenant la version adaptée de GWO)
    best_gwo_solution, best_gwo_fitness = run_gwo_from_scratch(
        problem_info,
        pop_size=gwo_pop_size,
        epochs=gwo_epochs,
        initial_population=initial_gwo_pop
    )
    # print(f"Inner GWO finished. Fitness: {best_gwo_fitness:.6f}") # Peut être commenté
    return best_gwo_fitness


def run_hybrid_sca_gwo_from_scratch(problem_info, sca_pop_size, sca_epochs, gwo_pop_size, gwo_epochs):
    """Exécute l'hybride SCA-GWO depuis zéro en utilisant la logique SCA adaptée."""
    dim = problem_info["dim"]
    lb = problem_info["lower_bound"]
    ub = problem_info["upper_bound"]

    # Initialisation SCA
    # Utiliser une initialisation uniforme simple
    positions = np.random.uniform(lb, ub, (sca_pop_size, dim))
    fitness = np.full(sca_pop_size, np.inf)

    # Évaluation initiale (coûteuse !) - Appel du wrapper GWO
    print("--- Initial SCA Population Evaluation (using inner GWO) ---")
    for i in range(sca_pop_size):
        fitness[i] = sca_objective_wrapper(positions[i], problem_info, gwo_pop_size, gwo_epochs)
        # print(f"Initial Agent {i+1}/{sca_pop_size} evaluated. Fitness: {fitness[i]:.6f}")

    # Trouver la meilleure solution initiale
    best_idx = np.argmin(fitness)
    best_pos = positions[best_idx].copy()
    best_fitness = fitness[best_idx]
    print(f"Initial Best Fitness: {best_fitness:.6f}")

    print(f"\n--- Starting SCA Main Loop (Epochs: {sca_epochs}) ---")
    # Boucle principale SCA (adaptée de scaCodeFromScratch.py)
    for t in range(sca_epochs):
        # Mettre à jour la meilleure position (Destination Point)
        # Fait implicitement à la fin de la boucle précédente/début de celle-ci

        # Paramètre r1 (a dans la référence) - contrôle exploration/exploitation
        r1 = 2 - 2 * (t / sca_epochs) # Décroît linéairement de 2 à 0

        # Pour chaque agent de recherche
        for i in range(sca_pop_size):
            # Pour chaque dimension
            for j in range(dim):
                # Générer r2, r3, r4 (aléatoire uniforme standard)
                r2 = (2 * math.pi) * np.random.rand() # [0, 2pi]
                r3 = 2 * np.random.rand()             # [0, 2]
                r4 = np.random.rand()                 # [0, 1]

                # Mettre à jour la position basé sur sin ou cos
                if r4 < 0.5:
                    # Équation Sinus
                    positions[i, j] = positions[i, j] + (r1 * math.sin(r2) * abs(r3 * best_pos[j] - positions[i, j]))
                else:
                    # Équation Cosinus
                    positions[i, j] = positions[i, j] + (r1 * math.cos(r2) * abs(r3 * best_pos[j] - positions[i, j]))

            # Vérifier les limites pour l'agent entier (plus efficace)
            # Utiliser np.clip comme dans notre gwo.py (plus simple que la référence)
            positions[i] = np.clip(positions[i], lb, ub)

            # Évaluer la nouvelle position (coûteux !) - Appel du wrapper GWO
            # print(f"\nEpoch {t+1}/{sca_epochs}, Evaluating Agent {i+1}/{sca_pop_size}...") # Verbosité
            new_fitness = sca_objective_wrapper(positions[i], problem_info, gwo_pop_size, gwo_epochs)

            # Mise à jour si meilleure (pour cet agent)
            # Note: La référence met à jour la population puis re-évalue le meilleur global.
            # Ici, on met à jour la fitness de l'agent directement.
            fitness[i] = new_fitness

        # Mettre à jour la meilleure solution globale après avoir évalué tous les agents
        current_best_idx = np.argmin(fitness)
        if fitness[current_best_idx] < best_fitness:
            best_fitness = fitness[current_best_idx]
            best_pos = positions[current_best_idx].copy()

        print(f"--- Epoch {t+1}/{sca_epochs} Completed. Best Fitness So Far: {best_fitness:.6f} ---")

    return best_pos, best_fitness
