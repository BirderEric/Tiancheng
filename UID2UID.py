import pandas as pd
import numpy as np


def UID2Device2UID(df):

    device = ['device_code1','device_code2',"device_code3"]
    for dev in device:
        #print('%s 设备数量统计中'%dev)
        temp = df.groupby('UID',as_index=False)[dev].agg({dev+'_num':'unique'})
        temp[dev+'_dev'] = temp[dev+'_num'].apply(lambda x: device_num(x)[0])
        temp[dev+'_dev_type'] = temp[dev+'_num'].apply(lambda x: device_num(x)[1])
        df = df.merge(temp[['UID',dev+'_dev',dev+'_dev_type']],on='UID',how='left')
        del temp
    df['device_sum'] = df['device_code1_dev'] + df['device_code2_dev'] + df['device_code3_dev']
    df = device2UID(df)
    return df

def device_num(array):

    cnt = 0
    device = []
    for v in array:
        if str(v) == 'nan':
            pass
        else:
            cnt +=1
            device.append(v)
    return [cnt,device]

def device2UID(df):
    # 唯一设备对应的UID数量统计
    device = ['device_code1','device_code2',"device_code3"]
    for dev in device:
        #print('%s 设备数量登录的UID数量统计中'%dev)
        temp = df.groupby(dev,as_index=False)['UID'].agg({dev+'_2UID':'unique'})
        df = df.merge(temp,on=dev,how='left')
    MulUIDnum = []
    MulUID = []
    for uid in zip(df['device_code1_2UID'].values,df['device_code2_2UID'].values,df['device_code3_2UID'].values):
        try:
            uid1 = [v for v in uid[0]] 
        except:
            uid1 = []
        try:
            uid2 = [v for v in uid[1]] 
        except:
            uid2 =[]
        try:
            uid3 = [v for v in uid[2]] 
        except:
            uid3 =[]
        newuid = list(set(uid1+uid2+uid3))
        MulUID.append(newuid)
        MulUIDnum.append(len(newuid))
    #print(newuid)
    df['Dev2UIDnum'] = MulUIDnum
    df['Dev2UID'] = MulUID
    return df.drop(['device_code1_2UID','device_code2_2UID','device_code3_2UID'],axis=1)

def Dev2UIDBlack(op,trans,threshold,ifTrain):
    
    if ifTrain:
        op['device_code3'] = op['device_code3'].apply(lambda x :np.nan if x =='14c09cc8ce23d46c' else x)
    else:
      
        op = op[(op['device_code3']!='14c09cc8ce23d46c') & (op['mode']!='d25caee90b27fa9b')]
    
    temp_op_test = UID2Device2UID(op)
    temp_trans_test = UID2Device2UID(trans)

    b = temp_op_test[(temp_op_test['Dev2UIDnum']>3)].UID.unique()
    #df = UID2Device2UID(test_operation_clean)
    a = temp_trans_test[(temp_trans_test['Dev2UIDnum']>3)].UID.unique()
    black = []
    for uid in b:
        if uid in a:
            black.append(uid)
    #print('训练集一共找到%s羊毛党'%len(black))
    return black