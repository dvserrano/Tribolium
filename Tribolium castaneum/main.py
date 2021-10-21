from flask import Flask, request
from flask.templating import render_template
from formulario import Formulario
import os
app = Flask (__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=['POST', 'GET'])
def inicio():
    form= Formulario()
    return render_template('login.html',form=form)

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