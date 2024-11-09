# functions here
import numpy as np
import pandas as pd

def simple_linear_regression(data, c1, c2):
    # on supprime
    a = c1
    b = c2
    for j in range(2):
        temp = data.copy()
        temp.dropna(inplace=True)
        moyenne_y = temp[a].mean()
        moyenne_x = temp[b].mean()
        moyenne_xy = temp[[a, b]].mean().sum()
        m_x_m_y = moyenne_x * moyenne_y
        moyenne_x_square = (temp[a]**2).mean()
        a1 = (moyenne_xy - m_x_m_y)/(moyenne_x_square - moyenne_x**2)
        a0 = moyenne_y - a1*moyenne_x
        data.loc[data[a].isna(), a] = a0 + a1 * data.loc[data[a].isna(), b]
        a = c2
        b = c1
    # supprimer les lignes qui n'ont pas de valeurs numériques
    data = data[~(data[c1].isna() & data[c2].isna())]
    return data

# regression linéaire multiple (not completed)
def MT(data, target_column):
    # supprimer les valeurs manquantes pour entrainer les données
    temp = data.copy()
    temp.dropna(inplace=True)
    n = temp.shape[0]
    target = temp[target_column]  # cible (y)

    # initialisation de X avec la première ligne et première colonne (n)
    X = np.ones((n, 1))

    for i in range(temp.shape[1]):
        if temp.columns[i] != target_column:  # ignorer la colonne y
            X = np.hstack([X, temp.iloc[:, i].values.reshape(-1, 1)])

    # Initialiser la matrice
    XtX = np.dot(X.T, X)
    XtY = np.dot(X.T, temp[target_column].values).reshape(-1, 1)
    # A = inv(X^T * X) * X^T * Y
    A = np.linalg.inv(XtX) @ XtY
    # les lignes de la cible qui n'ont pas de valeurs
    target_NaN_rows = data[target_column].isna()
    # supprimer la ligne si TOUTES ses valeurs sont vides
    data = data[~data.isna().all(axis=1)]

    for i in range(1, data.shape[1]):
        data.loc[target_NaN_rows, target_column] = A[0]

        for j in range(1, len(A)):
            data.loc[target_NaN_rows, target_column] += A[j] * data.iloc[:, j - 1].fillna(0)
    return data

def multiple_linear_regression(data):
    for i in range(data.shape[1]):
        # on applique la regression multiple pour toutes les colonnes du dataset
        data = MT(data, data.columns[i])
    return data