from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import concat, col, lit

if __name__ == "__main__":
    spark = SparkSession.builder.appName('sherar_bfs').master('yarn').getOrCreate()

    inp_schema = StructType(fields=[
        StructField("dst", IntegerType()),
        StructField("node", IntegerType())
    ])
    edges = spark.read.format("csv")\
          .schema(inp_schema)\
          .option("sep", "\t")\
          .load("/data/twitter/twitter_sample.txt")
  
    n = 10
    forward_edges = edges.select("node","dst").repartition(n).persist()

    bfs_schema = StructType(fields=[
        StructField("node", IntegerType()),
        StructField("path", StringType())
    ])
    start_node = 12
    path = "12"
    rdd = spark.sparkContext.parallelize([(start_node, path)]).partitionBy(n)
    distances = spark.createDataFrame(rdd, schema=bfs_schema)

    while True:
        new_nodes = distances.join(forward_edges, distances.node == forward_edges.node)
        new_distances = new_nodes.select(col("dst").alias("node"), concat(col("path"), lit(","), col("dst")).alias("path")).persist()
        if new_distances.filter(col("node") == 34).count() > 0:
            print((new_distances.filter(col("node") == 34).select("path").collect())[0][0])
            break
        else:
            distances = new_distances
