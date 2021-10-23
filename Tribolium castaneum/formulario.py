from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import EmailField

class Formulario(FlaskForm):
    usuario = StringField('usuario',validators=[DataRequired(message="El campo nombre es requerido")])
    nombre = StringField('nombre',validators=[DataRequired(message="El campo nombre es requerido")])
    sNombre = StringField('sNombre',validators=[DataRequired(message="El campo segundo nombre es requerido")])
    apellido = StringField('sNombre',validators=[DataRequired(message="El campo apellido es requerido")])
    sApellido = StringField('sNombre',validators=[DataRequired(message="El campo segundo apellido es requerido")])
    correo = EmailField('correo',validators=[DataRequired(message="El campo correo es requerido")])
    password = PasswordField('password',validators=[DataRequired(message= "El campo correo es requerido"), Length(min=6, max=8)])
    boton = SubmitField('Iniciar Sesión',render_kw={"onmouseover": "entrar()"})
    bot2 = SubmitField('Registrate',render_kw={"onmouseover": "registro()"})
    botonre = SubmitField('Registrar', render_kw={"onmouseover": "nuevo()"})



    
