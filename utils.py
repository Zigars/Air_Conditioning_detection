"""
对数据进行批量化的清洗、归一化、降采样处理
"""
import configparser
import os
import sys

import pandas as pd
import numpy as np
import scipy.signal as signal



def normalization(df, method="max_min_scaler"):
    """
    归一化处理
    """
    # df = list(df)
    # df = pd.DataFrame(df, columns=[data_type])
    # min_max标准化
    max_min_scaler = lambda x: (x - np.min(x)) / (np.max(x)-np.min(x))
    # Z-score标准化方法
    z_scaler = lambda x: (x - np.mean(x)) / (np.std(x, ddof=1))
    # 归一化
    df_norm = df.apply(max_min_scaler) if method == "max_min_scaler" else df.apply(z_scaler)
    return df_norm


def up_sample(df, data_type, source_sample=60, dest_sample=200):
    """
    降采样
    """
    # df = list(df[data_type])
    df = [float(data) for data in list(df)]
    # print(df)
    # l_result = int(len(df) * (dest_sample / source_sample))
    df_reshape = signal.resample_poly(df, dest_sample, source_sample)
    df_reshape = pd.DataFrame(df_reshape, columns=[data_type])
    # print(df_reshape)
    return df_reshape


def openpic():
    path1 = 'config.ini'
    cf = configparser.ConfigParser()
    cf.read(path1)  # 读取配置文件，如果写文件的绝对路径，就可以不用os模块
    ip = cf.get("IpConfig", "IP")  # 获取[Mysql-Database]中host对应的值
    port = cf.get("IpConfig", "Port")

    newPort = int(port)
    return ip, newPort

