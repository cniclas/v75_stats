import csv

def load_csv_data():
    # Path to csv file
    csv_file_path = 'data\data.csv'
    
    # Temporary variable to hold data while loading
    temp_data_entries = []

    with open(csv_file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        
        # Skip the first row if it's a header or a comment
        next(csvreader)
        
        for row in csvreader:
            temp_data_entries.append(row)

    return temp_data_entries
