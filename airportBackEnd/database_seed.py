import pymysql
from dotenv import load_dotenv
import os
import pandas as pd
import random

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
job_roles =['Flight Attendant','Co-Pilot','Flight Engineer','Captain','Flight Attendant Lead']


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
    for index, row in df.iterrows():#itterrows allows iteration through each row of dataframe df, each row accessed by index, 
        model = row['model_name']#subset of the row
        airline=row['airline_name']
        sql="INSERT INTO airplane(model_name,airline_name) VALUES(%s,%s)"
        cursor.execute(sql,(model,airline,))


def seed_employee(cursor):
    df=pd.read_csv('data/employee.csv')
    ssn_set =set()
    for index, row in df.iterrows():
        ssn = f"{random.randint(0,999999999)}"
        while True:
            formatted_ssn =f"{ssn[:3]}-{ssn[3:5]}-{ssn[5:]}"
            if formatted_ssn not in ssn_set:
                ssn_set.add(formatted_ssn)#add to hashmap to ensure uniqueness

                job_role = row['job_role']
                employ_fname = row['employ_fname']
                employ_lname = row['employ_lname']
                airline_name = row['airline_name']

                sql="INSERT INTO employee(employ_ssn,job_role,employ_fname,employ_lname,airline_name) VALUES(%s,%s,%s,%s,%s)"
                cursor.execute(sql,(formatted_ssn,job_role,employ_fname,employ_lname,airline_name))
                break


# === Print Utility Function ===

def print_table(tablename,cursor):
    query = f"SELECT * FROM {tablename}"
    cursor.execute(query)
    rows = cursor.fetchall()
    print(f"Inserted {tablename}:")
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
        #table seeding is in order with respect to relationships, run individually.
        seed_airlines(cursor)
        connection.commit()

        seed_terminals(cursor)
        connection.commit()

        seed_gates(cursor)
        connection.commit()
        
        seed_model(cursor)
        connection.commit()

        seed_airplane(cursor)
        connection.commit()

        seed_employee(cursor)
        connection.commit()
        '''
        connection.commit()

        # View data (optional)
        #print_table('terminal',cursor)
        #print_table('gate',cursor)
        #print_table('model',cursor)
        #print_table('airplane',cursor)
        print_table('employee',cursor)


    connection.close()

# Entry point
if __name__ == "__main__":
    main()
