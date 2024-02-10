from flask import Flask, render_template, request, jsonify
import pandas as pd

class DataLoader:
    def __init__(self):
        self.data = pd.DataFrame

    def load_data(self, filepath):
        self.data = pd.read_csv(filepath, parse_dates=["Datum"])

    def get_data(self):
        return self.data