import streamlit as st
import pandas as pd
import numpy as np

st.title("Analyse des Réponses du Formulaire et tableau de codage")

data_file = 'formulaire.csv'
try:
    data = pd.read_csv(data_file)
    st.write("Tableau de données :")
    st.dataframe(data)  #  tableau de données


    data['ID'] = range(1, len(data) + 1)
    st.success("On a ajouté la colonne ID, voici un exemple : ")
    st.dataframe(data.head(3))

    new_file_name = 'new_reponses.csv'
    data.to_csv(new_file_name, index=False)
    st.write(f"Fichier sauvegardé sous : {new_file_name}")

    st.write("Informations sur les données :")
    st.text(data.info())


    def display_unique_values(column_name, start_index):
        unique_values = data[column_name].unique()
        return {f"V{start_index + i}": value for i, value in enumerate(unique_values)}

    unique_values_info = {}
    columns_of_interest = ['Q1', 'Q2', 'Q4', 'Q6', 'Q8', 'Q9', 'Q10']
    for i, column in enumerate(columns_of_interest):
        unique_values_info[column] = display_unique_values(column, start_index=(i * 10) + 1)

    st.write("Noms des colonnes et valeurs uniques :")
    st.json(unique_values_info)

    new_data = pd.DataFrame()
    new_data['ID'] = data['ID']

    # Q1 :
    dummies_q1 = pd.get_dummies(data['Q1'], prefix='', prefix_sep='')
    dummies_q1.columns = ['V1', 'V2']
    new_data = pd.concat([new_data, dummies_q1], axis=1)

    # Q2 :
    dummies_q2 = pd.get_dummies(data['Q2'], prefix='', prefix_sep='')
    dummies_q2.columns = ['V3', 'V4', 'V5']
    new_data = pd.concat([new_data, dummies_q2], axis=1)

    # Q3 :
    def create_dummy_columns(value):
        return [1 if i < value else 0 for i in range(5)]

    dummy_columns_q3 = data['Q3'].apply(create_dummy_columns).tolist()
    dummy_df_q3 = pd.DataFrame(dummy_columns_q3, columns=['V6', 'V7', 'V8', 'V9', 'V10'])
    new_data = pd.concat([new_data, dummy_df_q3], axis=1)

    # Q4
    dummies_q4 = pd.get_dummies(data['Q4'], prefix='', prefix_sep='')
    dummies_q4.columns = ['V11', 'V12', 'V13', 'V14', 'V15']
    new_data = pd.concat([new_data, dummies_q4], axis=1)

    # Q5 :
    dummy_columns_q5 = data['Q5'].apply(create_dummy_columns).tolist()
    dummy_df_q5 = pd.DataFrame(dummy_columns_q5, columns=['V16', 'V17', 'V18', 'V19', 'V20'])
    new_data = pd.concat([new_data, dummy_df_q5], axis=1)

    # Q6
    dummies_q6 = pd.get_dummies(data['Q6'], prefix='', prefix_sep='')
    dummies_q6.columns = ['V21', 'V22', 'V23', 'V24']
    new_data = pd.concat([new_data, dummies_q6], axis=1)

    # Q7 : Créer des colonnes dummy
    dummy_columns_q7 = data['Q7'].apply(create_dummy_columns).tolist()
    dummy_df_q7 = pd.DataFrame(dummy_columns_q7, columns=['V25', 'V26', 'V27', 'V28', 'V29'])
    new_data = pd.concat([new_data, dummy_df_q7], axis=1)

    # Q8
    dummies_q8 = pd.get_dummies(data['Q8'], prefix='', prefix_sep='')
    dummies_q8.columns = ['V30', 'V31', 'V32', 'V33', 'V34', 'V35']
    new_data = pd.concat([new_data, dummies_q8], axis=1)

    # Q9
    dummies_q9 = pd.get_dummies(data['Q9'], prefix='', prefix_sep='')
    dummies_q9.columns = ['V37', 'V38', 'V39']
    new_data = pd.concat([new_data, dummies_q9], axis=1)

    # Q10
    dummies_q10 = pd.get_dummies(data['Q10'], prefix='', prefix_sep='')
    dummies_q10.columns = ['V40', 'V41', 'V42']
    new_data = pd.concat([new_data, dummies_q10], axis=1)

    new_data = new_data.astype(int)

    new_data_file = 'CODING_TABLE.csv'
    new_data.to_csv(new_data_file, index=False)
    st.success(f"Nouveau fichier créé et sauvegardé sous : {new_data_file}")

    st.write("Aperçu du nouveau DataFrame :")
    st.dataframe(new_data)

except FileNotFoundError:
    st.error("Le fichier 'formulaire.csv' n'a pas été trouvé. Assurez-vous qu'il est dans le même répertoire que ce script.")
except Exception as e:
    st.error(f"Une erreur est survenue : {e}")
