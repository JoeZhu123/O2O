#-*- coding:utf-8-*-

from NaiveBayes import BayesClassifier

from numpy import *

def main():

    file=open("D:\\CF\\Weather.txt",'r')

    features=[]            #数据集特征集

    labels=[]                #数据集类标集

    for line in file:         #一行行读数据文件

        line=line.strip()

        tempVec=line.split(',')

        labels.append(tempVec[len(tempVec)-1])

        tempVec2=[tempVec[i] for i in range(0,len(tempVec)-1)]

        features.append(tempVec2)

    Bay=BayesClassifier()

    Bay.train(features,labels)

    correct=0

    for i in range(0,len(features)):

        label=Bay.classify(features[i])

        print("Original:"+str(labels[i])+"==>"+"Classified:"+label)

        if str(label)==str(labels[i]):

            correct+=1

    print("Accuracy:",correct/len(features))    #正确率

if __name__=='__main__':

    main() 