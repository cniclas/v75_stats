import pandas as pd
import math

def calculate_scalar_field_statistics(all_data, filt_data, label):
  # Get the scalar field data
  data_scalar_field = all_data[label]
  filt_scalar_field = filt_data[label]

  # Calculate the statistics
  data_statistics = {
    "min": data_scalar_field.min(),
    "max": data_scalar_field.max(),
    "medel": data_scalar_field.mean(),
    "summa": data_scalar_field.sum(),
  }
  
  filt_statistics = {
    "min": filt_scalar_field.min(),
    "max": filt_scalar_field.max(),
    "medel": filt_scalar_field.mean(),
    "summa": filt_scalar_field.sum(),
  }
  
  stats = {
    "all_data": data_statistics,
    "filt_data": filt_statistics,
  }

  return stats

def format_number(number):
  if math.isnan(number):
    number = 0
  return "{:,}".format(int(number))

def calc_percentage(x, xtot):
  if xtot > 0:
    frac = x / xtot
  else:
    frac = 0
  return frac * 100

def generate_html_report(label, stats, nr_all_data, nr_filt_data):
    nr_percent = calc_percentage(nr_filt_data, nr_all_data)

    html = f"""
    <div class="scalar-results"> 
        <h2>Statistics for {label}</h2>
        <table>
            <thead>
                <tr>
                    <th>Omgångar</th>
                    <th>Pott total</th>
                    <th>Medel</th>
                    <th>Min</th>
                    <th>Max</th>
                </tr>
            </thead>
            <tbody>
                <tr> 
                    <td><b>{format_number(nr_all_data)}</b></td>
                    <td><b>{format_number(stats['all_data']['summa'])}</b></td>
                    <td><b>{format_number(stats['all_data']['medel'])}</b></td>
                    <td><b>{format_number(stats['all_data']['min'])}</b></td>
                    <td><b>{format_number(stats['all_data']['max'])}</b></td>
                </tr>
                <tr> 
                    <td>{nr_filt_data}</td>
                    <td>{format_number(stats['filt_data']['summa'])}</td>
                    <td>{format_number(stats['filt_data']['medel'])}</td>
                    <td>{format_number(stats['filt_data']['min'])}</td>
                    <td>{format_number(stats['filt_data']['max'])}</td>
                </tr>
                <tr> 
                    <td>{calc_percentage(nr_filt_data, nr_all_data):.1f}%</td> 
                    <td>{calc_percentage(stats['filt_data']['summa'], stats['all_data']['summa']):.1f}%</td>
                    <td>{calc_percentage(stats['filt_data']['medel'], stats['all_data']['medel']):.1f}%</td>
                    <td></td>
                    <td></td>
                </tr>
            </tbody>
        </table>
    </div> 
    """
    return html





def generate_scalar_html_report(all_data, filt_data, label):
    stats = calculate_scalar_field_statistics(all_data, filt_data, label)
    return generate_html_report(label, stats, len(all_data), len(filt_data))