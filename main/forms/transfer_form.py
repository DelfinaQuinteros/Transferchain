from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired


class TransferForm(FlaskForm):
    owner = IntegerField('',
                        validators=[DataRequired(message="El ID del dueño es obligatorio")],
                        render_kw={"placeholder": "ID del dueño"}
                        )

    new_owner = IntegerField('',
                             validators=[DataRequired(message='El ID del nuevo dueño es obligatorio')],
                             render_kw={"placeholder": "ID del nuevo dueño"}
                             )

    car_id = IntegerField('',
                          validators=[DataRequired(message='El ID del auto es obligatorio')],
                          render_kw={"placeholder": "ID del auto"}
                          )

    submit = SubmitField("Transferir")
