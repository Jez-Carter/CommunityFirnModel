import glob
import numpy as np
import pandas as pd
import json
import subprocess

cfm_main_path = '/home/jez/Community_Firn_Model_Forked/CFM_main/'
experiment_path = '/home/jez/Community_Firn_Model_Forked/SpinUp_Sensitivity_Example/'

### increasing average value of snowfall to speedup runtime.
for f in glob.glob(f'{cfm_main_path}CFMinput_example/example*'):
    df = pd.read_csv(f).T
    if 'BDOT' in f: ### increasing average value of snowfall to speedup runtime.
        df = df+1.0
    new_filename = f.split('/')[-1].replace('example','adjusted')
    df.T.to_csv(f'{experiment_path}CFMinput_example/{new_filename}',index=False, header=True)

### loading and editing JSON file for CFM run
with open(f'{cfm_main_path}example.json', 'r') as read_file: 
    adjusted_json = json.load(read_file)
adjusted_json['InputFileFolder'] = f'{experiment_path}CFMinput_example/'
adjusted_json['resultsFolder'] = f'{experiment_path}results'
adjusted_json['InputFileNameTemp'] = 'adjusted_TSKIN.csv'
adjusted_json['InputFileNamebdot'] = 'adjusted_BDOT.csv'
adjusted_json['InputFileNamemelt'] = 'adjusted_SMELT.csv'
adjusted_json['InputFileNameRain'] = 'adjusted_RAIN.csv'
adjusted_json['InputFileNameSublim'] = 'adjusted_SUBLIM.csv'
adjusted_json['InputFileNameStrain'] = 'adjusted_STRAIN.csv'
adjusted_json['InputFileNameIso'] = 'adjusted_ISOTOPE.csv'
adjusted_json['InputFileNamerho'] = 'adjusted_RHOS.csv'
adjusted_json['input_type'] = 'csv'
adjusted_json['TWriteStart'] = 980.0
adjusted_json['residual_strain'] = 0.0 
adjusted_json['doublegrid'] =  False
adjusted_json['grid_outputs'] =  False
with open(f'{experiment_path}adjusted.json', 'w') as json_file:
    json.dump(adjusted_json, json_file, indent=0)

### creating json file with sublimation turned off
with open(f'{experiment_path}adjusted.json', 'r') as read_file: 
    no_sublim_json = json.load(read_file)
no_sublim_json['resultsFolder'] = f'{experiment_path}results/no_sublim'
no_sublim_json['SUBLIM'] =  False
with open(f'{experiment_path}no_sublim.json', 'w') as json_file:
    json.dump(no_sublim_json, json_file, indent=0)

### Running CFM with edited JSON
subprocess.call(['python',f'{cfm_main_path}main.py',f'{experiment_path}adjusted.json','-n'])
subprocess.call(['python',f'{cfm_main_path}main.py',f'{experiment_path}no_sublim.json','-n'])