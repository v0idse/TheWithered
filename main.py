import os
from flask import Flask, render_template, redirect, request
import sqlite3
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
con = sqlite3.connect('./databases/users.db', check_same_thread=False)
cur = con.cursor()

@app.route('/')
def start():
	return render_template('startpage.html')

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/form_login',methods=['POST','GET'])
def login_form():
    con = sqlite3.connect('./databases/users.db', check_same_thread=False)
    cur = con.cursor()
    check1 = []
    name1=request.form['username']
    pwd=request.form['password']
    check = cur.execute(f"""SELECT hash_password FROM Main WHERE username = '{name1}'""")
    #con.close()
    for elem in check:
        check1.append(elem)
    noquote = str(*check1).replace("'", "")
    nostring = str(noquote).replace('(', '')
    if nostring!=str(pwd + ',)'):
        return render_template('login.html',info='Invalid Password')
    else:
        con.close()
        return render_template('home.html',name=name1)

@app.route('/register')
def register():
  return render_template('register.html')

@app.route('/form_register',methods=['POST','GET'])
def form_register():
    con = sqlite3.connect('./databases/users.db', check_same_thread=False)
    cur = con.cursor()
    check1 = []
    name1=request.form['username']
    pwd=request.form['password']
    email=request.form['email']
    cur.execute(f"""INSERT INTO Main (username, hash_password, email) VALUES ('{name1}', '{pwd}', '{email}')""")
    con.commit()
    con.close()
    return redirect('/login')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
