import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras import layers, models
import time
from sklearn.metrics import f1_score

def mlp_impute(data):
    start_time = time.time()
    # Séparer la colonne cible (dernière colonne) des features
    target_column = data.columns[-1]
    features = data.drop(columns=[target_column])
    target = data[target_column]

    # Séparer les données complètes et incomplètes
    df_complete = data.dropna()
    df_incomplete = data[data.isnull().any(axis=1)]

    # Préparation des données complètes
    scaler = MinMaxScaler()
    features_complete = df_complete.drop(columns=[target_column])
    target_complete = df_complete[target_column]
    features_complete_scaled = scaler.fit_transform(features_complete)

    # Définir le modèle MLP avec des dimensions appropriées
    model = models.Sequential([
        layers.Dense(128, activation='relu', input_shape=(features_complete_scaled.shape[1],)),
        layers.Dense(64, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(features_complete.shape[1])
    ])

    # Compiler et entraîner le modèle
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    history = model.fit(
        features_complete_scaled, 
        features_complete_scaled,
        epochs=50,
        batch_size=32,
        validation_split=0.2,
        verbose=1
    )

    # Créer un masque pour identifier les valeurs manquantes
    missing_mask = data.isna()
    
    # Traitement des données incomplètes
    features_incomplete = df_incomplete.drop(columns=[target_column])
    
    # Remplacer temporairement les NaN par 0 pour la mise à l'échelle
    features_incomplete_scaled = scaler.transform(features_incomplete.fillna(0))
    
    # Prédire les valeurs manquantes
    predictions = model.predict(features_incomplete_scaled)
    
    # Convertir les prédictions en DataFrame et inverse transformer
    predictions = scaler.inverse_transform(predictions)
    predictions_df = pd.DataFrame(predictions, columns=features_incomplete.columns, index=features_incomplete.index)
    
    # Utiliser le masque pour ne remplacer que les valeurs manquantes
    features_incomplete_imputed = features_incomplete.copy()
    for column in features_incomplete.columns:
        column_mask = missing_mask[column]
        features_incomplete_imputed.loc[column_mask, column] = predictions_df.loc[column_mask, column]

    # Réassembler le dataset complet
    result = pd.concat([
        df_complete,
        pd.concat([features_incomplete_imputed, df_incomplete[target_column]], axis=1)
    ]).sort_index()

    end_time = time.time()
    duree = end_time - start_time

    # Calculer les métriques comme dans sca_radi
    metrics = {}
    for column in data.columns:
        if missing_mask[column].any():
            threshold = data[column].median()
            original_values = data[~data[column].isna()][column]
            predicted_values = result[~data[column].isna()][column]
            
            y_true = (original_values > threshold).astype(int)
            y_pred = (predicted_values > threshold).astype(int)
            
            metrics[column] = {
                'column_name': column,
                'f_score': f1_score(y_true, y_pred),
            }

    # Convertir l'historique en métriques compatibles
    mse_history = history.history['loss']
    accuracies = [1 - mse for mse in mse_history]

    # Calculer l'accuracy comme pourcentage de prédictions correctes
    correct_predictions = 0
    total_predictions = 0
    
    for column in data.columns:
        if missing_mask[column].any():
            original_values = data[~data[column].isna()][column]
            predicted_values = result[~data[column].isna()][column]
            
            # Considérer une prédiction comme correcte si elle est dans une marge de 5% de la valeur réelle
            margin = 0.05 * (original_values.max() - original_values.min())
            correct_predictions += np.sum(np.abs(original_values - predicted_values) <= margin)
            total_predictions += len(original_values)

    prediction_accuracy = (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0

  

    return {
        'dataset_imputed': result,
        'missing_mask': missing_mask.values.tolist(),
        'metrics': metrics,
        'nb_imputed_values': missing_mask.sum().sum(),
        'overall_metrics': {
            'prediction_accuracy': prediction_accuracy,
            'total_improvement': ((mse_history[0] - mse_history[-1]) / mse_history[0]) * 100
        },
        'fitness_mse': mse_history,
        'accuracy': accuracies,
        'duree': duree,
    }