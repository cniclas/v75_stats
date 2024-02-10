from flask import request
from interval_input import IntervalInput

class IntervalInputJackpot(IntervalInput):
    def __init__(self, label, property_name):
        super().__init__(label, property_name)
        self._include_jackpots = False

    def generate_html(self):
        min_value, max_value = self._min_value, self._max_value
        max_value_text = str(max_value)

        template = """
        <div class="input-pair">
          <label for="{property_name}_min">{label} Min:</label>
          <input type="number" id="{property_name}_min" name="{property_name}_min" step="any" placeholder="0" value="{min_value}"/>
          <label for="{property_name}_max">{label} Max:</label>
          <input type="number" id="{property_name}_max" name="{property_name}_max" step="any" placeholder="Max" value="{max_value_text}"/>
          <label for="{property_name}_jackpots">{label} Include Jackpots:</label>
          <input type="checkbox" id="{property_name}_jackpots" name="{property_name}_jackpots">
        </div>
        """
        return template.format(label=self.label, property_name=self.property_name, min_value=min_value, max_value_text=max_value_text)

    def get_values(self):
        min_value, max_value = super().get_values()
        self._include_jackpots = request.form.get(f"{self.property_name}_jackpots", None)
        return min_value, max_value, self._include_jackpots