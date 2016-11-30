# -*- coding:utf-8 -*-

import urllib2
import re
import os
import csv



def loadData(fileName):
    csvfile = file(fileName, 'rb')
    reader = csv.reader(csvfile)
    data_list=[]
    for line in reader:
        data_list.append(line)
    csvfile.close()
    return data_list

#Table: 数据表基类
class Table:
    def __init__(self,User_id,Coupon_id,Date_received):
        #用户ID
        self.User_id=User_id
        #优惠券ID：null表示无优惠券消费，此时Discount_rate和Date_received字段无意义,对于Table2:“fixed”表示该交易是限时低价活动。
        self.Coupon_id=Coupon_id
        #领取优惠券日期
        self.Date_received=Date_received

#Table 1: 用户线下消费和优惠券领取行为
class Table1(Table):
    def __init__(self,User_id,Merchant_id,Coupon_id,Discount_rate,Distance,Date_received,Date):
        #继承Table基类
        Table.__init__(self,User_id,Coupon_id,Date_received)
        #商户ID
        self.Merchant_id=Merchant_id
        #优惠率：x \in [0,1]代表折扣率；x:y表示满x减y。单位是元
        self.Discount_rate=Discount_rate
        #user经常活动的地点离该merchant的最近门店距离是x*500米（如果是连锁店，则取最近的一家门店），x\in[0,10]；null表示无此信息，0表示低于500米，10表示大于5公里；
        self.Distance=Distance
        #消费日期：如果Date=null & Coupon_id != null，该记录表示领取优惠券但没有使用，即负样本；如果Date!=null & Coupon_id = null，则表示普通消费日期；如果Date!=null & Coupon_id != null，则表示用优惠券消费日期，即正样本；
        self.Date=Date
    def preprocess(self):
        #if(self.Discount_rate!=null):
        
        return self

#Table 2: 用户线上点击/消费和优惠券领取行为
class Table2(Table):
    def __init__(self,User_id,Merchant_id,Action,Coupon_id,Discount_rate,Date_received,Date):
        #继承Table基类
        Table.__init__(self,User_id,Coupon_id,Date_received)
        #商户ID
        self.Merchant_id=Merchant_id
        #Action：0 点击， 1购买，2领取优惠券
        self.Action=Action
        #优惠率：x \in [0,1]代表折扣率；x:y表示满x减y；“fixed”表示低价限时优惠；
        self.Discount_rate=Discount_rate
        #消费日期：如果Date=null & Coupon_id != null，该记录表示领取优惠券但没有使用；如果Date!=null & Coupon_id = null，则表示普通消费日期；如果Date!=null & Coupon_id != null，则表示用优惠券消费日期；
        self.Date=Date
    def preprocess(self):
        
        return self

#Table 3：用户O2O线下优惠券使用预测样本
class Table3(Table):
    def __init__(self,User_id,Merchant_id,Coupon_id,Discount_rate,Distance,Date_received):
        #继承Table基类
        Table.__init__(self,User_id,Coupon_id,Date_received)
        #商户ID
        self.Merchant_id=Merchant_id
        #优惠率：x \in [0,1]代表折扣率；x:y表示满x减y.
        self.Discount_rate=Discount_rate
        #user经常活动的地点离该merchant的最近门店距离是x*500米（如果是连锁店，则取最近的一家门店），x\in[0,10]；null表示无此信息，0表示低于500米，10表示大于5公里；
        self.Distance=Distance

#Table 4：选手提交文件字段，其中user_id,coupon_id和date_received均来自Table 3,而Probability为预测值
class Table4(Table):
    def __init__(self,User_id,Coupon_id,Date_received,Probability):
        #继承Table基类
        Table.__init__(self,User_id,Coupon_id,Date_received)
        #Probability: 15天内用券概率，由参赛选手给出
        self.Probability=Probability
    def giveProbability(self,Probability):
        self.Probability=Probability

#save data into csv files
def savecsv(dir_name,items):
    csvfile=open(dir_name+'.csv','a+')
    writer=csv.writer(csvfile)
    writer.writerow(items)
    csvfile.close()
    return 

#transform Date to Interger
def Date2Interger(datetime1,datetime2):
    datenum=0
    if datetime1[4:6]==datetime2[4:6]:
        datenum=int(datetime1)-int(datetime2)
    elif (int(datetime1[4:6])-int(datetime2[4:6]))==1:
        if datetime2[4:6]=='01' or datetime2[4:6]=='03' or datetime2[4:6]=='05' or datetime2[4:6]=='07' or datetime2[4:6]=='08' or datetime2[4:6]=='10' or datetime2[4:6]=='12':
            datenum=int(datetime1[6:8])+(31-int(datetime2[6:8]))
        elif datetime2[4:6]=='04' or datetime2[4:6]=='06' or datetime2[4:6]=='09' or datetime2[4:6]=='11':
            datenum=int(datetime1[6:8])+(30-int(datetime2[6:8]))
        elif datetime2[4:6]=='02':
            datenum=int(datetime1[6:8])+(29-int(datetime2[6:8]))   
    else:#隔了一个月才去用，时间间隔必然大于15天，所以令时间间隔datenum=16
        datenum=16
    return datenum

def giveLabel(dir_name,table,label):
    if table.Discount_rate != 'null' and table.Distance != 'null': 
        if ':' in table.Discount_rate:
            D_rate=table.Discount_rate.split(':')
            Rate=float(int(D_rate[0])-int(D_rate[1]))/int(D_rate[0])
            table.Discount_rate=round(Rate,2)
        items=[table.User_id,table.Merchant_id,table.Coupon_id,table.Discount_rate,table.Distance,table.Date_received,table.Date,label]
        savecsv(dir_name,items)
    return

if __name__ == '__main__':
    data_list=loadData('/Users/joe/Documents/O2O/ccf_data_revised/ccf_offline_stage1_train.csv')
    dir_name_all='./train_data/Date_all_no_null'
    for data_line in data_list:
        table=Table1(data_line[0],data_line[1],data_line[2],data_line[3],data_line[4],data_line[5],data_line[6])
        if table.Coupon_id != 'null':
            if table.Date == 'null':
                dir_name='./train_data/merchant_train_data/'+table.Merchant_id
                label='0'
                # giveLabel(dir_name,table,label)
            else:
                if Date2Interger(table.Date,table.Date_received)<=15:
                    dir_name='./train_data/merchant_train_data/'+table.Merchant_id+'_noNull'
                    label='1'
                    # giveLabel(dir_name,table,label)
                    giveLabel(dir_name,table,label)
                else:
                    dir_name='./train_data/merchant_train_data/'+table.Merchant_id+'_noNull'
                    label='0'
                    # giveLabel(dir_name,table,label)
                    giveLabel(dir_name,table,label)
            

    # test_list=loadData('/Users/joe/Documents/O2O/ccf_data_revised/ccf_offline_stage1_test_revised.csv')
    # tables_test=[]
    # dir_name='./test_data/data_revised'
    # for test_line in test_list:
    #     table_test=Table3(test_line[0],test_line[1],test_line[2],test_line[3],test_line[4],test_line[5])
    #     if table_test.Distance != 'null':
    #         if ':' in table_test.Discount_rate:
    #             D_rate=table_test.Discount_rate.split(':')
    #             Rate=float(int(D_rate[0])-int(D_rate[1]))/int(D_rate[0])
    #             table_test.Discount_rate=round(Rate,2)
    #         tables_test.append(table_test)
    #         items=[table_test.User_id,table_test.Merchant_id,table_test.Coupon_id,table_test.Discount_rate,table_test.Distance,table_test.Date_received]
    #         savecsv(dir_name,items) 
    # print len(tables_test)










