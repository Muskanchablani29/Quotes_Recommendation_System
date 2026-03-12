import pymysql

# Database connection
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='muskan123'
)

try:
    with connection.cursor() as cursor:
        # Drop and recreate database
        cursor.execute("DROP DATABASE IF EXISTS quotes_db")
        cursor.execute("CREATE DATABASE quotes_db CHARACTER SET utf8mb4")
        print("Database quotes_db dropped and recreated successfully!")
finally:
    connection.close()
