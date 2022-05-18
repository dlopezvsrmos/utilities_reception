from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

HOST = os.environ.get("host")
DATABASE = os.environ.get("database")
USER = os.environ.get("user")
PASSWORD = os.environ.get("password")


connection = psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                database=DATABASE)

    # Create a cursor to perform database operations
cursor = connection.cursor()