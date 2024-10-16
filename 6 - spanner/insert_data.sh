# for testing purpose

movies=`python3 parse_movies.py`


while IFS=, read -r line
do
    gcloud spanner databases execute-sql test-database --instance=test-instance \
        --sql="INSERT movies (movieId, title, genres) VALUES $line"
done <<< "$movies"


ratings=`python3 parse_ratings.py`

while IFS=, read -r line
do
    gcloud spanner databases execute-sql test-database --instance=test-instance \
        --sql="INSERT ratings (userId, movieId, rating, timestamp) VALUES $line"
done <<< "$ratings"