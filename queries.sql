/*Avg Duration by Passholder Type for Jan*/
select p.passholder_type, round(avg(f.duration),2) as Avg_Duration 
from bikeshare-422212.bikeshare_dataset.fact_bike f
join `bikeshare-422212.bikeshare_dataset.dim_passholdertype` p on p.passholdertype_id=f.passholdertype_id
join `bikeshare-422212.bikeshare_dataset.dim_date` d on d.date_id = f.start_time_id
WHERE SUBSTR(CAST(f.start_time_id AS STRING), 1, 6) = '202401'
group by p.passholder_type

/*Stations with less than 100 start times*/
SELECT DISTINCT s.station_id, s.Station_Name
FROM `bikeshare-422212.bikeshare_dataset.station_df` s
JOIN `bikeshare-422212.bikeshare_dataset.fact_bike` f ON f.start_station_id = s.Station_ID
GROUP BY s.station_id, s.Station_Name
HAVING COUNT(f.start_time_id) < 100;

/*Avg Duration by Bike Type*/
select b.bike_type, round(avg(f.duration),2) as Avg_Duration 
from bikeshare-422212.bikeshare_dataset.fact_bike f
join `bikeshare-422212.bikeshare_dataset.dim_bike` b on b.bike_id=f.bike_id
group by b.bike_type



