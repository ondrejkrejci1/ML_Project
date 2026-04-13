import pandas as pd
import os
import json


class DataLoader:

    def __init__(self, config_path='config.json'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        self.file_path = self.config.get('data_path', 'data/data_complete.csv')
        self.required_columns = self.config.get('disciplines', []) + ['Points']
        self.data = None

    def load_and_clean_data(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Critical error: The file '{self.file_path}' was not found!")

        df = pd.read_csv(self.file_path)

        for col in self.required_columns:
            if col not in df.columns:
                raise ValueError(f"The data is missing a required column: {col}")

        self.data = df.dropna(subset=self.required_columns)
        return self.data

    def get_data(self):

        if self.data is None:
            self.load_and_clean_data()
        return self.data