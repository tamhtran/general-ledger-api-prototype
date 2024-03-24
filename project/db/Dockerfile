# pull official base image
FROM postgres:15

# Update package repository and install jq
RUN apt-get update && apt-get install -y jq

# run 10_db_init.sql on init
ADD 10_db_init.sql /docker-entrypoint-initdb.d/10_db_init.sql

#Here, we extended the official Postgres image by adding 10_db_init.sql to the "docker-entrypoint-initdb.d" directory in the container. T
#This file will execute on init.

# Load regions and countries data from json file first
ADD 20_load_nested_json_data.sh /docker-entrypoint-initdb.d/20_load_nested_json_data.sh

# Make sure the script is executable
RUN chmod +x /docker-entrypoint-initdb.d/20_load_nested_json_data.sh

# Add account and transactions data after regions and countries data
ADD 30_db_load.sql /docker-entrypoint-initdb.d/30_db_load.sql

# Add test database for mockup
ADD 40_test_db_load.sql /docker-entrypoint-initdb.d/40_test_db_load.sql
