import psycopg2

def get_connection(name_db="SaveStage2"):
    # Check if the database name is "mydatabase" and print a message
    if name_db == "mydatabase":
        print("Connecting to mydatabase")

    # Establish and return a connection to the PostgreSQL database
    return psycopg2.connect(
        host="localhost",  # Database host
        database=name_db,  # Name of the database
        user="yshaul",  # Username for authentication
        password="s2023"  # Password for authentication
    )