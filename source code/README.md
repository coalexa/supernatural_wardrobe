Project 6 Portfolio Assignment - Supernatural Wardrobe
CS340 – Intro to Databases

Designed and implemented a web app using Python, Flask, and Jinja2 with a MySQL backend
Created Fall 2022 by Alexa Castro and Carolina Rodriguez.


Web-based UI implements a database for a costume warehouse. This contains 5 entities
costumes, themes, inventory,companies, and orders. An intersection table between costume
and orders. CRUD Implemenations such as CREATE/UDPATE/DELETE/SELECT can be perfomred 
on this app.

Built in Flask, Python, and MySQL. 




RUN Program:

pip3 install --user virtualenv
python3 -m venv .
source ./bin/activate
pip3 install flask-mysqldb
pip3 install gunicorn

Dependencies:
click==8.0.4
dataclasses==0.8
Flask==2.0.3
Flask-MySQLdb==1.0.1
gunicorn==20.1.0
importlib-metadata==4.8.3
itsdangerous==2.0.1
Jinja2==3.0.3
MarkupSafe==2.0.1
mysqlclient==2.1.1
python-dotenv==0.20.0
typing-extensions==4.1.1
Werkzeug==2.0.3
zipp==3.6.0
