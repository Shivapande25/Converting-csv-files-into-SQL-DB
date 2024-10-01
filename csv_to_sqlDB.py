import pandas as pd
from sqlalchemy import create_engine
import subprocess
import mysql.connector

# MySQL connection details (replace with actual values)
user = 'your_username'
password = 'your_password'
host = 'your_host'
port = 'your_port'
database = 'your_database'

# Create a MySQL connection
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    port=port
)

# Create a cursor object
cursor = conn.cursor()

# Create the database if it does not exist and use it
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database};")
cursor.execute(f"USE {database};")

# Close the cursor and connection
cursor.close()
conn.close()

# Create a connection to the MySQL database using SQLAlchemy
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')

# Load CSV file into a pandas DataFrame (replace with the actual path to your CSV file)
csv_file_path = 'path_to_your_csv_file.csv'
df = pd.read_csv(csv_file_path)

# Write the DataFrame to a MySQL table, creating the table if it doesn't exist
table_name = 'table-name'  # Replace with your table name
df.to_sql(table_name, engine, if_exists='replace', index=False)

print("Data has been successfully written to the MySQL database.")

# Dump the database into an SQL file with the database creation and selection commands
dump_file_path = 'path_to_your_dump_file.sql'
dump_command = f"mysqldump -u {user} -p{password} --add-drop-database --databases {database} > {dump_file_path}"

# Execute the command to dump the database
subprocess.run(dump_command, shell=True, check=True)

# Insert the CREATE DATABASE and USE commands at the beginning of the file
with open(dump_file_path, 'r+') as file:
    content = file.read()
    file.seek(0, 0)
    file.write(f"CREATE DATABASE IF NOT EXISTS {database};\nUSE {database};\n" + content)

print(f"Database has been successfully dumped to {dump_file_path}.")
