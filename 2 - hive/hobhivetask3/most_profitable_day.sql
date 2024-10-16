add jar
hdfs:/opt/cloudera/parcels/CDH/lib/hive/lib/json-serde-1.3.8-jar-with-dependencies.jar;

SET hive.cli.print.header=false;
SET mapred.input.dir.recursive=true;
SET hive.mapred.supports.subdirectories=true;

USE sherar;

DROP TABLE IF EXISTS kkt;
CREATE external TABLE kkt (
    kktRegId String,
    subtype String,
    content struct<userInn:string,totalSum:BIGINT, dtm:struct<dte:BIGINT>>
) ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES ("ignore.malformed.json" = "true", "mapping.dte" = "$date", "mapping.dtm" = "dateTime")
STORED AS TEXTFILE
LOCATION '/data/hive/fns2';

WITH ttlsum AS (
    SELECT sums.userInn, sums.dayOfMonth, SUM(sums.totalSum) as totalSum
    FROM (
        SELECT content.userInn as userInn, dayofmonth(from_unixtime(floor(content.dtm.dte/1000))) as dayOfMonth, COALESCE(content.totalSum, 0) as totalSum
        FROM kkt
        -- WHERE subtype="receipt"
    ) sums
    GROUP BY sums.userInn, sums.dayOfMonth
)
SELECT ttlsum.userInn, MAX(ttlsum.dayOfMonth), ttlsum.totalSum
FROM ttlsum RIGHT JOIN (
    SELECT ttlsum.userInn, MAX(ttlsum.totalSum) as totalSum FROM ttlsum
    GROUP BY ttlsum.userInn
) AS maxsum WHERE (ttlsum.userInn = maxsum.userInn) and (ttlsum.totalSum = maxsum.totalSum or ttlsum.totalSum IS NULL and maxsum.totalSum IS NULL)
GROUP BY ttlsum.userInn, ttlsum.totalSum
ORDER BY ttlsum.userInn;