from flask import Flask
from flask.templating import render_template
app = Flask (__name__)

@app.route('/login')
def inicio():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug= True)