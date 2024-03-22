from flask import request
import numpy as np
from itertools import combinations
from string_to_number import convert_string_to_number

class ArrayIntervalFilter:
    def __init__(self, nr_elements):   
        self.nr_elements = nr_elements    
        self.interval_filter_options = {
            "min_interval": 0,
            "max_interval": self.nr_elements,
            "min_race": 0,
            "max_race": self.nr_elements,
            "selected_elements": list(range(1, nr_elements + 1))
        }

    def filter(self):
        return [x for x in self.array if self.interval[0] <= x <= self.interval[1]]