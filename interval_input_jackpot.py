from flask import request
from interval_input import IntervalInput

class IntervalInputJackpot(IntervalInput):
    def __init__(self, label):
        super().__init__(label)
        self._include_jackpots = True

    def generate_html(self):
        min_value_str = str(self._min_value)
        
        if self._max_value >= self.global_max:
            max_value_str = "Max"
        else:
            max_value_str = str(self._max_value)
            

        # Dynamically assign `value` and `checked` attributes based on internal state
        checkbox_value = "on" if self._include_jackpots else "off"  # Clearer variable name
        checkbox_checked = "checked" if self._include_jackpots else ""

        template = """
        <div class="filter-container">
            <label>{label}</label>
            <label for="{property_name}_min"> Min:</label>
            <input type="number" id="{property_name}_min" name="{property_name}_min" step="any" placeholder="0" value="{min_value_text}"/>
            <label for="{property_name}_max"> Max:</label>
            <input type="number" id="{property_name}_max" name="{property_name}_max" step="any" placeholder="Max" value="{max_value_text}"/>
            <label for="{property_name}_jackpots"> Inkludera Jackpots:</label>
            <input type="checkbox" id="{property_name}_jackpots" name="{property_name}_jackpots"
                   value="{checkbox_value}" {checkbox_checked}>
        </div>
        """
        return template.format(label=self.label, property_name=self.property_name, min_value_text=min_value_str,
                              max_value_text=max_value_str, checkbox_value=checkbox_value, checkbox_checked=checkbox_checked)
    
    def update(self):
        super().update()
        self._include_jackpots = request.form.get(f"{self.property_name}_jackpots", None)

    def filter_data(self, data):
        if self._include_jackpots:
            df = data[data[self.label].between(self._min_value, self._max_value) | (data[self.label] == 0)]
        else:
            df = data[data[self.label].between(self._min_value, self._max_value)]
        return df