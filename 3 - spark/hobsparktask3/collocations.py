import re
import operator
import math

from pyspark import SparkConf, SparkContext
sc = SparkContext(conf=SparkConf().setAppName("sherar_collocations").setMaster("yarn"))

def clean_article(line):
    try:
        article_id, text = unicode(line.strip()).split('\t', 1)
        text = re.sub("^\W+|\W+$", "", text, flags=re.UNICODE)
        return text
    except ValueError as e:
        return

wiki = sc.textFile("hdfs:///data/wiki/en_articles_part").map(clean_article)
stop_words = sc.textFile("hdfs:///data/wiki/stop_words_en-xpo6.txt")
stop_words_set = sc.broadcast(set(stop_words.collect()))

def extract_words(text):
    words = map(lambda w: w.lower(), re.split("\W*\s+\W*", text, flags=re.UNICODE))
    return [word for word in words if word not in stop_words_set.value]

all_words = wiki.flatMap(extract_words)
all_words = all_words.map(lambda x: (x, None)).aggregateByKey(0, lambda a, x: a + 1, operator.iadd)

def make_pairs(text):
    words = extract_words(text)
    return map("_".join, zip(words, words[1:]))

all_pairs = wiki.flatMap(make_pairs)
all_pairs = all_pairs.map(lambda x: (x, None)).aggregateByKey(0, lambda a, x: a + 1, operator.iadd)

total_words = all_words.map(operator.itemgetter(1)).sum()
total_pairs = all_pairs.map(operator.itemgetter(1)).sum()

words = all_words.filter(lambda p: p[1] >= 500).cache()
pairs = all_pairs.filter(lambda p: p[1] >= 500).cache()

def split_pair(inp):
    pair, pair_cnt = inp
    w = pair.split("_")
    return w[0], (w[1], pair_cnt)

def prepare_join(inp):
    left, ((right, pair_cnt), left_cnt) = inp
    return (right, (left, left_cnt, pair_cnt))
    
def compute_npmi(inp):
    right, ((left, left_cnt, pair_cnt), right_cnt) = inp
    return (left + "_" + right, (math.log((left_cnt + right_cnt)) - math.log(total_words)) / (math.log(pair_cnt) - math.log(total_pairs)))
    
result = pairs.map(split_pair).join(words).map(prepare_join).join(words).map(compute_npmi)

output = result.sortBy(lambda x: x[1], ascending=False).take(39)

for pair, npmi in output:
    print pair