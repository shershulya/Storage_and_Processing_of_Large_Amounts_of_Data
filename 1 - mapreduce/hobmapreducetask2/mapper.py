#!/usr/bin/env python3

import sys
import re
from importlib import reload
from collections import defaultdict

session_pattern = re.compile('UUID of player\s.*?\s')
session_nickname_pattern = re.compile('\w+$')
command_pattern = re.compile(':\s.+\sissued server command')
command_nickname_pattern = re.compile('^(: [\b\w]+)')

user_sessions = defaultdict(int)
user_commands = defaultdict(int)
for line in sys.stdin:
    session = session_pattern.search(line)
    if session:
        nickname = session_nickname_pattern.search(session.group(0).strip())
        user_sessions[nickname.group(0)] += 1
    
    command = command_pattern.search(line)
    if command:
        nickname = command_nickname_pattern.search(command.group(0).strip())
        user_commands[nickname.group(0)[2:]] += 1

for nickname, sessions in user_sessions.items():
    print ("%s\t%d\t%d" % (nickname, user_commands[nickname], sessions))
