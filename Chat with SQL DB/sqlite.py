import sqlite3

## Connect to sqlite
connection = sqlite3.connect('student.db')

## Create a cursor object to execute SQL queries
cursor = connection.cursor()

## Create a table
table_info = """

CREATE TABLE STUDENT
                (id INTEGER PRIMARY KEY,
                name VARCHAR(20),
                age INTEGER NOT NULL,
                class VARCHAR(10),
                marks INTEGER);
"""

cursor.execute(table_info)

## Insert data into the table
cursor.execute("INSERT INTO STUDENT (name, age, class, marks) VALUES ('John', 15, 'X', 80)")
cursor.execute("INSERT INTO STUDENT (name, age, class, marks) VALUES ('Jane', 16, 'XI', 85)")
cursor.execute("INSERT INTO STUDENT (name, age, class, marks) VALUES ('Doe', 17, 'XII', 90)")   
cursor.execute("INSERT INTO STUDENT (name, age, class, marks) VALUES ('Sue', 18, 'XII', 90)")  
cursor.execute("INSERT INTO STUDENT (name, age, class, marks) VALUES ('Linda', 14, 'X', 99)")  
cursor.execute("INSERT INTO STUDENT (name, age, class, marks) VALUES ('David', 16, 'XI', 87)")

## Display the data
print("The data in the table is:")
data = cursor.execute("SELECT * FROM STUDENT")
for row in data:
    print(row)

## Commit the changes in the database
connection.commit()
connection.close()