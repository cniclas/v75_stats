from flask import request

class IntervalInput:
    def __init__(self, label, property_name):
        self.label = label
        self.property_name = property_name
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

    def get_values(self):
        min_value = request.form.get(f"{self.property_name}_min", None)
        max_value = request.form.get(f"{self.property_name}_max", None)
        max_unlimited = request.form.get(f"{self.property_name}_max_unlimited", None)

        # Update internal values based on user input
        self._min_value = min_value if min_value else 0
        self._max_value = max_value

        # Handle the "No upper limit" checkbox
        if max_unlimited:
            self._max_value = float('inf')

        # You may want to add validation or error handling here
        # to ensure min_value and max_value are valid (e.g., non-negative)

        return self._min_value, self._max_value
