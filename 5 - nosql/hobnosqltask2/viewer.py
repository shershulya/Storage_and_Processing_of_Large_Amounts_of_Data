#!/usr/bin/env python3

from collections import defaultdict

import argparse
import happybase
import logging
import random
import sys
import re

USAGE = """

To query top-10 weapons statistics for every match in interval (seconds), run:
  $ {0} --start 415 --end 678

""".format(sys.argv[0])

logging.basicConfig(level="DEBUG")

HOSTS = ['mipt-node0%01d.atp-fivt.org' % i for i in range(1, 2)]
TABLE = 'sherar_pubg'

pattern = re.compile('(.+)#(.+)$')

def connect():
    host = random.choice(HOSTS)
    connection = happybase.Connection(host)

    logging.debug('Connecting to HBase Thrift Server on {}'.format(host))
    connection.open()

    if b'sherar_pubg' not in connection.tables():
        raise RuntimeError('Table {} not exist'.format(TABLE))
    else:
        logging.debug('Using table {}'.format(TABLE))
    return happybase.Table(TABLE, connection)

def query(args, table):
    statistics = dict(dict())
    for time in range(args.start, args.end + 1):
        byte_time = (str(time) + '#').encode()
        for key, data in table.scan(row_prefix=byte_time):
            matcher = pattern.match(key.decode())
            match_id = matcher.group(2)
            key, value = data.popitem()
            weapon = key.decode()[7:]
            if match_id in statistics:
                if weapon in statistics[match_id]:
                    statistics[match_id][weapon] += int(value.decode())
                else:
                    statistics[match_id][weapon] = int(value.decode())
            else:
                statistics[match_id] = {}
                statistics[match_id][weapon] = int(value.decode())

    n = 0
    for match_id, weapons in statistics.items():
        print(match_id)
        for weapon, cnt in sorted(weapons.items(), key=lambda x: x[1], reverse=True):
            print('\t' + str(weapon) + '\t' + str(cnt))
        n += 1
        if n > 49:
            break
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="An HBase pubg statistics", usage=USAGE)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)

    args = parser.parse_args()
    table = connect()

    query(args, table)
