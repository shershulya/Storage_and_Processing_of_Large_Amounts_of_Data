from google.cloud import spanner
from google.auth.credentials import AnonymousCredentials
from google.cloud.spanner_v1.transaction import Transaction

def read_transaction(transaction: Transaction):
    for i in range(10):
        result = transaction.execute_sql(
          f"SELECT userId, movieId, rating \
            FROM ratings \
            ORDER BY userId, movieId \
            LIMIT 10 OFFSET {1000 + i * 10};"
        )
        for row in result:
            print(row)

spanner_client = spanner.Client(
    project='test-project',
    client_options={"api_endpoint": "0.0.0.0:9010"},
    credentials=AnonymousCredentials()
)

instance = spanner_client.instance("test-instance")
database = instance.database("test-database")

database.run_in_transaction(read_transaction)
