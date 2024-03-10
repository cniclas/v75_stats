from flask import request

class LocationInput:
    def __init__(self, label, available_strings):
        self.label = label
        self.property_name = label.replace(" ", "_")
        self.available_strings = available_strings
        self._selected_strings = available_strings

    def generate_html(self):
        checkboxes_html = ""
        for string in self.available_strings:
            checked = "checked" if string in self._selected_strings else ""
            checkboxes_html += f"""
                <label>
                    <input type="checkbox" name="{self.property_name}_{string}" value="{string}" {checked}> {string}
                </label>
            """

        template = f"""
            <div class="filter-container">
                <div class="banor-checkboxes">
                    <label>{self.label}</label>
                    {checkboxes_html}
                </div>
            </div>
        """
        return template

    def update(self):
        """Updates the selected strings based on checkbox selections."""

        # Initialize an empty list to store selected strings
        selected_strings = []

        # Loop through each available string
        for string in self.available_strings:
            # Check if the checkbox associated with the string is checked
            checkbox_name = f"{self.property_name}_{string}"
            is_checked = request.form.get(checkbox_name) is not None

            # Add the string to the list if it's checked
            if is_checked:
                selected_strings.append(string)

        # Update the internal variable with the selected strings
        self._selected_strings = selected_strings

    def get_selected_strings(self):
        return self._selected_strings
    
    def filter_data(self, data):
        df = data[data[self.label].isin(self._selected_strings)]
        return df

    def get_label(self):
        return self.label
    
    def get_filter_str(self):
        pass