#!/usr/bin/env python3

import sys
import io

import happybase

input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
output_stream = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

for line in input_stream:
    try:
        weapon,_,_,_,_,_,match_id,time,_,_,_,_ = line.strip().split(',', 11)
    except ValueError as e:
        continue
    print(('{}#{}#{}\t1').format(time, match_id, weapon), file=output_stream)
