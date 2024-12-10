import numpy as np
from mealpy import FloatVar, SCA
from sklearn.metrics import f1_score, accuracy_score
import pandas as pd
from sklearn.preprocessing import StandardScaler


def sca_impute(dataset):

    column_names = dataset.columns
    data = dataset.to_numpy()

    scaler = StandardScaler()
    non_nan_mask = ~np.isnan(data)
    temp_data = data.copy()

    # on impute les valeurs manquante avaec col.mean()
    for col in range(data.shape[1]):
        col_mean = np.nanmean(data[:, col])
        temp_data[np.isnan(data[:, col]), col] = col_mean

    # standardization sinon ça marche pas
    data_standardized = scaler.fit_transform(temp_data)
    data_standardized[~non_nan_mask] = np.nan

    data = data_standardized

    metrics = {}

    # indices des valeurs manquantes pour chaque colonne
    indices_nan = np.argwhere(np.isnan(data))
    n_cols = data.shape[1]

    # min et max pour chaque colonne
    min_values = np.nanmin(data, axis=0)
    max_values = np.nanmax(data, axis=0)

    # on copie le dataset et on le remplit avec des valeurs aléatoires
    temp = data.copy()
    for (i, j) in indices_nan:
        temp[i, j] = np.random.uniform(min_values[j], max_values[j])

    # Stocker les valeurs non manquantes
    original_values = {col: temp[~np.isnan(temp[:, col]), col].copy() for col in range(n_cols)}
    original_indices = {col: np.where(~np.isnan(temp[:, col]))[0] for col in range(n_cols)}

    mse_history = []

    def objective_function(solution):
        temp_data = temp.copy()
        idx = 0


        for col in range(n_cols):
            col_indices_nan = indices_nan[indices_nan[:, 1] == col]
            if len(col_indices_nan) > 0:
                temp_data[col_indices_nan[:, 0], col] = solution[idx:idx + len(col_indices_nan)]
                idx += len(col_indices_nan)

        # on calcul MSE pour les valeurs manquantes
        mse = 0
        n_valid_cols = 0
        for col in range(n_cols):
            if len(original_values[col]) > 0:
                #formule MSE
                col_mse = np.mean((temp_data[original_indices[col], col] - original_values[col]) ** 2)
                mse += col_mse
                n_valid_cols += 1

        return mse / max(1, n_valid_cols)

    problem_dict = {
        "bounds": FloatVar(lb=np.repeat(min_values, len(indices_nan)),
                           ub=np.repeat(max_values, len(indices_nan)),
                           name="missing_values"),
        "minmax": "min",
        "obj_func": objective_function
    }

    best_mse_history = []

    def on_epoch_end(epoch, population):
        best_mse = population[0].target.fitness
        best_mse_history.append(best_mse)

    class CustomSCA(SCA.DevSCA):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def evolve(self, epoch):
            mse_history.append(self.g_best.target.fitness)
            super().evolve(epoch)

    model = CustomSCA(epoch=500, pop_size=10)
    g_best = model.solve(problem_dict)

    # appliquer l'imputation imputation finale
    idx = 0
    for col in range(n_cols):
        col_indices_nan = indices_nan[indices_nan[:, 1] == col]
        temp[col_indices_nan[:, 0], col] = g_best.solution[idx:idx + len(col_indices_nan)]
        idx += len(col_indices_nan)

    # on calcule les mesures de performances
    for col in range(n_cols):
       # Vérifier si la colonne contient des nan
       if np.any(np.isnan(data[:, col])):  # si la colonne contient des nan
           threshold = np.median(data[~np.isnan(data[:, col]), col])  # Calculer le seuil basé sur les valeurs présentes

           # considérer que les données manquantes sont remplies ou traitées
           if len(original_values[col]) > 0:
               y_true = (original_values[col] > threshold).astype(int)
               y_pred = (data[original_indices[col], col] > threshold).astype(int)

               metrics[column_names[col]] = {
                   'column_name': column_names[col],
                   'f_score': f1_score(y_true, y_pred),
               }

    # enlever la standardisation
    temp = scaler.inverse_transform(temp)

    # accuracy/epoch
    accuracies = [1 - mse for mse in mse_history]

    results = {
        'dataset_imputed': pd.DataFrame(temp, columns=column_names),
        'missing_mask': np.isnan(data).tolist(),
        'metrics': metrics,
        'nb_imputed_values' : np.sum(np.isnan(data)),
        'overall_metrics': {
            'initial_mse': mse_history[0],
            'final_mse': mse_history[-1],
            'max_accuracy' : accuracies[-1],
            'total_improvement': ((mse_history[0] - mse_history[-1]) / mse_history[0]) * 100},
        'fitness_mse': mse_history,
        'accuracy' : accuracies
    }

    return results