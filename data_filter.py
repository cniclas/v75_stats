import pandas as pd

def filter_dataframe(df, **kwargs):
    query_parts = []
    
    f_add_jackpots = False
    for field, value in kwargs.items():
        if field == 'Inkludera Jackpots':
            # Special handling of jackpots, need to find if this is true before parsing other parameters
            if value:
                f_add_jackpots = True
    
    for field, value in kwargs.items():
        if field == 'Datum':
            # Ensure dates are in datetime format
            start_date, end_date = pd.to_datetime(value[0]), pd.to_datetime(value[1])
            query_parts.append(df[field].between(start_date, end_date))
        elif field == 'Bana':
            # Filter on all strings in value
            query_parts.append(df[field].isin(value))
        elif isinstance(value, list) and field != 'Datum':
            min_val, max_val = min(value), max(value)
            if field == '7 Rätt' and f_add_jackpots:
                condition = ((df[field].between(min_val, max_val, inclusive='both')) | (df[field] == 0))
            else:
                condition = (df[field].between(min_val, max_val, inclusive='both'))
            query_parts.append(condition)
    
    # Combine all query parts with logical AND
    if query_parts:
        total_query = query_parts[0]
        for query in query_parts[1:]:
            total_query = total_query & query
        filtered_df = df[total_query]
    else:
        filtered_df = df  # Return the original DataFrame if no filters are applied

    return filtered_df


