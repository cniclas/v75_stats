from flask import Flask
from data_loader import load_csv_data

app = Flask(__name__)

# Global variable to hold your data
data_entries = []

@app.route('/')
def home():
    # Use the global data_entries variable within your route
    return f"The data has {len(data_entries)} entries."

if __name__ == '__main__':
    # Load CSV data into the global variable before running the app
    data_entries = load_csv_data()
    app.run(debug=True)
