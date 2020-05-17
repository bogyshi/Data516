import sklearn
import pandas as pd
import pdb
import pickle as pk
import numpy as np
from sklearn.linear_model import LogisticRegressionCV
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path
import pathlib

import os
import random

homeDir = pathlib.Path.home()
currentDir = pathlib.Path.cwd()
githubDir = currentDir.parent.parent.parent
combFileDirP = '/Data516/Project/data/'
combFileDir =   Path(str(githubDir) + str(Path(combFileDirP)))
dataDirP='/Data512/finalProject/data/'
dataDir =   Path(str(githubDir) + str(Path(combFileDirP)))

inTrainData=0
outTrainData=1 # includes validation for cv
inTestData=2
outTestData=3

removeMonth = False

def prepareData(doSmall = False):

    with open(dataDir/'ins.pk','rb') as f:
        ins = pk.load(f)

    with open(dataDir/'outLabels.pk','rb') as f:
        outs = pk.load(f)

    #pdb.set_trace()

    if(removeMonth):
        ins = ins[:,:-12]
        ins = ins / ins.max(axis=0)
    else:
        ins[:,:-12] = ins[:,:-12] / (ins[:,:-12]).max(axis=0)

    '''
    Obsolete, was used to remove na values manually, but now addressed in formatData.py
    mask = np.ones(outs.shape, bool)
    mask[toRemove]=False
    outs = outs[mask]'''
    #outs = np.delete(outs, toRemove)
    np.random.seed(13)
    numEntries = ins.shape[0]
    numTrain = int(numEntries*(0.7))
    numRemain = numEntries-numTrain
    numVal = int(numRemain*0.60)
    numTest = int(numRemain-numVal)
    indexes = np.arange(0,numEntries,1)
    np.random.shuffle(indexes)
    trainIndexes = indexes[0:numTrain]
    valIndexes = indexes[numTrain:(numTrain+numVal)]
    testIndexes = indexes [(numTrain+numVal):]
    combTrainVal = np.concatenate((trainIndexes,valIndexes))
    inputData = ins[combTrainVal].astype(float)
    outData = outs.values[combTrainVal].astype(float)
    outs=outs.values
    #outs=outs-1
    #outs = outs*-1
    alldata=[ins[combTrainVal,:],outs[combTrainVal],ins[testIndexes,:],outs[testIndexes]]
    #if(doSmall):
    #    outs = np.

    return alldata

def baselineModel(data):
    TOUnumTrain = sum(data[outTrainData]==1)
    STDnumTrain = sum(data[outTrainData]==0)
    touWeight = TOUnumTrain/(TOUnumTrain+STDnumTrain)
    rc=0
    touCor=0
    stdCor=0
    incorStd=0
    incorTOU=0
    for x in data[inTestData]:
        guess = random.random()
        if(guess < touWeight):
            guess = 1
        else:
            guess = 0
        if(guess == data[outTestData][rc] and guess == 1):
            touCor+=1
        elif(guess == data[outTestData][rc] and guess == 0):
            stdCor+=1
        elif(guess != data[outTestData][rc] and guess == 1):
            incorStd+=1
        else:
            incorTOU+=1
        rc+=1
    print("Baseline Accuracy: %f"% ((stdCor+touCor)/rc))
    print("Baseline Accuracy on TOU: %f"% ((touCor)/(touCor+incorTOU)))
    print("Baseline Accuracy on STD: %f"% ((stdCor)/(stdCor+incorStd)))



def trainLR(data,modelName="tempLRModel",overwrite=False):
    TOUnumTrain = sum(data[outTrainData]==1)
    STDnumTrain = sum(data[outTrainData]==0)
    touWeight = TOUnumTrain/(TOUnumTrain+STDnumTrain)
    if(os.path.exists('/home/bdvr/Documents/GitHub/Data516/Project/Models/'+modelName+'.pk') and overwrite==False):
        print("This model has already been trained, pass overwrite == True to retrain the model")
    else:
#        clf = LogisticRegression(random_state=0,verbose=10,class_weight={0:1,1:(1/touWeight)})
        clf = LogisticRegression(random_state=0,verbose=10,class_weight={0:1,1:1},C=100,penalty='l2',tol=0.000001)
        clf.fit(data[inTrainData],data[outTrainData])
        with open('/home/bdvr/Documents/GitHub/Data516/Project/Models/'+modelName+'.pk','wb') as f:
            pk.dump(clf,f)
        print(clf.score(data[inTrainData],data[outTrainData]))
        print(clf.score(data[inTestData],data[outTestData]))

def trainGrid(data):
    #pdb.set_trace()
    #clf = LogisticRegressionCV(random_state=0,cv=5)
    #clf.fit(ins[combTrainVal],y=outs[combTrainVal])
    LR = LogisticRegression()
    TOUnumTrain = sum(data[outTrainData]==1)
    STDnumTrain = sum(data[outTrainData]==0)
    touWeight = TOUnumTrain/(TOUnumTrain+STDnumTrain)
    parameters = {'penalty':['l1','l2'],'C':[1,10,100,1000],'class_weight':[{0:(1-touWeight),1:(touWeight)},{0:1,1:1}],'solver':['liblinear']}
    clf = GridSearchCV(LR, parameters)
    clf.fit(data[inTrainData],data[outTrainData])
    #print(clf.score(ins[valIndexes],outs.values[valIndexes]))
    with open('/home/bdvr/Documents/GitHub/Data516/Project/Models/firstGridSearch.pk','wb') as f:
        pk.dump(clf,f)

def testModel(modelName):
    with open('/home/bdvr/Documents/GitHub/Data516/Project/Models/'+modelName+'.pk','wb') as f:
        clf = pk.load(f)

def trainRF(data,modelName="tempTreeModel",overwrite=False):
    if(os.path.exists('/home/bdvr/Documents/GitHub/Data516/Project/Models/'+modelName+'.pk') and overwrite==False):
        print("This model has already been trained, pass overwrite == True to retrain the model")
    else:
        clf = RandomForestClassifier(max_depth=4, random_state=0,class_weight={0:1,1:5})
        clf.fit(data[inTrainData],data[outTrainData])
        with open('/home/bdvr/Documents/GitHub/Data516/Project/Models/'+modelName+'.pk','wb') as f:
            pk.dump(clf,f)

def evaluateModel(data,modelName="tempTreeModel",modelType="LR"):
    with open('/home/bdvr/Documents/GitHub/Data516/Project/Models/'+modelName+'.pk','rb') as f:
        clf = pk.load(f)
    rc = 0
    cor=0
    stdCor = 0
    touCor = 0
    incorTOU=0
    incorStd=0
    for x in data[inTestData]:
        pred = clf.predict(x.reshape(1,-1))[0]
        #pdb.set_trace()
        if(pred == data[outTestData][rc] and pred == 1):
            touCor+=1
        elif(pred == data[outTestData][rc] and pred == 0):
            stdCor+=1
        elif(pred != data[outTestData][rc] and pred == 1):
            incorStd+=1
        else:
            incorTOU+=1
        rc+=1
    if(modelType == "LR"):
        print("Intercept: " + str(clf.intercept_))
        print("coefficients: " + str(clf.coef_.astype(str)))
    if(modelType=="RF"):
        print("feature importances: " + str(clf.feature_importances_.astype(str)))
    print("Accuracy: %f"% ((stdCor+touCor)/rc))
    print("Accuracy on TOU: %f"% ((touCor)/(touCor+incorTOU)))
    print("Accuracy on STD: %f"% ((stdCor)/(stdCor+incorStd)))
    #pdb.set_trace()
    return 0

def examineModel(data):
    with open('/home/bdvr/Documents/GitHub/Data516/Project/Models/firstGridSearch.pk','rb') as f:
        model = pk.load(f)
    print(model.cv_results_)
    pdb.set_trace()
    return 1

data = prepareData()
#trainModel(data)
#pdb.set_trace()
#trainGrid(data)
#examineModel(data)
#baselineModel(data)
trainLR(data,'LRWithMonth',overwrite=True)
evaluateModel(data,'LRWithMonth')
#trainRF(data,'RFWithMonth',overwrite=True)
#evaluateModel(data,'RFWithMonth',modelType = "RF")
