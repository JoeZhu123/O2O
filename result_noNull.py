# -*- coding:utf-8 -*-

import urllib2
import re
import os
import sys
import csv
from numpy import *
# import numpy as np
import model
from data import *
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from NaiveBayes import BayesClassifier

def testBayes():
	features=[]            #数据集特征集
	labels=[]                #数据集类标集

	features_t=[]
	maxProbability_t=[]
	tables_result=[]
	Merchant_ids_t=[]

	Merchant_ids_test={}		#商家ID字典,test
	Merchant_ids_train={}		#商家ID字典,train
	testData=[]
	trainData=[]

	#测试数据集读取
	test_data = open('./test_data/data_revised.csv')
	for line in test_data.readlines():
	    lineArr = line.strip().split(',')
	    Merchant_ids_t.append(int(lineArr[1]))
	    features_t.append([float(lineArr[3]), int(lineArr[4])])
	    table4=Table4(lineArr[0],lineArr[2],lineArr[5],'0')
	    tables_result.append(table4)
	    Merchant_ids_test[lineArr[2]]=testData.append([float(lineArr[3]), int(lineArr[4])])
	#训练数据集读取
	all_data = open('./train_data/Date_all.csv')
	for line in all_data.readlines():
	    lineArr = line.strip().split(',')
	    features.append([float(lineArr[3]), int(lineArr[4])])
	    labels.append(int(lineArr[7]))
	    Merchant_ids_train[lineArr[2]]=trainData.append([float(lineArr[3]),int(lineArr[4]),int(lineArr[7])])

	# print Merchant_ids_train.keys()
	# print Merchant_ids_test.keys()
	features_key=[]            #数据集特征集
	labels_key=[]                #数据集类标集
	num_not_in=0
	for i in range(0,len(features_t)):
			key=Merchant_ids_t[i]
			key_dir_name='./train_data/merchant_train_data/'+str(key)+'_noNull'+'.csv'
			features_key=[]
			labels_key=[]
			if os.path.exists(key_dir_name)==True:
				key_data = open(key_dir_name)
				for line in key_data.readlines():
				    lineArr = line.strip().split(',')
				    features_key.append([float(lineArr[3]), int(lineArr[4])])
				    labels_key.append(int(lineArr[7]))
				print len(features_key)
				print len(labels_key)

				if len(features_key)>1:
					Bay=BayesClassifier()
					Bay.train(features_key,labels_key)

				
					label,maxProbability=Bay.classify(features_t[i])
					print("maxProbability:"+str(maxProbability)+"==>"+"Classified:"+label)
					tables_result[i].giveProbability(str(maxProbability))
					items=[tables_result[i].User_id,tables_result[i].Coupon_id,tables_result[i].Date_received,tables_result[i].Probability]
					dir_name='./result/table4_4'
					savecsv(dir_name,items)
			else:
				num_not_in=num_not_in+1	
	print num_not_in


	# for line in file:         #一行行读数据文件
	# 	line=line.strip()
	# 	tempVec=line.split(',')
	# 	labels.append(tempVec[len(tempVec)-1])
	# 	tempVec2=[tempVec[i] for i in range(0,len(tempVec)-1)]
	# 	features.append(tempVec2)


	# print len(features)
	# print len(labels)
	# features_n = features[0:940000]
	# labels_n = labels[0:940000]

	# Bay=BayesClassifier()
	# Bay.train(features_n,labels_n)
	# # correct=0
	# # for i in range(0,len(features_t)):
	# # 	label=Bay.classify(features_t[i])
	# # 	print("Original:"+str(labels_t[i])+"==>"+"Classified:"+label)
	# # 	if str(label)==str(labels_t[i]):
	# # 		correct+=1
	# # print correct
	# # print len(features_t)
	# # Accuracy=correct/len(features_t)
	# # print "Accuracy:",Accuracy    #正确率
	# for i in range(0,len(features_t)):
	# 	label,maxProbability=Bay.classify(features_t[i])
	# 	print("maxProbability:"+str(maxProbability)+"==>"+"Classified:"+label)
	# 	tables_result[i].giveProbability(str(maxProbability))
	# 	items=[tables_result[i].User_id,tables_result[i].Coupon_id,tables_result[i].Date_received,tables_result[i].Probability]
	# 	dir_name='./result/table4_2'
	# 	savecsv(dir_name,items)



def testSVM():
	## step 1: load data
	print "step 1: load data..."
	dataSet = []
	labels = []
	# label_1 = open('./train_data/Date_label_1.csv')
	# label_0 = open('./train_data/Date_label_0.csv')
	# null_label_0 = open('./train_data/Date_null_label_0.csv')
	# for line in label_1.readlines():
	#     lineArr = line.strip().split(',')
	#     dataSet.append([float(lineArr[3]), int(lineArr[4])])
	#     labels.append(int(lineArr[7]))

	# for line in label_0.readlines():
	#     lineArr = line.strip().split(',')
	#     dataSet.append([float(lineArr[3]), int(lineArr[4])])
	#     labels.append(int('-1'))

	# for line in null_label_0.readlines():
	#     lineArr = line.strip().split(',')
	#     dataSet.append([float(lineArr[3]), int(lineArr[4])])
	#     labels.append(int('-1'))

	all_data = open('./train_data/Date_all.csv')
	for line in all_data.readlines():
	    lineArr = line.strip().split(',')
	    dataSet.append([float(lineArr[3]), int(lineArr[4])])
	    labels.append(int(lineArr[7]))
	    # if lineArr[7]=='1':
	    # 	labels.append(int(lineArr[7]))
	    # else:
	    # 	labels.append(int('-1'))

	print len(dataSet)
	print len(labels)
	dataSet_n = dataSet[0:40000]
	labels_n = labels[0:40000]
	# train_x = np.array(dataSet[0:60000])
	# train_y = np.array(labels[0:60000])
	label_num=-1
	for data_x in dataSet_n:
		label_num=label_num+1
		if labels_n[label_num]== 1:
			plt.plot(data_x[0], data_x[1], 'or')
		elif labels_n[label_num]== 0:
			plt.plot(data_x[0], data_x[1], 'ob')

	plt.show()
	
	#找数据规律可以发现，简单的：当距离固定，折扣率越大，核销率越大；
	#一般同一个用户在不同时间领同一种优惠券，其用与不用是一样的
	#
	# test_x = dataSet[60000:60200]
	# test_y = []

	## step 2: training...
	# print "step 2: training..."
	# clf=SVC()
	# clf.fit(train_x,train_y)

	# print clf.predict([[0.95, 3]])
	# for t_x in test_x:
	# 	print clf.predict([t_x])
		# test_y.append(clf.predict([t_x]))

	# ## step 2: training...
	# print "step 2: training..."
	# C = 0.6
	# toler = 0.001
	# maxIter = 50
	# svmClassifier = model.trainSVM(train_x, train_y, C, toler, maxIter, kernelOption = ('linear', 0))

	# ## step 3: testing
	# print "step 3: testing..."
	# accuracy = model.testSVM(svmClassifier, test_x, test_y)

	# ## step 4: show the result
	# print "step 4: show the result..."
	# print 'The classify accuracy is: %.3f%%' % (accuracy * 100)
	# model.showSVM(svmClassifier)	

if __name__ == '__main__':
	testBayes()
	# testSVM()


