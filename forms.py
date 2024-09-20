from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, EmailField
from wtforms.validators import InputRequired, EqualTo, NumberRange

class LoginForm(FlaskForm):
    user_id = StringField("User id:",
        validators=[InputRequired()])
    password = PasswordField("Password:",
        validators=[InputRequired()])
    submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    user_id = StringField("User id:",
        validators=[InputRequired()])
    password = PasswordField("Password:",
        validators=[InputRequired()])
    email = EmailField("Email:", 
        validators=[InputRequired()])
    submit = SubmitField("Register")