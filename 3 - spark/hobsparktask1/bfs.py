from pyspark import SparkContext, SparkConf

def parse_edge(s):
    user, follower = s.split("\t")
    return (int(user), int(follower))

def step(input):
    prev_vert, (path, next_vert) = input
    return (next_vert, path + "," + str(next_vert))

if __name__ == "__main__":
    sc = SparkContext(conf=SparkConf().setAppName("sherar_bfs").setMaster("yarn"))

    n = 10
    edges = sc.textFile("/data/twitter/twitter_sample.txt").map(parse_edge)

    forward_edges = edges.map(lambda e: (e[1], e[0])).partitionBy(n).persist()

    start_node = 12
    path = "12"
    distances = sc.parallelize([(start_node, path)]).partitionBy(n)
    while True:
        new_distances = distances.join(forward_edges, n).map(step).persist()
        if new_distances.filter(lambda x: x[0] == 34).count() > 0:
            print(new_distances.filter(lambda x: x[0] == 34).take(1)[0][1])
            break
        else:
            distances = new_distances
