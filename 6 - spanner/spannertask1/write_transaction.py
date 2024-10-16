from google.cloud import spanner
from google.auth.credentials import AnonymousCredentials
from google.cloud.spanner_v1.session import Session

spanner_client = spanner.Client(
    project='test-project',
    client_options={"api_endpoint": "0.0.0.0:9010"},
    credentials=AnonymousCredentials()
)

instance = spanner_client.instance("test-instance")
database = instance.database("test-database")

session = Session(database)
session.create()

with session.transaction() as transaction:
    fantasy_movies = transaction.execute_sql(
      f"SELECT movieId \
        FROM movies \
        WHERE 'Fantasy' IN UNNEST(genres)"
    )
    fantasy_movies = set(row[0] for row in fantasy_movies)
    
    result = transaction.execute_sql(
      f"UPDATE ratings \
        SET rating = rating + 2 \
        WHERE movieId in UNNEST([{','.join(map(str, fantasy_movies))}])"
    )
