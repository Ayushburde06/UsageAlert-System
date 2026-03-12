import pandas as pd
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    def __init__(self, contamination="auto"):
        self.contamination = contamination

    def fit_predict(self, df: pd.DataFrame, feature_columns: list) -> pd.DataFrame:
        """
        Fits the IsolationForest and predicts anomalies.
        Returns the dataframe with an 'anomaly_score' and 'is_anomaly' column.
        is_anomaly = 1 if anomaly, 0 if normal
        """
        n_samples = len(df)
        # For extremely small datasets (like 7 rows), "auto" or 5% is too small to detect anomalies.
        # We enforce a dynamic contamination rate to catch the top outliers.
        if self.contamination == "auto" and n_samples < 50:
            # For less than 50 rows, flag the top 30% as anomalies to force detection 
            # on small datasets (like a 7-day week).
            effective_contam = 0.3
        else:
            effective_contam = self.contamination

        model = IsolationForest(contamination=effective_contam, random_state=42)
        
        # Fit and predict
        preds = model.fit_predict(df[feature_columns])
        scores = model.decision_function(df[feature_columns])

        # Isolation forest returns -1 for anomaly, 1 for normal.
        df_out = df.copy()
        df_out['is_anomaly'] = (preds == -1).astype(int)
        df_out['anomaly_score'] = scores
        return df_out
