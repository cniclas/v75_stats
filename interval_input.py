from flask import request
from string_to_number import convert_string_to_number
from data_output import format_number

class IntervalInput:
    # Class variable to keep track of the count
    instance_count = 0
    
    def __init__(self, label_in):
        IntervalInput.instance_count += 1
        self.unique_id = IntervalInput.instance_count
        self.label = label_in
        self.property_name = label_in.replace(" ", "_")
        self.global_max = 2**64
        self._min_value = 0
        self._max_value = self.global_max

    def generate_html(self):
        min_value_str = str(format_number(self._min_value))
        
        if self._max_value >= self.global_max:
            max_value_str = "Max"
        else:
            max_value_str = str(format_number(self._max_value))

        template = """
        <div class="filter-container">
        <label>{label}</label>
        <label for="{property_name}_min"> Min:</label>
        <input type="text" class="large-number-input" id="{property_name}_min" name="{property_name}_min" step="any" placeholder="0" value="{min_value_text}" style="margin-right: 10px;"/>
        <label for="{property_name}_max"> Max:</label>
        <input type="text" class="large-number-input" id="{property_name}_max" name="{property_name}_max" step="any" placeholder="Max" value="{max_value_text}"/>
        </div>
        """
        return template.format(label=self.label, property_name= self.property_name + str(self.unique_id), min_value_text=min_value_str, max_value_text=max_value_str)

    def update(self):
        min_value_in = request.form.get(f"{self.property_name}{self.unique_id}_min", None)
        max_value_in = request.form.get(f"{self.property_name}{self.unique_id}_max", None)
        
        min_value = convert_string_to_number(min_value_in, error_value=0)
        if min_value < 0:
            min_value = 0
            
        max_value = convert_string_to_number(max_value_in, error_value=self.global_max)
        if max_value < min_value:
            max_value = min_value
        
        # Update internal values based on user input
        self._min_value = min_value
        self._max_value = max_value

    def filter_data(self, data):
        min_value = int(self._min_value)
        max_value = int(self._max_value)
        df = data[data[self.label].between(min_value, max_value)]
        return df
    
    def get_filter_str(self):
        min_value = int(self._min_value)
        max_value = int(self._max_value)
        # Instead of filtering the dataframe, return the logical expression as a string
        return f"(`{self.label}` >= {min_value} and `{self.label}` <= {max_value})"
    
    def get_values(self):
        return self._min_value, self._max_value
    
    def get_label(self):
        return self.label
