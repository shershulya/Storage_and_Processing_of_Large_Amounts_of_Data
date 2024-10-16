#!/usr/bin/env python3

import sys

current_key = None
sum_commands = 0
sum_sessions = 0
for line in sys.stdin:
    try:
        key, commands, sessions = line.strip().split('\t', 2)
        commands = int(commands)
        sessions = int(sessions)
    except ValueError as e:
        continue
    if current_key != key:
        if current_key:
            print ("%s\t%.1f\t%d" % (current_key, sum_commands/sum_sessions, sum_sessions))
        sum_commands = 0
        sum_sessions = 0
        current_key = key
    sum_commands += commands
    sum_sessions += sessions

if current_key:
    print ("%s\t%.1f\t%d" % (current_key, sum_commands/sum_sessions, sum_sessions))