import json
import subprocess
from src.paths import repo_path

cfm_data_path = f'{repo_path}CFM_Lancaster/data/cfm_input/'
results_path = f'{repo_path}CFM_Lancaster/results/'
cfm_main_path = f'{repo_path}CFM_main/'

stations = ['Summit','Kan-M']

for station in stations:
    ### Loading and editing JSON File for CFM Run
    with open(f"{repo_path}CFM_Lancaster/json_files/adjusted.json", "r") as read_file: 
        adjusted_json = json.load(read_file)

    adjusted_json['InputFileFolder'] = cfm_data_path
    adjusted_json['input_type'] = "csv"

    adjusted_json['InputFileNameTemp'] = f"{station}_tskin.csv"
    adjusted_json['InputFileNamebdot'] = f"{station}_snowfall.csv"
    adjusted_json['InputFileNamemelt'] = f"{station}_snowmelt.csv"
    adjusted_json['InputFileNameRain'] = f"{station}_rainfall.csv"
    adjusted_json['resultsFolder'] = f"{results_path}{station}"
    adjusted_json['resultsFileName'] = f'Results_{station}.hdf5'
    adjusted_json['spinFileName'] = f'Spin_{station}.hdf5'

    adjusted_json['physRho'] = 'KuipersMunneke2015'
    adjusted_json['TWriteStart'] = 1860.0 
    adjusted_json['outputs'] = ['depth','density','DIP','climate','compaction']
    adjusted_json['HbaseSpin'] = adjusted_json['H']-100
    adjusted_json['yearSpin'] =  10#0.1
    adjusted_json['NewSpin'] = True
    adjusted_json['stpsPerYear'] =  12
    adjusted_json['MELT'] =  True 
    adjusted_json['RAIN'] =  True 
    adjusted_json['liquid'] =  "bucket" 
    adjusted_json['merging'] =  True # If a model volume gets too thin, merge it with another. Needed for numerical stability with melt schemes.
    adjusted_json['merge_min'] =  1e-9 # If merging is true, the thickness threshold at which merging should occur.
    # adjusted_json['grid_outputs'] =  False
    adjusted_json['isoDiff'] =  False
    adjusted_json['iso'] =  'NoDiffusion'
    adjusted_json['GrGrowPhysics'] =  'Arthern'
    adjusted_json['physGrain'] =  True
    adjusted_json['SUBLIM'] =  False

    with open(f'{cfm_data_path}{station}.json', 'w') as json_file:
        json.dump(adjusted_json, json_file, indent=0)

    subprocess.call(["python",f"{cfm_main_path}main.py",f'{cfm_data_path}{station}.json'])
