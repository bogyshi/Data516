import numpy as np
from  pyspark  import  SparkContext
from pyspark.ml.classification import LogisticRegression
#from pyspark.mllib.classification import LogisticRegressionWithLBFGS
from pyspark.ml.linalg import Vectors
from pyspark.sql import Row
#from pyspark.mllib.regression import LabeledPoint
import time
from pyspark.ml.classification import LogisticRegressionTrainingSummary
from pyspark.ml.classification import LogisticRegressionSummary

sc = SparkContext.getOrCreate()
multFactor=10

def createLabeledPoints(ins,outs):
    counter = 0
    lbps = []
    while(counter<len(ins)):
        lbps.append( LabeledPoint(outs[counter],ins[counter,:]))
        counter+=1
    return lbps

def createRows(ins,outs):
    counter = 0
    lbps = []
    while(counter<len(ins)):
        lbps.append( Row(label=int(outs[counter,0]), features=Vectors.dense(ins[counter,:].astype(float).tolist() )))
        counter+=1
    return lbps

def makeLargeData(ins,outs,multFactor=2):
    startSize=0
    sizeInc=10000
    endSize = len(ins)
    multCounter = 0
    numPartitions = 6
    allRdds = []
    others = []
    while(multCounter<multFactor):
        startSize=0
        allRdds=[]
        while(startSize+sizeInc<endSize):
            allRdds.append(sc.parallelize(createRows(ins[startSize:startSize+sizeInc,:],outs[startSize:startSize+sizeInc,:]),numPartitions))
            startSize+=sizeInc
        allRdds.append(sc.parallelize(createRows(ins[startSize:,:],outs[startSize:,]),numPartitions))
        print("done making data b4 union")
        s2 = sc.union(allRdds)
        others.append(s2)
        multCounter+=1
    return s2


def getinfoLR(maxIters,ins,outs,numTrials=1):
    debug=False
    times=[]
    iters=[]
    counter = 0
    numPartitions = 6
    startSize=0
    endSize= ins.shape[0]
    allRdds = []
    print(endSize)
    sizeInc=1000000 # 1million rows
    while(startSize+sizeInc<endSize):
        allRdds.append(sc.parallelize(createRows(ins[startSize:startSize+sizeInc,:],outs[startSize:startSize+sizeInc,:]),numPartitions))
        startSize=startSize+sizeInc
    allRdds.append(sc.parallelize(createRows(ins[startSize:,:],outs[startSize:,]),numPartitions))
    s2 = sc.union(allRdds)   #s2 = sc.parallelize(createRows(ins,outs),numPartitions).toDF()
    '''
    replace the above with this
    rdd = sc.union([rdd1, rdd2, rdd3])
    '''
    print(s2.rdd.getNumPartitions())
    if(debug):
        print(s2.show(5))
    '''LogisticRegressionWithLBFGS.train(sc.parallelize(s),iterations=10,stepSize=10)'''
    while(counter<numTrials):
        print(counter)
        lr = LogisticRegression(maxIter=maxIters)
        start = time.time()
        lrModel = lr.fit(s2)
        end = time.time()
        times.append((end-start)*1000)
        iters.append(lrModel.summary.totalIterations)
        counter+=1
    print(np.mean(np.array(iters)))
    print(np.std(np.array(iters)))
    print(np.mean(np.array(times)))
    print(np.std(np.array(times)))


sampleSize=-1
if(sampleSize>0):
    outputs = np.fromfile('outData.bin',dtype=np.float32).reshape((-1,1))[0:sampleSize,:].reshape((-1,1))
    inputs = np.fromfile('inData2.bin',dtype=np.float32).reshape((-1,48))[0:sampleSize,:].reshape((-1,48))
else:
    outputs = np.fromfile('outData.bin',dtype=np.float32).reshape((-1,1))
    inputs = np.fromfile('inData2.bin',dtype=np.float32).reshape((-1,48))

inputsLarge = np.repeat(inputs,multFactor,axis=0)
outputsLarge = np.repeat(outputs,multFactor,axis=0)

assert(len(inputsLarge)==len(outputsLarge))
getinfoLR(1,inputsLarge,outputsLarge,1)

#makeLargeData(inputs,outputs,2)
'''
todo = [1,2,4]
for t in todo:
    getinfoLR(t,inputs,outputs,1)
'''
# tried running it this [hadoop@ip-172-31-29-198 ~]$ pyspark --master local[2] --driver-memory 10g --executor-memory 10g

#scp -i /home/bdvr/DATA516/keys/BDVRDATA516KP.pem /home/bdvr/DATA516/avanroi1/Project/launchJupyter.sh hadoop@ec2-18-212-249-123.compute-1.amazonaws.com:~/
#scp -i /home/bdvr/DATA516/keys/BDVRDATA516KP.pem /home/bdvr/DATA516/avanroi1/Project/data/outData.bin hadoop@ec2-18-212-249-123.compute-1.amazonaws.com:~/
#scp -i /home/bdvr/DATA516/keys/BDVRDATA516KP.pem /home/bdvr/DATA516/avanroi1/Project/data/inData2.bin hadoop@ec2-18-212-249-123.compute-1.amazonaws.com:~/
#206196.99001312256 1 iteration 2 nodes
#216386 2 iterations 2 nodes
# 367735 4 iterstions 2 nodes
#

#177871.99001312256,177612.7119064331 1 iteration 8 nodes
#393356, 477420,198135,363895,310144.07300949097 2 iterations 8 nodes
# 255813 4 iterstions 8 nodes

#  scp -i BDVRDATA516KP.pem /home/bdvr/DATA516/avanroi1/Project/inData2.bin  hadoop@ec2-54-224-44-44.compute-1.amazonaws.com:~/
# aws s3 cp  /home/bdvr/DATA516/avanroi1/Project/inData2.bin s3://awsdata516/
