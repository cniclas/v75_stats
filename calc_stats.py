from statistics import mean

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
   
