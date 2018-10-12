#-*- coding:utf-8 _*-  
""" 
@author:bluesli 
@file: naive_bayes.py
@time: 2018/10/13 
"""

import os
import jieba
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
import time

# 分词，切词
def preprocess(path):
    text_with_space = ""
    textfile = open(path,'r',encoding="utf8").read()
    textcut = jieba.cut(textfile)
    for word in textcut:
        text_with_space += word +" "
    return text_with_space


# 分类类标号
# 返回处理好的数据集和标签
def loadtrainset(path,classtag):
    # 通过系统拿所有的目录
    allfiles = os.listdir(path)
    processed_textset = []
    allclasstags = []
    for thisfile in allfiles:
        print(thisfile)
        # 把文件目录弄完整；
        path_name = path +"/"+thisfile
        processed_textset.append(preprocess(path))
        allclasstags.append(classtag)
        return processed_textset,allclasstags


process_textdata1,class1 = loadtrainset("path")
process_textdata2,class2 = loadtrainset("path2")

# 数据整合：
train_data = process_textdata1 +process_textdata2
classtags_list = class1+class2

# 转化词为词向量或者是矩阵
count_vector  = CountVectorizer()
vecot_matix = count_vector.fit_transform(train_data)


# 特征工程 TFIDF ：文本主题模型；特征提取方式；
# 这里相当于提取特征
train_tfidf = TfidfTransformer(use_idf=False).fit_transform(vecot_matix)

# 利用多分类的贝叶斯进行训练
clf = MultinomialNB().fit(train_tfidf,classtags_list)

# 判断真确率
test_set = []
path = "path _save"
allfiles = os.listdir(path)
hotel = 0
travel = 0
# 把文件读进去
for thisfile in allfiles:
    # 这里用transform就行了，fit用一次就行了，
    # fit相当于喂数据，transform相当于转换；
    # 提取的时候不需要，
    # 但是提取特征工程的时候需要；
    path_name = path + "/" +thisfile
    new_cout_vector = count_vector.transform([preprocess(path_name)])
    new_tfidf = TfidfTransformer(use_idf=False).fit_transform(new_cout_vector)

    predict_result = clf.predict(new_tfidf)
    print(predict_result)
    if(predict_result == "宾馆"):
        hotel += 1
    if (predict_result == "旅游"):
        travel+=1
print("宾馆" , str(hotel))
print("travel",travel)


# 如果发生编码错误，可能是文件格式错误的原因，
# 可以用notepad重新编码一下文本格式


# 这里的真确率低是数据量太低了；
# 可以扩展是为多分类的，同样的方式；
# 训练集足够的大，训练的结果正确率才高；