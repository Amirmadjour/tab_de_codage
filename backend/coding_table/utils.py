import pandas as pd


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
        unique_values = df[column].unique()

        if len(unique_values) == 2:
            tableau_de_codage_disjonctif_complet[f'{column}_1'] = df[column].map({unique_values[0]: 1, unique_values[1]: 0})
            tableau_de_codage_disjonctif_complet[f'{column}_2'] = df[column].map({unique_values[0]: 0, unique_values[1]: 1})

        elif len(unique_values) > 2:
            for i, value in enumerate(unique_values, start=1):
                tableau_de_codage_disjonctif_complet[f'{column}_{i}'] = df[column].map({v: 1 if v == value else 0 for v in unique_values})

    return tableau_de_codage_disjonctif_complet
