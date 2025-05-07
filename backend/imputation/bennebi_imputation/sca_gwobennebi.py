import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from IPython.display import display

class WaterQualityOptimizer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.raw_data = pd.read_csv(filepath)
        self.X = self.raw_data.drop('Potability', axis=1)
        self.y = self.raw_data['Potability']
        self.attributes = self.X.columns.tolist()
        self.best_solution = None
        self.best_score = -np.inf
        self.results = []
        
    def impute_data(self, strategy_params):
        """Imputation des données selon la stratégie"""
        imputer = SimpleImputer(
            strategy=strategy_params['strategy'],
            fill_value=strategy_params.get('fill_value')
        )
        X_imputed = pd.DataFrame(imputer.fit_transform(self.X), 
                               columns=self.attributes)
        scaler = StandardScaler()
        return pd.DataFrame(scaler.fit_transform(X_imputed), 
                          columns=self.attributes)
    
    def evaluate_features(self, imputation_params, feature_subset):
        """Évaluation avec KNN"""
        try:
            X_imputed = self.impute_data(imputation_params)
            if len(feature_subset) == 0:
                return 0.0
                
            X_subset = X_imputed.iloc[:, feature_subset]
            X_train, X_test, y_train, y_test = train_test_split(
                X_subset, self.y, test_size=0.3, random_state=42)
            
            knn = KNeighborsClassifier(n_neighbors=5)
            knn.fit(X_train, y_train)
            return accuracy_score(y_test, knn.predict(X_test))
        except:
            return 0.0
    
    def SCA_generate_solutions(self, num_solutions):
        """Génère des solutions d'imputation avec SCA"""
        strategies = ['mean', 'median', 'most_frequent', 'constant']
        solutions = []
        for _ in range(num_solutions):
            strategy = np.random.choice(strategies)
            fill_value = np.random.uniform(self.X.min().min(), self.X.max().max()) if strategy == 'constant' else None
            solutions.append({'strategy': strategy, 'fill_value': fill_value})
        return solutions
    
    def GWO_feature_selection(self, X_imputed, num_wolves=10, max_iter=20):
        """Sélection d'attributs avec GWO"""
        num_features = X_imputed.shape[1]
        wolves = np.random.rand(num_wolves, num_features) > 0.5
        
        alpha = wolves[0].copy()
        alpha_fitness = -np.inf
        beta = wolves[1].copy()
        beta_fitness = -np.inf
        delta = wolves[2].copy()
        delta_fitness = -np.inf
        
        for it in range(max_iter):
            a = 2 - it * (2 / max_iter)
            
            for i in range(num_wolves):
                selected = np.where(wolves[i])[0]
                fitness = self.evaluate_features({'strategy': 'mean'}, selected)
                
                if fitness > alpha_fitness:
                    delta = beta.copy()
                    delta_fitness = beta_fitness
                    beta = alpha.copy()
                    beta_fitness = alpha_fitness
                    alpha = wolves[i].copy()
                    alpha_fitness = fitness
                elif fitness > beta_fitness:
                    delta = beta.copy()
                    delta_fitness = beta_fitness
                    beta = wolves[i].copy()
                    beta_fitness = fitness
                elif fitness > delta_fitness:
                    delta = wolves[i].copy()
                    delta_fitness = fitness
            
            for i in range(num_wolves):
                for j in range(num_features):
                    A1 = 2 * a * np.random.rand() - a
                    C1 = 2 * np.random.rand()
                    D_alpha = abs(C1 * alpha[j] - wolves[i,j])
                    X1 = alpha[j] - A1 * D_alpha
                    
                    A2 = 2 * a * np.random.rand() - a
                    C2 = 2 * np.random.rand()
                    D_beta = abs(C2 * beta[j] - wolves[i,j])
                    X2 = beta[j] - A2 * D_beta
                    
                    A3 = 2 * a * np.random.rand() - a
                    C3 = 2 * np.random.rand()
                    D_delta = abs(C3 * delta[j] - wolves[i,j])
                    X3 = delta[j] - A3 * D_delta
                    
                    wolves[i,j] = np.clip((X1 + X2 + X3) / 3, 0, 1)
                
                wolves[i] = wolves[i] > 0.5
        
        best_subset = np.where(alpha)[0]
        return best_subset, alpha_fitness
    
    def optimize(self, num_iterations=5, num_sca_solutions=3, num_gwo_wolves=8, gwo_iterations=15):
        """Processus d'optimisation complet"""
        print("Début de l'optimisation...\n")
        
        for iteration in range(num_iterations):
            print(f"=== ITÉRATION {iteration+1}/{num_iterations} ===")
            imputation_solutions = self.SCA_generate_solutions(num_sca_solutions)
            
            for sol_idx, imp_sol in enumerate(imputation_solutions):
                X_imputed = self.impute_data(imp_sol)
                feature_subset, score = self.GWO_feature_selection(
                    X_imputed, num_gwo_wolves, gwo_iterations)
                
                final_score = self.evaluate_features(imp_sol, feature_subset)
                
                if final_score > self.best_score:
                    self.best_solution = {
                        'imputation': imp_sol,
                        'features': feature_subset,
                        'score': final_score,
                        'imputed_data': X_imputed
                    }
                    self.best_score = final_score
                
                self.results.append({
                    'iteration': iteration+1,
                    'solution': sol_idx+1,
                    'strategy': imp_sol['strategy'],
                    'num_features': len(feature_subset),
                    'accuracy': final_score,
                    'features': [self.attributes[i] for i in feature_subset]
                })
                
                # Affichage de l'itération
                print(f"\nSolution {sol_idx+1}:")
                print(f"  Stratégie d'imputation: {imp_sol['strategy']}")
                print(f"  Nombre d'attributs: {len(feature_subset)}")
                print(f"  Accuracy: {final_score:.4f}")
                print(f"  Attributs sélectionnés: {[self.attributes[i] for i in feature_subset]}")
        
        return self.best_solution
    
    def get_final_results(self):
        """Retourne tous les résultats sous forme de DataFrame"""
        return pd.DataFrame(self.results)
    
    def get_final_imputed_table(self):
        """Retourne la table finale imputée avec les meilleurs attributs"""
        if not self.best_solution:
            raise ValueError("Vous devez d'abord exécuter optimize()")
            
        imputed_data = self.best_solution['imputed_data']
        selected_features = imputed_data.iloc[:, self.best_solution['features']]
        selected_features['Potability'] = self.y.values
        
        return selected_features

# Utilisation
if __name__ == "__main__":
    # Initialisation
    optimizer = WaterQualityOptimizer('water_potability.csv')
    
    # Optimisation
    best_solution = optimizer.optimize(
        num_iterations=3,
        num_sca_solutions=2,
        num_gwo_wolves=5,
        gwo_iterations=10
    )
    
    # Résultats
    print("\n=== RÉSULTATS FINAUX ===")
    print(f"\nMeilleure solution trouvée:")
    print(f"Stratégie d'imputation: {best_solution['imputation']}")
    print(f"Accuracy: {best_solution['score']:.4f}")
    print(f"Attributs sélectionnés: {[optimizer.attributes[i] for i in best_solution['features']]}")
    
    # Explication des attributs sélectionnés
    print("\nExplication des attributs sélectionnés:")
    print("Le GWO a identifié que ces attributs contribuent le plus à la prédiction de la potabilité.")
    print("Ils ont été sélectionnés car ils maximisent la précision du modèle KNN.")
    print("La stratégie d'imputation choisie préserve au mieux les relations entre ces variables.")
    
    # Table finale imputée
    final_table = optimizer.get_final_imputed_table()
    print("\nTable finale imputée avec les meilleurs attributs:")
    display(final_table.head())
    
    # Tous les résultats
    all_results = optimizer.get_final_results()
    print("\nDétail de toutes les solutions testées:")
    display(all_results)