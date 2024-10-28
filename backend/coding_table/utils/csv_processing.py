import os
import pandas as pd

def process_csv(file_path):
    data = pd.read_csv(file_path)
    data['ID'] = range(1, len(data) + 1)

    # Enregistrer 'new_formulaire.csv' dans le dossier csv_files
    new_formulaire_path = os.path.join('csv_files', 'new_formulaire.csv')
    data.to_csv(new_formulaire_path, index=False)
    return data

def generate_coding_table(data):
    new_data = pd.DataFrame()
    new_data['ID'] = data['ID']
    
    # Ajouter dummies pour chaque colonne (code de transformation ici)

    new_data = new_data.astype(int)

    # Enregistrer 'CODING_TABLE.csv' dans le dossier csv_files
    coding_table_path = os.path.join('csv_files', 'CODING_TABLE.csv')
    new_data.to_csv(coding_table_path, index=False)
    return new_data
