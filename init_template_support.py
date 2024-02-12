from interval_input import IntervalInput
from interval_input_jackpot import IntervalInputJackpot
from vector_input import VectorInput

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

def init_filters(fieldnames):
    all_filters = []
    if '8 Rätt' in fieldnames:
        nr_max = 8
    else:
        nr_max = 7
        
    for name in fieldnames:
        filter_type = determine_filter_type(name)
        
        if filter_type == 'interval':
            current_filter = IntervalInput(name)
            all_filters.append(current_filter)
        elif filter_type == 'jackpot':
            current_filter = IntervalInputJackpot(name)
        
            all_filters.append(current_filter)
        
    return all_filters