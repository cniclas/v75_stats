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

def generate_html_report(label, stats_basic, stats_adv, nr_all_data, nr_basic_filt_data, nr_adv_filt_data):

    html = f"""
    <div class="scalar-results"> 
        <table>
            <thead>
                <tr>
                    <th>{label}</th>
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
                    <td><b>All Data</b></td>
                    <td><b>{format_number(nr_all_data)}</b></td>
                    <td><b>{format_number(stats_basic['all_data']['summa'])}</b></td>
                    <td><b>{stats_basic['all_data']['nr_jackpots']}</b></td>
                    <td><b>{format_number(stats_basic['all_data']['medel'])}</b></td>
                    <td><b>{format_number(stats_basic['all_data']['min'])}</b></td>
                    <td><b>{format_number(stats_basic['all_data']['max'])}</b></td>
                </tr>
                <tr> 
                    <td>Basic Filtered Data</td>
                    <td>{nr_basic_filt_data} ({calc_percentage(nr_basic_filt_data, nr_all_data):.1f}%)</td>
                    <td>{format_number(stats_basic['filt_data']['summa'])} ({calc_percentage(stats_basic['filt_data']['summa'], stats_basic['all_data']['summa']):.1f}%)</td>
                    <td>{stats_basic['filt_data']['nr_jackpots']} ({calc_percentage(stats_basic['filt_data']['nr_jackpots'], stats_basic['all_data']['nr_jackpots']):.1f}%)</td>
                    <td>{format_number(stats_basic['filt_data']['medel'])}</td>
                    <td>{format_number(stats_basic['filt_data']['min'])}</td>
                    <td>{format_number(stats_basic['filt_data']['max'])}</td>
                </tr>
                <tr> 
                    <td>Basic & Advanced Filtered Data</td>
                    <td>{nr_adv_filt_data} ({calc_percentage(nr_adv_filt_data, nr_basic_filt_data):.1f}%)</td>
                    <td>{format_number(stats_adv['filt_data']['summa'])} ({calc_percentage(stats_adv['filt_data']['summa'], stats_basic['all_data']['summa']):.1f}%)</td>
                    <td>{stats_adv['filt_data']['nr_jackpots']} ({calc_percentage(stats_adv['filt_data']['nr_jackpots'], stats_basic['all_data']['nr_jackpots']):.1f}%)</td>
                    <td>{format_number(stats_adv['filt_data']['medel'])}</td>
                    <td>{format_number(stats_adv['filt_data']['min'])}</td>
                    <td>{format_number(stats_adv['filt_data']['max'])}</td>
                </tr>
            </tbody>
        </table>
    </div> 
    """
    return html

def generate_scalar_html_report(all_data, df_basic, df_adv, label):
    stats_basic = calculate_scalar_field_statistics(all_data, df_basic, label)
    stats_adv = calculate_scalar_field_statistics(df_basic, df_adv, label)
    return generate_html_report(label, stats_basic, stats_adv, len(all_data), len(df_basic), len(df_adv))