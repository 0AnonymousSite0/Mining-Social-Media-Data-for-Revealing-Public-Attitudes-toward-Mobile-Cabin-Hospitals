# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/6/3 10:51
# @author   :Mo
# @function :train of fast text with baidu-qa-2019 in question title

# 适配linux
import pathlib
import sys
import os
project_path = str(pathlib.Path(os.path.abspath(__file__)).parent.parent.parent)
sys.path.append(project_path)
# 地址
from keras_textclassification.conf.path_config import path_model, path_fineture, path_model_dir, path_hyper_parameters
# 训练验证数据地址
from keras_textclassification.conf.path_config import path_byte_multi_news_valid, path_byte_multi_news_train, path_byte_multi_news_test, path_byte_multi_news_label
# 数据预处理, 删除文件目录下文件
from keras_textclassification.data_preprocess.text_preprocess import PreprocessTextMulti, preprocess_label_ques, load_json
# 模型图
from keras_textclassification.m04_TextRNN.graph import TextRNNGraph as Graph
# 模型评估
from sklearn.metrics import classification_report
# 计算时间
import time

import numpy as np


def pred_tet(path_hyper_parameter=path_hyper_parameters, path_test=None, rate=1.0):
    # 测试集的准确率
    hyper_parameters = load_json(path_hyper_parameter)
    if path_test: # 从外部引入测试数据地址
        hyper_parameters['data']['val_data'] = path_test
    time_start = time.time()
    # graph初始化
    graph = Graph(hyper_parameters)
    print("graph init ok!")
    graph.load_model()
    print("graph load ok!")
    ra_ed = graph.word_embedding
    # 数据预处理
    pt = PreprocessTextMulti(path_model_dir)

    ques = list()
    label_ori = list()
    label_pre = list()
    labels = list()
    with open(path_test, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[1:]:
            lqs = line.split('|,|')
            ques.append(lqs[1])
            label_ori.append(lqs[0].split(','))
    print(label_ori)
    for que in ques:
        que_embed = ra_ed.sentence2idx(que)
        if hyper_parameters['embedding_type'] in ['bert', 'albert']:
            x_val_1 = np.array([que_embed[0]])
            x_val_2 = np.array([que_embed[1]])
            x_val = [x_val_1, x_val_2]
        else:
            x_val = que_embed
        pred = graph.predict(x_val)
        pre = pt.prereocess_idx(pred[0])
        ls_multi = []
        if pre[0][0][1] >= 0.38:
            for ls in pre[0]:
                if ls[1] >= 0.38:
                    ls_multi.append(ls[0])
        elif pre[0][0][1] >= 0.15:
            ls_multi.append(pre[0][0][1])
        else:
            ls_multi.append('12')
        label_pre.append(ls_multi)
    print(label_pre)
    with open(path_byte_multi_news_label, 'r', encoding='utf-8') as ff:
        lines = ff.readlines()
        for line in lines:
            labels.append(line.split('\n')[0])
    print(labels)

    tes_acc = []
    count = 0
    for label in labels:
        num = 0
        sum = 0
        tp = 0
        for j in range(len(label_ori)):
            if label in label_ori[j]:
                num += 1
                count += 1
            if label in label_pre[j]:
                sum += 1
            if (label in label_ori[j]) and (label in label_pre[j]):
                tp += 1
        if num == 0 and sum == 0:
            prec = 1.000000000
            reca = 1.000000000
            fsco = 1.000000000
        elif num == 0 and sum != 0:
            prec = 0.000000000
            reca = 0.000000000
            fsco = 0.000000000
        elif num != 0 and sum == 0:
            prec = 0.000000000
            reca = 0.000000000
            fsco = 0.000000000
        elif num != 0 and sum != 0 and tp == 0:
            prec = 0.000000000
            reca = 0.000000000
            fsco = 0.000000000
        else:
            prec = float('%.9f'%(tp/sum))
            reca = float('%.9f'%(tp/num))
            fsco = float('%.9f'%((2*prec*reca)/(prec+reca)))
        row = [label, prec, reca, fsco, num]
        tes_acc.append(row)
    prec_te = 0.000000000
    reca_te = 0.000000000
    fsco_te = 0.000000000
    for x in tes_acc:
        prec_te = prec_te + (x[1])*x[4]
        reca_te = reca_te + (x[2])*x[4]
        fsco_te = fsco_te + (x[3])*x[4]
    prec_tes = float('%.9f'%(prec_te/count))
    reca_tes = float('%.9f'%(reca_te/count))
    fsco_tes = float('%.9f'%(fsco_te/count))
    row = ['avg', prec_tes, reca_tes, fsco_tes, count]
    tes_acc.append(row)
    for i in tes_acc:
        print(i)


def pred_input(path_hyper_parameter=path_hyper_parameters):
    # 输入预测
    # 加载超参数
    hyper_parameters = load_json(path_hyper_parameter)
    pt = PreprocessTextMulti(path_model_dir)
    # 模式初始化和加载
    graph = Graph(hyper_parameters)
    graph.load_model()
    ra_ed = graph.word_embedding
    ques = '我要打王者荣耀'
    # str to token
    ques_embed = ra_ed.sentence2idx(ques)
    if hyper_parameters['embedding_type'] in ['bert', 'albert']:
        x_val_1 = np.array([ques_embed[0]])
        x_val_2 = np.array([ques_embed[1]])
        x_val = [x_val_1, x_val_2]
    else:
        x_val = ques_embed
    # 预测
    pred = graph.predict(x_val)
    print(pred)
    # 取id to label and pred
    pre = pt.prereocess_idx(pred[0])
    ls_nulti = []
    for ls in pre[0]:
        if ls[1] >= 0.2:
            ls_nulti.append(ls[0])
    print(pre[0])
    print(ls_nulti)
    while True:
        print("请输入: ")
        ques = input()
        ques_embed = ra_ed.sentence2idx(ques)
        print(ques_embed)
        if hyper_parameters['embedding_type'] in ['bert', 'albert']:
            x_val_1 = np.array([ques_embed[0]])
            x_val_2 = np.array([ques_embed[1]])
            x_val = [x_val_1, x_val_2]
        else:
            x_val = ques_embed
        pred = graph.predict(x_val)
        pre = pt.prereocess_idx(pred[0])
        ls_nulti = []
        for ls in pre[0]:
            if ls[1] >= 0.4:
                ls_nulti.append(ls[0])
        print(pre[0])
        print(ls_nulti)


if __name__=="__main__":
    # 测试集预测
    pred_tet(path_test=path_byte_multi_news_test, rate=1) # sample条件下设为1,否则训练语料可能会很少

    # 可输入 input 预测
    pred_input()

# rate=0.01,random,char下训练一轮预测结果
# 2019-07              precision    recall  f1-score   support
#
#           游戏  0.786407767 0.880434783 0.830769231        92
#           生活  0.471428571 0.673469388 0.554621849        49
#           社会  0.363636364 0.333333333 0.347826087        12
#           文化  0.000000000 0.000000000 0.000000000         7
#           健康  0.775862069 0.737704918 0.756302521        61
#           体育  0.000000000 0.000000000 0.000000000         5
#           娱乐  0.549019608 0.700000000 0.615384615        40
#           商业  0.863636364 0.542857143 0.666666667        35
#           烦恼  0.722222222 0.650000000 0.684210526        20
#           汽车  0.000000000 0.000000000 0.000000000         5
#           电脑  0.722222222 0.764705882 0.742857143        51
#           教育  0.650000000 0.672413793 0.661016949        58
#           育儿  0.000000000 0.000000000 0.000000000         5
#           电子  0.000000000 0.000000000 0.000000000         8
#
#     accuracy                      0.671875000       448
#    macro avg  0.421745370 0.425351374 0.418546828       448
# weighted avg  0.643541455 0.671875000 0.651279537       448
