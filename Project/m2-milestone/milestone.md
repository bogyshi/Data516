
# Project Milestone: Spark and Machine Learning Scalability locally and in parallel
## Author: Alexander Van Roijen
## Date: 11/23/19
## Data: https://data.london.gov.uk/dataset/smartmeter-energy-use-data-in-london-households (~1GB w/out joins. Potentially up to 10GB w/joins)

### Computing Resources: Spark on AWS EMR instance, 1 master node, 2 or 8 worker nodes. V.S. GTX 960, amd fx 8320, 16gb ram w/SSD.

## Introduction:
Apache Spark and Nvidia Cuda both provide forms of parallelism for machine learning tasks. However, what are the limitations of each? Are there times when one outperforms the other? Overall, I seek to understand when one should use each. I will show that CUDA can perform better for small data sets (<1.5GB) using at GTX 960 to implement logistic regression compared to pyspark on AWS EMR. I will also demonstrate the bottle-neck effects on logistic regression on CUDA and the scale up / speed up of logistic regression on Spark with increasing available nodes and data set size.

## Evaluated Systems
  - Spark: Built on top of HDFS, this aims to act as a map reduce system, but with improvements for various tasks that involve multiple iterations over the same data. Sparks MLLib promises various popular ML algorithms that should be able to use its persistent memory and lineage graph resilience to great advantage
  - CUDA: A set of extensions built on top of C++ and its compiler that allow users to execute chunks of c++ code on their graphics card instead of their CPU. This gives users great flexibility to alternate between CPU and GPU processing for various tasks. CUDA is commonly used for various tasks, including machine learning tasks and training neural networks.

## Problem Statement

- 1) What preforms best on logistic regression for our UK Smart Meter data? Will the bottlenecks of CUDA prove too hampering for even small data sets? Or will it still achieve high levels of a parallelism? Even so, will its level of parallelism beat Sparks distributed performance on 2,4, or 8 worker nodes on AWS EMR?
- 2) If my hypothesis that CUDA outpreforms spark on small data, is there a point where Spark will outperform CUDA? If we increase the size of our data (artificially or not), what is this breaking point ? 10GB, 20GB, 100GB?

## Method
- I implemented logistic regression in C++ 11 with CUDA extensions enabled. The raw data was converted to fit a logistic regression based task where I attempt to classify whether a sample of a households energy consumption throughout a day is indicative of a house that is under Time of Use (ToU) or standard (std) pricing. Discussion on ToU

### The Data
*Data is publicly licensed and is allowed to be used for any purpose with proper accreditation to the UK Power Network and its partners, see references for details*
- Data was converted into a format where a row represents 48 half hour intervals and their corresponding energy consumption in kilowatts per half hour (KW/hh). All in all, we have approximately 2 million rows, with 48 columns representing our input. Our output was a 0 or 1 label representing std or ToU respectively with the same number of rows. All in all, about 0.5 GBs was generated and dumped into binary files for both processes.



With the data in hand, Pyspark's MLLib Logistic Regression was used on an AWS EMR cluster with either 2 or 8 worker nodes. Meanwhile, CUDA used my personal device, a GTX 960, which can hold up to 2GB of memory and has 1024 threads available to execute instructions in parallel.

## Results
*These results are tentative, and are subject to change with the incoming final report*
!["Execution time for 1,2, and 4 iterations on spark with 2 and 8 worker nodes"](../sparkResults.jpg "Execution time for 1,2, and 4 iterations on spark with 2 and 8 worker nodes")

!["Execution time for 200 iterations on CUDA with varying thread counts"](../CUDAResults.jpg "Execution time for 200 iterations on CUDA with varying thread counts")

We can see that on the original size of our dataset, CUDA preforms with much greater speed. Comparing the best case iteration time for both spark and CUDA, we see an approximate 300x speedup per iteration when using CUDA (<200ms per iter vs ~63750)

However, we know that Spark was meant to handle very large data sets. With only 0.5 GBs of data, is this really a fair comparison? Future results will include some analysis on artificially increased data.

### Complexity

CUDA on its own takes more effort to learn and program efficiently than spark on its own. The code to run the logistic regression example was about 400 lines of code that required plenty of error checking and documentation checking. Meanwhile, the spark code used to generate the results shown are only around 70 lines of code. I am biased in that I come from a rather techincal background and have used CUDA in the past, more-so than spark. However, for now I will say that CUDA is clearly better for those looking to parallelize computations on data under 2GB in size.

## Conclusion

There is a clear victor in this race when it comes to smaller scale data. Assuming we can store all data on our graphics card, and that there is minimal locking, we can expect great parallelized performance. Future work will have to be devoted to understanding how various tasks

## References
- Zaharia, M., Chowdhury, M., Das, T., Dave, A., Ma, J., McCauley, M., ... & Stoica, I. (2012, April). Resilient distributed datasets: A fault-tolerant abstraction for in-memory cluster computing. In Proceedings of the 9th USENIX conference on Networked Systems Design and Implementation (pp. 2-2). USENIX Association.
- Piggott, G (June 24th, 2015). Electricity Consumption in a Sample of London Households. Retrieved from https://data.london.gov.uk/blog/electricity-consumption-in-a-sample-of-london-households/
- UK Power Networks. (2015). SmartMeter Energy Consumption Data in London Households [Zip, Data File]. Retrieved from https://data.london.gov.uk/dataset/smartmeter-energy-use-data-in-london-households
- Terms and Conditions. (2019). Retrieved November 22, 2019, from London Data Store, London Data Store Terms and Conditions. Website, https://data.london.gov.uk/about/terms-and-conditions/
