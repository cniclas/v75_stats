

def executeBasicFilter(data, basic_filter_instances):
    
    df = data
    for curr_filter in basic_filter_instances:
        if curr_filter in basic_filter_instances:
            df = curr_filter.filter(data)
    
    return df
            
    
def executeAdvancedFilter(data, advanced_filter_instances):
    
    df = data
    for curr_filter in advanced_filter_instances:
        if curr_filter in advanced_filter_instances:
            df = curr_filter.filter(data)
    
    return df

def executeFiltration(data, available_filters):
    
    

    # Derive and process basic filters
    basic_filter_types = ['bana', 'date', 'interval']
    basic_filter_instances = []
    df_basic = executeBasicFilter(data, basic_filter_instances)
    
    # Derive and process advanced filters based on basic filtered data
    advanced_filter_instances = []
    df_adv = executeAdvancedFilter(df_basic, advanced_filter_instances)
    
    return data, df_basic, df_adv