from pyspark.sql.functions import *
from graphframes import *


# Obtain departure Delays data
delay = spark.read.csv("s3n://csed516/Flights/flights.csv", header="true",inferSchema="true")
delay.registerTempTable("departureDelays")
delay.cache()
# Obtain airports dataset
airports = spark.read.csv("s3n://csed516/Flights/airports.csv", header="true", inferSchema="true")
airports.registerTempTable("airports")

# create trip IATA codes table
tripIATA = sqlContext.sql("select distinct IATA from(select distinct ORIGIN as iata from departureDelays union all select distinct DEST as iata from departureDelays) a")
tripIATA.registerTempTable("tripIATA")

#merge airport data with tripIATA data
airports = sqlContext.sql("select f.IATA_CODE as IATA, f.City, f.State, f.Country from airports f join tripIATA t on t.IATA = f.IATA_CODE")
airports.registerTempTable("airports")
airports.cache()
# Build `departureDelays_geo` DataFrame
# Obtain key attributes such as Date of flight, delays, distance,
# and airport information (Origin, Destination)
departureDelays_geo = sqlContext.sql("select cast(f.FL_DATE as int) as tripid,cast(concat(concat(concat(concat(concat(concat('2017-',concat(concat(substr(cast(f.FL_DATE as string), 1, 2), '-')),substr(cast(f.FL_DATE as string), 3, 2)), ' '), substr(cast(f.FL_DATE as string), 5, 2)), ':'),substr(cast(f.FL_DATE as string), 7, 2)), ':00') as timestamp) as localdate,cast(f.DEP_DELAY as int) as delay, f.ORIGIN as src, f.DEST as dst, o.city as city_src,d.city as city_dst, o.state as state_src, d.state as state_dst from departuredelays f join airports o on o.IATA = f.ORIGIN join airports d on d.IATA = f.DEST")
departureDelays_geo.registerTempTable("departureDelays_geo")
# Cache and Count
departureDelays_geo.cache()
departureDelays_geo.count()


tripVertices = airports.withColumnRenamed("IATA", "id").distinct()
tripEdges = departureDelays_geo.select("tripid", "delay", "src", "dst", "city_dst", "state_dst")
# Cache Vertices and Edges
tripEdges.cache()
tripVertices.cache()
#lets look at the vertices and edges
tripVertices.show()
tripEdges.show()
#build a graph!
tripGraph = GraphFrame(tripVertices, tripEdges)
print tripGraph

print "Airports: %d" % tripGraph.vertices.count() # 299
print "Trips: %d" % tripGraph.edges.count() # 1526121, which makes sense with previous resultson the flights departure geo count

## What airport has the most number of flights incoming and outgoing?
mostTrips = tripGraph.degrees.orderBy(desc("degree")).show(1)
'''
+---+------+
| id|degree|
+---+------+
|ATL|193125|
+---+------+
'''

# run with tolerance
pageRankRes = tripGraph.pageRank(tol=0.01)
pageRankRes.vertices.orderBy(desc('pagerank')).show(30)
'''
+---+-----------------+-----+-------+------------------+
| id|             City|State|Country|          pagerank|
+---+-----------------+-----+-------+------------------+
|ATL|          Atlanta|   GA|    USA| 18.16277471770515|
|ORD|          Chicago|   IL|    USA|14.365606213272654|
|DEN|           Denver|   CO|    USA|10.734057987260552|
|LAX|      Los Angeles|   CA|    USA| 8.563547592457423|
|DFW|Dallas-Fort Worth|   TX|    USA| 8.182678023555283|
|MSP|      Minneapolis|   MN|    USA|7.4711217290504885|
|SFO|    San Francisco|   CA|    USA| 7.450839560309138|
|SEA|          Seattle|   WA|    USA| 7.113815498333691|
|IAH|          Houston|   TX|    USA| 6.739584713692203|
|DTW|          Detroit|   MI|    USA|6.4460466952784845|
|PHX|          Phoenix|   AZ|    USA| 6.364348943146698|
|SLC|   Salt Lake City|   UT|    USA| 6.141559957164036|
|LAS|        Las Vegas|   NV|    USA| 5.815261139941022|
|MCO|          Orlando|   FL|    USA| 5.589604466141755|
|BOS|           Boston|   MA|    USA| 4.939447053195026|
|EWR|           Newark|   NJ|    USA| 4.640421073897751|
|CLT|        Charlotte|   NC|    USA| 4.409029234242264|
|BWI|        Baltimore|   MD|    USA| 4.219631759970167|
|JFK|         New York|   NY|    USA| 4.110200567826439|
|FLL|   Ft. Lauderdale|   FL|    USA|3.6988063727658105|
|LGA|         New York|   NY|    USA|3.6477093408903656|
|MDW|          Chicago|   IL|    USA|3.6258455101664597|
|SAN|        San Diego|   CA|    USA|3.4896063252405978|
|PHL|     Philadelphia|   PA|    USA| 3.092881852031952|
|DCA|        Arlington|   VA|    USA| 2.873439286100013|
|PDX|         Portland|   OR|    USA| 2.825479255631742|
|TPA|            Tampa|   FL|    USA|2.7243711434705467|
|DAL|           Dallas|   TX|    USA|2.7217692541815843|
|MIA|            Miami|   FL|    USA|  2.71455513110814|
|ANC|        Anchorage|   AK|    USA| 2.687030121421858|
+---+-----------------+-----+-------+------------------+
'''
