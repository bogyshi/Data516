# Reading 4 reflection

The Snowflake Elastic Data warehouse, Dageville et al. 2015

# Notes
Feels like the main benefit of snowflake is its ability to handle unstrutured data like IoT and social media / cellphone data.

Pure Saas experience. So i dont need to choose a size or something? Not sure what the benefit is. Seems like a magic wave to say its easier even though i feel like i could just as easily run queries on AWS redshift.

Redshift is also similarly elastic

heterogenous workload is a good argument for seperation of hardware and computer

"It also enables
Snowflake to efficiently process DAG-shaped plans, as
opposed to just trees, creating additional opportunities
for sharing and pipelining of intermediate results."

ELT vs ETL. ELT sounds promising, but i dont fully understand it, or its drawbacks.

"no metadata for untyped data". This is particularly bad for pruning. It sounds like this means they do have some kind of index for the columnar storage (min max, std dev). I guess this isnt indexing, but seems to be part of it?

"Standard errors were insignificant and
thus omitted from the results." This makes no sense, there is not such thing as an insignificant standard error. It can be really small, but that can still mean something. The word "significance" should not be used here.

Something tells me columnar storage is not good for genomic sequencing work

# Reflection

Overall, I was most impressed by snowflakes ability to handle unstructured data quite well and its shared memory architecture. The shared nothing does make scaling a bit harder, as now our data has to be re-partitioned, or, somehow smartly transferred between machines as I add or remove machines. The mindset of heterogeneous workloads is also quite smart. However, in general, all the things snowflake achieves seems achievable with our current technologies. It does make things easier, ill at least give it this amount of credit. Its security features are nice, as I dont know the security architecture of any other data warehousing service.

    What is elasticity, why is it important, and how is it supported in Snowflake?

Elasticity is the ability of our system to handle workloads of various sizes by allocating various amounts of the warehouses to different tasks depending on the demand

    How is data storage handled in Snowflake, and why?  What would have been the alternatives?

Storage is done by amazons s3 which has a great amount of fault tolerance. This gives them the guarantees for their customers. They could create their own storage units, but this would prevent their infinitiely expanadable storage, and would also be much more comples on their end to handle.

    How are worker failures handled in Snowflake?  How does this compare to MapReduce?

MapReduce writes everything to disk, which snowflake does not. This saves us space, but means that if any node fails during the execution of a query, it needs to restart its entire operation.
   
    How does snowflake handle semistructure data?

It infers structure through a bloom filter on each table file, and keeps track of all paths. If a path isnt present, that means its not going to be needed in our query. So it keeps a metadata store with every table file to keep track of what data is available where. It also uses optimistic conversion to retain the raw version of our data and its conversion so we dont lose information on data that oculd be miscontrued as a date time or other type.

## Things i dont understand
 I am still a bit confused by the metadata it collects on the columnar data, along with how it does automatic type detection for unstructured data.
 Furthermore, I am unsure the ELT vs ETL difference, how is this accomplished? How does it make things easier/harder?
