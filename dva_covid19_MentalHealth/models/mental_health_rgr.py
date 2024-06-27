import pandas as pd
import numpy as np
import pickle
import argparse

from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.utils import shuffle
from imblearn.under_sampling import RandomUnderSampler

from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor

# Parse Command Line Arguments
parser = argparse.ArgumentParser(description='COVID - Mental Health Classifier')
parser.add_argument('--train', type=str, required=False)
args = parser.parse_args()


def mental_health_rgr():

    df = pd.read_csv('https://storage.googleapis.com/additional-data/CummulatedClean_Nov22_with_lock/0_CMaster2_HPS_CDC_CPS_Vaccinated_with_lock.csv')

    print(df.columns)
    df = df[['INCOME', 'WRKLOSS', 'MORTCONF', 'MORTLMTH', 'KINDWORK', 'CDCCOUNT', 'ANXIOUS', 'WORRY', 'lockdown', 'DOWN']]

    # Drop Missing Values and NaNs
    for col in df.columns:
        df.drop(df[df[col] == -88].index, inplace=True)
        df.drop(df[df[col] == -99].index, inplace=True)
        df.dropna(inplace=True)

    # One Hot Encode - KINDWORK
    enc_df = pd.get_dummies(df['KINDWORK'],
                            prefix='KINDWORK')
    df.drop(columns=['KINDWORK'], inplace=True)

    df = pd.concat((df, enc_df), axis=1)

    # Binarize - WRKLOSS - No=0, Yes=1
    df['WRKLOSS'] = df['WRKLOSS'].replace(to_replace=2, value=0)

    # Add Mental Stress Index
    df['MSI'] = df['WORRY'] + df['DOWN'] + df['ANXIOUS']

    # Drop unnecessary components
    df.drop(columns=['ANXIOUS', 'WORRY', 'DOWN'])

    # Reorder df columns
    cols = ['INCOME',
            'WRKLOSS',
            'MORTCONF',
            'MORTLMTH',
            'lockdown',
            'MSI']

    df = df[cols]

    # Undersample to balance class distributions
    undersamp = RandomUnderSampler(sampling_strategy='majority')
    X, y = undersamp.fit_resample(df.iloc[:, :5], df.iloc[:, -1])
    X, y, = shuffle(X, y)

    # Train Test Split
    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        test_size=0.20,
                                                        random_state=42)

    # If command line flag is set, train RF.
    if args.train == 'rf':
        print(f'Training Random Forest model...')

        # Hyperparameter Ranges for tuning
        param_grid = {'max_depth': list(range(1, 20)),
                      'n_estimators': list(range(100, 500, 50)),
                      'min_samples_split': list(range(2, 70)),
                      'min_samples_leaf': list(range(5, 50))}

        rf = RandomForestRegressor(n_jobs=-1)

        # Randomized Grid Search for Hyperparameter Tuning
        search = RandomizedSearchCV(estimator=rf, param_distributions=param_grid, cv=5, n_iter=10)

        rgr = search.fit(X_train, y_train)

        # Save model to disk
        with open('mental_health_rgr.pickle', 'wb') as handle:
            pickle.dump(rgr, handle, protocol=pickle.HIGHEST_PROTOCOL)

        print(rgr.best_params_)
        print(f'Regression Accuracy (Test Set): {rgr.score(X_test, y_test)}')

    # If command line flag is set, train XGB.
    elif args.train == 'xgb':
        print(f'Training XGB model...')

        # Hyperparameter Ranges for tuning
        param_grid = {'max_depth': list(range(1, 20)),
                      'n_estimators': list(range(100, 500, 50)),
                      'learning_rate': np.arange(0.1, 0.9, 0.1),
                      'colsample_bytree': np.arange(0.4, 1.0, 0.1),
                      'colsample_bylevel': np.arange(0.4, 1.0, 0.1),
                      'subsample': np.arange(0.4, 1.0, 0.1),
                      'alpha': np.arange(0.01, 0.5, 0.1),
                      'gamma': np.arange(0.3, 0.9, 0.1),
                      'lambda': np.arange(0.3, 0.9, 0.1)}

        xgb = XGBRegressor(n_jobs=-1)  # n_jobs=-1: Use all cores for training

        # Randomized Grid Search for Hyperparameter Tuning
        search = RandomizedSearchCV(estimator=xgb, param_distributions=param_grid, cv=5, n_iter=10)

        rgr = search.fit(X_train, y_train)

        # Save model to disk
        with open('mental_health_rgr.pickle', 'wb') as handle:
            pickle.dump(rgr, handle, protocol=pickle.HIGHEST_PROTOCOL)

        print(rgr.best_params_)
        print(f'Regression Accuracy (Test Set): {rgr.score(X_test, y_test)}')

    else:
        with open('mental_health_rgr.pickle', 'rb') as handle:
            rgr = pickle.load(handle)

        print(rgr.best_params_)
        print(f'Regression Accuracy (Test Set): {rgr.score(X_test, y_test)}')


if __name__ == '__main__':
    mental_health_rgr()
