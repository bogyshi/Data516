-- What is the total number of parts offered by each supplier? The query should return the name of the
--supplier and the total number of parts.

Select S_Name, SUM(PS.PS_AvailQty)
from supplier S, partsupp PS, part P
where PS.PS_PartKey = P.P_PartKey and PS.PS_SuppKey = S.S_SuppKey
group by S.S_Name;

--Query completed in 0.564 seconds
-- 10000 rows
/*
1

Supplier#000007502

420818
2

Supplier#000007509

421890
*/

-- What is the cost of the most expensive part by any supplier? The query should return only the price of
-- that most expensive part. No need to return the name.
Select max(P_RetailPrice) from part;
-- returned val: 	2098.99
-- Query completed in 0.453 seconds
-- num rows: 1

-- What is the cost of the most expensive part for each supplier? The query should return the name of the
--supplier and the cost of the most expensive part but you do not need to return the name of that part.
Select S_Name, max(P.P_RetailPrice)
from supplier S, partsupp PS, part P
where PS.PS_PartKey = P.P_PartKey and PS.PS_SuppKey = S.S_SuppKey
group by S.S_Name;

-- Query completed in 0.759 seconds
/*
1

Supplier#000007502

2076.98
2

Supplier#000007509

2083.98
*/
-- 10000 rows returned

-- What is the total number of customers per nation? The query should return the name of the nation
--and the number of unique customers.

Select N_Name, count(distinct C_CustKey)
from Customer C JOIN Nation N ON N.N_NationKey = C.C_NationKey
group by N_Name;

-- Query completed in 0.604 seconds
/* first 2
1
PERU

5975
2

KENYA

5992
*/
-- 25 rows

-- What is number of parts shipped between 10 oct, 1996 and 10 nov, 1996 for each supplier? The query
--should return the name of the supplier and the number of parts

Select S_Name, count(distinct L_OrderKey) as tot
from lineitem L, Supplier S
where L.L_SuppKey = S.S_SuppKey and
L.L_ShipDate between '10/10/1996' and '10/11/1996'
group by S_Name
order by tot;

Select S_Name, sum(flag) as tot from
(
  Select S_Name, CASE
  	WHEN L_ShipDate between '10/10/1996' and '10/11/1996' THEN 1
  	ELSE 0
  END as flag
  from supplier S JOIN lineitem L ON S.S_SuppKey = L.L_SuppKey
) as nw
group by S_Name;

-- Query completed in 0.839 seconds
/*1

Supplier#000003928

0

Supplier#000009569

2
*/
-- num rows returned: 10000

/*
A customer is considered a Gold customer if they have orders totalling more than $1,000,000.00.
Customers with orders totalling between $1,000,000.00 and $500,000.00 are considered Silver. Write
a SQL query to compute the number of customers in these two categories. Try different methods of
2writing the query (only SQL or use a UDF or a View to categorize a user). Discuss your experience
with the various methods to carry out such analysis. Use the 1GB data set and the 2-node cluster. (10
points)
*/
--v1
Select  gs2.membership, count(*)
from
(
  Select CASE
    WHEN gs.totalConsumption>1000000 THEN 'gold'
    ELSE silver
    END as membership
    from (
    Select O_CustKey,SUM(O_TotalPrice) as totalConsumption
    from orders O, customer C
    where C_CustKey = O_CustKey
    group by O_CustKey
    having totalConsumption > 500000
  ) as gs
) as gs2
group by gs2.membership;

--Query completed in 0.871 seconds
/*
gold

99091
2

silver

798
*/
--v2
create function f_py_greater (totalConsumption float)
returns varchar(6)
stable
as $$
if totalConsumption > 1000000:
  return "Gold"
else:
  return "Silver"
$$ language plpythonu;

Select  gs2.membership, count(*)
from
(
  Select f_py_greater (gs.totalConsumption) as membership
    from (
    Select O_CustKey,SUM(O_TotalPrice) as totalConsumption
    from orders O, customer C
    where C_CustKey = O_CustKey
    group by O_CustKey
    having totalConsumption > 500000
  ) as gs
) as gs2
group by gs2.membership;

-- Query completed in 2.441 seconds
/*
1

Gold

99091
2

Silver

798
*/
-- num rows returned 2
