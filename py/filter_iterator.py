

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

def filter_iterator(data, all_filters):
    df = data
    all_filters_str = []
    for curr_filter in all_filters:
        if curr_filter.get_label() == 'Bana':
            df = curr_filter.filter_data(df)
        elif curr_filter.get_label() == 'Datum':
            df = curr_filter.filter_data(df)
        else:
            all_filters_str.append(curr_filter.get_label())
    
    
    all_filter_labels_uniq = set(all_filters_str)
    for curr_label in all_filter_labels_uniq:
        query_string = get_logic_gating_string(all_filters, curr_label)
        
        if query_string:
            df = df.query(query_string)
        
    return df
    
    
