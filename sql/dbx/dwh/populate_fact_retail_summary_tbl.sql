COPY INTO skulytics_dev.default.fact_retail_summary_tbl
FROM 'abfss://demo-data@storage.dfs.core.windows.net/skulytics/data/fact_retail_summary_tbl.csv'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true');
