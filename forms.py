from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length
import re

class ContactForm(FlaskForm):
    name=StringField("Nombre", validators=[DataRequired(), Length(min=2, max=50)])
    email=StringField("Correo",validators=[DataRequired(), Email()])
    message=TextAreaField("Mensaje",validators=[DataRequired(), Length(min=10)])
    submit = SubmitField("Enviar")
    recaptcha=RecaptchaField()




# Función para validar el correo
def is_valid_email(email):
    """Valida que un correo sea válido usando expresiones regulares."""
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email)