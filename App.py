from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL,MySQLdb
import bcrypt
import os
import shutil

PORT = 5000
DEBUG= True

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


def scrapTheme(theme, max_images):
    try:
        if os.path.exists(f"scrapped"):
            flag=True
        else:
            os.mkdir(f"scrapped")
            flag=True
        if flag:
            if os.path.exists(f"scrapped/{theme}"):
                shutil.rmtree(f"scrapped/{theme}")
            # Crear la carpeta
           
            os.mkdir(f"scrapped/{theme}")
            os.system(f"instagram-scraper {theme} -m {max_images} -t image -d scrapped/{theme} -u benjaminmartincito341 -p supergoku")
            
            # Eliminar la foto de perfil
            
            directorio = os.listdir(f"scrapped/{theme}")
            directorio.sort()
            os.remove(f"scrapped/{theme}/{directorio[0]}")

    except:
        # Si falla
        print("False")
        return False

    print("True")
    return True



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
        return render_template('home.html')
    return render_template('home.html')

@app.route("/scrapper", methods=['POST'])
def scrap():
    lista= (("futboltvmemes","1"),("memes_futboleros_","2"),("outofcontextfutchile._","3"),("outofcontextcolocolo","4"),("nbamemes","5"),("basketball_.meme","6"),("basket_ball_memes","7"),("memesvoleibol","8"),("voleibol_memes","9"),("lossimpsonsmemesok","10"),("memesimpsonok","11"),("https://instagram.com/los.simpson.memes.2.0?utm_medium=copy_link","12"),("https://instagram.com/valorantmomentos?utm_medium=copy_link","13"),("https://instagram.com/memesvalorant.es?utm_medium=copy_link","14"),("https://instagram.com/memes.usm?utm_medium=copy_link","15"),("https://instagram.com/usm3mes?utm_medium=copy_link","16"),("https://instagram.com/usmemes.exe?utm_medium=copy_link","17"),("https://instagram.com/memes_de_perros?utm_medium=copy_link","18"),("https://instagram.com/memes_perros_cl?utm_medium=copy_link","19"),("https://instagram.com/memes_de_perross?utm_medium=copy_link","20"),("https://instagram.com/michis.para.ti?utm_medium=copy_link","21"),("https://instagram.com/memes_de_gatos?utm_medium=copy_link","22"),("https://instagram.com/memes_chistosos_de_gatos?utm_medium=copy_link","23"),("https://instagram.com/outofcontextpoliticoschile?utm_medium=copy_link","24"),("https://instagram.com/esdepoliticos?utm_medium=copy_link","25"),("https://instagram.com/politicalcompass.chile?utm_medium=copy_link","26"),("https://instagram.com/lol.chile?utm_medium=copy_link","27"),("https://instagram.com/leaguemasivo?utm_medium=copy_link","28"),("https://instagram.com/memes_lol.las?utm_medium=copy_link","29"),("https://instagram.com/ayudas.clubes.proo?utm_medium=copy_link","30"),("https://instagram.com/fifa_y_piscolas?utm_medium=copy_link","31"),("https://instagram.com/memes_dearte?utm_medium=copy_link","32"),("https://instagram.com/memesdearteclasico?utm_medium=copy_link","33"),("https://instagram.com/chilelawea?utm_medium=copy_link","34"),("https://instagram.com/memelasdeorizaba?utm_medium=copy_link","35"),("https://instagram.com/cabronazi?utm_medium=copy_link","36"),("https://instagram.com/stamamalon?utm_medium=copy_link","39"),("https://instagram.com/oufits_para_hombres?utm_medium=copy_link","38"),("https://instagram.com/frases_inspiradoras_oficial?utm_medium=copy_link","37"),("https://instagram.com/frases.motivacionales.diarias?utm_medium=copy_link","40"),("https://instagram.com/frasesmotivaciondetodounpoco?utm_medium=copy_link","41"),("https://instagram.com/minecraft_memes.esp?utm_medium=copy_link","42"),("https://instagram.com/minecraftmemeschile?utm_medium=copy_link","43"),("https://instagram.com/memes_minecraft1?utm_medium=copy_link","44"),("https://instagram.com/casadepapelmemes?utm_medium=copy_link","45"),("https://instagram.com/la_casa_de_papel_memess?utm_medium=copy_link","46"),("https://instagram.com/memes.casa.de.papel?utm_medium=copy_link","47"),("https://instagram.com/eljuegodelcalamar.memes?utm_medium=copy_link","48"),("https://instagram.com/el_juego_del_calamar_fans1?utm_medium=copy_link","49"),("https://instagram.com/memes.juego.calamar?utm_medium=copy_link","50"),("https://instagram.com/memesmusicales_?utm_medium=copy_link","51"),("https://instagram.com/aestudiaracasa?utm_medium=copy_link","52"),("https://instagram.com/memesdemusica_?utm_medium=copy_link","53"),("https://instagram.com/fortnitememeschile?utm_medium=copy_link","54"),("https://instagram.com/memes_chile_fortnite?utm_medium=copy_link","55"),("https://instagram.com/memesft_?utm_medium=copy_link","56"),("https://instagram.com/pokecitas?utm_medium=copy_link","57"),("https://instagram.com/pokememes_originales?utm_medium=copy_link","58"),("https://instagram.com/_shiny_posting_?utm_medium=copy_link","59"))
    if request.method == 'POST':
        email= session["email"]
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        gustos=user["gustos"].split(";")
        curl.close()
        for categoria in gustos:
            s = categoria.split(",")
            for a in s:
                for l in lista:
                    if l[1]==a:
                        scrapTheme(l[0], 3)
        return "DONE"
if __name__ ==  '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(port=PORT , debug=DEBUG)