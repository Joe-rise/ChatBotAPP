#-*- coding:utf-8 _*-  
""" 
@author:bluesli 
@file: extract_conv.py 
@time: 2018/10/15 
"""
import re
import sys
import pickle
from tqdm import tqdm


# 数据的简单处理
#将一些特殊符号的去除
#
def make_split(line):
    # # 如果发现了。？就去掉，然后通过，隔开；
    # if re.match(r'.*([，...?!\.,!？])$',''.join(line)):
    #     return []
    return line

# 判断是否是一个好句子；
# 判断英文字符，是否都大于2个，如果大于就返回False
def good_line(line):
    if len(re.findall(r'[a-zA-Z0-9]',''.join(line))) >2:
        return False
    return True


# 简单的处理
# 然后做一下替换；
def regular(sen):
    # sen = re.sub(r'\.{3,100}','...',sen)
    # sen = re.sub(r'...{2,100}','...',sen)
    # sen = re.sub(r'[,]{1,100}','，',sen)
    # sen = re.sub(r'[\.]{1,100}','。',sen)
    # sen = re.sub(r'[\?]{1,100}','？',sen)
    # sen = re.sub(r'[!]{1,100}', '！', sen)
    return sen

def my_main(limit=20,x_limit=3,y_limit=6):
    # 句子的编码
    from word_sequence import WordSequence
    print('extract lines')
    with open('dgk_shooter_min.conv','r',encoding='utf-8',errors='ignore') as fp:
        groups = []
        group = []

        for line in tqdm(fp):
            # print(line)
            if line.startswith('M '):
                # 去掉回车
                line = line.replace('\n','')
                if '/' in line:
                    line = line[2:].split('/')
                else:
                    line = list(line[2:])
                # 可能倒数是一个回车，所以不要；
                line = line[:-1]
                # 这是简单的一些正则化处理
                group.append(list(regular(''.join(line))))
            else:
                if group:
                    groups.append((group))
                    # 每一次叠加玩，都要清空；重复使用group
                    group = []
        if group:
            groups.append((group))
            group = []
        # 上面是把每一行读进来放入groups中；
        # 然后是对groups操作；
        print('extract group')
        print(groups[1:2])
        x_data = []
        y_data = []

        # 进度条的形式展示；
        for group in tqdm(groups):
            # 进行枚举
            # print(group[1:2])
            # 一个小的grup是一个完整的对话；groups整个对话的数据；
            # 这里是拿到的是三行数据；

            # 这里是做问答对的处理
            for i,line in enumerate(group):
                #
                last_line = None
                if i>0:
                    last_line = group[i-1]
                    if not good_line(last_line):
                        last_line =None
                next_line =None
                if i <len(group)-1:
                    next_line = group[i+1]
                    if not good_line(next_line):
                        next_line =None
                next_next_line = None
                if i<len(group)-2:
                    next_next_line = group[i+2]
                    if not good_line(next_next_line):
                        next_next_line=None

                if next_line:
                    x_data.append(line)
                    y_data.append(next_line)
                if last_line and next_line:
                    x_data.append(last_line+make_split(last_line) +line)
                    y_data.append(next_line)
                if next_line and next_next_line:
                    x_data.append(line)
                    y_data.append(next_line+make_split(next_line)+next_next_line)
    print(len(x_data),len(y_data))

    # 取出问和答的数据：
    # 只取前20个字符进行输出；
    for ask ,answer in zip(x_data[:20],y_data[:20]):
        print(''.join(ask))
        print(''.join(answer))
        print('-'*20)
    data = list(zip(x_data,y_data))

    data = [
        (x,y)
        for x,y in data
        if len(x)<limit and len(y)<limit and len(y)>=y_limit and len(x)>=x_limit
    ]
    x_data,y_data = zip(*data)

    print('fit word_sequence')

    ws_input = WordSequence()
    ws_input.fit(x_data +y_data)
    print('dump')
    pickle.dump(
        (x_data,y_data),
        open('chatbot.pkl','wb')
    )
    pickle.dump(ws_input,open('ws.pkl','wb'))
    print('Done')




if __name__ == '__main__':
    my_main()
    # x_str = '你好我是ricky?...'
    # new_X = make_split(x_str)
    # print(new_X)