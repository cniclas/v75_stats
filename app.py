from flask import Flask, render_template, request
import pandas as pd
from data_filter import filter_dataframe
from calc_stats import calc_stats
from datetime import datetime

app = Flask(__name__)

# Global variable to hold your data
    
# Read the CSV file into a Pandas DataFrame
df =  pd.DataFrame() #pd.read_csv('data\data.csv', header=0, parse_dates=['Datum'])

# Get unique 'Bana' values
alla_banor = [] #df['Bana'].unique().tolist()

# Get date initial settings
min_date = [] # df['Datum'].min().strftime('%Y-%m-%d')
max_date = []

# Data loading
@app.route('/load-data', methods=['POST'])
def load_data():
    global df, alla_banor, min_date, max_date  # Declare these variables as global

    race_type = request.form.get('race-type')
    
    if race_type == 'v75':
        df = pd.read_csv('data\data_v75.csv', header=0, parse_dates=['Datum'])
    elif race_type == 'v86':
        df = pd.read_csv('data\data_v86.csv', header=0, parse_dates=['Datum'])
    else:
        df = pd.DataFrame()  # Reset to an empty DataFrame if race type is unexpected

    # Update global variables based on the newly loaded data
    if not df.empty:  # Check if the DataFrame is not empty before trying to access its 'Datum' column
        alla_banor = df['Bana'].unique().tolist()
        min_date = df['Datum'].min().strftime('%Y-%m-%d')
        max_date = datetime.today().strftime('%Y-%m-%d')
    
    return render_template('index.html', alla_banor=alla_banor, min_date=min_date, max_date=max_date, request=request)

@app.route('/update-stats', methods=['POST'])
def update_stats():
    global df, alla_banor, min_date, max_date  # Declare these variables as global
    statistics = {}
    total_entries = len(df)
    relevant_entries = total_entries

    if request.method == 'POST':
        # Get Bana input and split by comma, strip whitespace
        bana_input = request.form.get('bana', '')
        req_banor = [b.strip() for b in bana_input.split(',') if b.strip()]

        # Construct filter arguments, considering blank inputs
        filter_args = {}
        if req_banor:
            filter_args['Bana'] = req_banor
            
        # Handle date
        datum_start = request.form.get('datum_start', '')
        datum_end = request.form.get('datum_end', '')

        # Convert date strings to datetime objects
        if datum_start:
            datum_start = datetime.strptime(datum_start, '%Y-%m-%d')
        if datum_end:
            datum_end = datetime.strptime(datum_end, '%Y-%m-%d')
            
        filter_args['Datum'] = [datum_start, datum_end]
            
        # Handle scalar field inputs
        scalar_fields = ['7 Rätt', '6 Rätt', '5 Rätt', 'Omsättning', 'Antal System']  # Add more scalar fields as needed
        for field in scalar_fields:
            start = request.form.get(f'{field}_min', None)
            end = request.form.get(f'{field}_max', None)
            if start or end:  # If either start or end is provided
                start = float(start) if start else 0  # Default start to 0 if blank
                end = float(end) if end else float('inf')  # Default end to infinity if blank
                filter_args[field] = [start, end]
                
        # Handle jackpot boolean
        filter_args['Inkludera Jackpots'] = 'inkludera_jackpots' in request.form
        # The variable inkludera_jackpots will be True if the checkbox was checked, and False otherwise.

        # Filter the dataframe based on inputs
        if filter_args:
            filtered_df = filter_dataframe(df, **filter_args)
            relevant_entries = len(filtered_df)
            
        statistics = calc_stats(filtered_df)

    return render_template('index.html', statistics=statistics, alla_banor=alla_banor, min_date=min_date, max_date=max_date, relevant_entries=relevant_entries, total_entries=total_entries, request=request)


@app.route('/', methods=['GET', 'POST'])
def home():
    global df, alla_banor, min_date, max_date  # Declare these variables as global

    return render_template('index.html', alla_banor=alla_banor, min_date=min_date, max_date=max_date, request=request)

if __name__ == '__main__':
    app.run(debug=True)
