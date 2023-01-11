import os
import secretflow as sf
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris



#隐私求交
def print_psi(name):
    sf.shutdown()#关闭之前已经运行的
    sf.init(['alice', 'bob', 'carol'], address='local')#alice， bob 和 carol 是在一台机器上创建的，以模拟多个参与者。


    data, target = load_iris(return_X_y=True, as_frame=True)
    data['uid'] = np.arange(len(data)).astype('str')
    data['month'] = ['Jan'] * 75 + ['Feb'] * 75

    print(data);

    os.makedirs('.data', exist_ok=True)#创建文件夹
    da, db, dc = data.sample(frac=0.9), data.sample(frac=0.8), data.sample(frac=0.7)#随机采样
    da.to_csv('.data/alice.csv', index=False)
    db.to_csv('.data/bob.csv', index=False)
    dc.to_csv('.data/carol.csv', index=False)

    alice, bob = sf.PYU('alice'), sf.PYU('bob')#明文设备
    spu = sf.SPU(sf.utils.testing.cluster_def(['alice', 'bob']))#密文设备
    #隐私求交
    input_path = {alice: '.data/alice.csv', bob: '.data/bob.csv'}
    output_path = {alice: '.data/alice_psi.csv', bob: '.data/bob_psi.csv'}
    spu.psi_csv('uid', input_path, output_path, 'alice')#隐私求交函数

    da_psi = pd.read_csv('.data/alice_psi.csv')
    db_psi = pd.read_csv('.data/bob_psi.csv')
    print(da)

#聚合运算
def print_juhe():
    print("聚合运算");
    sf.shutdown()
    sf.init(['alice', 'bob'], address='local')
   
    arr0, arr1 = np.random.rand(2, 3), np.random.rand(2, 3)
    print(arr0)
    print(arr1)
    alice, bob = sf.PYU('alice'), sf.PYU('bob')#参与方
    spu = sf.SPU(sf.utils.testing.cluster_def(['alice', 'bob']))
    spu_aggr = sf.security.aggregation.SPUAggregator(spu)
    # Simulate that alice and bob hold data respectively
    a = alice(lambda: arr0)()
    b = bob(lambda: arr1)()
    # Sum the data.
    sumData=sf.reveal(spu_aggr.sum([a, b], axis=0))
    print("求和运算");
    print(sumData)
    # Average the data.
    averageData=sf.reveal(spu_aggr.average([a, b], axis=0))
    print("求平均运算");
    print(averageData)

if __name__ == '__main__':
    print_juhe()

