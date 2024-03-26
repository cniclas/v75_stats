import numpy as np

def limit_value_one(value, nr_elements):
    if value < 1:
        value = 1
    elif value > nr_elements:
        value = nr_elements
    return value
    
def limit_value_zero(value, nr_elements):
    if value < 0:
        value = 0
    elif value > nr_elements:
        value = nr_elements
    return value

def get_relevant_column(data, label):
        relevant_column = data[label]
        transformed_column = relevant_column.apply(lambda x: np.array([int(i) for i in x.split()]))
        return transformed_column
    
def get_relevant_elements(vector, idx_vector):
    return vector[idx_vector]
    