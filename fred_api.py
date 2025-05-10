import pandas as pd
import requests
from fred_key import fred_key
from flask import Flask, jsonify, request
from flask_cors import CORS

#flask stuff
app = Flask(__name__)
CORS(app)

@app.route('/api/data', methods=['GET'])
def get_data():
    api_key = fred_key
    base_url = 'https://api.stlouisfed.org/fred/'
    obs_endpoint = 'series/observations'
    
    series_id = 'CPIAUCSL'
    start_date = '2000-01-01'
    end_date = '2023-06-30'
    ts_frequency = 'q'
    ts_units = 'pc1'
    
    obs_params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': start_date,
        'observation_end': end_date,
        'units': ts_units
    }
    
    response = requests.get(base_url + obs_endpoint, params=obs_params)
    
    if response.status_code == 200:
        res_data = response.json()
        obs_data = pd.DataFrame(res_data['observations'])
        # Convert dates and values to the format we need
        dates = obs_data['date'].tolist()
        values = [float(x) for x in obs_data['value'].tolist()]
        return jsonify({
            'dates': dates,
            'values': values
        })
    else:
        return jsonify({'error': 'Failed to fetch data'}), 500

if __name__ == '__main__':
    app.run(debug=True)