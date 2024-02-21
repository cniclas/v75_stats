from datetime import datetime
from flask import request

class DateIntervalInput:
    def __init__(self, label_in, min_date):
        self.label = label_in
        self.property_name = label_in.replace(" ", "_")
        self._min_date = min_date
        self._max_date = datetime.today()

    def generate_html(self):
        min_date_str = self._min_date.strftime("%Y-%m-%d") if self._min_date else ""
        max_date_str = self._max_date.strftime("%Y-%m-%d") if self._max_date else ""

        template = """
        <div class="filter-container">
            <label for="{property_name}_min_date">{label} Min Date:</label>
            <input type="date" id="{property_name}_min_date" name="{property_name}_min_date" value="{min_date_str}"/>
            <label for="{property_name}_max_date">{label} Max Date:</label>
            <input type="date" id="{property_name}_max_date" name="{property_name}_max_date" value="{max_date_str}"/>
        </div>
        """
        return template.format(label=self.label, property_name=self.property_name, min_date_str=min_date_str, max_date_str=max_date_str)

    def update(self):
        min_date_str = request.form.get(f"{self.property_name}_min_date")
        max_date_str = request.form.get(f"{self.property_name}_max_date")

        # Ensure min_date is before max_date if both are provided
        if min_date_str and max_date_str:
            min_date = datetime.strptime(min_date_str, "%Y-%m-%d")
            max_date = datetime.strptime(max_date_str, "%Y-%m-%d")
            if min_date > max_date:
                # Handle error or swap dates
                pass

        # Update internal values
        self._min_date = datetime.strptime(min_date_str, "%Y-%m-%d") if min_date_str else None
        self._max_date = datetime.strptime(max_date_str, "%Y-%m-%d") if max_date_str else None

        # You may want to add validation or error handling here
        # to ensure dates are valid

    def get_values(self):
        return self._min_date, self._max_date
    
    def filter_data(self, data):
        df = data[data[self.label].between(self._min_date, self._max_date, inclusive='both')]
        return df
