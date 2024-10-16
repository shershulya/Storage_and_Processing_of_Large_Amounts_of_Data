#!/usr/bin/env python3

import sys

(prevUserInn, prevKktRegId) = (None, None)
openShift = None
violations = []

for line in sys.stdin:
    line = line.strip().split("\t")

    time = None
    if line[2] != '\\N':
        time = int(line[2])
    userInn, kktRegId, timestamp, subtype = line[0], line[1], time , line[3]

    if (kktRegId) != (prevKktRegId):
        if (prevKktRegId) != (None):
            if len(violations) > 0:
                print(prevUserInn)
            violations = []
        prevUserInn = userInn
        prevKktRegId = kktRegId
        openShift = None

    if subtype == 'openShift':
        openShift = timestamp
    elif subtype == 'closeShift':
        openShift = None
    elif subtype == 'receipt':
        if openShift is None:
            violations.append((kktRegId, timestamp, subtype))

if (prevKktRegId):
    if len(violations) > 0:
        print(userInn)
    violations = []
