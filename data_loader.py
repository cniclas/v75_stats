import pandas as pd
from general_support import get_relevant_column

class DataLoader:
    def __init__(self):
        self.data = pd.DataFrame

    def load_data(self, filepath):
        self.data = pd.read_csv(filepath, parse_dates=["Datum"])

    def get_fieldnames(self):
        return self.data.columns.tolist()
        
    def get_data(self):
        return self.data
    
    def get_number_of_race_elements(self):
        col_data = get_relevant_column(self.data, "Startnummer")
        return col_data[0].size