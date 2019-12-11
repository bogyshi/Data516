import logging
import re
import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import StandardOptions
#from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.metrics import Metrics
from apache_beam.metrics.metric import MetricsFilter
import time

logging.getLogger().setLevel(logging.ERROR)
logging.basicConfig()
inFile ="muchAdo.txt"
outFile = "test.txt"
outFile2 = "test23.txt"
outFileHamlet = "test23Hamlet.txt"

#output_file ="simple_counts"

def classExample(line):
    # stolen from class notebook
    text_line = line.strip()
    words = re.findall(r'[A-Za-z\']+', text_line)
    return words

def countWordsOfLine(line):
    numWords = 0
    for x in line.strip().split(' '):
        if(x.isalpha()):
            numWords+=1
    return numWords

def countWordsOfLine2(line):
    arr=[]
    for x in line.strip().split(' '):
        arr.append(x.isalpha())
    return arr

options = PipelineOptions()
options.view_as(StandardOptions).runner ='DirectRunner'

#Set pipeline options
p = beam.Pipeline(options=options)
# Lines transform read the text from input file and to create a PCollection which contains all the text lines
lines = p |"read">> ReadFromText(inFile)
#Counts is a ParDo transform that invokes a function process_lines
#on each element that tokenizes the text lines into individual words
#this is then transformed to a tuple ('word',count) and grouped and counted to
#emit the outputs.
debug=2
if(debug==0):
    counts = ( lines
        | "split" >> beam.ParDo(classExample).with_output_types(str)
        | "pair_with_1" >> beam.Map(lambda x:(x,1))
        | "group" >> beam.GroupByKey()
        | "count" >> beam.Map( lambda x: (x[0], sum(x[1])))
    )
    output = counts | "format" >> beam.Map(lambda x:"%s: %s"%(x[0],x[1]))
    output | "write" >> WriteToText(outFile)
elif(debug == 1):
    sum = ( lines
        | "get_counts" >> beam.ParDo(countWordsOfLine2)
        | "pair_with_1" >> beam.Map(lambda x:(x,1))
        | "group" >> beam.GroupByKey()
        | "total" >>  beam.Map( lambda x: (x[0], sum(x[1])))
    )

    output2 = sum | "format" >> beam.Map(lambda x:"%s: %s"%(x[0],x[1]))
    output2 | "write" >> WriteToText(outFile2)
else:
    counts = ( lines
        | "split" >> beam.ParDo(classExample).with_output_types(str)
        | "pair_with_1" >> beam.Map(lambda x:(x,1))
        | "group" >> beam.GroupByKey()
        | "count" >> beam.Map( lambda x: (sum(x[1])))
        | beam.CombineGlobally(sum)
    )
    counts | "write" >> WriteToText(outFile2)



# now this gets the number of occurences of each word. What we want is a sum


times = time.time()
result = p.run()
rtime = times-time.time()
print(rtime)
result.wait_until_finish()
