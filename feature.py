

import pandas as pd
import numpy as np

class Feature():
    def __init__():
        pass

    def get_feature(op,trans,label,w2v,ifdrop):
        
        if ifdrop:
            op_feature = ['UID', 'mode','mac2','device_code1','device_code2', 'ip1', 'geo_code', 'ip1_sub']
            op_deliver = ['ip1','mac2','geo_code','device_code1','device_code2','device_code3']
            trans_feature = ['UID', 'channel', 'amt_src1','code1', 'trans_type1', 'device_code1','device_code2', 'device_code3', 'ip1','amt_src2', 'merchant', 'geo_code', 'trans_type2','ip1_sub']
        else:
            op_feature = op.columns
            op_deliver = ['ip1', 'ip1_sub', 'wifi', 'mac1', 'mac2', 'geo_code', 'mode', 'device1', 'device2','device_code1', 'device_code2', 'device_code3']
            trans_feature = trans.columns

        for feature in op_feature:
            if feature not in ['day']:
                if feature != 'UID':
                    label = label.merge(op.groupby(['UID'])[feature].count().reset_index(),on='UID',how='left')
                    label =label.merge(op.groupby(['UID'])[feature].nunique().reset_index(),on='UID',how='left')
                for deliver in op_deliver:
                    if feature not in deliver:
                        if feature != 'UID':
                            temp = op[['UID',deliver]].merge(op.groupby([deliver])[feature].count().reset_index(),on=deliver,how='left')[['UID',feature]] 
                            temp = temp.groupby('UID')[feature].sum().reset_index()
                            temp.columns = ['UID',feature+deliver]
                            label =label.merge(temp,on='UID',how='left')
                            del temp
                            temp = op[['UID',deliver]].merge(op.groupby([deliver])[feature].nunique().reset_index(),on=deliver,how='left')[['UID',feature]] 
                            temp = temp.groupby('UID')[feature].sum().reset_index()
                            temp.columns = ['UID',feature+deliver]
                            label =label.merge(temp,on='UID',how='left')
                            del temp
                        else:
                            temp = op[['UID',deliver]].merge(op.groupby([deliver])[feature].count().reset_index(),on=deliver,how='left')[['UID_x','UID_y']] 
                            temp = temp.groupby('UID_x')['UID_y'].sum().reset_index()
                            temp.columns = ['UID',feature+deliver]
                            label =label.merge(temp,on='UID',how='left')
                            del temp
                            temp = op[['UID',deliver]].merge(op.groupby([deliver])[feature].nunique().reset_index(),on=deliver,how='left')[['UID_x','UID_y']] 
                            temp = temp.groupby('UID_x')['UID_y'].sum().reset_index()
                            temp.columns = ['UID',feature+deliver]
                            label =label.merge(temp,on='UID',how='left')
                            del temp

            else:
                pass
                print(feature)
                        
        for feature in trans_feature:
            if feature not in ['trans_amt','bal','day']:
                if feature != 'UID':
                    label =label.merge(trans.groupby(['UID'])[feature].count().reset_index(),on='UID',how='left')
                    label =label.merge(trans.groupby(['UID'])[feature].nunique().reset_index(),on='UID',how='left')
                for deliver in ['ip1','geo_code','device_code1','device_code2','device_code3','mac1']:
                    if feature not in deliver: 
                        if feature != 'UID':
                            temp = trans[['UID',deliver]].merge(trans.groupby([deliver])[feature].count().reset_index(),on=deliver,how='left')[['UID',feature]] 
                            temp = temp.groupby('UID')[feature].sum().reset_index()
                            temp.columns = ['UID',feature+deliver]
                            label =label.merge(temp,on='UID',how='left')
                            del temp
                            temp = trans[['UID',deliver]].merge(trans.groupby([deliver])[feature].nunique().reset_index(),on=deliver,how='left')[['UID',feature]] 
                            temp = temp.groupby('UID')[feature].sum().reset_index()
                            temp.columns = ['UID',feature+deliver]
                            label =label.merge(temp,on='UID',how='left')
                            del temp
                        else:
                            temp = trans[['UID',deliver]].merge(trans.groupby([deliver])[feature].count().reset_index(),on=deliver,how='left')[['UID_x','UID_y']] 
                            temp = temp.groupby('UID_x')['UID_y'].sum().reset_index()
                            temp.columns = ['UID',feature+deliver]
                            label =label.merge(temp,on='UID',how='left')
                            del temp
                            temp = trans[['UID',deliver]].merge(trans.groupby([deliver])[feature].nunique().reset_index(),on=deliver,how='left')[['UID_x','UID_y']] 
                            temp = temp.groupby('UID_x')['UID_y'].sum().reset_index()
                            temp.columns = ['UID',feature+deliver]
                            label =label.merge(temp,on='UID',how='left')
                            del temp
            else:
                pass
                        
        print("Done")
        label = label.merge(w2v,on='UID',how='left')
        return label