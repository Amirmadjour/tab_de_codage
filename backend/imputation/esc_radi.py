import numpy as np
from mealpy import FloatVar, SCA
from sklearn.metrics import f1_score, accuracy_score
import pandas as pd
from sklearn.preprocessing import StandardScaler

def ESC(N, max_iter, lb, ub, dim, fobj):
    # Ensure bounds are arrays
    if np.isscalar(lb):
        lb = np.ones(dim) * lb
        ub = np.ones(dim) * ub

    # Initialize population
    population = np.random.rand(N, dim) * (ub - lb) + lb
    fitness = np.array([fobj(ind) for ind in population])
    idx = np.argsort(fitness)
    fitness = fitness[idx]
    population = population[idx]

    elite_size = 5
    beta_base = 1.5
    t = 0
    mask_probability = 0.5
    fitness_history = []
    best_solutions = population[:elite_size, :]

    def adaptive_levy_weight(beta_base, dim, t, max_iter):
        beta = beta_base + 0.5 * np.sin(np.pi / 2 * t / max_iter)
        beta = np.clip(beta, 0.1, 2)
        sigma = (np.math.gamma(1 + beta) * np.sin(np.pi * beta / 2) /
                 (np.math.gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))) ** (1 / beta)
        u = np.random.normal(0, sigma, dim)
        v = np.random.normal(0, 1, dim)
        w = np.abs(u / np.abs(v) ** (1 / beta))
        return w / (np.max(w) + np.finfo(float).eps)

    while t < max_iter:
        panic_index = np.cos(np.pi / 2 * (t / (3 * max_iter)))
        idx = np.argsort(fitness)
        fitness = fitness[idx]
        population = population[idx]
        calm_count = int(round(0.15 * N))
        conform_count = int(round(0.35 * N))
        calm = population[:calm_count, :]
        conform = population[calm_count:calm_count + conform_count, :]
        panic = population[calm_count + conform_count:, :]
        calm_center = np.mean(calm, axis=0)

        new_population = population.copy()

        for i in range(N):



            if t / max_iter <= 0.5:
                if i < calm_count:
                    mask1 = np.random.rand(dim) > mask_probability
                    weight_vector1 = adaptive_levy_weight(beta_base, dim, t, max_iter)
                    random_position = np.min(calm, axis=0) + np.random.rand(dim) * (
                                np.max(calm, axis=0) - np.min(calm, axis=0))
                    new_population[i, :] += mask1 * (weight_vector1 * (calm_center - population[i, :]) +
                                                     (random_position - population[i, :] + np.random.randn(
                                                         dim) / 50) )* panic_index
                elif i < calm_count + conform_count:
                    mask1 = np.random.rand(dim) > mask_probability
                    mask2 = np.random.rand(dim) > mask_probability
                    weight_vector1 = adaptive_levy_weight(beta_base, dim, t, max_iter)
                    weight_vector2 = adaptive_levy_weight(beta_base, dim, t, max_iter)
                    random_position = np.min(conform, axis=0) + np.random.rand(dim) * (
                                np.max(conform, axis=0) - np.min(conform, axis=0))
                    panic_individual = panic[np.random.randint(panic.shape[0])] if len(panic) > 0 else np.zeros(dim)
                    new_population[i, :] += mask1 * (weight_vector1 * (calm_center - population[i, :]) +
                                                     mask2 * weight_vector2 * (panic_individual - population[i, :]) +
                                                     (random_position - population[i, :] + np.random.randn(
                                                         dim) / 50) * panic_index)
                else:
                    mask1 = np.random.rand(dim) > mask_probability
                    mask2 = np.random.rand(dim) > mask_probability
                    weight_vector1 = adaptive_levy_weight(beta_base, dim, t, max_iter)
                    weight_vector2 = adaptive_levy_weight(beta_base, dim, t, max_iter)
                    elite = best_solutions[np.random.randint(elite_size)]
                    random_individual = population[np.random.randint(N)]
                    random_position = elite + weight_vector1 * (random_individual - elite)
                    new_population[i, :] += mask1 * (weight_vector1 * (elite - population[i, :]) +
                                                     mask2 * weight_vector2 * (random_individual - population[i, :]) +
                                                     (random_position - population[i, :] + np.random.randn(
                                                         dim) / 50) * panic_index)
            else:
                mask1 = np.random.rand(dim) > mask_probability
                mask2 = np.random.rand(dim) > mask_probability
                weight_vector1 = adaptive_levy_weight(beta_base, dim, t, max_iter)
                weight_vector2 = adaptive_levy_weight(beta_base, dim, t, max_iter)
                elite = best_solutions[np.random.randint(elite_size)]
                random_individual = population[np.random.randint(N)]
                new_population[i, :] += mask1 * weight_vector1 * (elite - population[i, :]) + \
                                        mask2 * weight_vector2 * (random_individual - population[i, :])

        # Boundary control
        new_population = np.clip(new_population, lb, ub)

        # Evaluate new population
        new_fitness = np.array([fobj(ind) for ind in new_population])

        # Replace individuals with better fitness
        for i in range(N):
            if new_fitness[i] < fitness[i]:
                population[i, :] = new_population[i, :]
                fitness[i] = new_fitness[i]

        # Update elite pool
        idx = np.argsort(fitness)
        fitness = fitness[idx]
        population = population[idx]
        best_solutions = population[:elite_size, :]

        # Record best fitness
        fitness_history.append(fitness[0])
        t += 1

    return fitness[0], population[0, :], fitness_history



def esc_impute(dataset):
    column_names = dataset.columns
    data = dataset.to_numpy()

    scaler = StandardScaler()
    non_nan_mask = ~np.isnan(data)
    temp_data = data.copy()

    for col in range(data.shape[1]):
        col_mean = np.nanmean(data[:, col])
        temp_data[np.isnan(data[:, col]), col] = col_mean

    data_standardized = scaler.fit_transform(temp_data)
    data_standardized[~non_nan_mask] = np.nan
    data = data_standardized

    metrics = {}
    indices_nan = np.argwhere(np.isnan(data))
    n_cols = data.shape[1]

    min_values = np.nanmin(data, axis=0)
    max_values = np.nanmax(data, axis=0)

    temp = data.copy()
    for (i, j) in indices_nan:
        temp[i, j] = np.random.uniform(min_values[j], max_values[j])

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

        mse = 0
        n_valid_cols = 0
        for col in range(n_cols):
            if len(original_values[col]) > 0:
                col_mse = np.mean((temp_data[original_indices[col], col] - original_values[col]) ** 2)
                mse += col_mse
                n_valid_cols += 1

        return mse / max(1, n_valid_cols)

    # paramétres de ESC
    N = 5  # pop size
    max_iter = 1200  # iterations
    dim = len(indices_nan)  
    
    lb = np.array([min_values[j] for i, j in indices_nan]) 
    ub = np.array([max_values[j] for i, j in indices_nan])  

    best_score, best_solution, fitness_history = ESC(N, max_iter, lb, ub, dim, objective_function)
    mse_history = fitness_history

    idx = 0
    for col in range(n_cols):
        col_indices_nan = indices_nan[indices_nan[:, 1] == col]
        temp[col_indices_nan[:, 0], col] = best_solution[idx:idx + len(col_indices_nan)]
        idx += len(col_indices_nan)

    #  mesures de performance
    for col in range(n_cols):
        if np.any(np.isnan(data[:, col])):
            threshold = np.median(data[~np.isnan(data[:, col]), col])

            if len(original_values[col]) > 0:
                y_true = (original_values[col] > threshold).astype(int)
                y_pred = (data[original_indices[col], col] > threshold).astype(int)

                metrics[column_names[col]] = {
                    'column_name': column_names[col],
                    'f_score': f1_score(y_true, y_pred),
                }

    temp = scaler.inverse_transform(temp)

    accuracies = [1 - mse for mse in mse_history]

    results = {
        'dataset_imputed': pd.DataFrame(temp, columns=column_names),
        'missing_mask': np.isnan(data).tolist(),
        'metrics': metrics,
        'nb_imputed_values': np.sum(np.isnan(data)),
        'overall_metrics': {
            'initial_mse': mse_history[0],
            'final_mse': mse_history[-1],
            'max_accuracy': accuracies[-1],
            'total_improvement': ((mse_history[0] - mse_history[-1]) / mse_history[0]) * 100
        },
        'fitness_mse': mse_history,
        'accuracy': accuracies
    }

    return results
