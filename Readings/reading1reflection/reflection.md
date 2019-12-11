# Reading 1 Reflection
- There are two forms of parallelism we can enjoy in shared nothing architecture
  - pipelined parallelism gives us the ability to pass on result from one computation ahead to the next stage of computation. Given enough processors, we can begin the second stage of processing rather than sitting around waiting for the entirety of the first set of computations to finish
  - partitioned parallelism allows several processors p to work independently of each other (ideally) on an even slice of the data (ideally). This lets us beat sequential processing easily

- Brent's Theorem gives us a good way to provide upper and lower bounds to our theoretical run times given a finite number of processors p .
- In particular, we know it is something less than the utopian infinite processor parallel run time, and a single thread run time with the ideallic perfect parallelism on a finite set of p processes (in an equation it would be something like $\frac{T_1}{p} \le T_p \le T_\inf + \frac{T_1}{p}$)

- The difficulty of parallel join is that we need to send the results of two tables into a shared node in the next stage to then join on a particular value.

- The relational model gives a great amount of latitude in how the actual execution of a query is d one.
  - The main benefit being we can iteratively improve the optimizer on the relational algebra side of things as we continue to advance our understanding of our parallelism (this ties into the query execution plan and optimizer we talked about last week)
