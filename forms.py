from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

#This is the part where they register and input their questions/answers 
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    master_password = PasswordField('Master Password', validators=[
        DataRequired(), Length(min=8)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('master_password')
    ])
    security_q1 = StringField('Security Question 1', validators=[DataRequired()])
    security_q1_answer = StringField('Answer to Question 1', validators=[DataRequired()])
    security_q2 = StringField('Security Question 2', validators=[DataRequired()])
    security_q2_answer = StringField('Answer to Question 2', validators=[DataRequired()])
    security_q3 = StringField('Security Question 3', validators=[DataRequired()])
    security_q3_answer = StringField('Answer to Question 3', validators=[DataRequired()])
    submit = SubmitField('Register')


# Custom validation for master password strength
    def validate_master_password(self, master_password):
        password = master_password.data
        # Check for password strength
        if len(password) < 8 or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password) or not any(c in "!@#$%^&*" for c in password):
            raise ValidationError(
                'Password is weak! It must be at least 8 characters long and include an uppercase letter, a digit, and a special character (!@#$%^&*).'
            )

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    master_password = PasswordField('Master Password', validators=[DataRequired()])
    submit = SubmitField('Login')
