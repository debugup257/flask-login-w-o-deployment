from mimetypes import init
from pickle import FALSE
from flask import Flask, render_template, render_template_string, request,redirect,url_for,session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from datetime import timedelta

conn = psycopg2.connect(
   database="trax", user='postgres', password='devesh1234', host='127.0.0.1', port= '5432'
)
c = conn.cursor()




app = Flask(__name__)
app.secret_key="hello"

app.config['SQLACHEMY_DATABASE_URI']='postgresql://postgres:devesh1234@localhost/trax'

app.config['SQLALCHEMY TRACK MOIFICATIONS'] = False
db=SQLAlchemy()

class user(db.Model):
    username = db.Column(db.String(100),primary_key=True)
    password = db.Column(db.String(100))
    user_type = db.Column(db.String(100))

    def __init__(self,username,password,user_type):
        self.username = username
        self.password = password
        self.user_type = user_type


conn = psycopg2.connect(
   database="trax", user='postgres', password='devesh1234', host='127.0.0.1', port= '5432'
)
c = conn.cursor()

@app.route('/', methods =["GET", "POST"])
def index():
    return render_template("login.html")

@app.route('/user',methods=["GET", "POST"])
def login():

    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        c.execute("SELECT username FROM users;")
        usernames = (c.fetchall())
        usernames_list=[]

        for i in usernames:
            usernames_list.append(i[0])
        conn.commit()
        
        c.execute("SELECT password FROM users;")
        passwords = (c.fetchall())
        passwords_list=[]

        for i in passwords:
            passwords_list.append(i[0])
        conn.commit()

        if username in usernames_list:
            if password in passwords_list:
                session.permanent=False
                session["user"]=username
                c.execute("""SELECT user_type FROM users WHERE username = %(value)s; """,{"value":username})
                user_type = (c.fetchall())
                if user_type[0][0]=="admin":
                    return redirect (url_for("admin_user"))


                

                
    return redirect (url_for("index"))

@app.route('/admin_user',methods=["GET", "POST"])
def admin_user():
    if "user" in session:
        if request.method=="POST":
            username = request.form.get("username")
            password = request.form.get("password")
            user_type = request.form.get("user_type")

            c.execute("""INSERT INTO users(username,password,user_type) VALUES('{value1}','{value2}','{value3}')""".format(value1=username,value2=password,value3=user_type))
            conn.commit()

        return render_template("admin_user.html")
    else:
        return render_template("login.html")

    

@app.route('/sales_form')
def sales_form():
    return render_template("sales_form.html")


if __name__ == '__main__':
    app.run(debug=True)