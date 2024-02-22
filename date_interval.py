from datetime import datetime
from flask import request

class DateIntervalInput:
    def __init__(self, label_in, min_date):
        self.label = label_in
        self.property_name = label_in.replace(" ", "_")
        self._min_date = min_date
        self._max_date = datetime.today()
        self._all_months = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
        self._selected_months = self._all_months

    def generate_html(self):
        min_date_str = self._min_date.strftime("%Y-%m-%d") if self._min_date else ""
        max_date_str = self._max_date.strftime("%Y-%m-%d") if self._max_date else ""

        month_checkboxes = ""
        for i, month_name in enumerate(self._all_months):
            checked = "checked" if month_name in self._selected_months else ""  # Use your member variables
            month_checkboxes += f"""
                <label for="{self.property_name}_month_{i + 1}">{month_name}</label>
                <input type="checkbox" id="{self.property_name}_month_{i + 1}" name="{self.property_name}_month_{i + 1}" value="{i + 1}" {checked}>
            """

        template = f"""
        <div class="filter-container">
            <label>{self.label}</label>
            <label for="{self.property_name}_min_date"> Min:</label>
            <input type="date" id="{self.property_name}_min_date" name="{self.property_name}_min_date" value="{min_date_str}"/>
            <label for="{self.property_name}_max_date"> Max:</label>
            <input type="date" id="{self.property_name}_max_date" name="{self.property_name}_max_date" value="{max_date_str}"/>
            <div class="selected_months"> 
                {month_checkboxes}
            </div>
        </div>
        """
        return template


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

        # Update selected months
        selected_months = []  # Use a list to store month names 

        # Loop through all months (adjust if you want to limit the range)
        for i in range(1, 13):  
            checkbox_name = f"{self.property_name}_month_{i}"
            is_checked = request.form.get(checkbox_name) is not None

            if is_checked:
                month_name = self._all_months[i - 1]  # Get the month name
                selected_months.append(month_name)

        # Update the internal variable with the selected months
        self._selected_months = selected_months 

    def get_values(self):
        return self._min_date, self._max_date
    
    def filter_data(self, data):
        df = data.copy()  # Create a copy to preserve the original structure

        df = df[data[self.label].between(self._min_date, self._max_date, inclusive='both')]

        df = df[df[self.label].dt.month_name().isin(self._selected_months)] 

        if df.empty:  # Check if any filtering removed all rows
            return data.iloc[0:0]  # Return an empty DataFrame with original columns

        return df

