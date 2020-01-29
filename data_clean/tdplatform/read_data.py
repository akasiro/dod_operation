# -*- coding: utf-8 -*
import pandas as pd
import numpy as np
import pickle

# Default
DATA_PATH = '/home/hadoop/sdl/hdfs_data/61/' #default datapath on the platform
FILE_NAME_PATH = '/home/hadoop/jupyter/sdl/code_ping/dod_td4/dod_td_data_file_name_listV1_derived.pkl' #default path of the data filename dict

class read_data():
    def __init__(self, datapath=DATA_PATH):
        '''
        this class is used for read origin data on the TalkingData platform and merge the daily day of the same month to a dataframe from a data filename dict.
        '''
        self.datapath = datapath

    
    def readonecsv(self, filename):
        '''
        Read data file that dosen't not contain header
        '''
        df = pd.read_csv('{}{}'.format(self.datapath,filename), header = None)
        df.columns = ['tdid','pkgName','is_active','type','type_code','frequecncy','appHash']
        return df

    def read_merge_df(self, l_header,l_noheader):
        '''
        read all data of the same month and merge them to a dataframe
        :param l_header: a list of data that contains headers
        :param l_noheader: a list of data that doesn't contain headers
        :return: a dataframe
        '''
        df1 = pd.DataFrame()
        df2 = pd.DataFrame()
        if len(l_header):
            for i in l_header:
                temp1 = pd.read_csv('{}{}'.format(self.datapath,i))
                df1 = df1.append(temp1,ignore_index=True)
        if len(l_noheader):
            for j in l_noheader:
                temp2 = self.readonecsv(j)
                df2 = df2.append(temp2,ignore_index=True)
        df = df1.append(df2,ignore_index=True)
        print('data has been read')
        return df

    def get_file_name_dict(self,file_name_dict_path = FILE_NAME_PATH):
        '''
        use pickle package to read file name dict
        :file_name_dict_path: the path of the pickle file
        :return: a dict structure {month: {'l_header':[], 'l_noheader':[]}}
        '''
        with open(file_name_dict_path,'rb') as f:
            file_name_dict = pickle.load(f)
        return file_name_dict

if __name__ == '__main__':
    rd = read_data()
    for month,filename_list in rd.get_file_name_dict().items():
        df = rd.read_merge_df(filename_list['l_header'], filename_list['l_noheader'])
        date = month
        print(date)
        break