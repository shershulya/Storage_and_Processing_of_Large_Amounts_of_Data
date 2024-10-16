# change config to local
gcloud config configurations create emulator
gcloud config set auth/disable_credentials true
gcloud config set project test-project
gcloud config set api_endpoint_overrides/spanner http://localhost:9020/

# create database
gcloud spanner instances create test-instance --config=emulator-config --description=Test --nodes=1
gcloud spanner databases create test-database --instance test-instance

# create tables
gcloud spanner databases ddl update test-database --instance=test-instance \
		--ddl='CREATE TABLE movies (movieId INT64, title STRING(256), genres ARRAY<STRING(64)>) PRIMARY KEY (movieId);'
gcloud spanner databases ddl update test-database --instance=test-instance \
		--ddl='CREATE TABLE ratings (userId INT64, movieId INT64, rating FLOAT64, timestamp TIMESTAMP) PRIMARY KEY (userId, movieId);'
