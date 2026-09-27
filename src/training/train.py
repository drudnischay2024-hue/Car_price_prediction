import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import json
import os

def load_data(filepath):
    df = pd.read_csv(filepath)
    # Drop features that cause data leakage (Min.Price, Max.Price)
    # Drop high cardinality string columns for this small dataset: Manufacturer, Model, Make
    drop_cols = ['Min.Price', 'Max.Price', 'Manufacturer', 'Model', 'Make']
    df = df.drop(columns=drop_cols)
    
    # Target variable
    X = df.drop(columns=['Price'])
    y = df['Price']
    return X, y

def build_pipeline():
    # Define feature types
    numeric_features = ['MPG.city', 'MPG.highway', 'EngineSize', 'Horsepower', 
                        'RPM', 'Rev.per.mile', 'Fuel.tank.capacity', 'Passengers', 
                        'Length', 'Wheelbase', 'Width', 'Turn.circle', 
                        'Rear.seat.room', 'Luggage.room', 'Weight']
    
    categorical_features = ['Type', 'AirBags', 'DriveTrain', 'Cylinders', 
                            'Man.trans.avail', 'Origin']

    # Numeric pipeline: Impute missing values with median, then scale
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    # Categorical pipeline: Impute missing with most frequent, then one-hot encode
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    # Combine into a ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    return preprocessor

def evaluate_model(model, X_test, y_test, name):
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    mse = mean_squared_error(y_test, preds)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, preds)
    print(f"--- {name} ---")
    print(f"MAE: {mae:.2f}, RMSE: {rmse:.2f}, R2: {r2:.2f}")
    return {"MAE": mae, "RMSE": rmse, "R2": r2}

def main():
    print("Loading data...")
    X, y = load_data('data/car_data.csv')
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    preprocessor = build_pipeline()
    
    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(random_state=42),
        "Random Forest": RandomForestRegressor(random_state=42, n_estimators=100),
        "Gradient Boosting": GradientBoostingRegressor(random_state=42)
    }
    
    best_model = None
    best_r2 = -float('inf')
    best_name = ""
    metrics_report = {}
    
    print("Training models...")
    for name, regressor in models.items():
        # Create full pipeline
        pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                   ('model', regressor)])
        
        # Train
        pipeline.fit(X_train, y_train)
        
        # Evaluate
        metrics = evaluate_model(pipeline, X_test, y_test, name)
        metrics_report[name] = metrics
        
        if metrics['R2'] > best_r2:
            best_r2 = metrics['R2']
            best_model = pipeline
            best_name = name

    print(f"\nBest Model: {best_name} with R2: {best_r2:.2f}")
    
    # Save the best model
    os.makedirs('models', exist_ok=True)
    model_path = 'models/best_model.pkl'
    joblib.dump(best_model, model_path)
    print(f"Saved best model to {model_path}")
    
    # Save metrics
    os.makedirs('reports', exist_ok=True)
    with open('reports/metrics.json', 'w') as f:
        json.dump({"best_model": best_name, "metrics": metrics_report}, f, indent=4)
        
    print("Done!")

if __name__ == "__main__":
    main()
