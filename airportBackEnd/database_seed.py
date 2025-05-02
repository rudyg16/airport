import pymysql
from dotenv import load_dotenv
import os
import pandas as pd

# Load environment variables
load_dotenv()
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Make arrays global so they can be used in other seeding that requires them as fk 
airlines = ["American Airlines", "Delta", "United Airlines", "Southwest Airlines", "JetBlue"]
terminal = ['A','B','C']
models =[
        ("Boeing 737-800", 160),
        ("Airbus A320", 150),
        ("Boeing 757", 200),
        ("Embraer 175", 88),
        ("Airbus A321", 185),
        ("Boeing 777-200", 300),
    ]


# === Seeder Functions ===

def seed_airlines(cursor):
    for airline in airlines:
        sql = "INSERT INTO airline(airline_name) VALUES(%s)"
        cursor.execute(sql, (airline,))
    print("Airlines inserted.")

def seed_terminals(cursor, count=3):
    for i in range(count):
        letter = chr(ord('A') + i)
        sql = "INSERT INTO terminal(terminal_letter) VALUES(%s)"
        cursor.execute(sql, (letter,))
    print("Terminals inserted.")

def seed_gates(cursor, terminal_count=3, gates_per_terminal=6):
    for i in range(terminal_count):
        letter = chr(ord('A') + i)
        for j in range(1, gates_per_terminal + 1):
            sql = "INSERT INTO gate(gate_num, terminal_letter) VALUES(%s, %s)"
            cursor.execute(sql, (j, letter))
    print(" Gates inserted.")

def seed_model(cursor):
    for model_name,capacity in models:
        sql="INSERT INTO model(model_name,capacity) VALUES(%s,%s)"
        cursor.execute(sql,(model_name,capacity,))

def seed_airplane(cursor):
    df = pd.read_csv('data/airplane.csv')
    for index, row in df.iterrows():#itterrows allows iteration through each row of dataframe df
        model = row['model_name']
        airline=row['airline_name']
        sql="INSERT INTO model(model_name,capacity) VALUES(%s,%s)"
        cursor.execute(sql,(model_name,capacity,))

# === Print Utility Functions ===

def print_airlines(cursor):
    cursor.execute("SELECT * FROM airline")
    rows = cursor.fetchall()
    print("Inserted Airlines:")
    for row in rows:
        print(row)

def print_terminals(cursor):
    cursor.execute("SELECT * FROM terminal")
    rows = cursor.fetchall()
    print("Inserted Terminals:")
    for row in rows:
        print(row)

def print_gates(cursor):
    cursor.execute("SELECT * FROM gate")
    rows = cursor.fetchall()
    print("Inserted Gates:")
    for row in rows:
        print(row)

def print_model(cursor):
    cursor.execute("SELECT * FROM model")
    rows = cursor.fetchall()
    print("Inserted Models:")
    for row in rows:
        print(row)




#run modular functions to initialize DB

def main():
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection.cursor() as cursor:
        '''
        seed_airlines(cursor)
        connection.commit()

        #gate is dependent on terminal so commit it before 
        seed_terminals(cursor)
        connection.commit()

        seed_gates(cursor)
        connection.commit()
        
        seed_model(cursor)
        connection.commit()
        '''

        # View data (optional)
        print_airlines(cursor)
        print_terminals(cursor)
        print_gates(cursor)
        print_model(cursor)

    connection.close()

# Entry point
if __name__ == "__main__":
    main()
