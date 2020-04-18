import numpy as np
import pandas as pd
import pickle as pk
import matplotlib.pyplot as plt
import datetime
import os
import pdb

#combFileDir = '/home/bdvr/DATA516/avanroi1/Project/data/'
combFileDir = '/home/bdvr/GitHub/DATA516/Project/data/'
dataDir = '/home/bdvr/Documents/GitHub/Data512/finalProject/data/'

def addOutLabel(outs):
    houseInfo = pd.read_csv(dataDir+'houseData.csv')
    replaceVal=None
    for x in houseInfo.values:
        lclid = x[0]
        if(x[1]=='Std'):
            replaceVal = 0
        else:
            replaceVal = 1
        outs = outs.replace({lclid:replaceVal})
        #395624 ToU labels
        #1551109 StdLabels
    return outs
def createBigInsBigOuts():
    ins = []
    outs = []
    tempTable = None
    rewrite=False
    for block in os.listdir(dataDir+'pivotData'):
        tempTable = pd.read_csv(os.path.join(dataDir+'pivotData',block),header=0,index_col=0)
        tempTable['month'] = pd.to_datetime(tempTable['Date']).dt.month.astype(int)
        tempTable = tempTable.drop('Date',axis=1).dropna()
        if(tempTable.index.name=='LCLid'):
            outData=pd.Series(tempTable.index)
            inData=tempTable
        elif(tempTable.index.name==None):
            inData = tempTable.loc[:, tempTable.columns != 'LCLid']
            outData = tempTable['LCLid']
        else:
            print('ERROR')
        #if(inData.shape[0]!=outData.shape[0]):
        #pdb.set_trace()
        ins.append(inData)
        outs.append(outData)
    #pdb.set_trace()

    if(os.path.exists('/home/bdvr/Documents/GitHub/Data516/Project/data/outLabels.pk') and rewrite==False):
        pass
    else:
        outs = addOutLabel(pd.concat(outs))
        pk.dump(outs,open('/home/bdvr/Documents/GitHub/Data516/Project/data/outLabels.pk','wb'))
    #months are in the order expected (0 is jan, 1 is feb, 2 is March, .... december is the 11th o indexed column at the end)
    pk.dump(pd.get_dummies(pd.concat(ins),columns=['month']).values,open('/home/bdvr/Documents/GitHub/Data516/Project/data/ins.pk','wb'))

def getNAIndexes():
    '''
    obsolete
    '''
    ins = []
    tempTable = None
    for block in os.listdir(dataDir+'pivotData'):
        tempTable = pd.read_csv(os.path.join(dataDir+'pivotData',block),header=0)
        tempTable = tempTable.drop('Date',axis=1)
        inData = tempTable.loc[:, tempTable.columns != 'LCLid']
        ins.append(inData)
    allIns = pd.concat(ins)
    badIndexes = pd.isnull(allIns).any(1).nonzero()[0]
    pdb.set_trace()
    pk.dump(badIndexes,open('/home/bdvr/Documents/GitHub/Data516/Project/data/badIndexes.pk','wb'))


def getNumSamples(df,houses):
    numEntries=[]
    for x in  houses:
        numEntries.append(df.values[(df['LCLid']==x)].shape[0])
    return numEntries

def combineHouses():
    dfs=[]
    for filename in os.listdir(combFileDir):
        dfs.append(pd.read_csv(os.path.join(combFileDir, filename),header=1,index_col=0,skiprows=range(2,3)))
    pd.concat(dfs).to_csv(os.path.join(combFileDir,'allCombined.csv'))

def combineHousesdd():
    combFileDir = '/home/bdvr/DATA516/avanroi1/Project/data/dd/'
    dfs=[]
    for filename in os.listdir(combFileDir):
        dfs.append(pd.read_csv(os.path.join(combFileDir, filename),header=1,index_col=0,skiprows=range(2,3)))
    pd.concat(dfs).to_csv(os.path.join(combFileDir,'allCombined.csv'))


def houseDataPerDay():
    d = '/home/bdvr/Documents/GitHub/Data512/finalProject/data/halfhourly_dataset/'
    od = '/home/bdvr/DATA516/avanroi1/Project/data/dd/'
    counter=0
    for filename in os.listdir(d):
        try:
            if filename.endswith(".csv"):
                print(filename)
                counter = filename.find('.')
                consumptionBlock0 = pd.read_csv(os.path.join(d, filename),header=0,encoding='ISO-8859-1')
                unqHousesBlk0 = np.unique(consumptionBlock0['LCLid'])
                consumptionBlock0.tstp = pd.to_datetime(consumptionBlock0.tstp,format='%Y-%m-%d %H:%M:%S.%f',errors='coerce')
                just2013Blk0 = consumptionBlock0.iloc[(consumptionBlock0.tstp >= '2013-01-01').values  & (consumptionBlock0.tstp < '2014-01-01').values]
                #somtin= unqHousesBlk0[np.array(getNumSamples(just2013Blk0,unqHousesBlk0))>16000]
                justGoodBlock0 = just2013Blk0
                justGoodBlock0['energy(kWh/hh)']=justGoodBlock0['energy(kWh/hh)'].astype(float)
                justGoodBlock0['Time'] = [datetime.datetime.time(d) for d in justGoodBlock0['tstp']]
                justGoodBlock0['Date'] = [datetime.datetime.date(d) for d in justGoodBlock0['tstp']]
                justGoodBlock0.pivot_table(values='energy(kWh/hh)',index=['LCLid','Date'],columns='Time').to_csv(os.path.join(od,'block'+filename[5:counter]+'sep.csv'))
        except:
            counter+=1

def avgHouseData():
    d = '/home/bdvr/Documents/GitHub/Data512/finalProject/data/halfhourly_dataset/'
    od = combFileDir
    counter=0
    for filename in os.listdir(d):
        try:
            if filename.endswith(".csv"):
                print(filename)
                counter = filename.find('.')
                consumptionBlock0 = pd.read_csv(os.path.join(d, filename),header=0,encoding='ISO-8859-1')
                unqHousesBlk0 = np.unique(consumptionBlock0['LCLid'])
                consumptionBlock0.tstp = pd.to_datetime(consumptionBlock0.tstp,format='%Y-%m-%d %H:%M:%S.%f',errors='coerce')
                just2013Blk0 = consumptionBlock0.iloc[(consumptionBlock0.tstp >= '2013-01-01').values  & (consumptionBlock0.tstp < '2014-01-01').values]
                somtin= unqHousesBlk0[np.array(getNumSamples(just2013Blk0,unqHousesBlk0))>16000]
                justGoodBlock0 = just2013Blk0.iloc[just2013Blk0.LCLid.isin(somtin).values]
                justGoodBlock0['energy(kWh/hh)']=justGoodBlock0['energy(kWh/hh)'].astype(float)
                justGoodBlock0['Time'] = [datetime.datetime.time(d) for d in justGoodBlock0['tstp']]
                justGoodBlock0.groupby(by=['LCLid','Time']).mean().unstack().to_csv(os.path.join(od,'block'+filename[5:counter]+'.csv'))
        except:
            counter+=1
#combineHouses()
# s = pd.read_csv('/home/bdvr/DATA516/avanroi1/Project/data/block_92.csv',header=1,index_col=0,skiprows=range(2,3))
#houseDataPerDay()
#combineHousesdd()
createBigInsBigOuts()
#getNAIndexes()
