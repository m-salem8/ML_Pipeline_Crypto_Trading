import boto3
import csv
import psycopg2

DB_ENDPOINT="postgres-1.clmlqirmvrik.eu-central-1.rds.amazonaws.com"
DB_PORT=5432
DB_NAME="OPA_project"
DB_USER="postgres"
DB_PASSWORD="datascientest"

def lambda_handler(event, context):
    # Initialize S3 client
    print("lambda_function started")
    s3 = boto3.client('s3')

    
    # Connect to RDS PostgreSQL database
    conn = psycopg2.connect(
        dbname= DB_NAME,
        user= DB_USER,
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
    
    for table in tables:
        table_name = table[0]
        
        # Execute SQL query to fetch all data from the current table
        cursor.execute(f"SELECT * FROM {table_name};")
        
        # Create a temporary CSV file to store data
        filename = f'/tmp/{table_name}.csv'
        
        with open(filename, 'w', newline='') as f:
            csv_writer = csv.writer(f)
            
            # Write column headers
            csv_writer.writerow([i[0] for i in cursor.description])
            
            # Write table data
            csv_writer.writerows(cursor.fetchall())
        
        # Upload the CSV file to S3, overwriting if the file already exists
        s3.upload_file(filename, 'your_s3_bucket', f'{table_name}.csv')
    
    print("Lambda function has completed")
    
    # Close database connection
    cursor.close()
    conn.close()
# For local testing
if __name__ == '__main__':
    lambda_handler(None, None)