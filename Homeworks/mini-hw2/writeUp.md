## Author: Alexander Van Roijen

## Questions
- 1: Purpose of each sample query
  - in a columnar format, we should be able to simply load just one column, user id in this case, and count all those where user_id is 1, rather than load all rows, like we normally would with a traditional row based system. this should be slightly faster.
  - cant read the other queries, so I am unable to determine what their particular purpose is.
  *However* I would venture to guess that from looking at the first query, it is a join on a column where particular column values are stored.
  considering the size of our dataset, I would guess that may cause some slow down, as the more columns we need to pull in data for, the less benefit we get from our column granular data storage.
  Overall, we know that columnar dbms do not handle updates well, which none of these do seemingly, so that is one good thing. Furthermore, it appears that they only request a few columns at a time, but the more columns of data we ask for, the less benefit we get from this column level phyiscal storage.


- 2:
- Query A: Select title,hotness from lobsters.stories order by hotness desc LIMIT 10;
[['GiyBTEsXBR', 99.9885090161], ['qISUKItSwC', 99.9805785608], ['bZYQevPKFy', 99.9792039579], ['zTJAhTqNgJ', 99.962903977], ['xvriRtRrvs', 99.8850728073], ['HaXZaHEWIT', 99.8716577729], ['kjxhCdSYyR', 99.8222696379], ['ZpkldiYJLx', 99.7675826054], ['AsTZYwyOTf', 99.7612080507], ['ZorLovUzWJ', 99.6313168876]]

- 3:
- Query B: Select title,hotness,upvotes,downvotes from lobsters.stories order by upvotes desc, downvotes asc LIMIT 10;
[['CXxOEtHUyp', 19.1955012236, 10, 0], ['FZzvBRTEQL', -96.9180169369, 10, 0], ['WMDJnthHxR', -94.0422849187, 10, 0], ['DdGuGfgMmR', -87.8176832647, 10, 0], ['ZelrXpNakL', 94.4666326731, 10, 0], ['rDefdxZwXE', 45.5148076851, 10, 0], ['csShiBeiUh', -23.7793005072, 10, 0], ['dVfQdzTVDk', 79.3422847424, 10, 0], ['xlqwCAQYTd', 15.0425866041, 10, 0], ['JnjSXezSjL', 91.0533544323, 10, 0]]

### Observation:
Clearly, hotness does not match up with just upvotes and downvotes, I would imagine it has some kind of temporal aspect, as perfectly rated stories can have high positive, high negative, or middling near zero hotness values.

- 4:
Raw time measurements:

71,5,7

70,5,6

74,12,7

69,5,7

77,5,7

68,6,7

- Results
Select * from lobsters.stories;
avg time: ~72ms
Select id from lobsters.stories;
avg time: ~6.2ms
Select id,title from lobsters.stories;
avg time: ~7ms


### Observations:
Intuitively, I would imagine that the first query would take the longest, followed by the third and the second being the shortest as it asks for only one column. This makes sense with our results. Perhaps small sample size makes the impact not as noticeable, along with the small sample size, but we still see the avg times listed above make sense with this theory.
