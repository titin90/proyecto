from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'usuarios'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

@app.route('/register')
def register():
    return render_template('registro.html')
    
@app.route('/user', methods=["POST"])
def user():
    if request.method == "POST":
        usuario= request.form["usuario"]
        contraseña= request.form["contraseña"]
        print(usuario)
        print(contraseña)
        return "received"

@app.route('/edit')
def edit():
    return render_template('edit.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

if __name__ ==  '__main__':
    app.run(port = 3000, debug = True )