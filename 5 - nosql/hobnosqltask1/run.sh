#!/usr/bin/env bash

python3 create.py

OUT_DIR="pubg"
NUM_REDUCERS=8

hdfs dfs -rm -r -skipTrash $OUT_DIR*

yarn jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -D mapreduce.job.name="sherar_pubg" \
    -D mapreduce.job.reduces=${NUM_REDUCERS} \
    -files mapper.py,reducer.py \
    -mapper mapper.py \
	-reducer reducer.py \
    -input /data/hobod/pubg \
    -output $OUT_DIR
