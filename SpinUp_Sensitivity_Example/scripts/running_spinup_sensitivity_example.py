import glob
import numpy as np
import pandas as pd
import json
import subprocess

### Adjusting BDOT
for f in glob.glob('/home/jez/Community_Firn_Model_Forked/CFM_main/CFMinput_example/example*'):
    df = pd.read_csv(f).T
    # if 'SMELT' in f:
    #     df = df+0.5
    # if 'BDOT' in f:
    #     df = df+1.0
    new_filename = f.split('/')[-1].replace('example','adjusted')
    df.T.to_csv(f'/home/jez/Community_Firn_Model_Forked/SpinUp_Sensitivity_Example/CFMinput_example/{new_filename}',index=False, header=True)

### Extending SpinUP 
for f in glob.glob('/home/jez/Community_Firn_Model_Forked/CFM_main/CFMinput_example/example*'):
    df = pd.read_csv(f).T
    # if 'SMELT' in f:
    #     df = df+0.5
    # elif 'BDOT' in f:
    #     df = df+1.0
    df_spin = df[df.index.astype('float32') < 1980]
    # if 'SMELT' in f:
    #     df_spin = df_spin+2
    #     df = df+5
    # elif 'BDOT' in f:
    #     df_spin = df_spin+1
    #     df = df+1
    df_extended = pd.concat([df_spin,df])
    old_index = df_extended.index.astype('float32')
    step_size = old_index[1]-old_index[0]
    new_index = np.arange(0,len(old_index))*step_size + old_index.max() - len(old_index)*step_size
    df_extended = df_extended.set_index(new_index)
    new_filename = f.split('/')[-1].replace('example','extended')
    df_extended.T.to_csv(f'/home/jez/Community_Firn_Model_Forked/SpinUp_Sensitivity_Example/CFMinput_example/{new_filename}',index=False, header=True)

### Loading and editing JSON file for CFM run
with open('/home/jez/Community_Firn_Model_Forked/CFM_main/example.json', 'r') as read_file: 
    adjusted_json = json.load(read_file)
adjusted_json['InputFileFolder'] = '/home/jez/Community_Firn_Model_Forked/SpinUp_Sensitivity_Example/CFMinput_example/'
adjusted_json['resultsFolder'] = '/home/jez/Community_Firn_Model_Forked/SpinUp_Sensitivity_Example/results'
# adjusted_json['InputFileNameTemp'] = 'adjusted_TSKIN.csv'
# adjusted_json['InputFileNamebdot'] = 'adjusted_BDOT.csv'
# adjusted_json['InputFileNamemelt'] = 'adjusted_SMELT.csv'
# adjusted_json['InputFileNameRain'] = 'adjusted_RAIN.csv'
# adjusted_json['InputFileNameSublim'] = 'adjusted_SUBLIM.csv'

adjusted_json['InputFileNameTemp'] = 'extended_TSKIN.csv'
adjusted_json['InputFileNamebdot'] = 'extended_BDOT.csv'
adjusted_json['InputFileNamemelt'] = 'extended_SMELT.csv'
adjusted_json['InputFileNameRain'] = 'extended_RAIN.csv'
adjusted_json['InputFileNameSublim'] = 'extended_SUBLIM.csv'
# adjusted_json['MELT'] =  False
# adjusted_json['RAIN'] =  False
adjusted_json['SUBLIM'] =  False
adjusted_json['input_type'] = 'csv'
adjusted_json['TWriteStart'] = 980.0
adjusted_json['residual_strain'] = 0.0 
adjusted_json['doublegrid'] =  False
adjusted_json['grid_outputs'] =  False
with open('/home/jez/Community_Firn_Model_Forked/CFM_main/adjusted.json', 'w') as json_file:
    json.dump(adjusted_json, json_file, indent=0)

### Running CFM with edited JSON
subprocess.call(['python','/home/jez/Community_Firn_Model_Forked/CFM_main/main.py','/home/jez/Community_Firn_Model_Forked/CFM_main/adjusted.json','-n'])