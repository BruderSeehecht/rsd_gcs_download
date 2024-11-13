# sql script to query the bigquery public dataset for landsat and sentinel 2 data and to create a table which can be used to bulk download the data from gcs
# landsat data access
SELECT 
*
FROM `bigquery-public-data.cloud_storage_geo_index.landsat_index` 
WHERE 
  EXTRACT(YEAR FROM sensing_time) = 2018
  AND cloud_cover < 30
  AND spacecraft_id = "LANDSAT_7"
  AND wrs_row = 69 OR wrs_row = 75

# sentinel 2 data access 
SELECT
*
FROM `bigquery-public-data.cloud_storage_geo_index.sentinel_2_sr_index`
WHERE
    EXTRACT(YEAR FROM sensing_time) = 2018
    AND cloud_cover < 30
    AND (mgrs_tile = "32UND" OR mgrs_tile = "32UQE")'