

def get_logic_gating_string(all_filters, label):
    # Initialize an empty list to store the query string
    query_string = []

    # Iterate over the relevant filters
    for curr_filt in all_filters:
        # Call the get_filter_str method on the current filter with the data as argument
        # Append the result to the query string
        if curr_filt.get_label() == label:
            query_string.append(curr_filt.get_filter_str())
        
    # Use the pandas query method to filter the data according to the query string
    # The query string is joined with the OR operator
    if query_string.__len__() > 1:
        return ' | '.join(query_string)
    elif query_string.__len__() == 1:
        return query_string[0]
    else:
        return ''
    
def is_min_max_type(label):
    if '8 Rätt' == label:
        return True
    elif '7 Rätt' == label:
        return True
    elif '6 Rätt' == label:
        return True
    elif '5 Rätt' == label:
        return True
    elif 'Omsättning' == label:
        return True
    elif 'Antal System' == label:
        return True
    else:
        return False
        

def filter_iterator(data, all_filters):
    df = data
    min_max_filter = []
    iloc_filters = []
    for curr_filter in all_filters:
        if curr_filter.get_label() == 'Bana':
            df = curr_filter.filter_data(df)
        elif curr_filter.get_label() == 'Datum':
            df = curr_filter.filter_data(df)
        else:
            if is_min_max_type(curr_filter.get_label()):
                min_max_filter.append(curr_filter.get_label())
            else:
                iloc_filters.append(curr_filter)
    
    # First handle the min max kind of filters
    all_filter_labels_uniq = set(min_max_filter)
    for curr_label in all_filter_labels_uniq:
        query_string = get_logic_gating_string(all_filters, curr_label)
        
        if query_string:
            df = df.query(query_string)
    
    # Now handle the vector data type filters of the same type
    total_iloc_idx = set()
    for curr_filter in iloc_filters:
        sum_iloc = curr_filter.sum_filter_iloc(df)
        interval_iloc = curr_filter.interval_filter_iloc(df)
        
        curr_iloc_idx = set(sum_iloc) & set(interval_iloc)
        
        # Or gate to the total 
        total_iloc_idx.union(curr_iloc_idx)
        
        # Apply the filter
        df = df.iloc[list(total_iloc_idx)]
        
    return df
    
    
