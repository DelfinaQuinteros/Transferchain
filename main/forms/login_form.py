from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.fields import EmailField
from wtforms import validators


class LoginForm(FlaskForm):
    email = EmailField('Email:',
                       [
                           validators.DataRequired(message="Email es obligatorio"),
                           validators.Email(message='Formato invalido'),
                       ],
                       render_kw={"placeholder": "Email"}
                       )

    password = PasswordField('Contraseña:', [
        validators.DataRequired(message='Password es obligatorio'),
    ],
                             render_kw={"placeholder": "Contraseña"}
                             )
    submit = SubmitField("Iniciar sesion")
