USE earthquake_db;

SELECT COUNT(*) AS total
FROM earthquakes;

#1. Top 10 strongest earthquakes (mag).
	##selected my earthquake database and counted the total number of records stored in the earthquakes table
SELECT id, time, place, mag
FROM earthquakes
ORDER BY mag DESC
LIMIT 10;

#2. Top 10 deepest earthquakes (depth_km).
select id, time, place , depth_km
from earthquakes
order by depth_km desc
limit 10;

#3. Shallow earthquakes < 50 km and mag > 7.5.
	#identified the 10 deepest earthquakes by sorting the depth column in descending order and limiting the output to 10 records
select id, time, place, depth_km, mag
from earthquakes
where depth_km < 50 
and mag > 7.5
limit 10;


#4. Average depth per continent.
	#filtered the dataset to identify strong, shallow earthquakes that satisfy both conditions. i used net instead of continent
select round(avg(depth_km),2) as Average_depth , net as Network
from earthquakes
group by net;

#5. Average magnitude per magnitude type (magType).
	#calculated the average earthquake depth for each reporting network. 
    #I used AVG to calculate the average and ROUND to display two decimal places.
select round(avg(mag),3) as Average_Magnitude , magType as Magnitude_types
from earthquakes
group by magType;

#Time Analysis

#6. Year with most earthquakes.
	#extracted the year from the time, grouped earthquakes by year, counted the records in each year, 
    #and returned the year with the highest count.
select year(time) , count(*) as No_of_times
from earthquakes
group by time
order by count(*) desc
limit 1;

#7. Month with highest number of earthquakes.
	#extracted month from time grouped the earthquake records by month name 
    #and identified the month with the highest number of recorded earth
select monthname(time) as Month, count(*) as Highest_earthquakes
from earthquakes
group by monthname(time)
order by count(*) desc
limit 1;

#8. Day of week with most earthquakes.
select dayname(time) as Day , count(*) as No_of_earthquakes
from earthquakes
group by dayname(time)
order by count(*) desc
limit 1;

#9. Count of earthquakes per hour of day.
select hour(time) as per_hrs , count(*) as No_of_earthquakes
from earthquakes
group by hour(time) 
order by per_hrs;


#10. Most active reporting network (net).
select net as active_net_work , count(*) as earthquakes
from earthquakes
group by net
order by count(*) desc
limit 1;
 
 #current dataset does not have this
#11.  Top 5 places with highest casualties. 
#12.  Total estimated economic loss per continent. #current dataset does not show a casualty column
#13.  Average economic loss by alert level.

#Event Type & Quality Metrics
#14.  Count of reviewed vs automatic earthquakes (status).
select status, count(*) as no_of_earthquakes
from earthquakes
group by status;

#15.  Count by earthquake type (type).
select type as earthquake_type , count(*) as No_of_earthquakes
from earthquakes
group by type;

#16.  Number of earthquakes by data type (types).
select types as data_types , count(*) as No_of_earthquakes
from earthquakes
group by types;

#17.  Average RMS and gap per continent.
select round(avg(rms),3) as RMS , round(avg(gap),3) as GAP, net,
count(*) as No_of_counts
from earthquakes
group by net;


##18.  Events with high station coverage (nst > threshold).
	#identify the highest number of seismic stations recorded for any earthquake in dataset.
select max(nst) as max_nst
from earthquakes;

select id, time, place, nst
from earthquakes
where nst > 100   #Keep only records with more than 100 reporting stations
order by nst desc;


#Tsunamis & Alerts
#19.  Number of tsunamis triggered per year.
select year(time) as year , tsunami as No_of_tsunami , count(*) as earthquakes 
from earthquakes
where tsunami = 1
group by year(time)
order by year;

#20.  Count earthquakes by alert levels (red, orange, etc.).
 #current listed columns do not include an alert column.

#Seismic Pattern & Trends Analysis.
#21.Find the top 5 countries with the highest average magnitude of earthquakes in the past 5 years  
select place as country,
round(avg(mag), 3) as average_magnitude
from earthquakes
where time >= date_sub(curdate(), interval 5 year)
  and place is not null
group by place
order by average_magnitude desc
limit 5;

#22.Find countries that have experienced both shallow and deep earthquakes within the same month.
select monthname(time) as month, place,
sum(case when depth_km < 70 then 1 else 0 end) as shallow,
sum(case when depth_km >= 70 then 1 else 0 end) as deep
from earthquakes
group by monthname(time), month(time), monthname(time), place
having shallow > 0
and deep > 0;


#23.Compute the year-over-year growth rate in the total number of earthquakes globally.
select year,
no_of_earthquakes,
previous_year,
round(           #Calculate the growth rate
	((no_of_earthquakes - previous_year) / previous_year) * 100, 2) as growth_rate
from( 
select year, no_of_earthquakes,   #Find the previous year's count
lag(no_of_earthquakes) over (order by year) as previous_year
from(
select year(time) as year,       #Count earthquakes for each year
count(*) as no_of_earthquakes
from earthquakes
group by year(time)
) as yearly_data
)as growth_data
order by year;

#List the 3 most seismically active regions by combining both frequency and average magnitude.
with network_stats as (     #Calculate network statistics and create a cte
    select net,
           count(*) as frequency,
           avg(mag) as average_magnitude
    from earthquakes
    group by net
),
scores as (               #Normalize the scores
    select net,
           frequency,
           average_magnitude,
           (frequency - min(frequency) over ())   #Frequency score
           / (max(frequency) over () - min(frequency) over ()) as frequency_score,
           
           (average_magnitude - min(average_magnitude) over ())   #Magnitude score
           / (max(average_magnitude) over () - min(average_magnitude) over ()) as magnitude_score
    from network_stats
)
select net,  #Calculate the combined score
       frequency,
       round(average_magnitude, 3) as average_magnitude,
       round((frequency_score + magnitude_score) / 2, 3) as combined_score
from scores
order by combined_score desc
limit 3;


#Depth, Location & Distance-Based  Analysis.
#25. For each country, calculate the average depth of earthquakes within ±5° latitude range of the equator.
   #filtered earthquake records within five degrees of the Equator and calculated the average depth and event count for each place.
select place, round(avg(depth_km), 3) as average_depth, 
count(*) as no_of_earthquakes
from earthquakes
where latitude between -5 and 5
group by place
order by average_depth desc;

# 26. Identify countries having the highest ratio of shallow to deep earthquakes.
#formula ratio= shallow/deep
select place,
       sum(case when depth_km < 70 then 1 else 0 end) as shallow,  #assigns true/false
       sum(case when depth_km >= 70 then 1 else 0 end) as deep,
       round(
           sum(case when depth_km < 70 then 1 else 0 end) /
           nullif(sum(case when depth_km >= 70 then 1 else 0 end), 0),
           2
       ) as shallow_deep_ratio
from earthquakes
group by place
having deep > 0
order by shallow_deep_ratio desc
limit 10;

# 27. Find the average magnitude difference between earthquakes with tsunami alerts and those without.
#Calculates the average magnitude separately for each tsunami flag value
select tsunami,
       round(avg(mag), 3) as average_magnitude
from earthquakes
group by tsunami;


select round(
           avg(case when tsunami = 1 then mag end) #with tsunami
           -
           avg(case when tsunami = 0 then mag end), #without tsunami
           3
       ) as magnitude_difference
from earthquakes;


#28. Using the gap and rms columns, identify events with the lowest data reliability (highest average error margins).
select id, time, place, gap, rms
from earthquakes
where gap is not null
  and rms is not null
order by gap desc, rms desc
limit 10;


#29. Find pairs of consecutive earthquakes (by time) that occurred within 50 km of each other and within 1 hour.

with consecutive as (               #Create the consecutive CTE
    select id, time, place, latitude, longitude,
        lag(id) over (order by time) as prev_id,
        lag(time) over (order by time) as prev_time,
        lag(place) over (order by time) as prev_place,
        lag(latitude) over (order by time) as prev_latitude,
        lag(longitude) over (order by time) as prev_longitude
    from earthquakes
)
select   #Select the earthquake details
    prev_id as earthquake_1,
    id as earthquake_2,
    prev_time as earthquake_1_time,
    time as earthquake_2_time,
    prev_place as earthquake_1_place,
    place as earthquake_2_place,
    timestampdiff(minute, prev_time, time) as time_difference_minutes,   #Calculate the time difference
    round(            # using Haversine formula
        6371 * 2 * asin(
            sqrt(
                pow(sin(radians(latitude - prev_latitude) / 2), 2) +
                cos(radians(prev_latitude)) *
                cos(radians(latitude)) *
                pow(sin(radians(longitude - prev_longitude) / 2), 2)
            )
        ),
        2
    ) as distance_km
from consecutive
where prev_time is not null   #Filter earthquakes by time
  and timestampdiff(minute, prev_time, time) <= 60        #Filter earthquakes by distance
  and 6371 * 2 * asin(             
        sqrt(
            pow(sin(radians(latitude - prev_latitude) / 2), 2) +
            cos(radians(prev_latitude)) *
            cos(radians(latitude)) *
            pow(sin(radians(longitude - prev_longitude) / 2), 2)
        )
      ) <= 50
order by time;


#30. Determine the regions with the highest frequency of deep-focus earthquakes (depth > 300 km).
	select net as region,
		   count(*) as deep_earthquakes
	from earthquakes
	where depth_km > 300
	group by net
	order by deep_earthquakes desc
	limit 3;


