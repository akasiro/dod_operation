# -*- coding: utf-8 -*
import os,sys
import pandas as pd
import numpy as np

sys.path.append('/home/hadoop/jupyter/sdl/code_ping/dod_td4')
from read_data import read_data

# Default value
game_type_code = ['T200100', 'T200200', 'T200300', 'T200400', 'T200500', 'T200600', 'T200700', 'T200800', 'T200900', 'T200999', 'T201000', 'T201100', 'T201200', 'T201300', 'T201400', 'T201500', 'T201600', 'T201700', 'T201800', 'T201900', 'T202000', 'T202100']
# clean data
def clean_data(df):
    # 提取需要的行列
    df = df[['tdid','type_code','appHash']]
    # 删掉空白的数据
    df = df.dropna(how = 'any')
    # 保留游戏
    df = df[df['type_code'].str.contains(r'T2\d*')]
    # 删除掉重复的条目
    df = df.drop_duplicates()
    return df

# 计算安装总数和安装的类别总数会用到的函数
# 1.计算安装游戏总数
def add_game_num(df):
    temp = 0
    for i in game_type_code:
        temp = temp + df[i]
    return temp
# 2.计算安装类型总数
def count_type_num(df):
    count = 0
    for i in game_type_code:
        if df[i]:
            count +=1
    return count

# 计算每个用户每个种类的安装数
def tdid_type_num(df):
    '''
    :param df: 经过clean_data 处理过的函数
    :return df_game: 每个用户在安装每个类型的游戏的个数
    '''
    # group计算每个用户安装每种类型游戏多少个
    dfg = df.groupby([df['tdid'],df['type_code']])
    df_count = dfg.count().reset_index()
    # 转化表格为行标题为每种类型，列标题为每个用户
    df_game = pd.DataFrame(columns = ['tdid'])
    for t in game_type_code:
        # 提取所寻找的类型
        temp = df_count[df_count['type_code'] == t][['tdid','appHash']]
        temp.rename(columns = {'appHash':t}, inplace = True)
        df_game = df_game.merge(temp,on = 'tdid', how = 'outer')
    df_game = df_game.fillna(0)
    return df_game


# 计算每个类别的需求特征
def tdid_type_demand_gv(df,date):
    '''
    :param df: 经过clean_data处理过的函数
    :param date: init
    '''
    # 寻找tdid与type的对应关系
    df_index = df[['type_code','tdid']].drop_duplicates()
    # 计算每个用户的需求
    df_game = tdid_type_num(df)
    # merge
    df = df_index.merge(df_game, on='tdid')
    # 循环计算每个类别需求特征
    temp_dict = {'type_code':[],
                'gv_type':[]}
    for type_code in game_type_code:
        temp_dict['type_code'].append(type_code)
        tmp_df_type = df[df['type_code'] == type_code][game_type_code]
        temp_dict['gv_type'].append(np.linalg.det(tmp_df_type.cov()))
    df_gv = pd.DataFrame(temp_dict)
    df_gv['date'] = date
    return df_gv

def tdid_demand_action(df):
    '''
    :param df: 经过clean_data处理过的函数
    :return df_game2 每个用户安装游戏的个数和类型的个数
    '''
    tmp_group = df.groupby(df['tdid'])
    df_game2 = tmp_group[['type_code','appHash']].agg('nunique').reset_index()
    df_game2.rename(columns = {'type_code':'type_num', 'appHash':'game_num'},inplace = True)
    return df_game2

def tdid_action_demand_gv(df,date):
    '''
    :param df: 经过clean_data处理过的函数
    :param date: init
    
    return df_gv2 根据用户安装类型个数和游戏个数计算得出的gv
    '''
    # match tdid and type
    df_index = df[['type_code','tdid']].drop_duplicates()
    # cal demand
    df_game2 = tdid_demand_action(df)
    # merge
    df = df_index.merge(df_game2, on='tdid')
    # loop type_code: cal gv
    temp_dict = {'type_code':[],
                'gv_action':[]}
    for type_code in game_type_code:
        temp_dict['type_code'].append(type_code)
        tmp_df_action = df[df['type_code'] == type_code][['type_num', 'game_num']]
        temp_dict['gv_action'].append(np.linalg.det(tmp_df_action.cov()))
    df_gv2 = pd.DataFrame(temp_dict)
    df_gv2['date'] = date
    return df_gv2

def main(month=20170131):
    '''
    for calculating from game_num of each type
    '''
    rd = read_data()
    file_name_dict = rd.get_file_name_dict()
    data_save_path = '/home/hadoop/jupyter/sdl/data_ping/dod_td4/demand_gv/permonth_catagory'
    #loop part
    i = file_name_dict[month]
    df = rd.read_merge_df(l_header=i['l_header'], l_noheader=i['l_noheader'])
    df = clean_data(df)
    date = month
    df_gv = tdid_type_demand_gv(df,date)
    #data save
    if not os.path.exists(os.path.join(data_save_path,'category_demand_gv{}.csv'.format(date))):
        df_gv.to_csv(os.path.join(data_save_path,'category_demand_gv{}.csv'.format(date)),index = False)
        print('category_demand_gv{}.csv created'.format(date))
    else:
        print('category_demand_gv{}.csv has existed'.format(date))
    return df_gv

def main2(month=20170131):
    '''
    for calculating from action(type_num and game_num)
    '''
    rd = read_data()
    file_name_dict = rd.get_file_name_dict()
    data_save_path = '/home/hadoop/jupyter/sdl/data_ping/dod_td4/demand_gv/permonth_catagory'
    #loop part
    i = file_name_dict[month]
    df = rd.read_merge_df(l_header=i['l_header'], l_noheader=i['l_noheader'])
    date = month
    df = clean_data(df)
    df_gv2 = tdid_action_demand_gv(df,date)
    #data save
    if not os.path.exists(os.path.join(data_save_path,'category_demand_action_gv{}.csv'.format(date))):
        df_gv2.to_csv(os.path.join(data_save_path,'category_demand_action_gv{}.csv'.format(date)),index = False)
        print('category_demand_action_gv{}.csv created'.format(date))
    else:
        print('category_demand_action_gv{}.csv has existed'.format(date))
    return df_gv2

def operate_Jan():
    '''
    for operating data of Jan because menory can't bear the data size
    '''
    jan_data_path = '/home/hadoop/jupyter/sdl/code_ping/origin_game201701.csv'
    if not os.path.exists(jan_data_path):
        rd = read_data()
        file_name_dict = rd.get_file_name_dict()
        data_save_path = '/home/hadoop/jupyter/sdl/data_ping/dod_td4/demand_gv/permonth_catagory'
        i = file_name_dict[20170131]
        jan_data_part1_path = '/home/hadoop/jupyter/sdl/code_ping/origin_game201701part1.csv'
        jan_data_part2_path = '/home/hadoop/jupyter/sdl/code_ping/origin_game201701part2.csv'
        if os.path.exists(jan_data_part1_path) and os.path.exists(jan_data_part2_path):
            df1 = pd.read_csv(jan_data_part1_path)
            df2 = pd.read_csv(jan_data_part2_path)
            df = df1.append(df2,ignore_index=True)
            df = clean_data(df)
            df.to_csv(jan_data_path, index = False)
            print('{} created'.format(jan_data_path))
        if not os.path.exists(jan_data_part1_path):
            df = rd.read_merge_df(l_header=i['l_header'], l_noheader=[])
            df = clean_data(df)
            df.to_csv(jan_data_part1_path,index = False)
            print('{} created'.format(jan_data_part1_path))
        else:
            print('{} exists'.format(jan_data_part1_path))
        if not os.path.exists(jan_data_part2_path):
            df = rd.read_merge_df(l_header=[], l_noheader=i['l_noheader'])
            df = clean_data(df)
            df.to_csv(jan_data_part2_path, index = False)
            print('{} created'.format(jan_data_part2_path))
        else:
            print('{} exists'.format(jan_data_part2_path))  
    else:
        print('{} already exists'.format(jan_data_path))
def main2_Jan():
    jan_data_path = '/home/hadoop/jupyter/sdl/code_ping/origin_game201701.csv'
    data_save_path = '/home/hadoop/jupyter/sdl/data_ping/dod_td4/demand_gv/permonth_catagory'
    df = pd.read_csv(jan_data_path)
    date = 20170131
    df_gv2 = tdid_action_demand_gv(df,date)
    #data save
    if not os.path.exists(os.path.join(data_save_path,'category_demand_action_gv{}.csv'.format(date))):
        df_gv2.to_csv(os.path.join(data_save_path,'category_demand_action_gv{}.csv'.format(date)),index = False)
        print('category_demand_action_gv{}.csv created'.format(date))
    else:
        print('category_demand_action_gv{}.csv has existed'.format(date))
    return df_gv2
