from flask import Flask, render_template, request
from data_loader import DataLoader
from init_template_support import init_filters_2
from data_output import generate_scalar_html_report
from filter_iterator import filter_iterator

app = Flask(__name__)

selected_version = 'v75' # Initialize v75 as default data selection
data_loader = DataLoader()  # Create a DataLoader instance
all_filters = [] # html string for filters
filter_inputs = []  # Store filter instances globally

@app.route('/')
def index():
    return render_template('index.html', selected_version=selected_version)
    
@app.route('/load_data', methods=['POST'])
def load_data():
    global data_loader, all_filters, selected_version
    selected_version = request.form.get('data_version')

    if selected_version == "v75":
        filepath = "data/data_v75.csv"
    else:
        filepath = "data/data_v86.csv"

    data_loader.load_data(filepath)  # Load the selected data
    
    basic_filters, adv_filters = init_filters_2(data_loader.get_data())
    
    
    basic_filters_html = ''.join(curr_filter.generate_html() for curr_filter in basic_filters)
    adv_filters_html = ''.join(curr_filter.generate_html() for curr_filter in adv_filters)
    
    # Process or display the loaded data as needed
    return render_template('index.html', selected_version=selected_version, 
                           basic_filters_html=basic_filters_html, 
                           adv_filters_html=adv_filters_html)

@app.route('/filter_data', methods=['POST'])
def filter_data():
    global data_loader, all_filters, selected_version
    for curr_filter in all_filters:
        curr_filter.update()
    all_filters_html = ''.join(curr_filter.generate_html() for curr_filter in all_filters)

    all_data = data_loader.get_data()
    df = filter_iterator(all_data, all_filters)
    
    # Calculate fraction of all avaialble data that is relevant
    total_entries = len(all_data)
    relevant_entries = len(df)
    if total_entries > 0:
        fraction = round(relevant_entries / total_entries, 2)
    else:
        fraction = 1
    relevant_percentage = 100 * fraction
    
    if '8 Rätt' in df.columns:
        scalar_html = generate_scalar_html_report(all_data, df, '8 Rätt')
        scalar_html += generate_scalar_html_report(all_data, df, '7 Rätt')        
        scalar_html += generate_scalar_html_report(all_data, df, '6 Rätt')
    else:
        scalar_html = generate_scalar_html_report(all_data, df, '7 Rätt')        
        scalar_html += generate_scalar_html_report(all_data, df, '6 Rätt')
        scalar_html += generate_scalar_html_report(all_data, df, '5 Rätt')
    
    return render_template('index.html', selected_version=selected_version, 
                           filter_inputs=all_filters_html, total_data_entries=total_entries, 
                           relevant_percentage=relevant_percentage, all_scalar_results_html=scalar_html)

if __name__ == '__main__':
    app.run(debug=True)
