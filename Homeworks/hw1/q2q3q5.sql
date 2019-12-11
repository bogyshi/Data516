-- What is the total number of parts offered by each supplier? The query should return the name of the
--supplier and the total number of parts.

Select S_Name, SUM(PS.PS_AvailQty)
from supplier S, partsupp PS, part P
where PS.PS_PartKey = P.P_PartKey and PS.PS_SuppKey = S.S_SuppKey
group by S.S_Name;

--Query completed in 1.892 +1.752+1.700+1.739, min 1.700, avg 1.77, max 1.892
-- 100000 rows
/*
1
Supplier#000025002

454730
2

Supplier#000025004

367204
*/

-- What is the cost of the most expensive part by any supplier? The query should return only the price of
-- that most expensive part. No need to return the name.
Select max(P_RetailPrice) from part;
-- returned val: 	2098.99
--  Query completed in 0.488 +0.412+0.448+0.435
-- num rows: 1

-- What is the cost of the most expensive part for each supplier? The query should return the name of the
--supplier and the cost of the most expensive part but you do not need to return the name of that part.
Select S_Name, max(P.P_RetailPrice)
from supplier S, partsupp PS, part P
where PS.PS_PartKey = P.P_PartKey and PS.PS_SuppKey = S.S_SuppKey
group by S.S_Name;

-- Query completed in 1.644 +1.562+1.717+0.937
-- 100000 rows returned
/*
Supplier#000000008

2072.95
2

Supplier#000000009

2073.95
*/

-- What is the total number of customers per nation? The query should return the name of the nation
--and the number of unique customers.

Select N_Name, count(distinct C_CustKey)
from Customer C JOIN Nation N ON N.N_NationKey = C.C_NationKey
group by N_Name;

-- Query completed in 0.505 +0.464+0.439+0.460
-- 25 rows
/* first 2
MOZAMBIQUE

59796
2

ROMANIA

60048
*/

-- What is number of parts shipped between 10 oct, 1996 and 10 nov, 1996 for each supplier? The query
--should return the name of the supplier and the number of parts

Select S_Name, sum(flag) as tot from
(
  Select S_Name, CASE
  	WHEN L_ShipDate between '10/10/1996' and '10/11/1996' THEN 1
  	ELSE 0
  END as flag
  from supplier S JOIN lineitem L ON S.S_SuppKey = L.L_SuppKey
) as nw
group by S_Name;

-- Query completed in 3.606 + 2.936 +3.826 + 3.107
-- num rows returned: 100000
/*1

Supplier#000036999

1

Supplier#000081864

0
*/

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
    ELSE 'silver'
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

--Query completed in 1.271 seconds
/*
1

gold

981185
2

silver

18132
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

-- Query completed in 13.602 seconds
/*
1

Silver

18132
2

Gold

981185
*/
-- num rows returned 2


--QUESTION 3
-- What is the total number of parts offered by each supplier? The query should return the name of the
--supplier and the total number of parts.

Select S_Name, SUM(PS.PS_AvailQty)
from supplier S, partsupp PS, part P
where PS.PS_PartKey = P.P_PartKey and PS.PS_SuppKey = S.S_SuppKey
group by S.S_Name;

--Query completed in 1.732+1.481+1.417+0.832, min 0.832, avg: 1.3655, max: 1.732
-- 100000 rows
/*
Supplier#000050002

410759
2

Supplier#000050005

390050
*/
--checkpoint, all of the first query done
-- What is the cost of the most expensive part by any supplier? The query should return only the price of
-- that most expensive part. No need to return the name.
Select max(P_RetailPrice) from part;
-- returned val: 	2098.99
--  Query completed in 0.374+0.381+0.433+0.389, min: 0.381 avg 0.394 max 0.433
-- num rows: 1
-- checpoint all of the seond query done

-- What is the cost of the most expensive part for each supplier? The query should return the name of the
--supplier and the cost of the most expensive part but you do not need to return the name of that part.
Select S_Name, max(P.P_RetailPrice)
from supplier S, partsupp PS, part P
where PS.PS_PartKey = P.P_PartKey and PS.PS_SuppKey = S.S_SuppKey
group by S.S_Name;

-- Query completed in 1.417+1.744+1.861+1.834 min 1.417 avg 1.714 max 1.861
-- 100000 rows returned
/*
1

Supplier#000025006

2097.96
2

Supplier#000025016

2097.91
*/

-- What is the total number of customers per nation? The query should return the name of the nation
--and the number of unique customers.

Select N_Name, count(distinct C_CustKey)
from Customer C JOIN Nation N ON N.N_NationKey = C.C_NationKey
group by N_Name;

-- Query completed in 0.439,0.586,0.386,0.452 min 0.386 avg 0.466 max 0.586
-- 25 rows
/* first 2
CHINA

60065
2

UNITED STATES

60006
*/

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


-- Query completed in 2.611,2,994,3.40,1.997, min: 1.997, avg 2.7505, max: 3.40
-- num rows returned: 100000
/*1

Supplier#000078610

0

Supplier#000065244

0
*/

--QUESTION 5
Select S_Name, SUM(PS.PS_AvailQty)
from tpchs4.supplier S, tpchs4.partsupp PS, tpchs4.part P
where PS.PS_PartKey = P.P_PartKey and PS.PS_SuppKey = S.S_SuppKey
group by S.S_Name;

--Query completed in 8.419, 7.760,9.453,8.508, min: 1.760, avg:8.54, max: 9.453
-- 100000 rows
/*
Supplier#000000010

409827
2

Supplier#000000015

394833
*/

-- What is the cost of the most expensive part by any supplier? The query should return only the price of
-- that most expensive part. No need to return the name.
Select max(P_RetailPrice) from tpchs4.part;
-- returned val: 	2098.99
--  Query completed in 1.621,1.338,1.256,1.422 min: 1.256, avg: 1.41, max: 1.621
-- num rows: 1
-- checpoint all of the seond query done

-- What is the cost of the most expensive part for each supplier? The query should return the name of the
--supplier and the cost of the most expensive part but you do not need to return the name of that part.
Select S_Name, max(P.P_RetailPrice)
from tpcsh4.supplier S, tpchs4.partsupp PS, tpchs4.part P
where PS.PS_PartKey = P.P_PartKey and PS.PS_SuppKey = S.S_SuppKey
group by S.S_Name;

-- Query completed in 7.455,7.757, 7.485,7.868, min: 7.455. avg: 7.64, max: 7.868
-- 100000 rows returned
/*

Supplier#000000003

2073.98
2

Supplier#000000006

2072.96
*/

-- What is the total number of customers per nation? The query should return the name of the nation
--and the number of unique customers.

Select N_Name, count(distinct C_CustKey)
from tpchs4.Customer C JOIN tpchs4.Nation N ON N.N_NationKey = C.C_NationKey
group by N_Name;

-- Query completed in 4.62+4.163+3.781+4.199 seconds, min: 3.781, avg: 4.19, max: 4.62
-- 25 rows
/* first 2
ALGERIA

59916
2

ARGENTINA

59841
*/

-- What is number of parts shipped between 10 oct, 1996 and 10 nov, 1996 for each supplier? The query
--should return the name of the supplier and the number of parts

Select S_Name, sum(flag) as tot from
(
  Select S_Name, CASE
  	WHEN L_ShipDate between '10/10/1996' and '10/11/1996' THEN 1
  	ELSE 0
  END as flag
  from tpchs4.supplier S JOIN tpchs4.lineitem L ON S.S_SuppKey = L.L_SuppKey
) as nw
group by S_Name;
--times 18.538+19.479+18.563+18.529, min: 18.529, avg: 18.78, max: 19.479
-- 100000 rows returned

/*
Supplier#000000012

0
2

Supplier#000000013

0
*/
