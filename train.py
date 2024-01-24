import os
import warnings

import pandas as pd
import joblib
import xgboost as xgb

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier


FILE_PATH = 'dataset/titanic.csv'
RANDOM_STATE = 42
TEST_SIZE = 0.3


def load_and_preprocess_data():
    df = pd.read_csv(FILE_PATH)

    label_encoder = LabelEncoder()

    X = df.drop(['Survived', 'Name', 'Ticket', 'Cabin', 'PassengerId'], axis=1)
    y = df['Survived']

    num_imputer = SimpleImputer(strategy='mean')
    numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns
    X[numerical_cols] = num_imputer.fit_transform(X[numerical_cols])

    # Impute categorical columns with the most frequent value (mode)
    cat_imputer = SimpleImputer(strategy='most_frequent')
    categorical_cols = X.select_dtypes(include=['object', 'category']).columns
    X[categorical_cols] = cat_imputer.fit_transform(X[categorical_cols])

    categorical_cols = ['Sex', 'Embarked']  # Add other categorical columns as needed

    # Apply label encoder to each column
    for col in categorical_cols:
        X[col] = label_encoder.fit_transform(X[col].astype(str))

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    return X_train, y_train, X_test, y_test


def train_and_save_model(model, params, X_train, y_train, model_name):
    grid_search = GridSearchCV(model, params, cv=5, scoring='f1')
    grid_search.fit(X_train, y_train)

    os.makedirs('models', exist_ok=True)
    model_path = f'models/{model_name}'
    if isinstance(model, xgb.XGBClassifier):
        grid_search.best_estimator_.save_model(f'{model_path}.bin')
    else:
        joblib.dump(grid_search.best_estimator_, f'{model_path}.pkl')

    print(f"Model {model_name} trained and saved.")


def main():
    # Disable warnings
    warnings.filterwarnings('ignore')


    X_train, y_train, *_ = load_and_preprocess_data()

    # Logistic Regression
    log_reg_params = {
        'C': [0.001, 0.01, 0.1, 1],
        'solver': ['liblinear', 'saga']
    }
    train_and_save_model(
        LogisticRegression(max_iter=1000),
        log_reg_params,
        X_train,
        y_train,
        'logistic_regression_model'
    )

    # Random Forest
    rf_params = {
        'n_estimators': [5, 7, 10],
        'max_depth': [5, 7, 10, 15],
        'min_samples_split': [3, 4, 5, 7, 10]
    }
    train_and_save_model(
        RandomForestClassifier(),
        rf_params,
        X_train,
        y_train,
        'random_forest_model'
    )

    # XGBoost
    xgb_params = {
        'n_estimators': [1, 2, 3],
        'learning_rate': [0.3, 0.5, 0.7, 1.0],
        'max_depth': [1, 2, 3]
    }
    train_and_save_model(
        xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss'),
        xgb_params,
        X_train,
        y_train,
        'xgboost_model'
    )

    # Reset warnings to default
    warnings.resetwarnings()

if __name__ == '__main__':
    main()
