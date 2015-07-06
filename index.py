from flask import render_template, Flask, request, session, redirect
import sqlite3
app = Flask(__name__)
app.secret_key = 'my_secret_key'

@app.route('/')
def main():
  return "This is not a valid page"

def userExists(username):
  checkUsers = '''SELECT COUNT(*) FROM users WHERE email=?;'''

  db = sqlite3.connect('users.db')
  c = db.cursor()
  data = c.execute(checkUsers, (username,))
  for row in data:
    numAccounts = row[0]
  db.close()

  if numAccounts > 0:
    return True
  else:
    return False

def storeNewColor(username, color):
  colorQuery = '''UPDATE users SET color=? WHERE email=?;'''
  db = sqlite3.connect('users.db')
  c = db.cursor()
  c.execute(colorQuery,(color,username,))
  db.commit()
  db.close()

def findUserColor(username):
  selectQuery = '''SELECT * FROM users WHERE email=?;'''

  db = sqlite3.connect('users.db')
  c = db.cursor()
  data = c.execute(selectQuery,(username,))
  for row in data:
    userColor = row[2]
    db.close()
    return userColor


def is_valid_login(username, password):
  selectQuery = '''SELECT * FROM users WHERE email=?;'''

  db = sqlite3.connect('users.db')
  c = db.cursor()
  data = c.execute(selectQuery,(username,))
  for row in data:
    if row[1] == password:
      db.close()
      return True
    else:
      break
  db.close()
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
    if userExists(session['username']):
      if is_valid_login(session['username'], session['password']):
        if session['username'] == "vaibhav" or session['username'] == "Vaibhav":
          session['username'] = "bottom bitch"
        if findUserColor(session['username']):
          session['color'] = findUserColor(session['username'])
          return render_template('color.html', color=session['color'], username=session['username'])
        return render_template('user.html', username=session['username'])
      else:
        error = 'Invalid password'
    else:
      error = 'Username does not exist'
  elif session['username'] is not None:
    return render_template('user.html', username=session['username'])
  return render_template('login.html', username=username, error=error)

@app.route('/color', methods=['POST', 'GET'])
def favColor():
  #session['color'] = "green"
  if request.method == 'POST' and session['username'] is not None:
    session['color'] = request.form['color']
    storeNewColor(session['username'], session['color'])
  if session['username'] is not None and session['color'] is not None:
    return render_template('color.html', color=session['color'], username=session['username'])
  return redirect('/login')

@app.route('/logout')
def logout():
  clearSession()
  return redirect('/login')

@app.route('/breach')
def breach():
  showData = '''SELECT * FROM users;'''

  db = sqlite3.connect('users.db')
  c = db.cursor()
  data = c.execute(showData)
  pydata = 'username | password | favorite color <br> <br>'
  for row in data:
    pydata += str(row[3]) + ': ' + str(row[0]) + '|' + str(row[1]) + '|' + str(row[2]) + '<br>'
  db.close()
  return pydata


@app.route('/register', methods=['post','get'])
def register():

  tableQuery = '''CREATE TABLE IF NOT EXISTS users(email TEXT,password TEXT, color TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT);'''
  checkUsers = '''SELECT COUNT(*) FROM users WHERE email=?;'''
  addUser = '''INSERT INTO users(email,password,color) VALUES(?,?,?);'''
  showData = '''SELECT * FROM users;'''
  clearTable = '''DELETE FROM users;'''
  error = None

  if request.method == "POST":
    newUsername = request.form['username']
    newPassword = request.form['password']
    db = sqlite3.connect('users.db')
    c = db.cursor()
    c.execute(tableQuery)

    #find if user exists
    data = c.execute(checkUsers, (newUsername,))
    for row in data:
      numAccounts = row[0]

    if numAccounts > 0:
      error = 'Username already exists. Account not created'
      db.close()
      return render_template('registerAccount.html', error=error)
    else:
      c.execute(addUser, (newUsername, newPassword, None))
      db.commit()
      db.close()
      error = 'Account created!'
      return render_template('registerAccount.html', error=error)

    #data = c.execute(showData)
    db.commit()
    db.close()

  return render_template('registerAccount.html')

if __name__ == '__main__':
  app.debug = True
  app.run()