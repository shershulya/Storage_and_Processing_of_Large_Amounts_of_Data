# Google Spanner Hometask 

[Spanner Hometask](https://docs.google.com/document/d/1sY9ZCztEzbqLQSjOGtsJ8vQQohrk4ZgyNcN122D-wMc)

## Requirements

[Spanner emulator](https://cloud.google.com/spanner/docs/emulator)

- requirements.txt - 

## Инструкции

- ./spanner_emator_up.sh - запустить эмулятор локально, 
- ./change_config.sh - переключить gcloud на локальную работу
- ./create_database.sh - создать базу
- ./create_tables.sh - создать таблицу
- ./insert_data.sh - загрузить данные в базу, данные должны быть в папке data


## 1 задание

- посчитал на 100к, так как оперативки для эмулятора не хватит

- spannertask1/read_transaction.py - транзакция на чтение
- spannertask1/write_transaction.py - транзакция на запись

- first_result.txt - результат чтения до записи
- updated_results.txt - результат чтения после записи
