from flask import Flask
from data_loader import load_csv_data
from data_filter import filter_dataframe

app = Flask(__name__)

# Global variable to hold your data
data_entries = []

@app.route('/')
def home():
    # Use the global data_entries variable within your route
    return f"The data has {len(data_entries)} entries."

if __name__ == '__main__':
    # Load CSV data into the global variable before running the app
    df = load_csv_data()
    
    # Example usage:
    # Filter for 'Bana' being either 'Kalmar' or 'Halmstad', 'Omsattning' between 0 and 99999,
    # and 'Datum' between '2023-01-01' and '2023-12-31'
    filtered_df = filter_dataframe(df, Bana=['Kalmar', 'Halmstad'], AntalSystem=[0, 999999999], Datum=('2020-01-01', '2023-12-31'))

    # Print or return the filtered DataFrame
    print(filtered_df)
    
    app.run(debug=True)
