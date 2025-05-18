import pyodbc
import requests

# Establish connection to SQL Server
conn = pyodbc.connect(
    "DRIVER={SQL Server};SERVER=AMBE\\SQLEXPRESS;DATABASE=college_api;Trusted_Connection=yes"
)
cursor = conn.cursor()

# Step 1: Create the table if it doesn't exist
create_table_query = """
USE college_api
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='college_info' AND xtype='U')
CREATE TABLE college_info (
    id VARCHAR(5) PRIMARY KEY NOT NULL,
    college VARCHAR(80),
    city VARCHAR(255),
    state VARCHAR(50)
)
"""
cursor.execute(create_table_query)
conn.commit()

# Step 2: Truncate the table (Clear old data) [TEMPORARILY COMMENT THIS OUT]
cursor.execute("TRUNCATE TABLE college_info")
conn.commit()

# Step 3: Fetch data from API
url = "https://script.google.com/macros/s/AKfycbxewSggSS7CARRBa2icS6_qn4SyavS4IR3awGTp0aetO_RPgnZFN_u9NQ45yfLx2kel7A/exec"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("API Response Type:", type(data))  # Debugging type
    print("API Response:", data)  # Debugging full API response
else:
    print("Failed to fetch data:", response.status_code)
    conn.close()
    exit()

# Verify API response format and extract the correct list
if isinstance(data, dict):  
    print("Available Keys in API Response:", data.keys())  # Debugging available keys
    data = data.get("data", [])  # Extract records list from 'data' key

# Print sample record to verify data structure
if isinstance(data, list) and len(data) > 0:
    print("Sample Record:", data[0])  # Debugging first record

print(f"Total records from API: {len(data)-1}" if isinstance(data, list) else "No valid data received")

# Step 4: Insert new data (excluding header row)
if isinstance(data, list) and len(data) > 1:  
    for item in data[1:]:  # Skip header row if necessary
        print("Processing:", item.get("college"), item.get("city"), item.get("state"))  # Debugging processed row
        print("Available keys in record:", item.keys())  # Debugging keys inside record
        
        # Check if the ID already exists
        cursor.execute("SELECT COUNT(*) FROM college_info WHERE id = ?", item.get("college"))
        row_exists = cursor.fetchone()[0]

        if row_exists == 0:  # If ID doesn't exist, insert new data
            try:
                cursor.execute(
                    "INSERT INTO college_info (id, college, city, state) VALUES (?, ?, ?, ?)",
                    item.get("college"), item.get("college"), item.get("city"), item.get("state")
                )
                print(f"Inserted: {item.get('college')}")  # Debugging insertion confirmation
                conn.commit()  # Ensure changes are saved after each insert
            except Exception as e:
                print("SQL Insert Error:", e)  # Print error if insertion fails

# Step 5: Display total number of rows **AFTER INSERTION**
cursor.execute("SELECT COUNT(*) FROM college_info")
total_rows = cursor.fetchone()[0]
print(f"Total number of rows in college_info: {total_rows}")  # Final row count

conn.close()  # Close connection
print("Table created, truncated, and data inserted successfully without duplicates!")
