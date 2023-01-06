import json
import subprocess

### Loading and editing JSON file for CFM run
with open('/CommunityFirnModel/CFM_main/example.json', 'r') as read_file: 
    adjusted_json = json.load(read_file)

adjusted_json['InputFileFolder'] = '/home/jez/Community_Firn_Model_Forked/CommunityFirnModel/CFM_main/CFMinput_example'
adjusted_json['input_type'] = 'csv'
adjusted_json['InputFileNamemelt'] = 'adjusted_SMELT.csv'
adjusted_json['SUBLIM'] =  False

with open('/CommunityFirnModel/CFM_main/adjusted.json', 'w') as json_file:
    json.dump(adjusted_json, json_file, indent=0)

### Running CFM with edited JSON
subprocess.call(['python','/CommunityFirnModel/CFM_main/main.py','/CommunityFirnModel/CFM_main/adjusted.json','-n'])


import pandas as pd
df = pd.read_csv('/CommunityFirnModel/CFM_main/CFMinput_example/example_SMELT.csv')
df.T[0][:] = 1.0
df.to_csv('/CommunityFirnModel/CFM_main/CFMinput_example/adjusted_SMELT.csv',index=False, header=True)



import glob
import pandas as pd
import numpy as np

for f in glob.glob('/CommunityFirnModel/CFM_main/CFMinput_example/example_*.csv'):
    df = pd.read_csv(f)
    df = df[np.argwhere(df.index.values.astype('float64')>1900).min():]
    if 'SMELT' in f:
        df.T[0][:] = 2.0
    file_end = f.split('example_')[-1]
    print(file_end)
    df.to_csv(f'/home/jez/Community_Firn_Model_Forked/CommunityFirnModel/CFM_main/CFMinput_example/adjusted_{file_end}',index=False, header=True)