from flask_wtf import FlaskForm, CSRFProtect
from wtforms import PasswordField, SubmitField
from wtforms.fields import EmailField
from wtforms import validators

csrf = CSRFProtect()

class LoginForm(FlaskForm):
    email = EmailField('',
                       [
                           validators.DataRequired(message="Email es obligatorio"),
                           validators.Email(message='Formato invalido'),
                       ], render_kw={"placeholder": "Email"}
                       )

    password = PasswordField('', [
        validators.DataRequired(message='Password es obligatorio')]
                             , render_kw={"placeholder": "Password"}
                             )

    submit = SubmitField("Iniciar sesion")
