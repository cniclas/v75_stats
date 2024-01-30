from statistics import mean, variance

from statistics import mean, variance

def calc_scalar_stats(data_vector):
    scalar_stats = {}
    if data_vector:  # Check if the list is not empty
        scalar_stats['min'] = min(data_vector)
        scalar_stats['max'] = max(data_vector)
        scalar_stats['avg'] = mean(data_vector)
        scalar_stats['sum'] = sum(data_vector)
    else:
        scalar_stats['min'] = None
        scalar_stats['max'] = None
        scalar_stats['avg'] = None
        scalar_stats['sum'] = None
    return scalar_stats

def calc_stats(df):
    # Init return variable
    stats = {}
    
    # List of scalar fields for which to calculate statistics
    scalar_fields = ['7 Rätt', '6 Rätt', '5 Rätt', 'Omsättning', 'Antal System']
    
    for field in scalar_fields:
        if field in df.columns:
            # Select non-null values for the field
            non_null_values = df[field].dropna()
            # Convert to list if it's not already a list (required for variance function)
            data_vector = non_null_values.tolist()
            # Calculate stats for the field
            stats[field] = calc_scalar_stats(data_vector)
    
    return stats

    
