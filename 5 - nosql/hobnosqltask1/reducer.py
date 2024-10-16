#!/usr/bin/env python3

import sys
import io
import re
import happybase

import random

input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
output_stream = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

current_key = None
sum_count = 0

hosts = ['mipt-node01.atp-fivt.org', 'mipt-node02.atp-fivt.org']
host = random.choice(hosts)

connection = happybase.Connection(host)

TABLE = 'sherar_pubg'

table = connection.table(TABLE)
batch = table.batch()


global_cnt = 0

pattern = re.compile('(.+#.+)#(.+)$')

for line in input_stream:
    try:
        key, count = line.strip().split('\t', 1)
        count = int(count)
    except ValueError as e:
        continue
    if current_key != key:
        if current_key:
            matcher = pattern.match(current_key)
            if matcher is None:
                print(current_key, file=sys.stderr)
                break
            current_key = matcher.group(1)
            weapon = matcher.group(2)
            batch.put(
                current_key.encode(), {
                    'weapon:{}'.format(weapon).encode(): '{}'.format(sum_count).encode()
                }
            )
            
            global_cnt += 1
            if global_cnt % 10000 == 0:
                batch.send()
                batch = table.batch()
        sum_count = 0
        current_key = key
    sum_count += count


if current_key:
    matcher = pattern.match(current_key)
    if matcher is None:
        print(current_key, file=sys.stderr)
        exit(0)
    current_key = matcher.group(1)
    weapon = matcher.group(2)
    batch.put(
        current_key.encode(), {
            'weapon:{}'.format(weapon).encode(): '{}'.format(sum_count).encode()
        }
    )

batch.send()
