from flask import Flask, render_template, request
import pandas as pd
from data_filter import filter_dataframe

app = Flask(__name__)

# Global variable to hold your data
    
# Read the CSV file into a Pandas DataFrame
df = pd.read_csv('data\data.csv', header=0, parse_dates=['Datum'])

@app.route('/', methods=['GET', 'POST'])
def home():
    total_entries = len(df)
    relevant_entries = total_entries

    if request.method == 'POST':
        # Get Bana input and split by comma, strip whitespace
        bana_input = request.form.get('bana', '')
        bana_list = [b.strip() for b in bana_input.split(',') if b.strip()]

        # Construct filter arguments, considering blank inputs
        filter_args = {}
        if bana_list:
            filter_args['Bana'] = bana_list
        
        # Handle scalar field inputs
        scalar_fields = ['Omsattning', '7ratt']  # Add more scalar fields as needed
        for field in scalar_fields:
            start = request.form.get(f'{field}_start', None)
            end = request.form.get(f'{field}_end', None)
            if start or end:  # If either start or end is provided
                start = float(start) if start else 0  # Default start to 0 if blank
                end = float(end) if end else float('inf')  # Default end to infinity if blank
                filter_args[field] = [start, end]

        # Filter the dataframe based on inputs
        if filter_args:
            filtered_df = filter_dataframe(df, **filter_args)
            relevant_entries = len(filtered_df)

    return render_template('index.html', relevant_entries=relevant_entries, total_entries=total_entries)

if __name__ == '__main__':
    app.run(debug=True)
