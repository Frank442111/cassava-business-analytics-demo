"""Synthetic-only chronological comparison; no storage, private imports or side effects."""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def compare_models(daily):
    frame = daily.loc[:, ['date', 'quantity_kg']].copy()
    frame['date'] = pd.to_datetime(frame.date, errors='raise')
    frame = frame.sort_values('date').reset_index(drop=True)
    values = pd.to_numeric(frame.quantity_kg, errors='raise').to_numpy(dtype=float)
    if len(frame) < 30 or not np.isfinite(values).all() or (values < 0).any():
        raise ValueError('The fictional scenario needs at least 30 complete daily observations.')
    if frame.date.isna().any() or frame.date.duplicated().any() or not frame.date.equals(
            pd.Series(pd.date_range(frame.date.min(), periods=len(frame), freq='D'), name='date')):
        raise ValueError('Missing or repeated fictional calendar dates are unknown, not zero sales.')
    frame['quantity_kg'] = values
    train, test = frame.iloc[:-14].copy(), frame.iloc[-14:].copy()
    features = pd.DataFrame({'day': np.arange(len(train)),
                             'weekday_sin': np.sin(2 * np.pi * train.date.dt.day_of_week / 7),
                             'weekday_cos': np.cos(2 * np.pi * train.date.dt.day_of_week / 7),
                             'lag_1': train.quantity_kg.shift(1),
                             'lag_7': train.quantity_kg.shift(7),
                             'rolling_7': train.quantity_kg.shift(1).rolling(7).mean()})
    fit_x, fit_y = features.iloc[7:], train.quantity_kg.iloc[7:]
    ridge = make_pipeline(StandardScaler(), Ridge(alpha=10.0)).fit(fit_x, fit_y)
    linear = LinearRegression().fit(np.arange(len(train)).reshape(-1, 1), train.quantity_kg)
    test['Moving Average'] = float(train.quantity_kg.tail(7).mean())
    test['Linear Regression'] = np.maximum(0, linear.predict(np.arange(len(train), len(frame)).reshape(-1, 1)))
    history, ridge_predictions, recursive_features = train.quantity_kg.tolist(), [], []
    for i, day in enumerate(test.date, start=len(train)):
        x = pd.DataFrame([[i, np.sin(2 * np.pi * day.day_of_week / 7),
                           np.cos(2 * np.pi * day.day_of_week / 7), history[-1], history[-7],
                           np.mean(history[-7:])]], columns=features.columns)
        prediction = max(0.0, float(ridge.predict(x)[0]))
        history.append(prediction)
        ridge_predictions.append(prediction)
        recursive_features.append(x)
    test['Enhanced Ridge'] = ridge_predictions
    scores = pd.DataFrame([{'SIMULATED model': name,
                            'SIMULATED test MAE (kg/day)': float(mean_absolute_error(test.quantity_kg, test[name]))}
                           for name in ['Moving Average', 'Linear Regression', 'Enhanced Ridge']])
    return train, test, scores, {'training_features': fit_x.copy(),
                                'scaler_mean': ridge.named_steps['standardscaler'].mean_.copy(),
                                'test_features': pd.concat(recursive_features, ignore_index=True)}
