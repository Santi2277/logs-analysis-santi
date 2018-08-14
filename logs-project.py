#!/usr/bin/env python3
from flask import Flask
import psycopg2
import datetime


# new object (using flask microfamework)
app = Flask(__name__)

# html code to be shown in response
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
QUERY2 = '''
<h1>2.- Who are the most popular article authors of all time?</h1>
<ol>
'''
PART3 = '''
  <li>{str1} -- {str2} views</li>
'''
QUERY3 = '''
<h1>3. On which days did more than 1% of requests lead to errors?</h1>
<ol>
'''
PART4 = '''
  <li>{str1} -- {str2}% errors</li>
'''

# method for when someone accesses to root directory


@app.route('/')
def hello():
    # connect to database news
    # NOTE my windows database code for test was
    # db = psycopg2.connect(dbname="news",
    # user="postgres", password="akiratoriyama")
    # NOTE db connection with vagrant
    try:
        db = psycopg2.connect(dbname="news")
    except:
        print ("Unable to connect to the database")
    c = db.cursor()

    # 1ST QUERY
    # execute query to find more popular 3 articles titles and its views
    c.execute(""" SELECT title, numb
                    FROM (SELECT path, COUNT(path) AS numb
                            FROM log
                            WHERE path != '/'
                            GROUP BY path
                            ORDER BY numb DESC
                             LIMIT 3) AS subquery
                                    JOIN articles
                                    ON subquery.path = CONCAT('/article/',
                                                                articles.slug)
                                    ORDER BY numb DESC""")
    message = c.fetchall()
    # pass the result of the query to an html code created
    # (PART2, python multi-line) which acts as a list line added to
    # initial html code (GET1)
    for path, numb in message:
        global GET1
        GET1 = GET1 + PART2.format(str1=path, str2=numb)
    SHOW = GET1+FINAL+QUERY2

    # 2ND QUERY
    # create a helper view with the articles, its visits and its author
    c.execute("""CREATE VIEW art_visits AS
                    SELECT title AS art_title, visits, author
                        FROM (SELECT path, COUNT(path) AS visits
                            FROM log WHERE path != '/'
                            GROUP BY path
                            ORDER BY visits DESC
                            LIMIT 8) AS subquery
                                    JOIN articles
                                    ON subquery.path = CONCAT('/article/',
                                                                articles.slug)
                                    ORDER BY visits DESC""")
    db.commit()
    # 2nd query, sum visits of an author (sum its articles visits)
    # using the helper view
    c.execute("""SELECT name, count_vis
                    FROM (SELECT author, sum(visits) AS count_vis
                     FROM art_visits
                     GROUP BY author) AS subquery
                                        JOIN authors
                                        ON subquery.author = authors.id
                                        ORDER BY count_vis DESC""")
    message = c.fetchall()
    for name, count_vis in message:
        SHOW = SHOW + PART3.format(str1=name, str2=count_vis)
    # drop helper view
    c.execute("drop view art_visits")
    db.commit()

    # 3rd QUERY
    SHOW2 = SHOW+FINAL+QUERY3
    # view1 -- log_date
    # (contains log with status and time in date format to know the day)
    c.execute("""CREATE VIEW log_date AS
                                        SELECT status, CAST(time AS DATE)
                                        FROM log""")
    db.commit()
    # view2 -- log_date_tot_req
    # (log with day and total requests for that day)
    c.execute("""CREATE VIEW log_date_tot_req AS
                    SELECT time, COUNT(status) AS count_tot
                    FROM log_date
                    GROUP BY time""")
    db.commit()
    # view3 -- log_date_err_req
    # (log with day and total error requests for that day)
    c.execute("""CREATE VIEW log_date_err_req AS
                    SELECT time, COUNT(status) AS count_err
                    FROM (SELECT time, status
                            FROM log_date
                            WHERE status LIKE '4%'
                                OR status LIKE '5%') AS subquery
                            GROUP BY subquery.time""")
    db.commit()
    # 3rd query (NOTE percentage is multiplied by 100, 2.5% will be 250 here)
    # (days more 1% requests lead errors)
    c.execute("""SELECT a.time, 10000*count_err/count_tot AS expr
                    FROM log_date_err_req a
                        JOIN log_date_tot_req b
                        ON b.time = a.time
                        WHERE (10000*count_err/count_tot) > 100""")
    message = c.fetchall()
    for name, count_vis in message:
        err = count_vis/100.0
        SHOW2 = SHOW2 + PART4.format(str1=name.strftime("%B %d, %Y"),
                                     str2="%.1f" % err)

    # drop views
    c.execute("drop view log_date_tot_req")
    db.commit()
    c.execute("drop view log_date_err_req")
    db.commit()
    c.execute("drop view log_date")
    db.commit()

    db.close()
    # return that html code plus the code necessary (FINAL)
    # to close the ordered list
    return SHOW2+FINAL

# initiliaze the app on that port
app.run(port=4996)
