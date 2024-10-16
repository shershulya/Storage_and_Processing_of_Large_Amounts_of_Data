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
    content struct<userInn:string,totalSum:BIGINT>
) ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES ( "ignore.malformed.json" = "true")
LOCATION '/data/hive/fns2';