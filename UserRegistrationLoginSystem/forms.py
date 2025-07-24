from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,Length,Email,EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('username',validators=[InputRequired(),Length(min=4,max=150)])

    email = StringField('email',validators=[InputRequired(),Email()])

    password = PasswordField('password',validators=[InputRequired(),Length(min=6)])

    confirm_password = PasswordField('conform password',validators=[InputRequired(),EqualTo('password')])

    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField("Username",validators=[InputRequired(),Length(min=4,max=150)])
    password = PasswordField("password",validators=[InputRequired(),Length(min=6)])
    submit = SubmitField("Login")