import bcrypt
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flaskext.mysql import MySQL

app = Flask(__name__)
app.secret_key = 'mysecretkey'

mysql = MySQL()

# MySQL configuration
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'flask'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)


@app.route('/')
def hello():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return redirect(url_for('login'))


@app.route('/welcome')
def home():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with mysql.get_db().cursor() as cursor:
            cursor.execute("SELECT password FROM users WHERE username = %s", username)
            result = cursor.fetchone()
            if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
                session['username'] = username
                return redirect(url_for('home'))
            else:
                return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('hello'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        with mysql.get_db().cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            if result:
                return render_template('signup.html', error='Username already taken')
            elif password != confirm_password:
                return render_template('signup.html', error='Passwords do not match')
            else:
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
                mysql.get_db().commit()
                session['username'] = username
                return redirect(url_for('home'))
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)