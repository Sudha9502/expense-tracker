from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

# Register Form
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

from wtforms import FloatField, SelectField, DateField, TextAreaField

class ExpenseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Shopping', 'Shopping'),
        ('Bills', 'Bills'),
        ('Other', 'Other')
    ])
    date = DateField('Date', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Add Expense')
