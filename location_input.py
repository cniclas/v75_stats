import json
from flask import request

class LocationInput:
    def __init__(self, label, available_strings):
        self.label = label
        self.property_name = label.replace(" ", "_")
        self.available_strings = available_strings
        self._selected_strings = available_strings

    def generate_html(self):
        selected_strings_str = ",".join(self._selected_strings)

        template = """
        <div class="input-pair">
            <label for="{property_name}">Select {label}:</label>
            <input type="text" id="{property_name}" name="{property_name}" value="{selected_strings_str}" placeholder="Comma-separated values"/>
        </div>
        """
        return template.format(label=self.label, property_name=self.property_name, selected_strings_str=selected_strings_str)

    def update(self):
        selected_strings_str = request.form.get(self.property_name)
        self._selected_strings = [string.strip() for string in selected_strings_str.split(",")] if selected_strings_str else []
    
    def reset(self):
        self._selected_strings = self.available_strings[:]  # Copy the entire list

    def get_selected_strings(self):
        return self._selected_strings

