
#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 

Course work: 

@author: Gokul and Team

Source:
    https://stackoverflow.com/questions/13279399/how-to-obtain-values-of-request-variables-using-python-and-flask
'''

from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)


database = 'db/test.db'

def select_all(conn):
    """
    Query all rows in the flask1 table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM flask1")
 
    rows = cur.fetchall()
    
    print('rows count : '+str(len(rows)))
    
    if(len(rows) <= 0):
        print('No Data available')
 
    item_list = []
    for row in rows:
        print(row) 

        current_id = row[0]
        current_name = row[1]
        current_dept = row[2]

        current_dict = {
            'id' : current_id,
            'name' : current_name,
            'dept' : current_dept
        }

        item_list.append(current_dict)

    return item_list

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    
    name = None

    if request.method == 'POST':
        name = request.values.get("name")

    return name

'''
    http://127.0.0.1:5000/api/base
'''
@app.route('/api/base')
def api_base():
    
    result = {
        'food' : 'Poori',
        'name' : 'Rakshmitha'
    }

    return result

'''
    http://127.0.0.1:5000/api/student?name=gokul
'''
@app.route('/api/student')
def api_get_param():

    name = request.values.get("name")
    
    result = {
        'name' : name
    }

    return result

'''
    http://127.0.0.1:5000/api/path/test/chennai/tamilnadu
'''
@app.route('/api/path/test/<city>/<state>')
def api_get_path_variable(city, state):
    
    result = {
        'food' : 'Poori',
        'name' : 'Rakshmitha',
        'city' : city,
        'state' : state
    }

    return result

'''
    http://127.0.0.1:5000/api/db/vanilla/select
'''
@app.route('/api/db/vanilla/select')
def api_db_vanilla_select():

    item_list = None
    with sqlite3.connect("db/test.db") as conn:
        item_list = select_all(conn)

    result = {
        'users' : item_list
    }

    return result

if __name__ == "__main__":
    app.run(debug=True)