#/usr/bin/env python3
import pandas as pd

movies = pd.read_csv("data/movies.csv")
movies['genres'] = movies['genres'].map(lambda genres: '[' + ','.join(map(lambda s: "'" + s.replace('"', '') + "'", genres.split('|'))) + ']')
movies['title'] = movies['title'].map(lambda s: s.replace('"', ""))

counter = 0
end = ', '
for index, row in movies.iterrows():
    if counter % 1000 == 0 or counter == movies.shape[0] - 1:
        end = ';\n'
    else:
        end = ', '
    
    print('(' + str(row['movieId']) + ', "' + row['title'] + '", ' + row['genres'] + ')', end=end)
    counter += 1
