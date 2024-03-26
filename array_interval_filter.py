from flask import request
import numpy as np
from itertools import combinations
from string_to_number import convert_string_to_number
from general_support import limit_value_zero, get_relevant_column, get_relevant_elements

class ArrayIntervalFilter:
    
    temp_count = 1000
    
    def __init__(self, label_in, nr_elements):
        ArrayIntervalFilter.temp_count += 1
        self.unique_id = ArrayIntervalFilter.temp_count
        self.label = label_in  
        self.nr_elements = nr_elements    
        self.interval_filter_options = {
            "min_interval": 0,
            "max_interval": self.nr_elements,
            "min_race": 0,
            "max_race": self.nr_elements,
            "selected_elements": list(range(1, nr_elements + 1))
        }
    
    def get_unique_id(self):
        return self.unique_id
        
    def generate_html(self):
        interval_html = f"""
        <div class="filter-row">
            <label for="{self.label}{self.unique_id}_interval_min">Interval Filter:</label>
            <input type="number" id="{self.label}{self.unique_id}_interval_min" name="{self.label}{self.unique_id}_min_interval" step="any" placeholder="0" value="{self.interval_filter_options['min_interval']}" style="width: 50px; height: 25px; padding: 5px;">
            -
            <input type="number" id="{self.label}{self.unique_id}_interval_max" name="{self.label}{self.unique_id}_max_interval" step="any" placeholder="Max" value="{self.interval_filter_options['max_interval']}" style="width: 50px; height: 25px; padding: 5px;">
            <span>
                <label for="{self.label}{self.unique_id}_interval_min_race">Min Race:</label>
                <input type="number" id="{self.label}{self.unique_id}_interval_min_race" name="{self.label}{self.unique_id}_min_race" value="{self.interval_filter_options['min_race']}" style="width: 50px; height: 25px; padding: 5px;">
                -
                <label for="{self.label}{self.unique_id}_interval_max_race">Max Race:</label>
                <input type="number" id="{self.label}{self.unique_id}_interval_max_race" name="{self.label}{self.unique_id}_max_race" value="{self.interval_filter_options['max_race']}" style="width: 50px; height: 25px; padding: 5px;">
            </span>
        """
        for i in range(1, self.nr_elements + 1):
            checked = "checked" if i in self.interval_filter_options["selected_elements"] else ""
            interval_html += f"""
            <span>
                <label for="{self.label}{self.unique_id}_interval_element_{i}">{i}</label>
                <input type="checkbox" id="{self.label}{self.unique_id}_interval_element_{i}" name="{self.label}{self.unique_id}_interval_elements_{i}" value="{i}" {checked}>
            </span>
        """
        interval_html += f"""<button type="button" onclick="deleteFilterObject({self.unique_id})">Delete</button>"""
        interval_html += "</div>"
        return interval_html
    
    def update(self):
        self.interval_filter_options["min_interval"] = convert_string_to_number(request.form.get(f"{self.label}{self.unique_id}_min_interval", ""), 0)
        self.interval_filter_options["max_interval"] = convert_string_to_number(request.form.get(f"{self.label}{self.unique_id}_max_interval", ""), 2**64)
        
        self.interval_filter_options["min_race"] = convert_string_to_number(request.form.get(f"{self.label}{self.unique_id}_min_race", ""), 0)
        self.interval_filter_options["min_race"] = limit_value_zero(self.interval_filter_options["min_race"], self.nr_elements)
        self.interval_filter_options["max_race"] = convert_string_to_number(request.form.get(f"{self.label}{self.unique_id}_max_race", ""), 2**64)
        self.interval_filter_options["max_race"] = limit_value_zero(self.interval_filter_options["max_race"], self.nr_elements)
        
        selected_elements = []
        for i in range(1, self.nr_elements + 1):
            checkbox_name = f"{self.label}{self.unique_id}_interval_elements_{i}"
            if request.form.get(checkbox_name):  # Check if the checkbox is checked
                selected_elements.append(int(i))  # Cast to int for consistency
        self.interval_filter_options["selected_elements"] = selected_elements

    def filter_data(self, data):
        relevant_rows = self.interval_filter_iloc(data)
        return data.iloc[relevant_rows]
    
    def interval_filter_iloc(self, data):
        relevant_data = get_relevant_column(data, self.label)
        relevant_idxs = [i - 1 for i in self.interval_filter_options['selected_elements']]

        min_limit = self.interval_filter_options['min_interval']
        max_limit = self.interval_filter_options['max_interval']
        min_hit = self.interval_filter_options['min_race']
        max_hit = self.interval_filter_options['max_race']
        relevant_rows = []
        for row_idx, row in enumerate(relevant_data):
            hit_count = 0
            rel_data = get_relevant_elements(row, relevant_idxs)

            for col in rel_data:
                if col >= min_limit and col <= max_limit:
                    hit_count += 1
                
            if hit_count >= min_hit and hit_count <= max_hit:
                relevant_rows.append(row_idx)
        
        return relevant_rows