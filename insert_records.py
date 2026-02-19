from api_request import mock_data, fetch_data 
import psycopg2

mocked_response = mock_data()

print("Mocked API Response:")
print(mocked_response)

def connect_db():
    # Simulate database connection
    print("Connecting to the database...")
    try:
        conn = psycopg2.connect(
            dbname="weather_data",
            user="weather_user",
            password="weather_pass",
            host="localhost",
            port=5432
        )
        print(conn)
        return conn
    except:
        print("Database connection established.")
        return True
    
def create_table(conn):
    print("Creating weather_data table if not exists...")
    try:
        cursor = conn.cursor()
        create_table_query = """
        CREATE SCHEMA IF NOT EXISTS weather_schema;
        CREATE TABLE IF NOT EXISTS weather_schema.weather_data (
            id SERIAL PRIMARY KEY,
            location_name VARCHAR(100),
            country VARCHAR(100),
            temperature INT,
            weather_description VARCHAR(255),
            wind_speed INT,
            humidity INT
        )
        """
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        print("Table created successfully.")
    except Exception as e:
        print(f"An error occurred while creating the table: {e}")
        
def insert_weather_data(conn, data):
    print("Inserting data into the database...")
    try:
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO weather_schema.weather_data (location_name, country, temperature, weather_description, wind_speed, humidity)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            data['location']['name'],
            data['location']['country'],
            data['current']['temperature'],
            data['current']['weather_descriptions'][0],
            data['current']['wind_speed'],
            data['current']['humidity']
        )
        cursor.execute(insert_query, values)
        conn.commit()
        cursor.close()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")
        
def main():
    data = fetch_data()
    conn = connect_db() 
    if isinstance(conn, bool):
        print("Database connection failed, exiting...")
        return
    create_table(conn)
    insert_weather_data(conn, data)
    conn.close()

main()