hive -f select_total_sum.sql

# (hive -f time_table.sql 2>&1) > result.txt
# grep --color -n "MapReduce Total cumulative CPU time" result.txt