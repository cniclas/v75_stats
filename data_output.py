import pandas as pd

def calculate_scalar_field_statistics(data, label):
  """
  Calculates the minimum, maximum, mean, and sum of a scalar field in a dataset.

  Args:
    data: A pandas DataFrame containing the data.
    label: The name of the scalar field to analyze.

  Returns:
    A dictionary containing the calculated statistics.
  """
  # Get the scalar field data
  scalar_field = data[label]

  # Calculate the statistics
  statistics = {
    "min": scalar_field.min(),
    "max": scalar_field.max(),
    "medel": scalar_field.mean(),
    "summa": scalar_field.sum(),
  }

  return statistics

def generate_html_report(label, statistics):
  """
  Generates HTML code to present the statistics for a specific label.

  Args:
    label: The name of the scalar field.
    statistics: A dictionary containing the calculated statistics.

  Returns:
    A string containing the HTML code.
  """

  html = f"""
  <div class="statistics-row">
    <span class="label">{label.capitalize()}:</span>
    """

  for key, value in statistics.items():
    html += f"""
    <span class="statistic">
      <span class="value">{key.capitalize()}: {value}</span>
    </span>
    """

  html += """
  </div>
  """

  return html

def generate_scalar_html_report(data, label):
    stats = calculate_scalar_field_statistics(data, label)
    return generate_html_report(label, stats)