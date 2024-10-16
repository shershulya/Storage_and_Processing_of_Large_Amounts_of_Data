cat logs/2017-11-30-1.log | ./mapper.py | sort | ./reducer.py | sort -k2rn | head -200
