from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL,MySQLdb
import bcrypt

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("home.html")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("login.html")
    


@app.route('/registrarse')
def registrarse():
    return render_template('register.html')
    
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",(name,email,hash_password,))
        mysql.connection.commit()
        
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('home'))     

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("index.html")

@app.route('/gustos', methods=['GET', 'POST'])
def gustos():
    if request.method == 'POST': 
        gustos= request.form.getlist('mycheckbox')
        salida=""
        for s in gustos:
            salida+=s+";"
        salida=salida[:-1]
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET gustos=(%s) WHERE email=(%s) ", (salida,session['email']))
        mysql.connection.commit()
        print(salida)
        print(session['email'])
        return 'Done'
    return render_template('home.html')

if __name__ ==  '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(port = 3000, debug = True )