from mealpy import FloatVar, BinaryVar, SCA, GWO
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

def combined_imputation_selection(data, epoch_sca=50, pop_sca=10, epoch_gwo=10, pop_gwo=5):
    features = data[:, :-1]
    target = data[:, -1]
    nan_indices = np.argwhere(np.isnan(features))

    complete_rows = ~np.isnan(features).any(axis=1)
    scaler = StandardScaler()
    scaler.fit(features[complete_rows])
    scaled_bounds = scaler.transform(features[complete_rows])
    
    # min and max for each column
    lb_feat = np.nanmin(scaled_bounds, axis=0)
    ub_feat = np.nanmax(scaled_bounds, axis=0)

    # bounds for each missing value
    lb = [lb_feat[c] for r, c in nan_indices]
    ub = [ub_feat[c] for r, c in nan_indices]

    def sca_fitness(solution):
        temp_features = features.copy()
        for i, (r, c) in enumerate(nan_indices):
            temp_features[r, c] = solution[i]

        try:
            scaled = scaler.transform(temp_features)
        except:
            return 1.0  # invalid data fallback

        def gwo_fitness(mask):
            mask = np.round(mask).astype(int)

            # If no feature is selected, randomly select one to avoid crash
            if np.sum(mask) == 0:
                idx = np.random.randint(0, len(mask))
                mask[idx] = 1
            
            selected = scaled[:, mask == 1]
            X_train, X_test, y_train, y_test = train_test_split(
                selected, target, test_size=0.2, random_state=42)
              
            if (X_train.shape[1] == 0): 
              return 1.0

            model = KNeighborsClassifier(n_neighbors=5)
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            acc = accuracy_score(y_test, preds)
            return 1 - acc  # minimize

        gwo_problem = {
            "bounds": BinaryVar(n_vars=features.shape[1], name="feature_mask"),
            "minmax": "min",
            "obj_func": gwo_fitness
        }

        gwo_model = GWO.OriginalGWO(epoch=epoch_gwo, pop_size=pop_gwo)
        gwo_result = gwo_model.solve(gwo_problem)
        return gwo_result.target.fitness  # 1 - acc

    sca_problem = {
        "bounds": FloatVar(lb=lb, ub=ub, name="impute_vals"),
        "minmax": "min",
        "obj_func": sca_fitness
    }

    sca_model = SCA.DevSCA(epoch=epoch_sca, pop_size=pop_sca)
    result = sca_model.solve(sca_problem)

    # Imputation
    final_features = features.copy()
    for i, (r, c) in enumerate(nan_indices):
        final_features[r, c] = result.solution[i]
    final_features = scaler.transform(final_features)
    best_mask = result.solution.astype(bool)
    final_accuracy = 1 - result.target.fitness


    print(f"✅ Meilleure sélection d'attributs : {best_mask}")
    print(f"🎯 Accuracy finale : {final_accuracy:.4f}")
    return best_mask, final_accuracy

# === Utilisation ===
df = pd.read_csv("water_potability.csv")
data = df.to_numpy()
selected_features, acc = combined_imputation_selection(data, epoch_sca=10, pop_sca=10, epoch_gwo=10, pop_gwo=10)
