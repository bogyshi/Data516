# Reading 5 reflection

## Articles and links
SM. Zaharia et al. Resilient distributed datasets: A fault-tolerant abstraction for in-memory cluster computing. In NSDI, 2012. [pdf].

MLlib: Machine Learning in Apache Spark Xiangrui Meng, Joseph Bradley, Burak Yavuz, Evan Sparks, Shivaram Venkataraman, Davies Liu, Jeremy Freeman, DB Tsai, Manish Amde, Sean Owen, Doris Xin, Reynold Xin, Michael Franklin, Reza Zadeh, Matei Zaharia, Ameet Talwalkar Journal of Machine Learning Research, 17 (34), Apr. 2016. [pdf] and also online documentation available here. Make sure to click on "MLLib Guide".

https://spark.apache.org/docs/latest/ml-guide.html

[Optional paper - Read only if you want] Spark SQL: Relational Data Processing in Spark Michael Armbrust, Reynold Xin, Yin Huai, Davies Liu, Joseph K. Bradley, Xiangrui Meng, Tomer Kaftan, Michael Franklin, Ali Ghodsi, Matei Zaharia. ACM SIGMOD Conference 2015, May. 2015. [pdf].

## Notes
Zaharia, RDD paper

1) It says that RDDscan be persisted in multiple ways, but what other way besides in-memory storage? Can I ask it to do on disk storage and have it act like MapReduce? (yes)

2) "They can also ask that
an RDD’s elements be partitioned across machines based
on a key in each record. This is useful for placement op-
timizations, such as ensuring that two datasets that will
be joined together are hash-partitioned in the same way."
is this doing a version of a hypercube algorithm or hash join?

3) in Sec 2.2, looks like i can persist like in map reduce, and can set a priority to put things on disk when there is not enough ram in a particular order.

4)" Our scheduler assigns tasks to machines based on data
locality using delay scheduling [32]. If a task needs to
process a partition that is available in memory on a node,
we send it to that node. Otherwise, if a task processes
a partition for which the containing RDD provides pre-
ferred locations (e.g., an HDFS file), we send it to those."

Feels like this only works out well if all our tasks end up on in memory machines uniquely! What about skew? if my preferred location is the same as one that has it all in memory?

5) check pointing seems really smart. Although the lineage graphs are also really cool.

6) One final question is why previous frameworks have
not offered the same level of generality. We believe that
this is because these systems explored specific problems
that MapReduce and Dryad do not handle well, such as
iteration, without observing that the common cause of
these problems was a lack of data sharing abstractions

Question, why is it that its coarse grained transformations are what allow spark to recover data efficiently? Why wouldnt fine grained be okay?

MlLib paper.

Nice speedup, glad to see that the community is putting a lot of effort into the project. But what is the ALS algorithm?
