from flask import render_template, Flask, request, session, redirect
import sqlite3
app = Flask(__name__)
default_password = "password"
app.secret_key = 'my_secret_key'

def getdb():
  return db

def getCursor():
  return getdb().cursor()

def connectdb():
  db = sqlite3.connect('users.db')

def closedb():
  getdb().close()

@app.route('/')
def main():
  return "This is not a valid page"

def is_valid_login(password):
  if password == default_password:
      return True
  return False

def parse_form(form):
  if 'username' in request.form:
    username = request.form['username']
  else:
    username = ""

  if 'password' in request.form:
    password = request.form['password']
  else:
    password = None
  return username, password

def clearSession():
  session['color'] = None
  session['username'] = None
  session['password'] = None

@app.route('/login', methods=['POST', 'GET'])
def login():
  error = None
  username = ""
  clearSession()
  if request.method == 'POST':
    session['username'], session['password'] = parse_form(request.form)
    if is_valid_login(session['password']):
      if session['username'] == "vaibhav" or session['username'] == "Vaibhav":
        session['username'] = "bottom bitch"
      return render_template('user.html', username=session['username'])
    else:
      error = 'Invalid username/password'
  elif session['username'] is not None:
    return render_template('user.html', username=session['username'])
  return render_template('login.html', username=username, error=error)

@app.route('/color', methods=['POST', 'GET'])
def favColor():
  #session['color'] = "green"
  if request.method == 'POST':
    session['color'] = request.form['color']
  if session['username'] is not None and session['color'] is not None:
    return render_template('color.html', color=session['color'], username=session['username'])
  return redirect('/login')

@app.route('/logout')
def logout():
  clearSession()
  return redirect('/login')

@app.route('/register', methods=['post','get'])
def register():

  tableQuery = '''CREATE TABLE IF NOT EXISTS users(email TEXT,password TEXT, color TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT);'''
  checkUsers = '''SELECT 1 FROM users WHERE email=?;'''
  addUser = '''INSERT INTO users(email,password,color) VALUES(?,?,?);'''
  showData = '''SELECT * FROM users;'''

  if request.method == "POST":
    newUsername = request.form['username']
    newPassword = request.form['password']
    db = sqlite3.connect('users.db')
    c = db.cursor()
    c.execute(tableQuery)
    c.execute(addUser, (newUsername, newPassword, None))
    data = c.execute(showData)
    db.commit()

    #pyData = []
    #for item in data:



    db.close()
  return render_template('registerAccount.html')


if __name__ == '__main__':
  app.debug = True
  app.run()