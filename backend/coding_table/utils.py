import pandas as pd
import numpy as np

def create_coding_table(df, ordinal_cols=None):
    tableau_de_codage = pd.DataFrame()

    for column in df.columns:
        unique_values = df[column].unique()

        if len(unique_values) == 2:
            tableau_de_codage[f'{column}_1'] = df[column].map({unique_values[0]: 1, unique_values[1]: 0})
            tableau_de_codage[f'{column}_2'] = df[column].map({unique_values[0]: 0, unique_values[1]: 1})

        elif len(unique_values) > 2:
            for i, value in enumerate(unique_values, start=1):
                tableau_de_codage[f'{column}_{i}'] = df[column].map({v: 1 if v == value else 0 for v in unique_values})

        if ordinal_cols and column in ordinal_cols:
            for i in range(1, len(unique_values) + 1):
                tableau_de_codage[f'{column}_{i}'] = df[column].apply(lambda x: 1 if x >= unique_values[i - 1] else 0)

    return tableau_de_codage

def create_coding_table_disjonctif_complet(df):
    tableau_de_codage_disjonctif_complet = pd.DataFrame()

    for column in df.columns:
        unique_values = sorted(df[column].unique())
        # si la variable est ordinale
        if pd.api.types.is_integer_dtype(df[column]):
            for i, value in enumerate(unique_values, start=1):
                tableau_de_codage_disjonctif_complet[f'{column}_{i}'] = df[column].apply(lambda x: 1 if x == value else 0)
        # norminale
        if len(unique_values) == 2:
            tableau_de_codage_disjonctif_complet[f'{column}_1'] = df[column].map({unique_values[0]: 1, unique_values[1]: 0})
            tableau_de_codage_disjonctif_complet[f'{column}_2'] = df[column].map({unique_values[0]: 0, unique_values[1]: 1})

        elif len(unique_values) > 2:
            for i, value in enumerate(unique_values, start=1):
                tableau_de_codage_disjonctif_complet[f'{column}_{i}'] = df[column].map({v: 1 if v == value else 0 for v in unique_values})
    return tableau_de_codage_disjonctif_complet

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