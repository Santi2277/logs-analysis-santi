# Logs Analysis - Udacity

### Full Stack Web Development ND

_______________________

## About

This project consists in a web server (created with Python3, SQL and Html).

Which analyzes a fictional database containing newspaper articles.

Displaying the information about the kind of articles the site's readers like.

 - What are the most popular three articles of all time?

 - Who are the most popular article authors of all time?

 - On which days did more than 1% of requests lead to errors?


The database contains 3 tables: authors (4 entries), articles (8),  
and log (more than 1000 entries). The log one registers the user's movements  
at the page. The connection between them and its data make possible to find a  
solution for each question.


## Prerequisites

* [Python 3](https://www.python.org/downloads/)  
Download for Windows, run `brew install python3` on Mac  
or `sudo apt-get install python3` on Linux

* [VirtualBox 3](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)  
Necessary download and install to use vagrant on it

* [Vagrant](https://www.vagrantup.com/downloads.html)  
Install, then in terminal change directory to the vagrant folder,  
run `vagrant up` to initialize, run `vagrant ssh` after to log in

* [News Database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)  
Follow the link to download the data for the database (put this .sql file  
in the vagrant directory)


## Installation

After installing all the necessary specified below and run vagrant ssh.

Change directory again to vagrant.

Use the command `psql -d news -f newsdata.sql` to load the database.

Use `psql -d news` to acces to the database with vagrant.

To enable the app (**server**) run  `python logs-project.py` and send the GET  

request with other terminal to the shown port. It will display the solution

like ordered lists in Html.


## Create View Statements


The following helper views were created in order to make SQL queries
more readable.

```sql
CREATE VIEW art_visits AS

    SELECT title AS art_title, visits, author

    FROM (SELECT path, COUNT(path) AS visits

          FROM log WHERE path != '/'

          GROUP BY path

          ORDER BY visits DESC

          LIMIT 8) AS subquery

            JOIN articles

             ON subquery.path = CONCAT('/article/',

                                       articles.slug)

             ORDER BY visits DESC
```

```sql
CREATE VIEW log_date AS

                                       SELECT status, CAST(time AS DATE)

                                       FROM log
```
```sql
CREATE VIEW log_date_tot_req AS

                   SELECT time, COUNT(status) AS count_tot

                   FROM log_date

                   GROUP BY time
```
```sql
CREATE VIEW log_date_err_req AS

                   SELECT time, COUNT(status) AS count_err

                   FROM (SELECT time, status

                           FROM log_date

                           WHERE status LIKE '4%'

                               OR status LIKE '5%') AS subquery

                           GROUP BY subquery.time
```
## Known Bugs

The tests were separated in two parts. SQL queries were tested with vagrant

but the server itself (Python3 code and Html)  was tested by Windows (running

the server with the Bash terminal and accessing via webbrowser, with a similar

created Windows database) due to having problems on doing a GET request with

other vagrant terminal.