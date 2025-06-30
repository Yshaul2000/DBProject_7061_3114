import psycopg2

def get_connection(name_db="SaveStage2"):
    if name_db == "mydatabase":
        print("Connecting to mydatabase")
    return psycopg2.connect(
        host="localhost",
        database=name_db,
        user="yshaul",
        password="s2023"
    )

