
import pandas as pd

def load_csv_data():
    
    # Path to csv file
    csv_file_path = 'data\data.csv'
    
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(csv_file_path, header=0, parse_dates=['Datum'])
    
    # Splitting the 'Startnummer', 'Ranknummer', 'Instatsprocent', 'Vinnarodds' columns into lists
    # Assuming these columns are stored as strings of space-separated values in the CSV
    int_columns = ['Startnummer', 'Ranknummer']
    float_columns = ['Instatsprocent', 'Vinnarodds']
    
    for col in int_columns:
        df[col] = df[col].apply(lambda x: [int(i) for i in x.split()])

    for col in float_columns:
        df[col] = df[col].apply(lambda x: [float(i) for i in x.split()])

    # Convert '7ratt', '6ratt', '5ratt', 'Omsattning' to float and 'AntalSystem' to int
    df['7ratt'] = df['7ratt'].astype(float)
    df['6ratt'] = df['6ratt'].astype(float)
    df['5ratt'] = df['5ratt'].astype(float)
    df['Omsattning'] = df['Omsattning'].astype(float)
    df['AntalSystem'] = df['AntalSystem'].astype(int)
    
    return df
