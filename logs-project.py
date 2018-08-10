from flask import Flask
import psycopg2

#new object (using flask microfamework)
app = Flask(__name__)

#html code to be shown in response
GET1 = '''
<h1>LOGS ANALYSIS PROJECT (Udacity, Santi Lozano)</h1>
<h1>1.- What are the most popular three articles of all time?</h1>
<ol>
'''
PART2 = '''
  <li>"{str1}" -- {str2} views</li>
'''
FINAL = '''
 </ol>
'''

#method for when someone accesses to root directory
@app.route('/')
def hello():
    #connect to database news
    db = psycopg2.connect(dbname="news", user="postgres", password="akiratoriyama")
    c = db.cursor()
    #execute query to find more popular 3 articles titles and its views
    c.execute(" select title, numb from (select path, count(path) as numb from log where path != '/' group by path order by numb desc limit 3) as subquery join articles on subquery.path = CONCAT('/article/', articles.slug) order by numb desc")
    message = c.fetchall()

    #pass the result of the query to an html code created (PART2 python multi-line), as a list line added to
    #initial html code (GET1)
    for path, numb in message:
        global GET1
        GET1= GET1 + PART2.format(str1=path, str2=numb)
    db.close()
    #return that html code plus the code necessary (FINAL) to close the ordered list
    return GET1+FINAL

#initiliaze the app on that port
app.run(port=4996)
