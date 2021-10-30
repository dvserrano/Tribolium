from flask import Flask, request, session, redirect, url_for
from flask.templating import render_template
from flask_wtf import form
from formulario import Formulario
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os
import sqlite3
from markupsafe import escape
import hashlib 

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
            sql = cur.execute("select password from usuario where correo=?", [correo]).fetchone()
            if(sql != None):
                variable =sql[0]
                # if variable == password:
                if check_password_hash(variable,password):
                    session['correo']= correo
                    return render_template("feed.html")
            return render_template("login.html",form=form)
            
    return ('error')


 

@app.route('/ir',methods=['POST','GET'])
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

@app.route('/nuevo', methods=['POST','GET'])
def nuevo():
    form = Formulario()
    print('hola')
    # session.clear()
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
            return render_template('registro.html',form=form)
        else:
            with sqlite3.connect('data.db') as conexion:
                cur = conexion.cursor()
                #cur.execute ('insert into USUARIO (correo, password) values (?,?)',(correo,cifrando))
                cur.execute ('insert into USUARIO (nombre1,nombre2,apellido1, apellido2, correo, password) values (?,?,?,?,?,?)',(nombre,sNombre,apellido, sApellido, correo,cifrando))
                #confirma la transaccion
                conexion.commit()
                return render_template('feed.html')
    return ('paso algo de error')

UPLOAD_FOLDER = 'static/imagenes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/crear', methods=['GET', 'POST'])
def crear():
    form = Formulario()
    if request.method == 'POST':
        file = request.files['file']           
        filename = secure_filename(file.filename)
        basedir = os.path.abspath(os.path.dirname(__file__))
        file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
        descripcion = form.descripcion.data
        with sqlite3.connect('data.db') as conexion:
                cur = conexion.cursor()
                cur.execute ('insert into PUBLICACION (descripcion, fecha, img, id_usuario) values (?,?,?,?)',(descripcion, "hoy", filename, 1 ))
                conexion.commit()
        return render_template('feed.html', filename=filename)        
    return render_template('CrearPub.html', form=form)
  
  
@app.route('/buscar')
def buscar():
    return render_template('buscar.html')

@app.route('/chat')
def chat():
    return render_template('chatymensajes.html')

@app.route('/feed')
def feed():
    return render_template('feed.html')

@app.route('/notificaciones/<id_publicacion>', methods=['POST', 'GET','PUT'])
def notificaciones(id_publicacion):
    if request.method == 'GET':
        with sqlite3.connect('data.db') as conexion:
            cur = conexion.cursor()
            sql = cur.execute("select * from PUBLICACION WHERE id_publicacion=?",id_publicacion).fetchone()
            user = cur.execute("select nombre1 from usuario where id_usuario=?",sql[4]).fetchone()
            temp=(sql[0],sql[1],sql[2],sql[3],sql[4],sql[5],sql[6],user[0])
            return render_template('notificaciones.html',context=temp)
    if request.method == 'PUT':
        request_data = request.get_json()
        like= request_data['like']
        dislike= request_data['dislike']
        idpublicacion= request_data['id']
        with sqlite3.connect('data.db') as conexion:
            cur = conexion.cursor()
            print(idpublicacion)
            sql = cur.execute("select * from PUBLICACION WHERE id_publicacion=?",str(idpublicacion)).fetchone()
            if(like>0):
                suma=sql[5]+1
                elm=cur.execute("UPDATE PUBLICACION SET me_gusta=? WHERE id_publicacion=?",[str(suma),str(idpublicacion)])
            if(dislike):
                suma=sql[6]+1
                elm=cur.execute("UPDATE PUBLICACION SET no_gusta=? WHERE id_publicacion=?",[str(suma),str(idpublicacion)])
            user = cur.execute("select nombre1 from usuario where id_usuario=?",sql[4]).fetchone()
            temp=(sql[0],sql[1],sql[2],sql[3],sql[4],sql[5],sql[6],user[0])
    return render_template('notificaciones.html',context=[])


@app.route('/perfil')
def perfil():
    return render_template('perfil.html', usuario="Profesor Super O")

@app.route('/editar', methods=["POST", "GET"])
def editar():
    form = Formulario()
    return render_template('Editardatos.html', form=form)

@app.route('/editarperfil', methods=["POST", "GET"])
def editarperfil():
    form = Formulario()
    # if 'usuario' in session:
    if request.method == 'POST':
        correo1 = escape(form.correo1.data)
        password1 = escape(form.password1.data)
        password2 = escape(form.password2.data)
        with sqlite3.connect('data.db') as conexion:
            cur = conexion.cursor()
            sql = cur.execute("select password from usuario where correo=?", [correo1]).fetchone()
            if(sql != None):
                variable =sql[0]
                if check_password_hash(variable,password1):
                    session['correo']= correo1
                    print (correo1, password1, variable )
                    password2 = escape(form.password2.data)
                    cifrando = generate_password_hash(password2,'sha512')
                    print(cifrando)
                    cur.execute('update USUARIO set password=? where correo=?',[cifrando, correo1])
                    conexion.commit()
                    if conexion.total_changes > 0:
                        return ("contraseña actualizada")
                    return ('No se actualizo el registro')
                return ('paso algo de error')
    return ('paso algo de error')
    # return ('error')


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
    if request.method == 'GET':
        with sqlite3.connect('data.db') as conexion:
            cur = conexion.cursor()
            sql = cur.execute("select * from PUBLICACION ").fetchall()
            lista=[]
            for sql in sql:
                user = cur.execute("select nombre1 from usuario where id_usuario=?",sql[4]).fetchone()
                temp=(sql[0],sql[1],sql[2],sql[3],sql[4],sql[5],sql[6],user[0])
                lista.append(temp)
            return render_template('feedAdmin.html',context=lista)
    return render_template('feedAdmin.html',context=[])

@app.route('/feedAdmin/<id_publicacion>',methods=['DELETE'])
def feedAdminEliminar(id_publicacion):
    print(id_publicacion)
    if request.method == 'DELETE':
        with sqlite3.connect('data.db') as conexion:
            cur = conexion.cursor()
            sqldos = cur.execute("DELETE from PUBLICACION WHERE id_publicacion=?",id_publicacion)
            sql = cur.execute("select * from PUBLICACION ").fetchall()
            lista=[]
            for sql in sql:
                user = cur.execute("select nombre1 from usuario where id_usuario=?",sql[4]).fetchone()
                temp=(sql[0],sql[1],sql[2],sql[3],sql[4],sql[5],sql[6],user[0])
                lista.append(temp)
            return redirect(url_for('feedAdmin'))
    return redirect(url_for('feedAdmin'))




# if __name__ == "__main__":
#     app.run(debug= True)