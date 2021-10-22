from flask import Flask, request, session
from flask.templating import render_template
from formulario import Formulario
from werkzeug.security import check_password_hash, generate_password_hash
import os
import sqlite3
from markupsafe import escape

app = Flask (__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=['POST', 'GET'])
def inicio():
    session.clear()
    form= Formulario()
    return render_template('login.html',form=form)

@app.route('/entrar', methods=['POST', 'GET'])
def entrar():
    form = Formulario()
    session.clear()
    if request.method == 'POST':
        correo = form.correo.data
        password = form.password.data
        with sqlite3.connect('data.db') as conexion:
            cur = conexion.cursor()
            sql = cur.execute("select password from usuarios where correo=?", [correo]).fetchone()
            print (sql)
            print (correo)
            if(sql != None):
                variable =sql[0]
                print (variable)
                if variable == password:
                # check_password_hash(variable,password):
                    session['correo']= correo
                    return render_template("feed.html")
            return render_template("login.html",form=form)
            
    return ('error')


 

@app.route('/feed',methods=['POST','GET'])
def ir():
    form = Formulario()
    if request.method == "POST":
        nombre = form.nombre.data
        sNombre = form.sNombre.data
        apellido = form.apellido.data
        sApellido = form.sApellido.data
        correo = form.correo.data
        password = form.password.data
        print(correo, password, nombre, sNombre, apellido, sApellido)
        return render_template('feed.html')
        

@app.route('/registro', methods=['POST', 'GET'])
def registro():
    form= Formulario()
    return render_template('registro.html',form=form)

@app.route('/registro/crear ',methods=['POST','GET'])
def registrocrear():
    form = Formulario()
    if request.method == 'POST':
        correo =  escape(form.correo.data)
        password = escape(form.password.data)
        nombre = form.nombre.data
        sNombre = form.sNombre.data
        apellido = form.apellido.data
        sApellido = form.sApellido.data
        cifrando = generate_password_hash(password,'sha512')
        print("cifrando",cifrando)
        if((correo == None or len(correo) == 0) or (password == None or len(password) == 0)):            
            return render_template("feed.html",form=form)
        else:
            with sqlite3.connect('data.db') as conexion:
                cur = conexion.cursor()
                cur.execute('insert into usuarios (nombre1,nombre2,apellido1, apellido2, correo, password) values (?,?,?,?,?,?)'
                            ,(nombre,sNombre,apellido, sApellido, correo,cifrando))
                #confirma la transaccion
                conexion.commit()
                return ('El login se inserto correctamente')
    return ('paso algo de error')

@app.route('/crear', methods=['GET'])
def crear():
    return render_template('CrearPub.html')
  
@app.route('/buscar')
def buscar():
    return render_template('buscar.html')

@app.route('/chat')
def chat():
    return render_template('chatymensajes.html')

# @app.route('/feed')
# def feed():
#     return render_template('feed.html')

@app.route('/notificaciones')
def notificaciones():
    return render_template('notificaciones.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/editar', methods=['POST', 'GET'])
def editar():
    return render_template('Editardatos.html')

@app.route('/detalle' ,methods=['GET'])
def detalle():
    return render_template('detallepost.html')

@app.route('/perfilp',methods=['GET'])
def perfilp():
    return render_template('perfilPub.html')


# rutas administrador
@app.route('/buscarAdmin',methods=['POST', 'GET','PUT','DELETE'])
def buscarAdmin():
    return render_template('buscarAdmin.html')

@app.route('/feedAdmin',methods=['POST', 'GET','PUT','DELETE'])
def feedAdmin():
    return render_template('feedAdmin.html')




if __name__ == "__main__":
    app.run(debug= True)