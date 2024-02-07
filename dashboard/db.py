import psycopg2 
import click

from flask import current_app, g

import csv
from datetime import datetime
import os

# for initialising the database.
def init_db():
    database_connection = psycopg2.connect(database='titanic', user='postgres', password='k@rabo2024', host='localhost', port='5432')

    curr = database_connection.cursor()

    # creating the passenger table if is not there in the database
    curr.execute('''CREATE TABLE IF NOT EXISTS Passenger (id serial \ 
        PRIMARY KEY, name varchar(100), sex varchar(10), age int, \
        sibsp int, parch int, fare float, embarked varchar(1), survived int);''')

    database_connection.commit()

    curr.close()
    database_connection.close()


# for getting the database connection.
def get_db():
    if 'database_connection' not in g:
        g.database_connection = psycopg2.connect(database='titanic', user='postgres', password='k@rabo2024', host='localhost', port='5432')

    return g.database_connection

# for closing the database connection after completing a request.
def close_db():
    db = g.get('database_connection', None)
    if db is not None:
        db.close()

# for loading the data to the passenger table
def load_data():
    filaPath = os.path.join(os.pardir(), 'titanic.csv')

    with open(filaPath, 'r') as csvFile:
            reader = csv.DictReader(csvFile)
            cur = get_db().cursor()

            for row in reader:
                name = row['Name'].strip()
                sex = row['Sex'].strip()
                age = row['Age'].strip()
                embarked = row['Embarked'].strip()
                if len(sex) == 0 or len(age) == 0 or len(name) == 0 or len(embarked) == 0:
                    continue

                fare = row['Fare'].strip()
                sibsp = row['Sibsp'].strip()
                parch = row['Parch'].strip()
                survived = row['Survived'].strip()
                if len(fare) == 0 or len(sibsp) == 0 or len(parch) == 0 or len(survived):
                    continue
                
                # cur = get_db().cursor()
                cur.execute('''INSERT INTO Passenger (name, sex, age, sibsp, parch, fare, embarked, survived) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);''', (name, sex, age, sibsp, parch, fare, embarked, survived))
            # close the cursor
            cur.close()
            get_db().commit()
            

# command for initialising the database
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo("Initialiased the database!")

# command for initialising the database
@click.command('load-data')
def load_data_command():
    load_data()
    click.echo("Loaded the data to the database!")


# for adding methods to the app
def add_methods(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(load_data_command)


