import boto3
import csv
import psycopg2

DB_ENDPOINT="postgres-1.clmlqirmvrik.eu-central-1.rds.amazonaws.com"
DB_PORT=5432
DB_NAME="OPA_project"
DB_USER="postgres"
DB_PASSWORD="datascientest"

 
# Connect to RDS PostgreSQL database
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_ENDPOINT,
    port=DB_PORT
)
cursor = conn.cursor()

# Get list of all table names in the database
cursor.execute("""
    SELECT tablename 
    FROM pg_catalog.pg_tables 
    WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';
""")

tables = cursor.fetchall()
# print(tables)
# Print table names
for table in tables:
    print(f"Table name: {table[0]}")

# Close database connection
cursor.close()
conn.close()

print("Script has completed")


s3 = boto3.client("s3")

response = s3.list_buckets()

print(response)