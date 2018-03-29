import sqlite3

connection = sqlite3.connect("cities.db")
cursor = connection.cursor()

cursor.execute("""DROP TABLE cities;""")

create_table_cities = """
CREATE TABLE cities (
City VARCHAR(100),
States VARCHAR(100));"""

