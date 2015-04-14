from flask import render_template, Flask, request, session, redirect
app = Flask(__name__)
default_password = "password"

app.secret_key = 'my_secret_key'

@app.route('/')
def main():
  return "This is not a valid page"

def is_valid_login(password):
  if password == default_password:
      return True
  return False

def log_the_user_in(username):
  # we don't use sessions here so there is no extra work to be done
  pass

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

@app.route('/color', methods=['POST'])
def favColor():
  #session['color'] = "green"
  session['color'] = request.form['color']
  if session['username'] is not None and session['color'] is not None:
    return render_template('color.html', color=session['color'], username=session['username'])

@app.route('/logout')
def logout():
  clearSession()
  return redirect('/login')

if __name__ == '__main__':
  app.debug = True
  app.run()