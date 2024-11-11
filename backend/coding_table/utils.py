import pandas as pd
import numpy as np

def create_coding_table(data, ordinale_order={}):
    tab_de_codage = pd.DataFrame()
    print(ordinale_order)

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
                        tab_de_codage.loc[i, f"{col}_{val}"] = 1
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
    tableaux = {}

    for i, col1 in enumerate(data.columns):
        for j, col2 in enumerate(data.columns):
            if i < j:
                # création du tableau de contingence
                tableau_de_contigence = data.pivot_table(
                    index=col1,
                    columns=col2,
                    aggfunc='size',
                    fill_value=0
                )

                row_totals = tableau_de_contigence.sum(axis=1)
                tableau_de_profil_ligne = tableau_de_contigence.div(row_totals, axis=0)

                col_totals = tableau_de_contigence.sum(axis=0)
                tableau_de_profil_colonne = tableau_de_contigence.div(col_totals, axis=1)


                unique_rows = tableau_de_profil_ligne.index
                unique_cols = tableau_de_profil_ligne.columns
                x_coords = np.arange(len(unique_rows))
                y_coords = np.arange(len(unique_cols))

                # centre de gravité
                total_values = tableau_de_contigence.values.sum()
                poids_x = 0
                poids_y = 0
                # formule du centre de gravité
                for ligne_id, row_val in enumerate(x_coords):
                    for col_id, col_val in enumerate(y_coords):
                        poids = tableau_de_contigence.iloc[ligne_id, col_id] / total_values
                        poids_x += row_val * poids
                        poids_y += col_val * poids

                centre_de_gravite = (round(poids_x, 4), round(poids_y, 4))


                #  N(I)
                nuage_points = []
                for idd, row in tableau_de_profil_ligne.iterrows():
                    f_i = row_totals[idd] / row_totals.sum()
                    profil_coords = [(round(row[j], 4)) for j in tableau_de_profil_ligne.columns]
                    nuage_points.append([profil_coords, (round(f_i, 4))])


                # N(J)
                nuage_points_J = []
                for col in tableau_de_profil_colonne.columns:
                    f_j = col_totals[col] / col_totals.sum()  # Poids de la colonne
                    profil_coords = [(round(tableau_de_profil_colonne.loc[i, col], 4)) for i in tableau_de_profil_colonne.index]
                    nuage_points_J.append([profil_coords, round(f_j, 4)])

                # export
                tableaux[f"{col1}_|_{col2}"] = {
                    'tableau': tableau_de_contigence,
                    'centre_de_gravite': tuple(centre_de_gravite),
                    'N(I)': nuage_points,
                    'N(J)': nuage_points_J

                }

    return tableaux