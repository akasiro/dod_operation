import os,pickle
import pandas as pd

def read_file_name(file_path='dod_td_data_file_name_20200122_origin.xlsx'):
    df = pd.read_excel(file_path)
    return df

def gen_file_name_dict(df):
    df = df[df['missing']==0]
    file_name_dict = {}
    for month in df['month'].drop_duplicates().values.tolist():
        tmp_df = df[df['month']==month]
        l_header = tmp_df[tmp_df['header']==1]['file_name'].values.tolist()
        l_noheader = tmp_df[tmp_df['header']==0]['file_name'].values.tolist()
        file_name_dict[month] = {'l_header':l_header, 'l_noheader':l_noheader}
    return file_name_dict

def save_dict_to_pickle(file_name_dict, file_name='dod_td_data_file_name_listV1_derived.pkl'):
    if not os.path.exists(file_name):
        with open(file_name,'ab') as f:
            pickle.dump(file_name_dict,f)
        print('file save: {}'.format(os.path.abspath(file_name)))
    else:
        print('file name duplicate')

if __name__ == '__main__':
    df = read_file_name()
    file_name_dict = gen_file_name_dict(df)
    save_dict_to_pickle(file_name_dict)
