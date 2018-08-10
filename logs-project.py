from flask import Flask
import psycopg2
from prettytable import PrettyTable


app = Flask(__name__) #new object

GET1 = '''
<h1>LOGS ANALYSIS PROJECT (Udacity, Santi Lozano)</h1>
<h1>1.- What are the most popular three articles of all time?</h1>
<table style="width:100%">
  <tr>
    <th>Name</th>
    <th>Bio</th>
    <th>ID</th>
  </tr>
'''
PART2 = '''
  <tr>
    <td>{str1}</td>
    <td>{str2}</td>
    <td>{str3}</td>
  </tr>
'''
FINAL = '''
 </table>
'''

@app.route('/')
def hello():
    db = psycopg2.connect(dbname="news", user="postgres", password="akiratoriyama")
    c = db.cursor()
    c.execute("select * from authors")
    message = c.fetchall()

    #query result, put in the table
    for name, bio, id in message:
        global GET1
        GET1= GET1 + PART2.format(str1=name, str2=bio, str3=id)
    db.close()

    return GET1+FINAL

app.run(port=4996)
