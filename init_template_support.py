from interval_input import IntervalInput
from interval_input_jackpot import IntervalInputJackpot
from vector_input import VectorInput
from date_interval import DateIntervalInput
from location_input import LocationInput

def is_interval_field(fieldname):
    interval_fields = ['Omsättning', 'Antal System']
    return fieldname in interval_fields

def is_interval_jackpot(fieldname):
    interval_fields = ['8 Rätt', '7 Rätt', '6 Rätt', '5 Rätt']
    return fieldname in interval_fields

def is_vector_field(fieldname):
    vector_fields = ['Startnummer', 'Ranknummer', 'Instatsprocent', 'Vinnarodds']
    return fieldname in vector_fields

def is_bana_field(fieldname):
    return fieldname == 'Bana'

def determine_filter_type(fieldname):
    if is_interval_field(fieldname):
        type = 'interval'
    elif is_interval_jackpot(fieldname):
        type = 'jackpot'
    elif is_vector_field(fieldname):
        type = 'vector'
    elif is_bana_field(fieldname):
        type = 'bana'
    else:
        type = 'date'
    return type

def gather_type_of_filters(data, label):
    # Gathers type of filters in to groups of the same type.
    # This enables us to specify several desired intervals. (minx1,max1) || (minx2,max2) || ... || (minxn,maxn)
    # Ex 1: 
    # (Omsättning > 10 && Omsättning < 20) || (Omsättning > 100 && Omsättning < 200)
    # 
    # 
    pass
    

def init_filters(data):
    all_filters = []
    all_fields = data.columns.tolist()
    if '8 Rätt' in all_fields:
        nr_max = 8
    else:
        nr_max = 7
        
    for name in all_fields:
        filter_type = determine_filter_type(name)
        
        if filter_type == 'bana':
            available_locs = data['Bana'].unique()
            current_filter = LocationInput(name, available_locs)
            all_filters.append(current_filter)
        elif filter_type == 'date':
            oldest_date = data['Datum'].min()
            newest_date = data['Datum'].max()
            current_filter = DateIntervalInput(name, oldest_date, newest_date)
            all_filters.append(current_filter)
        elif filter_type == 'interval':
            current_filter = IntervalInput(name)
            all_filters.append(current_filter)
        elif filter_type == 'jackpot':
            current_filter = IntervalInputJackpot(name)
            all_filters.append(current_filter)
        elif filter_type == 'vector':
            current_filter = VectorInput(name, nr_max)
            all_filters.append(current_filter)
        
    return all_filters