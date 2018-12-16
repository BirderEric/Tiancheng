# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
from UID2UID import *
from feature import Feature
import os

class data_process():

	def __init__(self,clean_label,ifdrop):
		self.ifclean = clean_label
		self.ifdrop = ifdrop
		self.data_dir = os.getcwd() + '/dataset/'

	def read_data(self):

		self.op_train = pd.read_csv(self.data_dir + 'content/开放数据_甜橙杯数据建模_中国电信（补充）/operation_train_new.csv')
		self.trans_train = pd.read_csv(self.data_dir + 'content/开放数据_甜橙杯数据建模_中国电信（补充）/transaction_train_new.csv')
		self.op_test = pd.read_csv(self.data_dir + '/content/test_operation_round2.csv')
		self.trans_test = pd.read_csv(self.data_dir + '/content/test_transaction_round2.csv')
		self.Label = pd.read_csv(self.data_dir + 'content/开放数据_甜橙杯数据建模_中国电信（补充）/tag_train_new.csv')
		self.sub = pd.read_csv(self.data_dir + '/content/submit_example.csv')
		self.w2v = pd.read_csv(self.data_dir + '/content/w2v_features.csv')
	def data_clean(self):

		self.op_train['device_code3'] = self.op_train['device_code3'].apply(lambda x :np.nan if x =='14c09cc8ce23d46c' else x)
		self.op_test = self.op_test[(self.op_test['device_code3']!='14c09cc8ce23d46c') &(self.op_test['mode']!='d25caee90b27fa9b')]

	def label_pro(self):
		threshold = 4
		IsTrain = True
		dev2UIDBlack_train = Dev2UIDBlack(self.op_train,self.trans_train,threshold,IsTrain)
		new_label = []
		label_o = self.Label['Tag'].values
		cnt = 0
		for v in self.Label['UID'].values:
			if v in dev2UIDBlack_train:
				new_label.append(1)
			else:
				new_label.append(label_o[cnt])
			cnt += 1  
		self.Label['Tag'] = new_label
	def data_pro(self):

		self.read_data() #读取数据
		print('读取数据完成！')
		if self.ifclean:
			self.data_clean()#数据清洗
			print('数据清洗完成！')
		else:
			pass
		self.label_pro() #训练集标签处理
		print('训练集标签处理完成！')
		if self.ifdrop:
			train = Feature.get_feature(self.op_train,self.trans_train,self.Label,self.w2v,1)
			print('训练集特征提取完成！')
			test = Feature.get_feature(self.op_test,self.trans_test,self.sub,self.w2v,1)
			print('测试集特征提取完成！')
		else:
			train = Feature.get_feature(self.op_train,self.trans_train,self.Label,self.w2v,0)
			print('训练集特征提取完成！')
			test = Feature.get_feature(self.op_test,self.trans_test,self.sub,self.w2v,0)
			print('测试集特征提取完成！')
		label = self.Label
		sub = self.sub
		return train,test,label,sub
	