# Reading 1 Reflection
4.1.1 (takeaway: the Hypercube Algorithm) Notes: Still confused on this slightly
4.1.2 (takeaway: how to compute the optimal shares) Notes: Makes sense, the load is simply contingent on what processor gets the most number of relations to scan through? am i thinking of this correctly?
4.1.3 (takeaway: quick way to compute optimal shares for a uniform db) Seems to me that it would be a uniform amount of processors given to each dimension?
4.1.4 (takeaway: quick way to compute the optimal load for a non-uniform db)
4.1.6 (takeaway: make sure you understand well example 4.5) I understand the linear speedup when R is considered much larger than S and T, but I dont understand the converse
4.2.1 (takeaway: the AGM bound; its application to multi-round parallel computation); skip the last part on the Connection to the Quasi-packing Number.


Reflection:
In general, using multiple rounds with communication can help in a few ways, namely in helping us reduce skew.
The hypercube algorithm can achieve linear speedup in ideal situations (look at notes in) 4.1.6. However, sublinear is plausible assuming no particular dimension or relation has many more tuples than the other two dimensions.
I hope we can discuss some of the terminology and proofs in class, its a bit hard to keep track of some of the variables. I understand that the load seems to be a function of the number of tuples passed to each processor p, but the other terminology, such as tau which is some weighted combination of weights is lost on me.

What i dont understand:
- polytope?
- fractional edge covering number?
- tau is indicative of some optimal share number right?
- How does a multi round query work if the machine is stateles? Are we storing intermediate results on disk?
