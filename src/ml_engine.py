import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor


class ModelManager:

    def __init__(self, config_path='config.json'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        self.models_dir = self.config.get('models_dir', 'saved_models')
        if not os.path.exists(self.models_dir):
            os.makedirs(self.models_dir)

    def generate_model_filename(self, disciplines):
        sorted_dis = sorted(disciplines)
        name = "_".join(sorted_dis)
        return os.path.join(self.models_dir, f"ensemble_{name}.joblib")

    def get_or_train_ensemble(self, data, disciplines):
        model_path = self.generate_model_filename(disciplines)

        if os.path.exists(model_path):
            return joblib.load(model_path)

        input_features = data[disciplines]
        target = data['Points']

        ensemble_models = []

        for i in range(10):
            X_train, _, y_train, _ = train_test_split(input_features, target, test_size=0.2, random_state=i * 100)

            model = GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=3,
                random_state=i * 100
            )

            model.fit(X_train, y_train)
            ensemble_models.append(model)

        joblib.dump(ensemble_models, model_path)

        return ensemble_models

    def predict_score(self, data, user_inputs):
        disciplines = list(user_inputs.keys())

        models = self.get_or_train_ensemble(data, disciplines)

        input_df = pd.DataFrame([user_inputs])

        individual_predictions = []
        for model in models:
            pred = model.predict(input_df)[0]
            individual_predictions.append(pred)

        final_prediction = np.mean(individual_predictions)

        return int(round(final_prediction))