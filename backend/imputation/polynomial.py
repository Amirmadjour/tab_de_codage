from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def find_optimal_degree(X, y, max_degree=3):
    """Trouve le degré polynomial optimal en utilisant la validation croisée"""
    best_score = float('-inf')
    best_degree = 1
    
    for degree in range(1, max_degree + 1):
        poly = PolynomialFeatures(degree=degree)
        X_poly = poly.fit_transform(X)
        
        model = LinearRegression()
        scores = cross_val_score(model, X_poly, y, cv=5, scoring='neg_mean_squared_error')
        mean_score = np.mean(scores)
        
        if mean_score > best_score:
            best_score = mean_score
            best_degree = degree
            
    return best_degree

def plot_polynomial_degrees(X, y, max_degree=3):
    """Visualise les scores pour différents degrés polynomiaux"""
    degrees = range(1, max_degree + 1)
    scores = []
    
    for degree in degrees:
        poly = PolynomialFeatures(degree=degree)
        X_poly = poly.fit_transform(X)
        
        model = LinearRegression()
        cv_scores = cross_val_score(model, X_poly, y, cv=10, scoring='neg_mean_squared_error')
        scores.append(-np.mean(cv_scores))  # On inverse le signe pour avoir l'erreur positive
    
    # Retirer le tracé et retourner les scores
    return degrees, scores  # Retourne les degrés et les scores

def polynomial_imputation(data, target_column):
    """
    Impute missing values using polynomial regression with standardized data
    """
    temp = data.dropna()
    
    # Initialize scalers
    target_scaler = StandardScaler()
    features_scaler = StandardScaler()
    
    # Scale target variable
    y = target_scaler.fit_transform(temp[target_column].values.reshape(-1, 1))
    
    # Scale features
    X = features_scaler.fit_transform(temp.drop(columns=[target_column]).values)
    
    # Find optimal degree
    degrees, scores = plot_polynomial_degrees(X, y)  # Appel modifié
    optimal_degree = degrees[np.argmin(scores)]
    
    # Create and fit polynomial model with scaled data
    poly_features = PolynomialFeatures(degree=optimal_degree)
    X_poly = poly_features.fit_transform(X)
    
    model = LinearRegression()
    model.fit(X_poly, y)
    
    # Impute missing values
    for idx in data.index:
        if pd.isna(data.loc[idx, target_column]):
            features = data.loc[idx].drop(target_column).values.reshape(1, -1)
            
            # Handle missing features by replacing with mean
            features = np.where(
                pd.isna(features), 
                np.nanmean(data.drop(columns=[target_column]).values, axis=0), 
                features
            )
            
            # Scale features
            features_scaled = features_scaler.transform(features)
            
            # Transform scaled features to polynomial features
            features_poly = poly_features.transform(features_scaled)
            
            # Predict and inverse transform to get original scale
            prediction = model.predict(features_poly)
            prediction_original_scale = target_scaler.inverse_transform(prediction.reshape(-1, 1))
            
            data.loc[idx, target_column] = prediction_original_scale[0]
    
    return data

def polynomial_regression_imputation(data):
    data_copy = data.copy()
    plot_info = {}
    for column in data.columns:
        if data[column].isna().any():
            # Impute les valeurs manquantes
            data_copy = polynomial_imputation(data_copy, column)
            
            # Recalculer X et y après l'imputation
            temp = data_copy.dropna()
            target_scaler = StandardScaler()
            features_scaler = StandardScaler()
            y = target_scaler.fit_transform(temp[column].values.reshape(-1, 1))
            X = features_scaler.fit_transform(temp.drop(columns=[column]).values)
            
            # Obtenir les degrés et les scores
            degrees, scores = plot_polynomial_degrees(X, y)
            optimal_degree = degrees[np.argmin(scores)]
            
            # Créer et ajuster le modèle polynomial final
            poly_features = PolynomialFeatures(degree=optimal_degree)
            X_poly = poly_features.fit_transform(X)
            model = LinearRegression()
            model.fit(X_poly, y)
            
            # Stocker les informations du modèle
            plot_info[column] = {
                'optimal_degree': optimal_degree,
                'x_values': list(degrees),
                'y_values': scores,
                'coefficients': model.coef_[0].tolist(),  # Convertir en liste pour la sérialisation JSON
                'intercept': float(model.intercept_),
                'feature_names': poly_features.get_feature_names_out()  # Noms des caractéristiques polynomiales
            }

    return data_copy, plot_info