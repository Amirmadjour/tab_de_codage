# functions here
import numpy as np
import pandas as pd
import math
from sklearn.impute import KNNImputer

def knn_imputer(data):
    imputer = KNNImputer(n_neighbors=5, weights="uniform", metric="nan_euclidean")
    indices_nan = np.isnan(data).tolist()

    return imputer.fit_transform(data)

def nbValManquantes(pd):
  valManqua = {}
  for col in pd:
    sum = 0
    for row in pd[col]:
      if math.isnan(row):
        sum += 1

    valManqua[col] = sum

  return valManqua

# KNN
def calculate_row_distances_with_nan(data, target_row_index):
    # Extract the target row
    target_row = data[target_row_index]

    data = data[~np.isnan(data[:, 0])]

    # Initialize an array to store distances
    distances = []

    for i, row in enumerate(data):
        if i == target_row_index:
            continue  # Skip the target row itself

        # Element-wise difference (ignoring NaN values)
        diff = row - target_row

        # Only calculate the squared difference where both elements are not NaN
        squared_diff = (diff ** 2)

        nan_count = np.sum(np.isnan(squared_diff))

        # Sum the squared differences, ignoring NaN values
        squared_sum = ((len(diff) - 1) / (len(diff) - nan_count)) * np.nansum(squared_diff)

        # Take the square root of the squared sum
        distance = np.sqrt(squared_sum)

        distances.append(distance)

    return np.array(distances)



def knn_imputer_madjour(data, k):
    def calculate_distance(row1, row2):
        # Element-wise difference, ignoring NaNs
        diff = row1 - row2
        # Squared difference where both elements are not NaN
        squared_diff = np.where(~np.isnan(diff), diff ** 2, 0)
        # Count non-NaN elements
        valid_count = np.sum(~np.isnan(diff))
        if valid_count == 0:
            return np.inf  # If no valid comparisons, return infinite distance
        # Return square root of normalized sum
        return np.sqrt(np.sum(squared_diff) * ((len(row1) - 1) / valid_count))

    # Create a copy of the data to avoid modifying the original
    data_imputed = data.copy()

    # Get the indices of NaN values
    nan_indices = [
        [int(row), col]
        for col in range(data.shape[1])
        for row in np.argwhere(np.isnan(data[:, col])).flatten()
    ]

    for nan_row, nan_col in nan_indices:
        # Extract the target row with missing value
        target_row = data_imputed[nan_row]
        if(nan_row == 318 and nan_col):
            print(target_row)

        # Compute distances to all other rows
        distances = []
        for i, row in enumerate(data_imputed):
            if i != nan_row:  # Skip the target row itself
                distance = calculate_distance(target_row, row)
                distances.append((distance, i))

        # Sort distances and select the k nearest neighbors with non-NaN values in the column
        distances.sort(key=lambda x: x[0])
        k_nearest_indices = [
            index for _, index in distances if not np.isnan(data[index, nan_col])
        ][:k]  # Limit to k neighbors

        # Impute the missing value using the mean of the k nearest neighbors
        if k_nearest_indices:
            neighbor_values = [data[i, nan_col] for i in k_nearest_indices]
            data_imputed[nan_row, nan_col] = np.average(neighbor_values)

    return data_imputed

# regression linéaire multiple
def MT(data, target_column):

    temp = data.dropna()
    n = temp.shape[0]

    y = temp[target_column].values.reshape(-1, 1)
    X = temp.drop(columns=[target_column]).values


    X = np.hstack([np.ones((n, 1)), X])


    XtX = np.dot(X.T, X)  # X^T * X
    XtY = np.dot(X.T, y)  # X^T * Y
    A = np.linalg.pinv(XtX).dot(XtY)  # A = (X^T * X)^-1 * X^T * Y


    for idx in data.index:
        if pd.isna(data.loc[idx, target_column]):  # si la cible est manquante
            features = data.loc[idx].drop(target_column).values

            features = np.where(pd.isna(features), np.nanmean(data.drop(columns=[target_column]).values, axis=0), features)


            features = np.insert(features, 0, 1)  #[1,x1,x2,x3......]


            prediction = np.dot(features, A)     # 1a0+x1a1+x2*a2.........
            data.loc[idx, target_column] = prediction[0]

    return data

def multiple_linear_regression(data):
    #je dois ajouter une condition : si la colonne contient des valeurs NaN
    data_copy = data.copy()
    for i in range(data.shape[1]):
        # on applique la regression multiple pour toutes les colonnes du dataset
        data_copy = MT(data_copy, data.columns[i])

    return data_copy



#correlation matrix
def Standardisation(data):
  column_means = np.mean(data, axis=0)
  column_std = np.std(data, axis=0)

  return (data - column_means) / column_std

def MatriceCorrelation(Z, n):
  return 1/n * Z.T.dot(Z)


# boxplot

def boxplot(data):
    return {col: data[col].to_numpy() for col in data.columns}


def histogram(data):
    tableaux = {}
    for column in data.columns:
        col_data = data[column].dropna()

        min_val = col_data.min()
        max_val = col_data.max()
        plage = round(max_val - min_val, 4)
        nb_classes = int(np.ceil(1+3.3322*np.log10(len(col_data))))  # sturges
        longueur = round(plage / nb_classes, 4)

        # Built-in function to calculate histogram frequencies
        bins = np.linspace(min_val, max_val, nb_classes + 1)
        frequencies, _ = np.histogram(col_data, bins=bins)

        tableaux[column] = {
            'nom_colonne': column,
            'frequences': frequencies.tolist(),
            'longueur_classe': longueur,
            'nb_classes': nb_classes
        }

    return tableaux