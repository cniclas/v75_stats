from flask import request
import numpy as np
from itertools import combinations
from string_to_number import convert_string_to_number

class VectorInput:
    """
    Generates HTML code for filter options and tracks user selections.
    """

    instance_count = 0
    
    def __init__(self, label_in, nr_elements):
        VectorInput.instance_count += 1
        self.unique_id = VectorInput.instance_count
        self.label = label_in
        self.nr_elements = nr_elements
        self.sum_filter_options = {
            "min_sum": 0,
            "max_sum": 2**64,
            "in_nr_races": self.nr_elements,
            "selected_elements": list(range(1, nr_elements + 1))  # Initially all elements selected
        }
        self.interval_filter_options = {
            "min_interval": 0,
            "max_interval": self.nr_elements,
            "min_race": 0,
            "max_race": self.nr_elements,
            "selected_elements": list(range(1, nr_elements + 1))
        }
        
    def generate_html(self):
        
        max_sum_str = self.sum_filter_options['max_sum']
        if max_sum_str >= 2**64:
            max_sum_str = "Max"
        
        html = f"""
            <div class="filter-container">
            <h3>{self.label}, Global Id: {self.unique_id}</h3>
            """

        # Create HTML structure for "sum" filter options with multiple inputs on the same row
        sum_html = f"""
        <div class="filter-row">
            <label for="{self.label}{self.unique_id}_sum_min">Summa Intervall:</label>
            <input type="number" id="{self.label}{self.unique_id}_sum_min" name="{self.label}{self.unique_id}_min_sum" step="any" placeholder="0" value="{self.sum_filter_options['min_sum']}" style="width: 50px; height: 25px; padding: 5px;">
            -
            <input type="number" id="{self.label}{self.unique_id}_sum_max" name="{self.label}{self.unique_id}_max_sum" step="any" placeholder="Max" value="{max_sum_str}" style="width: 50px; height: 25px; padding: 5px;">
            i 
            <input type="number" id="{self.label}{self.unique_id}_in_nr_races" name="{self.label}{self.unique_id}_in_nr_races" value="{self.sum_filter_options['in_nr_races']}" style="width: 50px; height: 25px; padding: 5px;">
             av loppen.
        """
        for i in range(1, self.nr_elements + 1):
            checked = "checked" if i in self.sum_filter_options["selected_elements"] else ""
            sum_html += f"""
            <span>
                <label for="{self.label}{self.unique_id}_sum_element_{i}">{i}</label>
                <input type="checkbox" id="{self.label}{self.unique_id}_sum_element_{i}" name="{self.label}{self.unique_id}_sum_elements_{i}" value="{i}" {checked}>
            </span>
        """
        sum_html += "</div>"

        # Create HTML structure for "interval" filter options
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
        interval_html += "</div>"

        # Combine sections and return complete HTML
        html += sum_html + interval_html + "</div>"
        return html

    def update(self):
        """
        Gets filter options selected by the user from form data.

        Args:
            request: The Flask request object.

        Returns:
            dict: A dictionary containing selected filter options.
        """

        self.sum_filter_options["min_sum"] = convert_string_to_number(request.form.get(f"{self.label}{self.unique_id}_min_sum", ""), 0)
        self.sum_filter_options["max_sum"] = convert_string_to_number(request.form.get(f"{self.label}{self.unique_id}_max_sum", ""), 2**64)

        self.sum_filter_options["in_nr_races"] = convert_string_to_number(request.form.get(f"{self.label}{self.unique_id}_in_nr_races", ""), self.nr_elements)
        self.sum_filter_options["in_nr_races"] = self.limit_value_one(self.sum_filter_options["in_nr_races"])
        
        selected_elements = []
        for i in range(1, self.nr_elements + 1):
            checkbox_name = f"{self.label}{self.unique_id}_sum_elements_{i}"
            if request.form.get(checkbox_name):  # Check if the checkbox is checked
                selected_elements.append(int(i))  # Cast to int for consistency
        self.sum_filter_options["selected_elements"] = selected_elements
            
        self.interval_filter_options["min_interval"] = convert_string_to_number(request.form.get(f"{self.label}{self.unique_id}_min_interval", ""), 0)
        self.interval_filter_options["max_interval"] = convert_string_to_number(request.form.get(f"{self.label}{self.unique_id}_max_interval", ""), 2**64)
        
        self.interval_filter_options["min_race"] = convert_string_to_number(request.form.get(f"{self.label}{self.unique_id}_min_race", ""), 0)
        self.interval_filter_options["min_race"] = self.limit_value_zero(self.interval_filter_options["min_race"])
        self.interval_filter_options["max_race"] = convert_string_to_number(request.form.get(f"{self.label}{self.unique_id}_max_race", ""), 2**64)
        self.interval_filter_options["max_race"] = self.limit_value_zero(self.interval_filter_options["max_race"])
        
        selected_elements = []
        for i in range(1, self.nr_elements + 1):
            checkbox_name = f"{self.label}{self.unique_id}_interval_elements_{i}"
            if request.form.get(checkbox_name):  # Check if the checkbox is checked
                selected_elements.append(int(i))  # Cast to int for consistency
        self.interval_filter_options["selected_elements"] = selected_elements
    
    def limit_value_one(self, value):
        if value < 1:
            value = 1
        elif value > self.nr_elements:
            value = self.nr_elements
        return value
    
    def limit_value_zero(self, value):
        if value < 0:
            value = 0
        elif value > self.nr_elements:
            value = self.nr_elements
        return value
    
    def get_relevant_column(self, data):
        relevant_column = data[self.label]
        transformed_column = relevant_column.apply(lambda x: np.array([int(i) for i in x.split()]))
        return transformed_column
    
    def get_relevant_elements(self, vector, idx_vector):
        return vector[idx_vector]
    
    def interval_filter(self, data):
        relevant_rows = self.interval_filter_iloc(data)
        return data.iloc[relevant_rows]
    
    def calculate_sums(self, vector, nr_elements):
        if len(vector) < nr_elements:
            raise ValueError("Du har specifierat fler kombinationer än lopp.")

        sums = []
        for subset in combinations(vector, nr_elements):
            sums.append(sum(subset))
        return sums
    
    def sum_filter(self, data):
        relevant_rows = self.sum_filter_iloc(data)
        return data.iloc[relevant_rows]  
        
    def filter_data(self, data):
        df = self.interval_filter(data)
        df = self.sum_filter(df)
        return df

    def get_label(self):
        return self.label
    
    def get_filter_str(self):
        pass
    
    def sum_filter_iloc(self, data):
        relevant_data = self.get_relevant_column(data)
        relevant_idxs = [i - 1 for i in self.sum_filter_options['selected_elements']]

        min_limit = self.sum_filter_options['min_sum']
        max_limit = self.sum_filter_options['max_sum']
        nr_races = self.sum_filter_options['in_nr_races']

        relevant_rows = []
        for row_idx, row in enumerate(relevant_data):
            rel_data = self.get_relevant_elements(row, relevant_idxs)

            sums = self.calculate_sums(rel_data, nr_races)
            
            for curr_sum in sums:
                if curr_sum >= min_limit and curr_sum <= max_limit:
                    relevant_rows.append(row_idx)
                    break
        return relevant_rows
    
    def interval_filter_iloc(self, data):
        relevant_data = self.get_relevant_column(data)
        relevant_idxs = [i - 1 for i in self.interval_filter_options['selected_elements']]

        min_limit = self.interval_filter_options['min_interval']
        max_limit = self.interval_filter_options['max_interval']
        min_hit = self.interval_filter_options['min_race']
        max_hit = self.interval_filter_options['max_race']
        relevant_rows = []
        for row_idx, row in enumerate(relevant_data):
            hit_count = 0
            rel_data = self.get_relevant_elements(row, relevant_idxs)

            for col in rel_data:
                if col >= min_limit and col <= max_limit:
                    hit_count += 1
                
            if hit_count >= min_hit and hit_count <= max_hit:
                relevant_rows.append(row_idx)
        
        return relevant_rows
    