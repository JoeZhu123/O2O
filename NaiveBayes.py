#-*- coding:utf-8 -*-

from __future__ import division

class BayesClassifier():            #简单贝叶斯分类器

    def __init__(self):

        pass

    def train(self,features,labels):                          #训练简单贝叶斯分类器

        featuresNum=len(features[1])                  #样本特征数目

        self.sampleNum=len(features)                 #样本数目

        self.countDic={}                                    #统计各个条件概率的出现次数

        self.labelSet=set([])                               #集合存放类标，如：Y=1 or Y=-1

        for i in range(0,len(labels)):                    #统计类标不同值出现的次数

            tempStr='Y='+str(labels[i])

            self.labelSet.add(str(labels[i]))

            if tempStr in self.countDic:    

                self.countDic[tempStr]+=1

            else:

                self.countDic[tempStr]=1

        for i in range(0,len(features)):               #统计各个条件概率组合出现的次数

            for j in range(0,featuresNum):

                tempStr='F'+str(j)+'='+str(features[i][j])+'|'+'Y='+str(labels[i])

                if tempStr in self.countDic:

                    self.countDic[tempStr]+=1

                else:

                    self.countDic[tempStr]=1

        for key in self.countDic.keys():        #遍历次数统计字典计算概率

            if key.find('|')!=-1:                      #计算条件概率P(Fi=a|Y=b)

                targetStr=key[key.find('|')+1:]       #类标字符串:  Y=1 or Y=-1

                self.countDic[key]/=self.countDic[targetStr]    #算出条件概率P(Fi=a|Y=b)=Count(Fi=a,Y=b)/Count(Y=b)

        for label in self.labelSet:          #计算类标概率P(Y=b)

            tempStr="Y="+str(label)

            self.countDic[tempStr]/=self.sampleNum                                     

               

    def classify(self,feature):                                 #使用训练后的贝叶斯分类器分类新样本

        #计算后验概率P(Y=b|Sample=feature)

        probabilityMap={}

        for label in self.labelSet:

            tempProbability=1.0

            for i in range(0,len(feature)):

                tempStr='F'+str(i)+'='+str(feature[i])+'|Y='+label

                if tempStr not in self.countDic:        #遇到新的特征值，导致该概率P(Fi=a|Y=b)为0，将它校正为非0值（1/Count(Y=b))

                    tempProbability*=(1.0/self.countDic['Y='+label])/self.sampleNum

                else:

                    tempProbability*=self.countDic[tempStr]

            tempProbability*=self.countDic['Y='+label]

            probabilityMap[label]=tempProbability

        maxProbability=0.0

        for label in self.labelSet:                       #选取使后验概率P(Y=b|Sample=feature)最大的类标作为目标类标

            if  probabilityMap[label]>maxProbability:

                maxProbability=probabilityMap[label]

                targetLabel=label

        probabilityMap.clear()

        return targetLabel,maxProbability

    def __del__(self):

        self.countDic.clear()