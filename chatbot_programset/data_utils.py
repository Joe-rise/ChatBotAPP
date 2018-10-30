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

# 设置一个全局的数据量阈值：
VOCAB_SIZE_THRESHOLD_CPU = 50000

def _get_available_gpus():
    # 获取数据的信息；
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos if x.device_type =='GPU']


#对于输入的数据是需要占据内存的，如果全部使用gpu处理会占用过多的显存,可能现存吃不下；
#所以需要对数据设置一个阈值，如果大于某一个阈值就使用CPU；
# 跟训练时的情况相反；
def _get_embed_device(vocab_size):
    gpus = _get_available_gpus()
    if not gpus and vocab_size> VOCAB_SIZE_THRESHOLD_CPU:
        return "/cpu:0"
    return "/gup:0"


# 转换一下句子
# 一个句子经过ws转换，转化成数组；
def transform_sentence(sentence,ws,max_len=None,add_end=False):
    encoded = ws.transform(
        sentence,
        max_len=max_len if max_len is not None else len(sentence))
    encoded_len = len(sentence) +(1 if add_ else 0)

if __name__ == '__main__':
    print(_get_available_gpus())
    size =30000
    print(_get_embed_device(size))
