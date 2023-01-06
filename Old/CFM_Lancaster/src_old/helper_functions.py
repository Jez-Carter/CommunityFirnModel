import glob
import pandas as pd

def load_all_input_dataframes(path):
    df_all = None
    for f in glob.glob(path):
        df = pd.read_csv(f).T.reset_index()
        df.rename(columns = {"index":"time",0:f"{f.split('/')[-1]}"}, inplace = True)
        if df_all is None:
            df_all=df
        else:
            df_all = pd.merge(df_all,df,on='time')
    return(df_all)