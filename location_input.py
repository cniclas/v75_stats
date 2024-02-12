import json
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
                    <input type="checkbox" name="{self.property_name}" value="{string}" {checked}> {string}
                </label>
            """

        template = f"""
            <div class="input-pair">
                <label>{self.label}:</label>
                {checkboxes_html}
            </div>
        """
        return template

    def update(self):
        selected_strings = request.form.getlist(self.property_name)  # Get list of selected values
        self._selected_strings = selected_strings

    def reset(self):
        self._selected_strings = []

    def get_selected_strings(self):
        return self._selected_strings
