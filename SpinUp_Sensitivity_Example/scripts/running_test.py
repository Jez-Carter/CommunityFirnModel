import glob
import numpy as np
import pandas as pd
import json
import subprocess

cfm_main_path = '/home/jez/Community_Firn_Model_Forked/CFM_main/'
input_path = '/home/jez/Community_Firn_Model_Forked/CFM_Lancaster/data/cfm_input'
experiment_path = '/home/jez/Community_Firn_Model_Forked/SpinUp_Sensitivity_Example/'

### loading and editing JSON file for CFM run
with open(f'{cfm_main_path}example.json', 'r') as read_file: 
    adjusted_json = json.load(read_file)
adjusted_json['InputFileFolder'] = f'{input_path}'
adjusted_json['resultsFolder'] = f'{experiment_path}results_test'
adjusted_json['InputFileNameTemp'] = 'Kan-M_tskin.csv'
adjusted_json['InputFileNamebdot'] = 'Kan-M_snowfall.csv'
adjusted_json['InputFileNamemelt'] = 'Kan-M_snowmelt.csv'
adjusted_json['InputFileNameRain'] = 'Kan-M_rainfall.csv'
adjusted_json['input_type'] = 'csv'

adjusted_json['HbaseSpin'] = 2950.0
adjusted_json['TWriteStart'] = 1500.0
adjusted_json['residual_strain'] = 0.0 
adjusted_json['isoDiff'] = False 
adjusted_json['doublegrid'] =  False
adjusted_json['grid_outputs'] =  False
adjusted_json['SUBLIM'] =  False
with open(f'{experiment_path}test.json', 'w') as json_file:
    json.dump(adjusted_json, json_file, indent=0)

### Running CFM with edited JSON
subprocess.call(['python',f'{cfm_main_path}main.py',f'{experiment_path}test.json','-n'])
