#!/usr/bin/env python3

import happybase
import random

hosts = ['mipt-node01.atp-fivt.org', 'mipt-node02.atp-fivt.org']
host = random.choice(hosts)

connection = happybase.Connection(host)

TABLE = 'sherar_pubg'

if b'sherar_pubg' in connection.tables():
    connection.disable_table(TABLE)
    connection.delete_table(TABLE)
    connection.create_table(
        TABLE,
        families={
            'weapon': dict()
        }
    )
