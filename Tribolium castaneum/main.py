from flask import Flask
from flask.templating import render_template
app = Flask (__name__)

@app.route('/login', methods=['POST', 'GET'])
def inicio():
    return render_template('login.html')

@app.route('/CrearPub', methods=['GET'])
def crear():
    return render_template('CrearPub.html')




if __name__ == "__main__":
    app.run(debug= True)