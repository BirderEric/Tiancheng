import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import StratifiedKFold
from feature import Feature

class lgbmodel():
	#build lbg model
	
	def __init__(self,train,test,label,sub,random_seed):
		
		self.sub = sub
		self.train =  train.drop(['Tag','UID'],axis = 1).fillna(-1)
		self.test_id = test['UID']
		self.test = test.drop(['Tag','UID'],axis = 1).fillna(-1)
		self.label = label['Tag']
		self.best_score = []
		self.oof_preds = np.zeros(self.train.shape[0])
		self.sub_preds = np.zeros(self.test_id.shape[0])
		self.lgb_model = lgb.LGBMClassifier(boosting_type='gbdt', num_leaves=100, reg_alpha=3, reg_lambda=5, max_depth=-1,
    				n_estimators=5000, objective='binary', subsample=0.9, colsample_bytree=0.77, subsample_freq=1, learning_rate=0.05,
    				random_state=1000, n_jobs=16, min_child_weight=4, min_child_samples=5, min_split_gain=0)
		self.skf = StratifiedKFold(n_splits=5, random_state=random_seed, shuffle=True)	
	

	def tpr_weight_funtion(self,y_true, y_predict):

	    d = pd.DataFrame()
	    d['prob'] = list(y_predict)
	    d['y'] = list(y_true)
	    d = d.sort_values(['prob'], ascending=[0])
	    y = d.y
	    PosAll = pd.Series(y).value_counts()[1]
	    NegAll = pd.Series(y).value_counts()[0]
	    pCumsum = d['y'].cumsum()
	    nCumsum = np.arange(len(y)) - pCumsum + 1
	    pCumsumPer = pCumsum / PosAll
	    nCumsumPer = nCumsum / NegAll
	    TR1 = pCumsumPer[abs(nCumsumPer - 0.001).idxmin()]
	    TR2 = pCumsumPer[abs(nCumsumPer - 0.005).idxmin()]
	    TR3 = pCumsumPer[abs(nCumsumPer - 0.01).idxmin()]
	    return 0.4 * TR1 + 0.3 * TR2 + 0.3 * TR3

	def modeltrain(self):

		for index, (train_index, test_index) in enumerate(self.skf.split(self.train, self.label)):
		    self.lgb_model.fit(self.train.iloc[train_index], self.label.iloc[train_index], verbose=50,
		                  eval_set=[(self.train.iloc[train_index], self.label.iloc[train_index]),
		                            (self.train.iloc[test_index], self.label.iloc[test_index])], early_stopping_rounds=30)
		    self.best_score.append(self.lgb_model.best_score_['valid_1']['binary_logloss'])
		    print(self.best_score)
		    self.oof_preds[test_index] = self.lgb_model.predict_proba(self.train.iloc[test_index], num_iteration=self.lgb_model.best_iteration_)[:,1]

		    test_pred = self.lgb_model.predict_proba(self.test, num_iteration=self.lgb_model.best_iteration_)[:, 1]
		    self.sub_preds += test_pred / 5

		tpr = self.tpr_weight_funtion(y_predict=self.oof_preds, y_true=self.label)
		print('TPR SCORE:%s'%tpr)
		self.sub['Tag'] = self.sub_preds
		self.sub.to_csv('DataAI%s.csv'%tpr,index=False)
		

