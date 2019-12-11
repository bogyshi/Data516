# Reading 3 Reflection
Jeffrey Dean and Sanjay Ghemawat. MapReduce: Simplified Data Processing on Large Clusters. OSDI'04. [pdf].

Read only sections 1,2,3
This is understanding how map reduce works

D. DeWitt and M. Stonebraker. Mapreduce – a major step backward. In Database Column (Blog), 2008.  [pdf].

5 main problems with map reduce
1) it isnt novel , tech was around since the 80s, HOWEVER, it does package it together more nicely?
2) No indexing, does brute force instead (but nicer over the scale? better for anything that is an aggregate rather than search?)
3) mapreduce doesnt use schemas or a high level language (not relational), makes it difficult to use
4) missing common functionality, like views, schemas, indexing, updates, integrity and referential integrity constraints
5) not compatible with modern DBMS tools, like data mining tools, BI tools ... Not that important imo, but i dont use it for these things, should I?

Ashish Thusoo, Joydeep Sen Sarma, Namit Jain, Zheng Shao, Prasad Chakka, Ning Zhang, Suresh Anthony, Hao Liu, Raghotham Murthy: Hive - a petabyte scale data warehouse using Hadoop. ICDE 2010: 996-1005. [pdf].

Read sections 1, 2, and skim through section 4 (focus on the optimizations)

No insert, update, or delete is pretty ridiculous. I need to create a new table with every new snapshot? What about transactions?

Are there any query execution plans that are not acyclic? why would we have a loop? would that mean its not determnitistic ?

HiveQL sits on top of HDFS and allows for sql like queries as well as low level map reduce code. In general this new layer is meant to provide some optimizations for facebook needs as well as create a higher level language for map reduce functionality with SQL like queries.

"Map side joins – In the cases where some of
the tables in a join are very small, the small
tables are replicated in all the mappers and
joined with other tables." - is this a broadcast join?

can add more rules / transformations for the optimizer, which is really good.

re partionitioning for spatial aggregation, is this such that for a common value, say seattle, i could subdivide my groupby into smaller pieces and then add them back up? is this like the average calculation?

Execution engine seems to not use pipeline parallelism

Suggested discussion topics:

How do these three papers fit together?  What is the big story that they are telling?
What are some advantages/disadvantages of MapReduce compared to parallel databases? How does MapReduce address skew?  How does MapReduce address worker failures?
Why was MapReduce needed in Facebook? Why was it insufficient?  What are some limitations of HiveSQL?  Why does it only support only INSERT OVERWRITE?  What are some of the optimizations in Hive?

## Discussion
There is a clear flow of papers here. We first learn a bit about the inner workings of MapReduce, what its benefits are in fault tolerance and parallelism and relatively simple philosophy for computation (you have mappers and reducers, thats it!). Then we have our paper by DeWitt and Stonebraker (awesome name) that raises valid issues with MapReduce. I would agree the indexing is quite powerful and likely out performs MapReduce for search /scan operations. Finally, the paper on Hive from Ashish et al. seems to relieve many of the concerns expressed by DeWitt and Stonebraker. They allow for SQL like queries on the MapReduce framework, which was another troubling point for DeWitt and Stonebraker. It also seems to address skew by using a multiple round repartitioning scheme (I think?). Sounds like that it tries to re-hash and distribute values from the map phase to the reduce phase. For example, if Seattle, WA was a really skewed key, it re-hashes and transmits the data to be handled by other reducers. Or at least that is my guess. Other optimizations in Hive include the relational algebra shortcuts we discussed, such as moving down selections as far down the execution plan. This fails to mention the other shortcuts, including join reordering and some others I cant fully remember.

Things im unsure of:
Why does hive only support insert overwrite? I think it had to deal with simplicity? updating tables is hard and takes a lot of time. but there is no index, so it shouldnt be that much of a problem.
