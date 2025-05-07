import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
# from IPython.display import display # Non utilisé dans l'API

class WaterQualityOptimizerLogic:
    def __init__(self, input_dataframe: pd.DataFrame, target_column_name: str = 'Potability'):
        self.raw_data = input_dataframe.copy()
        if target_column_name not in self.raw_data.columns:
            raise ValueError(f"Target column '{target_column_name}' not found in the provided DataFrame.")
        
        self.X_original_df = self.raw_data.drop(target_column_name, axis=1)
        self.y_original_series = self.raw_data[target_column_name]
        self.attributes = self.X_original_df.columns.tolist()
        
        self.best_solution_details = None # Stockera les détails de la meilleure solution trouvée
        self.best_score_achieved = -np.inf
        self.all_run_results = [] # Pour stocker les détails de chaque solution testée
        
    def impute_data(self, X_df_to_impute: pd.DataFrame, strategy_params: dict):
        """Imputation des données selon la stratégie"""
        imputer = SimpleImputer(
            strategy=strategy_params['strategy'],
            fill_value=strategy_params.get('fill_value') # Sera None si non 'constant'
        )
        # S'assurer que l'imputation est faite sur une copie pour éviter les SettingWithCopyWarning
        X_imputed_np = imputer.fit_transform(X_df_to_impute.copy())
        X_imputed_df = pd.DataFrame(X_imputed_np, columns=self.attributes, index=X_df_to_impute.index)
        
        scaler = StandardScaler()
        # Le scaler doit être ajusté sur les données imputées avant transformation
        X_scaled_np = scaler.fit_transform(X_imputed_df)
        return pd.DataFrame(X_scaled_np, columns=self.attributes, index=X_imputed_df.index)
    
    def evaluate_features_knn(self, X_imputed_scaled_df: pd.DataFrame, feature_indices_subset: list):
        """Évaluation avec KNN sur un sous-ensemble de features d'un DataFrame déjà imputé et normalisé."""
        try:
            if not feature_indices_subset: # Si la liste est vide
                return 0.0 
                
            # S'assurer que les indices sont valides
            valid_indices = [idx for idx in feature_indices_subset if idx < X_imputed_scaled_df.shape[1]]
            if not valid_indices:
                return 0.0

            X_subset_df = X_imputed_scaled_df.iloc[:, valid_indices]
            
            # Utiliser self.y_original_series qui correspond au DataFrame original
            X_train, X_test, y_train, y_test = train_test_split(
                X_subset_df, self.y_original_series, test_size=0.3, random_state=42, stratify=self.y_original_series
            )
            
            if X_train.shape[0] == 0 or X_test.shape[0] == 0: return 0.0

            knn = KNeighborsClassifier(n_neighbors=min(5, X_train.shape[0])) # Gérer les petits datasets
            knn.fit(X_train, y_train)
            return accuracy_score(y_test, knn.predict(X_test))
        except Exception:
            # import traceback
            # print(f"Error in evaluate_features_knn: {e}")
            # print(traceback.format_exc())
            return 0.0 # Retourner 0 en cas d'erreur (par ex. pas assez d'échantillons)
    
    def SCA_generate_imputation_strategies(self, num_strategies_to_generate: int):
        """Génère des stratégies d'imputation (similaire à SCA dans l'esprit du code original)"""
        possible_strategies = ['mean', 'median', 'most_frequent', 'constant']
        generated_strategies = []
        for _ in range(num_strategies_to_generate):
            chosen_strategy = np.random.choice(possible_strategies)
            fill_val = None
            if chosen_strategy == 'constant':
                # Utiliser les min/max des données originales non imputées pour le fill_value
                min_val = self.X_original_df.min().min() # Min global sur toutes les features
                max_val = self.X_original_df.max().max() # Max global
                if pd.isna(min_val) or pd.isna(max_val): # Fallback si tout est NaN
                    min_val, max_val = 0,1
                fill_val = np.random.uniform(min_val, max_val)
            generated_strategies.append({'strategy': chosen_strategy, 'fill_value': fill_val})
        return generated_strategies
    
    def GWO_feature_selection(self, X_imputed_scaled_df_for_gwo: pd.DataFrame, 
                              num_wolves=10, max_gwo_iter=20):
        """Sélection d'attributs avec GWO sur un DataFrame déjà imputé et normalisé."""
        num_features = X_imputed_scaled_df_for_gwo.shape[1]
        
        # Initialisation des loups (positions binaires: 0 ou 1 pour chaque feature)
        wolf_positions_binary = np.random.randint(0, 2, size=(num_wolves, num_features))
        
        # Initialisation des leaders (alpha, beta, delta)
        alpha_pos_binary = np.zeros(num_features, dtype=int)
        alpha_fitness = -np.inf 
        beta_pos_binary = np.zeros(num_features, dtype=int)
        beta_fitness = -np.inf
        delta_pos_binary = np.zeros(num_features, dtype=int)
        delta_fitness = -np.inf
        
        for iteration_gwo in range(max_gwo_iter):
            a_gwo_param = 2 - iteration_gwo * (2 / max_gwo_iter) # Paramètre 'a' de GWO
            
            for i in range(num_wolves):
                current_wolf_feature_indices = np.where(wolf_positions_binary[i] == 1)[0].tolist()
                # La fitness est l'accuracy KNN pour le sous-ensemble de features du loup courant
                current_wolf_fitness = self.evaluate_features_knn(X_imputed_scaled_df_for_gwo, current_wolf_feature_indices)
                
                # Mise à jour des leaders alpha, beta, delta
                if current_wolf_fitness > alpha_fitness:
                    delta_pos_binary, delta_fitness = beta_pos_binary.copy(), beta_fitness
                    beta_pos_binary, beta_fitness = alpha_pos_binary.copy(), alpha_fitness
                    alpha_pos_binary, alpha_fitness = wolf_positions_binary[i].copy(), current_wolf_fitness
                elif current_wolf_fitness > beta_fitness:
                    delta_pos_binary, delta_fitness = beta_pos_binary.copy(), beta_fitness
                    beta_pos_binary, beta_fitness = wolf_positions_binary[i].copy(), current_wolf_fitness
                elif current_wolf_fitness > delta_fitness:
                    delta_pos_binary, delta_fitness = wolf_positions_binary[i].copy(), current_wolf_fitness
            
            # Mise à jour des positions des loups (sauf alpha, beta, delta qui sont les meilleurs)
            for i in range(num_wolves):
                new_wolf_pos_continuous = np.zeros(num_features)
                for j in range(num_features): # Pour chaque dimension (feature)
                    # Mouvement par rapport à alpha
                    r1, r2 = np.random.rand(), np.random.rand()
                    A1, C1 = 2 * a_gwo_param * r1 - a_gwo_param, 2 * r2
                    D_alpha = abs(C1 * alpha_pos_binary[j] - wolf_positions_binary[i,j])
                    X1 = alpha_pos_binary[j] - A1 * D_alpha
                    
                    # Mouvement par rapport à beta
                    r1, r2 = np.random.rand(), np.random.rand()
                    A2, C2 = 2 * a_gwo_param * r1 - a_gwo_param, 2 * r2
                    D_beta = abs(C2 * beta_pos_binary[j] - wolf_positions_binary[i,j])
                    X2 = beta_pos_binary[j] - A2 * D_beta
                    
                    # Mouvement par rapport à delta
                    r1, r2 = np.random.rand(), np.random.rand()
                    A3, C3 = 2 * a_gwo_param * r1 - a_gwo_param, 2 * r2
                    D_delta = abs(C3 * delta_pos_binary[j] - wolf_positions_binary[i,j])
                    X3 = delta_pos_binary[j] - A3 * D_delta
                    
                    new_wolf_pos_continuous[j] = (X1 + X2 + X3) / 3
                
                # Conversion en binaire (0 ou 1) en utilisant un seuil (par exemple 0.5)
                # ou une fonction sigmoïde comme dans certaines implémentations GWO pour binaire
                wolf_positions_binary[i] = (new_wolf_pos_continuous > np.random.rand(num_features)).astype(int) # Simple seuil aléatoire
        
        best_feature_indices_subset = np.where(alpha_pos_binary == 1)[0].tolist()
        return best_feature_indices_subset, alpha_fitness # alpha_fitness est l'accuracy KNN
    
    def optimize_pipeline(self, num_sca_iterations=5, num_sca_strategies_per_iter=3, 
                          num_gwo_wolves_param=8, num_gwo_iterations_param=15):
        """Processus d'optimisation complet."""
        # print("Début de l'optimisation du pipeline Bennebi...\n")
        
        for sca_iter_idx in range(num_sca_iterations):
            # print(f"=== ITÉRATION SCA {sca_iter_idx+1}/{num_sca_iterations} ===")
            # 1. SCA génère des stratégies d'imputation
            current_imputation_strategies = self.SCA_generate_imputation_strategies(num_sca_strategies_per_iter)
            
            for strategy_idx, imputation_strategy_params in enumerate(current_imputation_strategies):
                # 2. Imputer les données originales (X_original_df) avec la stratégie courante
                #    et normaliser.
                X_imputed_and_scaled_df = self.impute_data(self.X_original_df, imputation_strategy_params)
                
                # 3. GWO pour la sélection de features sur ce dataset imputé et normalisé
                best_features_indices_from_gwo, gwo_accuracy_score = self.GWO_feature_selection(
                    X_imputed_and_scaled_df, 
                    num_wolves=num_gwo_wolves_param, 
                    max_gwo_iter=num_gwo_iterations_param
                )
                
                # La `gwo_accuracy_score` est déjà l'accuracy finale pour cette combinaison
                # d'imputation et de sélection de features, car GWO utilise `evaluate_features_knn`.
                final_accuracy_for_combination = gwo_accuracy_score
                
                # Stocker les résultats de cette combinaison
                current_result_details = {
                    'sca_iteration': sca_iter_idx + 1,
                    'strategy_within_sca_iter': strategy_idx + 1,
                    'imputation_strategy_details': imputation_strategy_params,
                    'num_selected_features': len(best_features_indices_from_gwo),
                    'selected_feature_indices': best_features_indices_from_gwo,
                    'selected_feature_names': [self.attributes[i] for i in best_features_indices_from_gwo],
                    'final_accuracy_knn': final_accuracy_for_combination,
                }
                self.all_run_results.append(current_result_details)
                
                # Mettre à jour la meilleure solution globale trouvée
                if final_accuracy_for_combination > self.best_score_achieved:
                    self.best_score_achieved = final_accuracy_for_combination
                    self.best_solution_details = current_result_details
                    # Stocker aussi le DataFrame imputé correspondant à la meilleure solution
                    self.best_solution_details['best_imputed_scaled_dataframe'] = X_imputed_and_scaled_df.copy() 
        
        if self.best_solution_details is None: # Si aucune solution n'a été trouvée (par ex. toutes les accuracies étaient 0)
            return {
                "error": "Aucune solution valide n'a pu être trouvée par le pipeline d'optimisation."
            }

        # Préparer le DataFrame final pour le retour (uniquement les features sélectionnées de la meilleure solution)
        best_imputed_df_for_return = self.best_solution_details['best_imputed_scaled_dataframe']
        best_selected_indices = self.best_solution_details['selected_feature_indices']
        
        # Créer le DataFrame final avec les features sélectionnées et la colonne cible
        final_df_selected_features_only = best_imputed_df_for_return.iloc[:, best_selected_indices].copy()
        # Ajouter la colonne cible originale (non normalisée)
        final_df_selected_features_only[self.y_original_series.name] = self.y_original_series.values 

        return {
            "best_solution_found": self.best_solution_details,
            "best_overall_accuracy_knn": self.best_score_achieved,
            "final_imputed_table_selected_features_json": final_df_selected_features_only.to_json(orient="split"),
            "all_tried_solutions_details": self.all_run_results # Peut être volumineux
        }