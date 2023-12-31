import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


dbconfig = {
    'host': 'localhost',
    'database': 'admin_traveling',
    'user': os.environ["DB_USERNAME"],
    'password': os.environ["DB_PASSWORD"],
}

try:
    connection = psycopg2.connect(**dbconfig)

    cursor = connection.cursor()
    cursor.execute(open("init_tables.sql", "r").read())
    cursor.execute(open("trigger.sql", "r").read())

    connection.commit()

except (Exception, psycopg2.Error) as error:
    print(f"Error with connect to database {dbconfig['database']}. Reason: {str(error)}")

finally:
    if connection and cursor:
        cursor.close()
        connection.close()
