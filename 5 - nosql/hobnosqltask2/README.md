
# Task2: Fetch data from hbase and cumulate it for statistics

int('hob2022101'[3:]) % 4 +1 = 2. Therefore I solved second variant of this task. 

You should launch `./run.sh` to check the task with default params or your can run:

```bash
python3 viewer.py
```
To see Usage of the script, or:

```bash
python3 viewer.py --start 391 --end 456
```

To run the script with custom values of start and end point in seconds of the match.

I notice that volume of the unique match_id is about 500 000, 
so i print only first 50 unique matches with their weapons statistics to reduce ouput logs.
