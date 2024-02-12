from flask import Flask, render_template, request, jsonify
from interval_input import IntervalInput
from interval_input_jackpot import IntervalInputJackpot
from data_loader import DataLoader
from vector_input import VectorInput
from init_template_support import init_filters

app = Flask(__name__)

selected_version = 'v75'
data_loader = DataLoader()  # Create a DataLoader instance
all_filters = []
interval_inputs = []  # Store filter instances globally

@app.route('/')
def index():
    return render_template('index.html', selected_version=selected_version)
    
@app.route('/load_data', methods=['POST'])
def load_data():
    global data_loader, all_filters
    selected_version = request.form.get('data_version')

    if selected_version == "v75":
        filepath = "data/data_v75.csv"
    else:
        filepath = "data/data_v86.csv"

    data_loader.load_data(filepath)  # Load the selected data
    
    all_filters = init_filters(data_loader.get_data())
    
    all_filters_html = ''.join(curr_filter.generate_html() for curr_filter in all_filters)

    # Process or display the loaded data as needed
    return render_template('index.html', selected_version=selected_version, interval_inputs=all_filters_html)

@app.route('/filter_data', methods=['POST'])
def filter_data():
    global all_filters
    for curr_filter in all_filters:
        curr_filter.update()
    all_filters_html = ''.join(curr_filter.generate_html() for curr_filter in all_filters)

    return render_template('index.html', selected_version='v75', interval_inputs=all_filters_html)

if __name__ == '__main__':
    app.run(debug=True)
