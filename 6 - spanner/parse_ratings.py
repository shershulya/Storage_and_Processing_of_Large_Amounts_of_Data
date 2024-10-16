#/usr/bin/env python3
import pandas as pd

ratings = pd.read_csv("data/ratings_100k.csv")

counter = 0
end = ', '
for index, row in ratings.iterrows():
    if counter % 1000 == 0 or counter == ratings.shape[0] - 1:
        end = ';\n'
    else:
        end = ', '
        
    print('(' + str(int(row['userId'])) + ", " + str(int(row['movieId'])) + ", " + 
           str(row['rating']) + ", TIMESTAMP_SECONDS(" + str(int(row['timestamp'])) + '))',end=end)
    counter += 1