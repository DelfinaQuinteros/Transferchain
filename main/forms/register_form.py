from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField
from wtforms.fields import EmailField
from wtforms import validators


class RegisterForm(FlaskForm):
    name = StringField('Name:',
                       [
                           validators.DataRequired(message="El nombre es obligatorio"),
                       ],
                       render_kw={"placeholder": "Nombre"})

    last_name = StringField('Last Name:',
                            [
                                validators.DataRequired(message="El apellido es obligatorio"),
                            ],
                            render_kw={"placeholder": "Apellido"})

    address = StringField("Address:",
                          [
                              validators.DataRequired(message="La direccion es obligatorio")
                          ],
                          render_kw={"placeholder": "Direccion"})

    dni = StringField("DNI:", [
        validators.DataRequired(message="El DNI es obligatorio")
    ],)

    email = EmailField('Email:',
                       [
                           validators.DataRequired(message="El email es obligatorio"),
                           validators.Email(message='Formato no valido'),
                       ],
                       render_kw={"placeholder": "Email"})

    password = PasswordField('Contraseña:', [
        validators.DataRequired()
    ],
                             render_kw={"placeholder": "Contraseña"})

    submit = SubmitField("Registrarse")
