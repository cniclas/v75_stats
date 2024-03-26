from flask import request
from itertools import combinations
from string_to_number import convert_string_to_number
from general_support import limit_value_one, get_relevant_column, get_relevant_elements

class ArraySumIntervalFilter:
    
    instance_count = 0
    
    def __init__(self, label_in, nr_elements):
        ArraySumIntervalFilter.instance_count += 1
        self.unique_id = ArraySumIntervalFilter.instance_count
        self.label = label_in
        self.nr_elements = nr_elements
        self.sum_filter_options = {
            "min_sum": 0,
            "max_sum": 2**64,
            "in_nr_races": self.nr_elements,
            "selected_elements": list(range(1, nr_elements + 1))  # Initially all elements selected
        }
        
    def get_unique_id(self):
        return self.unique_id

    def generate_html(self):
        max_sum_str = self.sum_filter_options['max_sum']
        if max_sum_str >= 2**64:
            max_sum_str = "Max"
            
        sum_html = f"""
        <div class="adv-filter-single-container">
            <label for="{self.label}{self.unique_id}_sum_min">{self.label} Summa Intervall, Unique Id: {self.unique_id}</label>
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
        sum_html += f"""<button type="button" onclick="deleteFilterObject({self.unique_id})">Delete</button>"""
        sum_html += "</div>"
        return sum_html
    
    def update(self):
        self.sum_filter_options["min_sum"] = convert_string_to_number(request.form.get(f"{self.label}{self.unique_id}_min_sum", ""), 0)
        self.sum_filter_options["max_sum"] = convert_string_to_number(request.form.get(f"{self.label}{self.unique_id}_max_sum", ""), 2**64)

        self.sum_filter_options["in_nr_races"] = convert_string_to_number(request.form.get(f"{self.label}{self.unique_id}_in_nr_races", ""), self.nr_elements)
        self.sum_filter_options["in_nr_races"] = limit_value_one(self.sum_filter_options["in_nr_races"], self.nr_elements)
        
        selected_elements = []
        for i in range(1, self.nr_elements + 1):
            checkbox_name = f"{self.label}{self.unique_id}_sum_elements_{i}"
            if request.form.get(checkbox_name):  # Check if the checkbox is checked
                selected_elements.append(int(i))  # Cast to int for consistency
        self.sum_filter_options["selected_elements"] = selected_elements
        
    def sum_filter(self, data):
        relevant_rows = self.sum_filter_iloc(data)
        return data.iloc[relevant_rows] 
    
    def sum_filter_iloc(self, data):
        relevant_data = get_relevant_column(data, self.label)
        relevant_idxs = [i - 1 for i in self.sum_filter_options['selected_elements']]

        min_limit = self.sum_filter_options['min_sum']
        max_limit = self.sum_filter_options['max_sum']
        nr_races = self.sum_filter_options['in_nr_races']

        relevant_rows = []
        for row_idx, row in enumerate(relevant_data):
            rel_data = get_relevant_elements(row, relevant_idxs)

            sums = self.calculate_sums(rel_data, nr_races)
            
            for curr_sum in sums:
                if curr_sum >= min_limit and curr_sum <= max_limit:
                    relevant_rows.append(row_idx)
                    break
        return relevant_rows
    
    def calculate_sums(self, vector, nr_elements):
        if len(vector) < nr_elements:
            raise ValueError("Du har specifierat fler kombinationer än lopp.")
        sums = []
        for subset in combinations(vector, nr_elements):
            sums.append(sum(subset))
        return sums
        
    def filter_data(self, data):
        relevant_rows = self.sum_filter_iloc(data)
        return data.iloc[relevant_rows]