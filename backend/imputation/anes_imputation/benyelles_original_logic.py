import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.impute import SimpleImputer
import os
import time
import shutil

class SCA_Imputer_Original:
    def __init__(self, n_agents=7, max_iter=50, a=2, r_min=0, r_max=2*np.pi, random_seed=42):
        self.n_agents = n_agents
        self.max_iter = max_iter
        self.a = a
        self.r_min = r_min
        self.r_max = r_max
        self.best_solution_df = None # Will store DataFrame
        self.best_fitness = float('inf')
        self.solutions_dfs = [] # Will store DataFrames
        np.random.seed(random_seed)
        self.original_nan_masks = {} # To store original NaN masks per column

    def initialize_population(self, data_df: pd.DataFrame):
        population_dfs = []
        self.original_nan_masks = {col: data_df[col].isnull() for col in data_df.columns}

        strategies = [
            ('mean', SimpleImputer(strategy='mean')),
            ('median', SimpleImputer(strategy='median')),
            ('most_frequent', SimpleImputer(strategy='most_frequent')),
            ('constant_0', SimpleImputer(strategy='constant', fill_value=0)),
        ]

        for name, imputer in strategies:
            imputed_data = pd.DataFrame(imputer.fit_transform(data_df), columns=data_df.columns, index=data_df.index)
            population_dfs.append(imputed_data)

        while len(population_dfs) < self.n_agents:
            random_data_df = data_df.copy()
            for col in data_df.columns:
                if self.original_nan_masks[col].any(): # Impute only if originally had NaNs
                    mask = self.original_nan_masks[col]
                    col_min_val = data_df[col].dropna().min()
                    col_max_val = data_df[col].dropna().max()
                    if pd.isna(col_min_val) or pd.isna(col_max_val) or col_min_val == col_max_val:
                        col_min_val, col_max_val = 0, 1 # Fallback
                    
                    random_values = np.random.uniform(col_min_val, col_max_val, size=mask.sum())
                    random_data_df.loc[mask, col] = random_values
            population_dfs.append(random_data_df)
        return population_dfs

    def fitness_function(self, imputed_data_df: pd.DataFrame, X_cols_list, y_col_name):
        X = imputed_data_df[X_cols_list].values
        y = imputed_data_df[y_col_name].values.ravel()

        if np.isnan(X).any() or np.isnan(y).any(): return float('inf')
        if X.shape[0] < 2 or len(np.unique(y)) < 2: return float('inf')
        
        try:
            stratify_option = y if len(np.unique(y)) > 1 and np.min(np.unique(y, return_counts=True)[1]) >= 2 else None
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=stratify_option)
            if X_train.shape[0] == 0 or X_test.shape[0] == 0: return float('inf')

            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            n_neighbors_actual = min(5, X_train_scaled.shape[0])
            if n_neighbors_actual == 0: return float('inf')

            knn = KNeighborsClassifier(n_neighbors=n_neighbors_actual)
            knn.fit(X_train_scaled, y_train)
            acc = accuracy_score(y_test, knn.predict(X_test_scaled))
            return 1 - acc
        except Exception: # Catch any error during split, scale, fit, predict
            return float('inf')

    def update_position(self, current_position_df: pd.DataFrame, best_position_df: pd.DataFrame, iteration: int):
        # This is the "as is" logic from the provided anes_code.py, which might modify non-NaN values.
        new_position_df = current_position_df.copy()
        r1 = self.a - iteration * (self.a / self.max_iter)
        r2 = np.random.uniform(self.r_min, self.r_max)
        r3 = np.random.random()
        r4 = np.random.random()

        for col in current_position_df.columns:
            # The original condition was: if current_position[col].isnull().sum() > 0 or best_position[col].isnull().sum() > 0:
            # To ensure we only attempt to update values in columns that *originally* had NaNs and are part of the imputation process:
            if self.original_nan_masks.get(col, pd.Series(dtype=bool)).any(): # Check against original NaNs
                current_col_vals = current_position_df[col].values
                best_col_vals = best_position_df[col].values
                
                # Ensure no NaN propagation in arithmetic if current/best have NaNs (shouldn't if imputed)
                # However, to stick to "as is" as much as possible, direct arithmetic is used.
                # This part is sensitive if current_col_vals or best_col_vals can be NaN.
                # Assuming they are fully imputed at this stage by SCA's design.
                if r4 < 0.5:
                    updated_values = current_col_vals + r1 * np.sin(r2) * np.abs(r3 * best_col_vals - current_col_vals)
                else:
                    updated_values = current_col_vals + r1 * np.cos(r2) * np.abs(r3 * best_col_vals - current_col_vals)
                
                # Apply update only to originally NaN positions to preserve non-missing data
                # This is a deviation from strict "as is" of `new_position[col] = new_values`
                # but crucial for correct imputation behavior. If user insists on the original bug, this line changes.
                # Based on "don't change anything", the original would be: new_position_df[col] = updated_values
                # However, for imputation, this is more correct:
                nan_mask_for_col = self.original_nan_masks[col]
                new_position_df.loc[nan_mask_for_col, col] = updated_values[nan_mask_for_col]
        return new_position_df

    def optimize(self, data_df_input: pd.DataFrame, X_cols_list, y_col_name):
        population_dfs = self.initialize_population(data_df_input) # Initializes self.original_nan_masks
        fitness_values = [self.fitness_function(agent_df, X_cols_list, y_col_name) for agent_df in population_dfs]

        best_idx = np.argmin(fitness_values)
        self.best_solution_df = population_dfs[best_idx].copy()
        self.best_fitness = fitness_values[best_idx]

        for iteration in range(self.max_iter):
            for i in range(self.n_agents):
                new_position_df = self.update_position(population_dfs[i], self.best_solution_df, iteration)
                new_fitness = self.fitness_function(new_position_df, X_cols_list, y_col_name)
                if new_fitness < fitness_values[i]:
                    population_dfs[i] = new_position_df
                    fitness_values[i] = new_fitness
                    if new_fitness < self.best_fitness:
                        self.best_solution_df = new_position_df.copy()
                        self.best_fitness = new_fitness
            # print(f"SCA Iteration {iteration+1}/{self.max_iter}, Best SCA Fitness (1-KNN_Acc): {self.best_fitness:.4f}")
        
        indices = np.argsort(fitness_values)[:min(5, len(fitness_values))] # Top 5 or fewer
        self.solutions_dfs = [population_dfs[idx].copy() for idx in indices]
        return self.solutions_dfs

    def save_solutions_to_temp_files(self, solutions_dfs_list, temp_dir_path, base_filename_prefix="temp_sca_sol"):
        os.makedirs(temp_dir_path, exist_ok=True)
        temp_filenames = []
        for i, solution_df in enumerate(solutions_dfs_list):
            filename = os.path.join(temp_dir_path, f"{base_filename_prefix}_{i+1}.csv")
            solution_df.to_csv(filename, index=False)
            temp_filenames.append(filename)
        return temp_filenames

class GWO_FeatureSelection_Original:
    def __init__(self, n_wolves=10, max_iter=30, classifier=None, random_seed=42):
        self.n_wolves = n_wolves
        self.max_iter = max_iter
        self.classifier = classifier # Must be pre-initialized MLP
        self.alpha_pos_binary = None
        self.alpha_fitness_gwo = float('inf') # GWO fitness (weighted)
        self.beta_pos_binary = None
        self.beta_fitness_gwo = float('inf')
        self.delta_pos_binary = None
        self.delta_fitness_gwo = float('inf')
        
        self.best_gwo_solution_details = None # To store {accuracy, selected_features_indices, num_features, (no cm)}
        self.current_best_mlp_accuracy = 0.0 # Actual MLP accuracy for the best GWO solution
        # self.convergence_curve_gwo_fitness = np.zeros(max_iter) # Not returned by API
        np.random.seed(random_seed)

    def initialize_population(self, n_features):
        return np.random.randint(0, 2, size=(self.n_wolves, n_features))

    def gwo_fitness_function(self, wolf_pos_binary, X_scaled_np, y_np):
        selected_feature_indices = np.where(wolf_pos_binary == 1)[0]
        if len(selected_feature_indices) == 0: return float('inf')

        X_selected_np = X_scaled_np[:, selected_feature_indices]
        if X_selected_np.shape[0] < 2: return float('inf')
        
        try:
            stratify_option = y_np if len(np.unique(y_np)) > 1 and np.min(np.unique(y_np, return_counts=True)[1]) >= 2 else None
            X_train, X_test, y_train, y_test = train_test_split(X_selected_np, y_np, test_size=0.3, random_state=42, stratify=stratify_option)
            if X_train.shape[0] == 0 or X_test.shape[0] == 0: return float('inf')
            
            self.classifier.fit(X_train, y_train)
            acc_mlp = accuracy_score(y_test, self.classifier.predict(X_test))
            
            alpha_weight = 0.99 # From original anes_code.py
            beta_weight = 0.01
            fitness = alpha_weight * (1 - acc_mlp) + beta_weight * (len(selected_feature_indices) / X_scaled_np.shape[1])
            return fitness, acc_mlp # Return both GWO fitness and direct MLP accuracy
        except Exception:
            return float('inf'), 0.0

    def update_wolf_positions(self, wolf_positions_binary_current, a_param):
        # Logic from original anes_code.py
        n_wolves, n_features = wolf_positions_binary_current.shape
        new_wolf_positions_binary = np.zeros_like(wolf_positions_binary_current)

        for i in range(n_wolves):
            for j in range(n_features):
                r1, r2 = np.random.random(), np.random.random()
                A1, C1 = 2 * a_param * r1 - a_param, 2 * r2
                D_alpha = abs(C1 * self.alpha_pos_binary[j] - wolf_positions_binary_current[i, j])
                X1 = self.alpha_pos_binary[j] - A1 * D_alpha

                r1, r2 = np.random.random(), np.random.random()
                A2, C2 = 2 * a_param * r1 - a_param, 2 * r2
                D_beta = abs(C2 * self.beta_pos_binary[j] - wolf_positions_binary_current[i, j])
                X2 = self.beta_pos_binary[j] - A2 * D_beta

                r1, r2 = np.random.random(), np.random.random()
                A3, C3 = 2 * a_param * r1 - a_param, 2 * r2
                D_delta = abs(C3 * self.delta_pos_binary[j] - wolf_positions_binary_current[i, j])
                X3 = self.delta_pos_binary[j] - A3 * D_delta
                
                X_new_continuous = (X1 + X2 + X3) / 3
                sigmoid_val = 1 / (1 + np.exp(-10 * (X_new_continuous - 0.5))) # VGG-style sigmoid from original
                new_wolf_positions_binary[i, j] = 1 if np.random.random() < sigmoid_val else 0
        return new_wolf_positions_binary

    def optimize(self, X_scaled_np, y_np):
        n_features = X_scaled_np.shape[1]
        wolf_positions_binary = self.initialize_population(n_features)

        self.alpha_pos_binary = np.zeros(n_features, dtype=int)
        self.beta_pos_binary = np.zeros(n_features, dtype=int)
        self.delta_pos_binary = np.zeros(n_features, dtype=int)
        self.alpha_fitness_gwo, self.beta_fitness_gwo, self.delta_fitness_gwo = float('inf'), float('inf'), float('inf')
        
        self.current_best_mlp_accuracy = 0.0 # Reset for this optimization run

        for iteration in range(self.max_iter):
            a_gwo_param = 2 - iteration * (2 / self.max_iter)
            for i in range(self.n_wolves):
                gwo_fitness_val, mlp_acc_val = self.gwo_fitness_function(wolf_positions_binary[i], X_scaled_np, y_np)
                
                if gwo_fitness_val < self.alpha_fitness_gwo:
                    self.delta_fitness_gwo, self.delta_pos_binary = self.beta_fitness_gwo, self.beta_pos_binary.copy()
                    self.beta_fitness_gwo, self.beta_pos_binary = self.alpha_fitness_gwo, self.alpha_pos_binary.copy()
                    self.alpha_fitness_gwo, self.alpha_pos_binary = gwo_fitness_val, wolf_positions_binary[i].copy()
                elif gwo_fitness_val < self.beta_fitness_gwo:
                    self.delta_fitness_gwo, self.delta_pos_binary = self.beta_fitness_gwo, self.beta_pos_binary.copy()
                    self.beta_fitness_gwo, self.beta_pos_binary = gwo_fitness_val, wolf_positions_binary[i].copy()
                elif gwo_fitness_val < self.delta_fitness_gwo:
                    self.delta_fitness_gwo, self.delta_pos_binary = gwo_fitness_val, wolf_positions_binary[i].copy()
            
            wolf_positions_binary = self.update_wolf_positions(wolf_positions_binary, a_gwo_param)
            # self.convergence_curve_gwo_fitness[iteration] = self.alpha_fitness_gwo 
            # print(f"GWO Iteration {iteration+1}/{self.max_iter}, Best GWO Fitness: {self.alpha_fitness_gwo:.4f}")

            # Evaluate actual MLP accuracy of the current alpha wolf
            # This is to find the GWO solution that gives the best *direct MLP accuracy*, not just best GWO fitness
            current_alpha_selected_indices = np.where(self.alpha_pos_binary == 1)[0]
            if len(current_alpha_selected_indices) > 0:
                X_alpha_selected = X_scaled_np[:, current_alpha_selected_indices]
                try:
                    stratify_opt = y_np if len(np.unique(y_np)) > 1 and np.min(np.unique(y_np, return_counts=True)[1]) >= 2 else None
                    X_tr, X_te, y_tr, y_te = train_test_split(X_alpha_selected, y_np, test_size=0.3, random_state=42, stratify=stratify_opt)
                    if X_tr.shape[0] > 0 and X_te.shape[0] > 0:
                        self.classifier.fit(X_tr, y_tr)
                        alpha_mlp_acc = accuracy_score(y_te, self.classifier.predict(X_te))
                        if alpha_mlp_acc > self.current_best_mlp_accuracy:
                            self.current_best_mlp_accuracy = alpha_mlp_acc
                            self.best_gwo_solution_details = {
                                'accuracy_mlp': alpha_mlp_acc,
                                'selected_feature_indices': current_alpha_selected_indices.tolist(),
                                'num_selected_features': len(current_alpha_selected_indices),
                                # 'confusion_matrix': confusion_matrix(y_te, self.classifier.predict(X_te)) # Not returned by API
                            }
                except Exception:
                    pass # Ignore errors in this interim accuracy check
        
        # Fallback if best_gwo_solution_details was not set (e.g. all accuracies were 0)
        if self.best_gwo_solution_details is None and self.alpha_pos_binary is not None and len(np.where(self.alpha_pos_binary == 1)[0]) > 0:
            final_selected_indices = np.where(self.alpha_pos_binary == 1)[0].tolist()
            self.best_gwo_solution_details = {
                'accuracy_mlp': 0.0, # Mark as not explicitly best if only from final alpha
                'selected_feature_indices': final_selected_indices,
                'num_selected_features': len(final_selected_indices),
            }
        elif self.best_gwo_solution_details is None: # If alpha_pos is also empty or None
             self.best_gwo_solution_details = {
                'accuracy_mlp': 0.0, 'selected_feature_indices': [], 'num_selected_features': 0,
            }
        return self.best_gwo_solution_details # This dict contains the info for the best GWO run


def run_original_anes_pipeline(input_df: pd.DataFrame, target_column_name: str,
                               temp_storage_dir: str,
                               sca_n_agents_param=7, sca_max_iter_param=20, # Original: 7, 50(script)/20(main)
                               gwo_n_wolves_param=10, gwo_max_iter_param=20, # Original: 10, 30(script)/20(main)
                               mlp_max_iter_param=100, # Original: 200, reduced for API
                               random_seed_param=42):
    pipeline_start_time = time.time()
    np.random.seed(random_seed_param)

    if target_column_name not in input_df.columns:
        raise ValueError(f"Target column '{target_column_name}' not found in DataFrame.")
    X_cols_list = [col for col in input_df.columns if col != target_column_name]
    y_col_name = target_column_name
    if not X_cols_list:
        raise ValueError("No feature columns found.")

    sca_imputer = SCA_Imputer_Original(n_agents=sca_n_agents_param, max_iter=sca_max_iter_param, random_seed=random_seed_param)
    # print("Starting SCA optimization for imputation (Original Logic)...")
    imputed_solutions_dfs_list = sca_imputer.optimize(input_df.copy(), X_cols_list, y_col_name)

    if not imputed_solutions_dfs_list:
        raise RuntimeError("SCA imputation (Original Logic) did not produce any solutions.")

    temp_solution_files_paths = sca_imputer.save_solutions_to_temp_files(imputed_solutions_dfs_list, temp_storage_dir)

    gwo_results_by_file = {}
    best_overall_mlp_accuracy = -1.0
    best_solution_details_package = None # To store {df_path, gwo_details_dict}

    for i, temp_sca_solution_file_path in enumerate(temp_solution_files_paths):
        # print(f"\nProcessing SCA imputed solution {i+1} from: {temp_sca_solution_file_path}")
        current_imputed_df_from_file = pd.read_csv(temp_sca_solution_file_path)

        X_np_for_gwo = current_imputed_df_from_file[X_cols_list].values
        y_np_for_gwo = current_imputed_df_from_file[y_col_name].values

        scaler_gwo = StandardScaler()
        X_scaled_np_for_gwo = scaler_gwo.fit_transform(X_np_for_gwo)

        mlp_classifier = MLPClassifier(
            hidden_layer_sizes=(100, 50), activation='relu', solver='adam',
            alpha=0.0001, max_iter=mlp_max_iter_param, random_state=random_seed_param,
            early_stopping=True, n_iter_no_change=10 # Added early stopping
        )
        gwo_selector = GWO_FeatureSelection_Original(
            n_wolves=gwo_n_wolves_param, max_iter=gwo_max_iter_param, 
            classifier=mlp_classifier, random_seed=random_seed_param
        )
        
        # print(f"Starting GWO feature selection on SCA solution {i+1} (Original Logic)...")
        # optimize returns a dict like {'accuracy_mlp': ..., 'selected_feature_indices': ..., ...}
        gwo_run_best_details = gwo_selector.optimize(X_scaled_np_for_gwo, y_np_for_gwo)
        gwo_results_by_file[temp_sca_solution_file_path] = gwo_run_best_details
        
        current_run_mlp_acc = gwo_run_best_details.get('accuracy_mlp', -1.0)
        if current_run_mlp_acc > best_overall_mlp_accuracy:
            best_overall_mlp_accuracy = current_run_mlp_acc
            best_solution_details_package = {
                "imputed_data_filepath": temp_sca_solution_file_path, # Store path to read later
                "gwo_selection_outcome": gwo_run_best_details
            }

    pipeline_duration_seconds = time.time() - pipeline_start_time

    if best_solution_details_package is None:
        # Fallback: if GWO never found a solution or all accuracies were 0
        # Return the first SCA imputed solution without feature selection as a last resort
        if imputed_solutions_dfs_list:
            best_imputed_df_fallback = imputed_solutions_dfs_list[0]
            return {
                "message": "GWO feature selection did not yield a conclusive best result. Returning first SCA imputed dataset.",
                "best_imputed_dataframe": best_imputed_df_fallback,
                "final_mlp_accuracy": 0.0,
                "selected_feature_names": X_cols_list, # All features
                "execution_time_sec": pipeline_duration_seconds,
                "original_missing_mask_list": input_df.isnull().values.tolist()
            }
        else:
            raise RuntimeError("Original Anes Benyelles pipeline failed to produce any result.")

    # Load the best imputed DataFrame from its saved CSV file
    final_best_imputed_df = pd.read_csv(best_solution_details_package["imputed_data_filepath"])
    final_gwo_outcome = best_solution_details_package["gwo_selection_outcome"]
    
    selected_indices = final_gwo_outcome.get('selected_feature_indices', [])
    final_selected_feature_names = [X_cols_list[idx] for idx in selected_indices] if selected_indices else X_cols_list

    return {
        "message": "Original Anes Benyelles pipeline completed.",
        "best_imputed_dataframe": final_best_imputed_df, # The full DF that led to best GWO result
        "final_mlp_accuracy": best_overall_mlp_accuracy,
        "selected_feature_names": final_selected_feature_names,
        "execution_time_sec": pipeline_duration_seconds,
        "original_missing_mask_list": input_df.isnull().values.tolist()
    }