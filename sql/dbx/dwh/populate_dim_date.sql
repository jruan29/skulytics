COPY INTO skulytics_dev.default.dim_date
FROM 'abfss://demo-data@storage.dfs.core.windows.net/skulytics/data/dim_date.csv'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true');
