import pandas as pd

def filter_dataframe(df, **kwargs):
    query_parts = []

    for field, value in kwargs.items():
        if field == 'Datum' and isinstance(value, tuple):
            # Ensure dates are in datetime format
            start_date, end_date = pd.to_datetime(value[0]), pd.to_datetime(value[1])
            query_parts.append(df[field].between(start_date, end_date))
        elif isinstance(value, list) and field != 'Datum':
            if all(isinstance(x, str) for x in value):  # Handling categorical fields
                query_parts.append(df[field].isin(value))
            else:  # Handling numerical ranges
                query_parts.append(df[field].between(min(value), max(value), inclusive='both'))
    
    # Combine all query parts with logical AND
    if query_parts:
        total_query = query_parts[0]
        for query in query_parts[1:]:
            total_query = total_query & query
        filtered_df = df[total_query]
    else:
        filtered_df = df  # Return the original DataFrame if no filters are applied

    return filtered_df


