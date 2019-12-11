# Reading 7 reflection

## Articles and links
Da Yan, Yingyi Bu, Yuanyuan Tian and Amol Deshpande (2017), "Big Graph Analytics Platforms", Foundations and Trends in Databases: Vol. 7: No. 1-2, pp 1-195.

Read Chapters 3-5.[pdf].

The Design and Implementation of Modern Column-Oriented Database Systems Daniel Abadi, Peter Boncz, Stavros Harizopoulos, Stratos Idreos, Samuel Madden. Foundations and Trends® in Databases (Vol 5, Issue 3, 2012, pp 197-280)  [pdf].

## Notes

Pregel has checkpoints?

also a bit lost on how aggregation works, do we wait until all mesages from a step come in? dont we already do this?

Is the shared memory abstraction useful for large graph like problems highlighted in section 3.5 only a solution if there is skew? otherwise im not sure how this solves the fact that you dont have neough main memory  to hold everything at once.

out of core execution makes sense, but ties into the hypercube networking alogrithm i think. Can each worker be fully connected to the others?


light weight checkpointing is pretty smart

(2) For algorithms with asymmetric con-
vergence rate, Section 4.2 reviews several systems that adapts Pregel’s
model for asynchronous execution, which schedule the computation fre-
quency of each vertex according to its convergence rate.

wasnt this something highlighted in pregel? like a dynamic workload?

block centric computation
"
but when block-centric computation is used, it is non-trivial to find
a function that maps the IDs of all vertices in a block B to the ID of
the worker that contains B"

I dont fully understand this limitation. Arent all vertexes in a block handled by the same worker? so doesnt when I partition tell me where my vertex is?

Are blocks in blogel basically this subgraph scenario described before.

*Asyncrhonous message passing*
Is stale computation actually worth while? im not sure, only if there is nothing to be gained from any iteration of any other subgraph? A bit skeptical, how does it make up for time lost if there is a value coming in later? Or is this only approximate convergence? tagging messages is interesting, but then i gotta hold onto it

note, online queries vs offline queries indicate if there is a necessary order to them. online being there is a sequential order that may impact future queries e.g. updates

*section 5, shared mem architecture and vector centric queries*
So unlike before, all our neighbors are in the same piece of memory and I can access its vertex and edges through it. No pointer jumping though! not in the same memory!

Specifically, an
input graph is first partitioned among different worker machines, where
each worker W is assigned a subset of vertices V W along with their adja-
cent edges.
This doesnt make sense, wouldnt we want the nodes that are close to each other to be partiitoned together. Otherwise, wed have to go over the network for this information.

edge partitioning seems much smarter, when would this be bad? Probably when i need to send a lot of updates to a vertex and end up having to pass multiple messages / aggregations to a vertex from diff partitions.

Using the bitmap, GraphChi skips the computation
on unflagged vertices. smart way to avoid hte setup of a useless partition, but this doesnt help in stuff like page rank and what not till after at least one iteration, i still need to see every partition


In-edges in each
shard file are sorted by source vertex.
why?
*columnar storage*

To better understand indexing, as discussed here 
always try to propose a set of
“covering” indexes, i.e., a set of indexes where ideally every query can
be fully answered by one or more indexes avoiding access to the base
(row-oriented) data.
Does this mean its using the same offset techinque?ex if I need only one column of data and I know the width, I can load only this data right?

Seems like data locality is important (e.g. a hard disk head doesnt have to travel far to find the next bit of data). This ties into columnar indexes versus storing base data in column format. Indexes tell us where, but we still need to seek quite a bit (I think?).

vectorized processing seems smart for handling intermediate results, but seems like it could be slower due to context shifts selecting vs aggregating

Adaptive execution. also smart. seems like some smarter than CPU execution logic

Also feels like there are typos throughout this. E.g. select statements in figure 4.1

Im glad they highlighted that late materialization doesnt solve all problems.


## Reflection

We focused on vertex architecture for DBMS and the types of analyses we were interested in. Unforauntely, there was no reference to transactio based DBs on these kinds of systems. Does that make sense even? Either way, after an introduction to vertex architectures, there was discussion of block based systems, asyncrhnous message passing, pointer jumping, and shared memory. Partioning on vertex doesnt seem very smart, but partioning on edges does. I suppose they likely have pros and cons to each. 

For column storage, the article certainly lists plenty of pros. However, I have realized that since most of these articles usually refer to one main subject and perhaps the occassional reference to old systems related to it, they dont highlight all possible alternatives. What I mean to say is that there are lots of cool optimizations you can get out of columnar based storage and access, but it doesnt mean its necessarily better, there are plenty of workloads that work much better for row based storage, just as an example, not to mention graph and stream based.

I will further note that columnar storage on its own, as is explained throughout, does okay, but is much better when given many optimizations that can be applied to row based systems as well.


