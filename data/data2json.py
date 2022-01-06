"""
对数据进行批量化的清洗、归一化、降采样处理
"""

import csv
import os

import json,os,re

import pandas as pd
import numpy as np
import scipy.signal as signal



def find_All_file(file_path, file_list):
    """
    获取文件列表
    """
    filelist = os.listdir(file_path)
    for filename in filelist:
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            # print(filepath)
            find_All_file(filepath, file_list)
        else:
            file_list.append(filepath)
    return file_list


def csv2json(i, name):
    new_path = 'json_data/'
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    new_name = name.split('/')[-1].split('.')[0] + ".txt"
    csv_File = open(name, 'r')  # 打开csv文件
    with open(new_path + new_name, 'a+') as f:
        dict_reader = csv.DictReader(csv_File)
        print(dict_reader.fieldnames)
        out_dic = {"air_data": [row for row in dict_reader]}

        out = json.dumps(out_dic, ensure_ascii=False, skipkeys=False)
        f.write(out)



if __name__ == '__main__':
    # 读取文件名列表
    path = 'csv_data/'
    csv_list = []
    csv_list = find_All_file(path, csv_list)
    # print(csv_list)
    # 标签和序列
    labels = []
    air_serial = []
    # g = 0

    for i, name in enumerate(csv_list):
        print(i, name)
        # fix_name(i, name)
        csv_File = open(name, 'r', encoding='GBK')  # 打开csv文件
        csv2json(i, name)