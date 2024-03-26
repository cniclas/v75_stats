

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
        
def filter_iterator(data, basic_filters, adv_filters):
    
    df_basic = data
    for curr_filter in basic_filters:
        df_basic = curr_filter.filter_data(df_basic)
        
    df_adv = df_basic
    for curr_filter in adv_filters:
        df_adv = curr_filter.filter_data(df_adv)
    
    return df_basic, df_adv
    
    
    
