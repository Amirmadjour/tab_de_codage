import pandas as pd
import numpy as np

def create_coding_table(data, ordinale_order={}):
    tab_de_codage = pd.DataFrame()

    for col in data.columns:
        unique_values = data[col].dropna().unique()
        if col in ordinale_order:
            for index, val in enumerate(unique_values):
                tab_de_codage[f"{col}_{ordinale_order[col][index]}"] = 0
        else:
            for val in unique_values:
                tab_de_codage[f"{col}_{val}"] = 0

    for i in range(data.shape[0]):
        for col in data.columns:
            value = data.loc[i, col]
            if pd.notna(value):

                if col in ordinale_order:
                    unique_values = data[col].dropna().unique()
                    for index, val in enumerate(unique_values):
                        tab_de_codage.loc[i, f"{col}_{ordinale_order[col][index]}"] = 1
                        if val == value:
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
    tab_de_contingence = []

    for i, col1 in enumerate(data.columns):
        for j, col2 in enumerate(data.columns):
            if i < j:
                tableau = data.pivot_table(
                    index=col1,
                    columns=col2,
                    aggfunc='size',
                    fill_value=0
                )

                tab_de_contingence.append(tableau)

    return tab_de_contingence