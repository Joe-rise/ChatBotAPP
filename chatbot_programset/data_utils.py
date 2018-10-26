#-*- coding:utf-8 _*-  
""" 
@author:bluesli 
@file: data_utils.py 
@time: 2018/10/27 
"""
import random
import numpy as np
from tensorflow.python.client import device_lib
from word_sequence import WordSequence

def _get_available_gpus():
    # 获取数据的信息；
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos if x.device_type =='GPU']


if __name__ == '__main__':
    print(_get_available_gpus())
