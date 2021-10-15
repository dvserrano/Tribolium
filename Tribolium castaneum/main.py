from flask import Flask
from flask.templating import render_template
app = Flask (__name__)

@app.route('/', methods=['POST', 'GET'])
def inicio():
    return render_template('login.html')

@app.route('/registro', methods=['POST', 'GET'])
def registro():
    return render_template('registro.html')

@app.route('/crear', methods=['GET'])
def crear():
    return render_template('CrearPub.html')

@app.route('/buscar')
def buscar():
    return render_template('buscar.html')

@app.route('/chat')
def chat():
    return render_template('chatymensajes.html')

@app.route('/feed')
def feed():
    return render_template('feed.html')

@app.route('/notificaciones')
def notificaciones():
    return render_template('notificaciones.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/editar', methods=['POST', 'GET'])
def editar():
    return render_template('Editardatos.html')

@app.route('/detalle')
def detalle():
    return render_template('detallepost.html')

@app.route('/perfilp')
def perfilp():
    return render_template('perfilPub.html')


# rutas administrador
@app.route('/buscarAdmin')
def buscarAdmin():
    return render_template('buscarAdmin.html')

@app.route('/feedAdmin')
def feedAdmin():
    return render_template('feedAdmin.html')




if __name__ == "__main__":
    app.run(debug= True)