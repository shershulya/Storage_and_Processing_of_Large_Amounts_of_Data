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

WITH forenoonAvg AS (
    SELECT forenoon.userInn, FLOOR(AVG(forenoon.totalSum)) as fAvg
    FROM (
        SELECT content.userInn as userInn, hour(from_unixtime(floor(content.dtm.dte/1000))) as trHour, COALESCE(content.totalSum, 0) as totalSum
        FROM kkt
        WHERE subtype="receipt"
    ) forenoon
    WHERE forenoon.trHour < 13
    GROUP BY forenoon.userInn
)
SELECT forenoonAvg.userInn, forenoonAvg.fAvg, afternoonAvg.aAvg
FROM forenoonAvg INNER JOIN (
    SELECT afternoon.userInn, FLOOR(AVG(afternoon.totalSum)) as aAvg
    FROM (
        SELECT content.userInn as userInn, hour(from_unixtime(floor(content.dtm.dte/1000))) as trHour, COALESCE(content.totalSum, 0) as totalSum
        FROM kkt
        WHERE subtype="receipt"
    ) afternoon
    WHERE afternoon.trHour >= 13
    GROUP BY afternoon.userInn
) AS afternoonAvg WHERE forenoonAvg.userInn = afternoonAvg.userInn and forenoonAvg.fAvg > afternoonAvg.aAvg
ORDER BY forenoonAvg.fAvg limit 50;