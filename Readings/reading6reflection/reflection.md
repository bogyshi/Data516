# Reading 6 reflection

## Articles and links
Jure Leskovec, Anand Rajaraman, and Jeffrey D. Ullman. Mining of Massive Datasets. [pdf]


Chapter 3 Similar Items, read only sections 3.1 through 3.4.

Suggested discussion points: what are some applications of the Jaccard similarity? What is the purpose of the minhash signature?  What is the purpose of LSH applied to minhash signatures?

Chapter 4 Streaming Algorithms:

Section 4.1
Section 4.2
Section 4.3
Section 4.4
Sections 4.5.1-4.5.3

Suggested discussion points: pick your own.  Note that some of these topics were discussed in class; the only new topic is the hyperloglog algorithm.

## Notes

I understand the explanation of why larger shingles hashed down to four bytes is better than 4 bytes of plain k=4 shingles. 
its because we know that not all characters are created equal, or at least not used as often. Meaning that the amount of unique possibilities is still is at least, if not more, equivalent, due to the favoritism of vertain characters, so a compressed higher shingle k is better than one of the same size that is less in uniqueness

This subject of minhasing and jaccard similarity is really well explained here. Further, a good point is raised about how getting random permuted matrices of our rows of our characteristic matrix is not feasible for very large ones.

Great recap as well at the end of section 3.4

Real world examples in sec 4.1 are awesome.

determining moments has a similar notion / principle to determining unique counts of users

Further, many of these calculations involve the probablity that approximates 1/epislome ^ episolom or something like that

## Reflection

Stream processing, I think, will become the norm as we move ahead. Privacy regulations and standards will continue to become increasingly well defined and stringent. Not wanting to hold onto data and risk both privacy and security risks, lets just pass through the data once and forget about it afterwards. I also very much enjoyed their discussion of approximation algorithms. I appreciated their examples used to help re-enforce information. This is one of the few readings where I wasnt left with many lingering questions. I feel I understood most of this reading quite well and want to learn more about both of these concepts

