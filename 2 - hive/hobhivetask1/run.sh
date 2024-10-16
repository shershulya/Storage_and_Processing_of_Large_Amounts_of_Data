hive -f setup.sql
hive --database sherar -e "select * from kkt limit 50"