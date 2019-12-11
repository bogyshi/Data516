
# Project Proposal: Spark and Machine Learning Scalability locally and in parallel
## Author: Alexander Van Roijen
## Date: 11/2/19
## Data: https://data.london.gov.uk/dataset/smartmeter-energy-use-data-in-london-households (~1GB w/out joins. Potentially up to 10GB w/joins)

## Objective:
I seek to understand the tradeoffs in performance (run time) in a standard logistic regression classification problem on smart meter energy task.

In particular, I am aiming to discover how a locally run GPU enabled logistic regression algorithm fairs in performance to a Spark frameworks attempt at the same problem. Formally, my hypothesis is that a GPU enabled instance locally has the benefit of executing large cross products in parallel over the Spark framework, showing an improvement in performance on the same size dataset. Thus, my prediction is that doing a classification task using logistic regression on my local machine with a GTX 960 (1024 cores) and 16gb of RAM and an AMD FX 8320 fm processor will have a lower execution time than the Spark framework on AWS with one master node and two worker nodes.

The particular use of the data will be, given a row containing the smart-meter readings for a random household throughout the day at 30 minute intervals,I want to know if the house it belongs to is from a wealthy, average, or low income neighborhood. Or perhaps instead if it belongs to a house in a neighborhood that is mostly young children, or older people. The exact specifics of what will be classified is to be determined. But for now, it will be logistic regression using gradient descent on half hour interval data throughout an entire day (or perhaps an aggregate over all days belonging to the same house), and asking it to classify in a one-vs-one or one-vs-rest manner, what kind of neighborhood it belongs to. Note, I will be running this classification task thoroughly, so as to ensure the warm-up penalty for loading the data into memory doesnt adversely impact the Spark framework.

## Computing Resources: Spark on AWS EMR instance, 1 master node, 2 worker nodes. V.S. GTX 960, amd fx 8320, 16gb ram w/SSD.

## People involved: Myself, and potentially instructors for advice on running this on Spark efficiently
