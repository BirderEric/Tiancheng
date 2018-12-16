# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import Datapro
import Lgbmodel
import random
def main():
    
    Data = Datapro.data_process(clean_label=True,ifdrop=False)
    train,test,label,sub = Data.data_pro()
    for i in range(2):
	    model = Lgbmodel.lgbmodel(train,test,label,sub,random_seed=random.randint(1024,2018))
	    model.modeltrain()

if __name__ == '__main__':
	main()