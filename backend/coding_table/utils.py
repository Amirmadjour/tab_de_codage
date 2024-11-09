import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans

def create_coding_table(data, ordinale_order={}):
    tab_de_codage = pd.DataFrame()
    print("ordinal_order my man: ", ordinale_order)

    for col in data.columns:
        unique_values = data[col].dropna().unique()
        if col in ordinale_order:
            for val in ordinale_order[col]:
               if val in unique_values:
                    tab_de_codage[f"{col}_{val}"] = 0
        else:
            for val in unique_values:
                tab_de_codage[f"{col}_{val}"] = 0

    for i in range(data.shape[0]):
        for col in data.columns:
            value = data.loc[i, col]
            if pd.notna(value):

                if col in ordinale_order:
                    for val in ordinale_order[col]:
                        if val == value:
                            tab_de_codage.loc[i, f"{col}_{val}"] = 1
                            break
                else:
                    tab_de_codage.loc[i, f"{col}_{value}"] = 1

    tab_de_codage.reset_index(drop=True, inplace=True)
    tab_de_codage = tab_de_codage.fillna(0)
    tab_de_codage = tab_de_codage.astype(int)

    return tab_de_codage




def create_coding_table_disjonctif_complet(data, tab_de_codage):
    tab_de_codage_disjonctif = pd.DataFrame()

    for col in data.columns:
        unique_values = data[col].dropna().unique()
        for val in unique_values:
            tab_de_codage_disjonctif[f"{col}_{val}"] = 0

    for i in range(data.shape[0]):
        for col in data.columns:
            value = data.loc[i, col]
            if pd.notna(value):
                tab_de_codage_disjonctif.loc[i, f"{col}_{value}"] = 1

    tab_de_codage_disjonctif.fillna(0, inplace=True)
    tab_de_codage_disjonctif = tab_de_codage_disjonctif.astype(int)

    # sorted avec tableau de codage
    ordered_columns = tab_de_codage.columns.tolist()
    tab_de_codage_disjonctif = tab_de_codage_disjonctif[ordered_columns]

    return tab_de_codage_disjonctif


def tab_de_distance(tab_codage):

  # Mesure de ressemblance
  rows, columns = tab_codage.shape
  tab_de_distance = pd.DataFrame(np.zeros((columns, columns)), columns=tab_codage.columns)

  def calcRessemblance(a, b):
    resultat = 0
    for i in range(0, len(a)):
      if(a[i] == b[i]):
        resultat += 1
    return resultat/len(a)


  for i in range(0, len(tab_codage.columns)):
    for j in range(0, len(tab_codage.columns)):
      tab_de_distance.iloc[i, j] =(calcRessemblance(tab_codage.iloc[:, i], tab_codage.iloc[:, j]))

  return tab_de_distance

def tab_burt(tab_de_codage_disjonctif_complet):
  Burt = tab_de_codage_disjonctif_complet.T.dot(tab_de_codage_disjonctif_complet)
  return Burt

def create_tableau_de_contingence(data):
    tableaux = {}

    for i, col1 in enumerate(data.columns):
        for j, col2 in enumerate(data.columns):
            if i < j:
                # Créer le tableau de contingence
                tableau = data.pivot_table(
                    index=col1,
                    columns=col2,
                    aggfunc='size',
                    fill_value=0
                )

                le_x, le_y = LabelEncoder(), LabelEncoder()

                x_encoded = le_x.fit_transform(tableau.index)
                y_encoded = le_y.fit_transform(tableau.columns)

                x_coords = np.repeat(x_encoded, len(y_encoded))
                y_coords = np.tile(y_encoded, len(x_encoded))
                values = tableau.values.flatten()

                points = np.array([x_coords, y_coords]).T
                weights = values / values.sum()

                kmeans = KMeans(n_clusters=1, random_state=0)
                barycenter = kmeans.fit(points, sample_weight=weights).cluster_centers_[0]

                tableaux[f"{col1}_|_{col2}"] = {
                    'tableau': tableau,
                    'centre_de_gravite': tuple(barycenter)
                }

    return tableaux
