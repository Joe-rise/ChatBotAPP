#-*- coding:utf-8 _*-  
""" 
@author:bluesli 
@file: word_sequence.py 
@time: 2018/10/15 
"""
import numpy as np


# 编码
class WordSequence(object):
    PAD_TAG = '<pad>'
    UNK_TAG = '<unk>'
    START_TAG = '<s>'
    END_TAG = '</s>'

    PAD = 0
    UNK = 1
    START = 2
    END = 3



    def __init__(self):
        self.dict ={
                WordSequence.PAD_TAG:WordSequence.PAD,
                WordSequence.UNK_TAG:WordSequence.UNK,
                WordSequence.START_TAG : WordSequence.START,
                WordSequence.END_TAG : WordSequence.END,
        }
        # 定义是否训练，刚开始是没有训练的；
        self.fited = False

        # 把字换成index
    def to_index(self,word):
        assert self.fited, 'WordSequence 尚未进行fit操作'
        if word in self.dict:
            return self.dict[word]
        return WordSequence.UNK

    # 把index（标签）换成字
    def to_word(self,index):
        assert self.fited, 'WordSequence 尚未进行fit操作'
        for k,v in self.dict.items():
            if v==index:
                return k
        return WordSequence.UNK_TAG

    # 返回字典的大小
    def size(self):
        assert self.fited,'wordSequence 尚未进行fit操作'
        return len(self.dict) +1

    # 返回当前字典的长度；
    def __len__(self):
        return self.size()

    # 数据处理的类中都有，fit是一个拟合的过程；
    def fit(self,sentences,min_count=5,max_count=None,max_features=None):
        assert not self.fited, 'WordSequence 只能fit一次'
        # 统计的counts
        count = {}
        # 把句子拿进来，进行简单的统计
        for sentence in sentences:
            arr = list(sentence)
            for a in arr:
                #如果a没有被统计为0
                if a not in count:
                    count[a] = 0
                if a in count:
                    count[a] +=1
            if min_count is not None:
                # 如果比最小的大我们需要机型统计；
                count = {k:v for k,v in count.items() if v>=min_count}
            if max_count is not None:
                # 如果比最大的小我们也要进行统计
                count = {k:v for k,v in count.items() if v<=max_count}


            self.dict = {
                WordSequence.PAD_TAG: WordSequence.PAD,
                WordSequence.UNK_TAG: WordSequence.UNK,
                WordSequence.START_TAG: WordSequence.START,
                WordSequence.END_TAG: WordSequence.END,
            }
            # 判断最大特征数是不是int类型；
            # 统计最大的特征数；
            if isinstance(max_features,int):
                # 把每一个item进行排序
                count = sorted(list(count.items()),key=lambda x:x[1])
                # 如果最大特征数不为None并且count大于最大特征数
                if max_features is not None and len(count)>max_features:
                    # 那么就取count中排序好的最大特征数的数据；
                    count = count[-int(max_features):]
                    # 通过for循环将长度放入字典中
                    for w, _ in count:
                        self.dict[w] = len(self.dict)

            else:
                # 通过key进行排序
                # 如果他不是int类型的，那么就直接将字典放入
                for w in sorted(count.keys()):
                    self.dict[w] = len(self.dict)
            self.fited = True


    # 将句子转换成向量
    def transform(self,sentence,max_len=None):
        assert self.fited, 'wordSequence 尚未进行fit操作'

        # 判断它是不是最大长度，如果是最大的长度则让他乘以最大的长度
        if max_len is not None:
            r = [self.PAD]*max_len
        else:
            # 如果他不是最大的长度就乘以句子的长度；
            r = [self.PAD] * len(sentence)
        for index ,a in enumerate(sentence):
            if max_len is not None and index >=len(r):
                break
            r[index] = self.to_index(a)
        return np.array(r)

    # 将向量转化成句子；
    def inverse_transform(self,indices,ignore_pad=False,ignore_unk=False,ignore_start=False,ignore_end=False):
        ret = []
        for i in indices:
            word = self.to_word(i)
            if word ==WordSequence.PAD_TAG and ignore_pad:
                continue
            if word == WordSequence.UNK_TAG and ignore_unk:
                continue
            if word == WordSequence.START_TAG and ignore_start:
                continue
            if word == WordSequence.END_TAG and ignore_end:
                continue
            ret.append(word)
        return ret

def test():
    ws = WordSequence()
    ws.fit([
        ['你','好','啊'],
        ['你', '好', '噢'],

    ])

    indice = ws.transform(['我','们','你','你'])
    print(indice)
    back = ws.inverse_transform(indice)
    print(back)

if __name__ == '__main__':
    test()







