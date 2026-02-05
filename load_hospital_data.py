import mysql.connector
import csv
import os
from datetime import datetime

# Database connection
conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    password='password123',
    database='hospital_db'
)
cursor = conn.cursor()

# Path to your CSV files
data_path = r'C:\Users\User\Downloads\Hospital+Patient+Records'

# CSV file to table mapping
files_to_load = {
    'patients.csv': 'patients',
    'encounters.csv': 'encounters',
    'procedures.csv': 'procedures',
    'payers.csv': 'payers'
}

def load_csv(filename, table_name):
    filepath = os.path.join(data_path, filename)
    print(f"Loading {filename} into {table_name}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        if not rows:
            print(f"  No data in {filename}")
            return
        
        # Get column names from CSV
        columns = list(rows[0].keys())
        
        # Create INSERT statement
        placeholders = ', '.join(['%s'] * len(columns))
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        
        # Insert data
        count = 0
        for row in rows:
            values = [row[col] if row[col] != '' else None for col in columns]
            try:
                cursor.execute(insert_query, values)
                count += 1
                if count % 100 == 0:
                    print(f"  Loaded {count} rows...")
            except Exception as e:
                print(f"  Error on row {count}: {e}")
        
        conn.commit()
        print(f"  ✓ Loaded {count} total rows into {table_name}\n")

# Load all files
for csv_file, table in files_to_load.items():
    load_csv(csv_file, table)

cursor.close()
conn.close()
print("All data loaded successfully!")