from flask import request

class IntervalInput:
    def __init__(self, label_in):
        self.label = label_in
        self.property_name = label_in.replace(" ", "_")
        self._min_value = None
        self._max_value = None

    def generate_html(self):
        min_value = self._min_value or 0
        max_value = self._max_value or "Max"

        # Ensure max_value is a string for consistent rendering
        max_value_text = str(max_value)

        template = """
        <div class="input-pair">
        <label for="{property_name}_min">{label} Min:</label>
        <input type="number" id="{property_name}_min" name="{property_name}_min" step="any" placeholder="0" value="{min_value}" style="margin-right: 10px;"/>
        <label for="{property_name}_max">{label} Max:</label>
        <input type="number" id="{property_name}_max" name="{property_name}_max" step="any" placeholder="Max" value="{max_value_text}"/>
        </div>
        """
        return template.format(label=self.label, property_name=self.property_name, min_value=min_value, max_value_text=max_value_text)

    def update(self):
        min_value = request.form.get(f"{self.property_name}_min", None)
        max_value = request.form.get(f"{self.property_name}_max", None)
        
        # Update internal values based on user input
        self._min_value = float(min_value) if min_value else 0
        self._max_value = float(max_value) if max_value else float('inf')

        # You may want to add validation or error handling here
        # to ensure min_value and max_value are valid (e.g., non-negative)

    def filter_data(self, data):
        min_value = float(self._min_value)
        max_value = float(self._max_value)
        df = data[data[self.label].between(min_value, max_value)]
        return df
    
    def get_values(self):
        return self._min_value, self._max_value
