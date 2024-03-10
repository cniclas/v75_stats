import pandas as pd
import math

def calculate_scalar_field_statistics(all_data, rel_data, label):
  # Get the scalar field data and remove the jackpots
  all_data_jkpt_comp = all_data[all_data[label] != 0][label]
  rel_data_jkpt_comp = rel_data[rel_data[label] != 0][label]
  
  # Remove and count Jackpots in the set
  nr_total_jackpot_entries = len(all_data) - len(all_data_jkpt_comp)
  nr_relevant_jackpot_entries = len(rel_data) - len(rel_data_jkpt_comp)

  # Calculate the statistics
  data_statistics = {
    "nr_jackpots": nr_total_jackpot_entries,
    "min": all_data_jkpt_comp.min(),
    "max": all_data_jkpt_comp.max(),
    "medel": all_data_jkpt_comp.mean(),
    "summa": all_data_jkpt_comp.sum(),
  }
  
  filt_statistics = {
    "nr_jackpots": nr_relevant_jackpot_entries,
    "min": rel_data_jkpt_comp.min(),
    "max": rel_data_jkpt_comp.max(),
    "medel": rel_data_jkpt_comp.mean(),
    "summa": rel_data_jkpt_comp.sum(),
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
  if xtot > 0 and not math.isnan(xtot) and not math.isnan(x):
    frac = x / xtot
  else:
    frac = 0
  return frac * 100

def generate_html_report(label, stats, nr_all_data, nr_filt_data):

    html = f"""
    <div class="scalar-results"> 
        <h2>Statistik för {label}</h2>
        <table>
            <thead>
                <tr>
                    <th>Omgångar</th>
                    <th>Pott total</th>
                    <th>Jackpots</th>
                    <th>Medel</th>
                    <th>Min</th>
                    <th>Max</th>
                </tr>
            </thead>
            <tbody>
                <tr> 
                    <td><b>{format_number(nr_all_data)}</b></td>
                    <td><b>{format_number(stats['all_data']['summa'])}</b></td>
                    <td><b>{stats['all_data']['nr_jackpots']}</b></td>
                    <td><b>{format_number(stats['all_data']['medel'])}</b></td>
                    <td><b>{format_number(stats['all_data']['min'])}</b></td>
                    <td><b>{format_number(stats['all_data']['max'])}</b></td>
                </tr>
                <tr> 
                    <td>{nr_filt_data}</td>
                    <td>{format_number(stats['filt_data']['summa'])}</td>
                    <td>{stats['filt_data']['nr_jackpots']}</td>
                    <td>{format_number(stats['filt_data']['medel'])}</td>
                    <td>{format_number(stats['filt_data']['min'])}</td>
                    <td>{format_number(stats['filt_data']['max'])}</td>
                    
                </tr>
                <tr> 
                    <td>{calc_percentage(nr_filt_data, nr_all_data):.1f}%</td> 
                    <td>{calc_percentage(stats['filt_data']['summa'], stats['all_data']['summa']):.1f}%</td>
                    <td>{calc_percentage(stats['filt_data']['nr_jackpots'], stats['all_data']['nr_jackpots']):.1f}%</td>
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