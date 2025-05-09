import pandas as pd
import requests
from fred_key import fred_key
import matplotlib.pyplot as plt
from flask import Flask, jsonify, request

#flask stuff
app = Flask(__name__)

percentage_data = [{}]
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
    'units' : ts_units
}

response = requests.get(base_url + obs_endpoint, params= obs_params)

if response.status_code == 200:
    res_data = response.json()
    obs_data = pd.DataFrame(res_data['observations'])
    obs_data['data'] = pd.to_datetime(obs_data['date'])
    obs_data.set_index('data', inplace=True)
    obs_data['value'] = obs_data['value'].astype(float)
    print(res_data)
    print("--------------------------------")
    print(res_data.keys())
else:
    print("beeeeeeeeee")
    print ("failed" + response.status_code)
print("hello")