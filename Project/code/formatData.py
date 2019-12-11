import numpy as np
import pandas as pd
import pickle as pk
import matplotlib.pyplot as plt
import datetime
import os

def getNumSamples(df,houses):
    numEntries=[]
    for x in  houses:
        numEntries.append(df.values[(df['LCLid']==x)].shape[0])
    return numEntries

def combineHouses():
    combFileDir = '/home/bdvr/DATA516/avanroi1/Project/data/'
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
    od = '/home/bdvr/DATA516/avanroi1/Project/data/'
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
combineHousesdd()
