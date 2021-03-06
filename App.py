from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from flask.cli import routes_command
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

def listafoto():
    listafotos=[]
    for file in os.listdir("uploads"):
        for foto in os.listdir("uploads/"+file):
            listafotos.append((file,foto))
    return listafotos



@app.route('/uploads/<carpeta>/<nombreFoto>')
def uploads(carpeta,nombreFoto):
    CARPETA=os.path.join("uploads/"+carpeta)
    app.config["CARPETA"]=CARPETA
    return send_from_directory(app.config["CARPETA"],nombreFoto)

@app.route('/predeterminada/images.png')
def predeterminada():
    CARPETA=os.path.join("predeterminada/")
    app.config["CARPETA"]=CARPETA
    return send_from_directory(app.config["CARPETA"],"images.png")


def scrapTheme(theme, max_images, x):
    try:
        if os.path.exists("uploads"):
            flag=True
        else:
            os.mkdir(f"uploads")
            flag=True
        if flag:
            if os.path.exists(f"uploads/{x}"):
                shutil.rmtree(f"uploads/{x}")
            # Crear la carpeta
           
            os.mkdir(f"uploads/{x}")
            os.system(f"instagram-scraper {theme} -m {max_images} -t image -d uploads/{x} -u trabajoiwg8@gmail.com -p Holamundo.")
            
            # Eliminar la foto de perfil
            
            directorio = os.listdir(f"uploads/{x}")
            directorio.sort()
            os.remove(f"uploads/{x}/{directorio[0]}")

    except:
        # Si falla
        return False

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

@app.route('/foto', methods=["GET",'POST'])
def foto():
    listfoto=scrap()
    return render_template('foto.html',listfoto=listfoto)

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
            salida+=s+","
        salida=salida[:-1]
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET gustos=(%s) WHERE email=(%s) ", (salida,session['email']))
        mysql.connection.commit()
        return render_template('home.html')
    return render_template('home.html')

@app.route('/likes', methods=['GET', 'POST'])
def likes():
    if request.method == 'POST': 
        likes= request.form.getlist('mycheckbox')
        carpeta=""
        listalikes=[]
        k=0
        listafotos=[]
        promedio=""
        for file in os.listdir("uploads"):
            for foto in os.listdir("uploads/"+file):
                listafotos.append((file,foto))
        for a in listafotos:
            if a[0] != carpeta:
                listalikes.append(promedio)
                promedio=0
                carpeta=a[0]
                promedio+=int(likes[k])
                k+=1
            else:
                promedio+=int(likes[k])
                k+=1
        listalikes.append(promedio)
        del listalikes[0]

        #Update gustos

        email= session["email"]
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        gustos=user["gustos"].split(",")
        curl.close()
        i=len(listalikes)
        c=0
        print(listalikes)
        print(gustos)
        for x in range(i):
            if listalikes[x]<0:
                del gustos[x-c]
                c+=1
        print(gustos)
        salida=""
        for s in gustos:
            salida+=s+","
        salida=salida[:-1]
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET gustos=(%s) WHERE email=(%s) ", (salida,session['email']))
        mysql.connection.commit()
        return render_template('home.html')
    return render_template('home.html')

@app.route("/scrapper", methods=['POST'])
def scrap():
    lista = (("futboltvmemes","1"),("memes_futboleros_","2"),("outofcontextfutchile._","3"),("outofcontextcolocolo","4"),("nbamemes","5"),("basketball_.meme","6"),("basket_ball_memes","7"),("memesvoleibol","8"),("voleibol_memes","9"),("lossimpsonsmemesok","10"),("memesimpsonok","11"),("los.simpson.memes.2.0","12"),("valorantmomentos","13"),("memesvalorant.es","14"),("memes.usm","15"),("usm3mes","16"),("usmemes.exe","17"),("memes_de_perros","18"),("memes_perros_cl","19"),("memes_de_perross","20"),("michis.para.ti","21"),("memes_de_gatos","22"),("memes_chistosos_de_gatos","23"),("outofcontextpoliticoschile","24"),("esdepoliticos","25"),("politicalcompass.chile","26"),("lol.chile","27"),("leaguemasivo","28"),("memes_lol.las","29"),("ayudas.clubes.prook","30"),("fifa_y_piscolas","31"),("memes_dearte","32"),("memesdearteclasico","33"),("chilelawea","34"),("memelasdeorizaba","35"),("cabronazi","36"),("stamamalon","39"),("oufits_para_hombres","38"),("frases_inspiradoras_oficial","37"),("frases.motivacionales.diarias","40"),("frasesmotivaciondetodounpoco","41"),("minecraft_memes.esp","42"),("minecraftmemeschile","43"),("memes_minecraft1","44"),("casadepapelmemes","45"),("la_casa_de_papel_memess","46"),("memes.casa.de.papel","47"),("eljuegodelcalamar.memes","48"),("el_juego_del_calamar_fans1","49"),("memes.juego.calamar","50"),("memesmusicales_","51"),("aestudiaracasa","52"),("memesdemusica_","53"),("fortnitememeschile","54"),("memes_chile_fortnite","55"),("memesft_","56"),("pokecitask","57"),("pokememes_originales","58"),("_shiny_posting_","59"))

    if request.method == 'POST':
        email= session["email"]
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        gustos=user["gustos"].split(",")
        curl.close()
        if os.path.exists("uploads"):
            shutil.rmtree("uploads")
            os.mkdir(f"uploads")
        for s in gustos:
            for l in lista:
                if l[1]==s:
                    scrapTheme(l[0], 3,l[1])
        listfoto=listafoto()
        return (listfoto)
if __name__ ==  '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(port=PORT , debug=DEBUG)