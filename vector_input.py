from flask import request

class VectorInput:
    """
    Generates HTML code for filter options and tracks user selections.
    """

    def __init__(self, name, nr_elements):
        self.name = name
        self.nr_elements = nr_elements
        self.sum_filter_options = {
            "min_sum": "",
            "max_sum": "",
            "in_nr_races": self.nr_elements,
            "selected_elements": list(range(1, nr_elements + 1))  # Initially all elements selected
        }
        self.interval_filter_options = {
            "min_interval": "",
            "max_interval": "",
            "min_race": 0,
            "max_race": self.nr_elements,
            "selected_elements": list(range(1, nr_elements + 1))
        }
        
    def generate_html(self):
        html = f"<h3>{self.name}</h3>"

        # Create HTML structure for "sum" filter options with multiple inputs on the same row
        sum_html = f"""
        <div class="filter-row">
            <label for="{self.name}_sum_min">Sum Filter:</label>
            <input type="number" id="{self.name}_sum_min" name="{self.name}_min_sum" step="any" placeholder="0" value="{self.sum_filter_options['min_sum']}" style="width: 50px; height: 25px; padding: 5px;">
            -
            <input type="number" id="{self.name}_sum_max" name="{self.name}_max_sum" step="any" placeholder="Max" value="{self.sum_filter_options['max_sum']}" style="width: 50px; height: 25px; padding: 5px;">
            i 
            <input type="number" id="{self.name}_in_nr_races" name="{self.name}_in_nr_races" value="{self.sum_filter_options['in_nr_races']}" style="width: 50px; height: 25px; padding: 5px;">
             av loppen.
        """
        for i in range(1, self.nr_elements + 1):
            checked = "checked" if i in self.sum_filter_options["selected_elements"] else ""
            sum_html += f"""
            <span>
                <label for="{self.name}_sum_element_{i}">{i}</label>
                <input type="checkbox" id="{self.name}_sum_element_{i}" name="{self.name}_sum_elements" value="{i}" {checked}>
            </span>
        """
        sum_html += "</div>"

        # Create HTML structure for "interval" filter options
        interval_html = f"""
        <div class="filter-row">
            <label for="{self.name}_interval_min">Interval Filter:</label>
            <input type="number" id="{self.name}_interval_min" name="{self.name}_min_interval" step="any" placeholder="0" value="{self.interval_filter_options['min_interval']}" style="width: 50px; height: 25px; padding: 5px;">
            -
            <input type="number" id="{self.name}_interval_max" name="{self.name}_max_interval" step="any" placeholder="Max" value="{self.interval_filter_options['max_interval']}" style="width: 50px; height: 25px; padding: 5px;">
            <span>
                <label for="{self.name}_interval_min_race">Min Race:</label>
                <input type="number" id="{self.name}_interval_min_race" name="{self.name}_min_race" value="{self.interval_filter_options['min_race']}" style="width: 50px; height: 25px; padding: 5px;">
                -
                <label for="{self.name}_interval_max_race">Max Race:</label>
                <input type="number" id="{self.name}_interval_max_race" name="{self.name}_max_race" value="{self.interval_filter_options['max_race']}" style="width: 50px; height: 25px; padding: 5px;">
            </span>
        """
        for i in range(1, self.nr_elements + 1):
            checked = "checked" if i in self.interval_filter_options["selected_elements"] else ""
            interval_html += f"""
            <span>
                <label for="{self.name}_interval_element_{i}">{i}</label>
                <input type="checkbox" id="{self.name}_interval_element_{i}" name="{self.name}_interval_elements" value="{i}" {checked}>
            </span>
        """
        interval_html += "</div>"

        # Combine sections and return complete HTML
        html += sum_html + interval_html
        return html

    def update(self):
        """
        Gets filter options selected by the user from form data.

        Args:
            request: The Flask request object.

        Returns:
            dict: A dictionary containing selected filter options.
        """

        self.sum_filter_options["min_sum"] = request.form.get(f"{self.name}_min_sum", "")
        self.sum_filter_options["min_sum"] = float(self.sum_filter_options["min_sum"]) if self.sum_filter_options["min_sum"] else 0
        self.sum_filter_options["max_sum"] = request.form.get(f"{self.name}_max_sum", "")
        self.sum_filter_options["max_sum"] = float(self.sum_filter_options["max_sum"]) if self.sum_filter_options["max_sum"] else float('inf')
        self.sum_filter_options["in_nr_races"] = request.form.get(f"{self.name}_in_nr_races", "")
        self.sum_filter_options["in_nr_races"] = int(self.sum_filter_options["in_nr_races"]) if self.sum_filter_options["in_nr_races"] else int(self.nr_elements)
        self.sum_filter_options["in_nr_races"] = self.limit_value_one(self.sum_filter_options["in_nr_races"])
        self.sum_filter_options["selected_elements"] = request.form.getlist(f"{self.name}_sum_elements", type=int) or []

        self.interval_filter_options["min_interval"] = request.form.get(f"{self.name}_min_interval", "")
        self.interval_filter_options["min_interval"] = float(self.interval_filter_options["min_interval"]) if self.interval_filter_options["min_interval"] else 0
        self.interval_filter_options["max_interval"] = request.form.get(f"{self.name}_max_interval", "")
        self.interval_filter_options["max_interval"] = float(self.interval_filter_options["max_interval"]) if self.interval_filter_options["max_interval"] else float('inf')
        self.interval_filter_options["min_race"] = request.form.get(f"{self.name}_min_race", "")
        self.interval_filter_options["min_race"] = int(self.interval_filter_options["min_race"]) if self.interval_filter_options["min_race"] else 0
        self.interval_filter_options["min_race"] = self.limit_value_zero(self.interval_filter_options["min_race"])
        self.interval_filter_options["max_race"] = request.form.get(f"{self.name}_max_race", "")
        self.interval_filter_options["max_race"] = int(self.interval_filter_options["max_race"]) if self.interval_filter_options["max_race"] else int(self.nr_elements)
        self.interval_filter_options["max_race"] = self.limit_value_zero(self.interval_filter_options["max_race"])
        self.interval_filter_options["selected_elements"] = request.form.getlist(f"{self.name}_interval_elements", type=int) or []

        # Combine both filter options into a single dictionary
        filtered_options = {
            "sum": self.sum_filter_options,
            "interval": self.interval_filter_options
        }

        return filtered_options
    
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
    
    def filter_data(self, data):
        return data
