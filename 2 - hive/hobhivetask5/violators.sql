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

ADD FILE ./reducer.py;

WITH kkt_sorted AS (
    SELECT content.userInn as userInn, kktRegId, content.dtm.dte as dte, subtype
    FROM kkt
    WHERE subtype="openShift" or subtype="receipt" or subtype="closeShift"
    DISTRIBUTE BY userInn, kktRegId
    SORT BY userInn, kktRegId, dte
)
SELECT DISTINCT userInn FROM (
    SELECT TRANSFORM(userInn, kktRegId, dte, subtype) USING 'reducer.py' as userInn
    FROM  kkt_sorted
) violators
ORDER BY userInn
LIMIT 50;