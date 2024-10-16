import sys
import re
from collections import defaultdict

reload(sys)
sys.setdefaultencoding('utf-8')

stop_words = set()
with open("stop_words_en.txt") as fd:
    for line in fd:
        stop_words.add(line.strip())
pattern = re.compile("^([A-Z]){1}([a-z]){5,8}$")
for line in sys.stdin:
    try:
        article_id, text = unicode(line.strip()).split('\t', 1)
    except ValueError as e:
        continue
    words = re.split("\W*\s+\W*", text, flags=re.UNICODE)
    word_stat = defaultdict(int)
    proper_noun_stat = defaultdict(int)
    for word in words:
        if len(word) >= 6 and len(word) <= 9:
            if pattern.match(word):
                proper_noun_stat[word.lower()] += 1
            else:
                word_stat[word.lower()] += 1

    for word, count in word_stat.iteritems():
        proper_noun_stat.pop(word, None)

    for word, count in proper_noun_stat.iteritems():
        if word in stop_words:
            continue
        print "%s\t%d" % (word, count)
