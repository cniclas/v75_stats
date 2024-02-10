from flask import Flask, render_template, request, jsonify
from interval_input import IntervalInput
from interval_input_jackpot import IntervalInputJackpot
from data_loader import DataLoader

app = Flask(__name__)

data_loader = DataLoader()  # Create a DataLoader instance
interval_inputs = []  # Store filter instances globally

@app.route('/')
def index():
    return render_template('index.html', interval_inputs=[])  # Initially no filters

@app.route('/load_data', methods=['POST'])
def load_data():
    global data_loader
    data_version = request.form.get('data_version')

    if data_version == "v75":
        filepath = "data/data_v75.csv"
    else:
        filepath = "data/data_v86.csv"

    data_loader.load_data(filepath)  # Load the selected data

    # Process or display the loaded data as needed
    return render_template('index.html', selected_version=data_version)

@app.route('/add_filter')
def add_filter():
    global interval_inputs
    interval_inputs.append(IntervalInputJackpot("New Filter", f"filter_{len(interval_inputs) + 1}"))  # Generate unique property name
    return jsonify({'html': interval_inputs[-1].generate_html()})  # Return HTML for the new filter

@app.route('/', methods=['POST'])
def apply_filters():
    global interval_inputs
    # ... (Handle form submission and data filtering using interval_inputs)
    return render_template('index.html', interval_inputs=interval_inputs)

if __name__ == '__main__':
    app.run(debug=True)
