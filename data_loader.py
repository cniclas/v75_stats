import pandas as pd

class DataLoader:
    def __init__(self):
        self.data = pd.DataFrame

    def load_data(self, filepath):
        self.data = pd.read_csv(filepath, parse_dates=["Datum"])

    def get_fieldnames(self):
        return self.data.columns.tolist()
        
    def get_data(self):
        return self.data