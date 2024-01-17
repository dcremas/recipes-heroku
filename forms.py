from flask_wtf import FlaskForm
from wtforms import (StringField, EmailField, SubmitField, PasswordField,
                     SelectField, TextAreaField, BooleanField)
from wtforms.validators import DataRequired, Length, EqualTo


class SignupForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=25)]) 
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Password Confirm', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register Account')


class RecipeForm(FlaskForm):

    category = StringField('Category', validators=[DataRequired(), Length(min=2, max=25)])
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=25)])
    prep_time = StringField('Prep Time', validators=[DataRequired(), Length(min=2, max=30)])
    cooking_time = StringField('Cooking Time', validators=[DataRequired(), Length(min=2, max=25)])
    yield_amount = StringField('Servings Yielded', validators=[DataRequired(), Length(min=2, max=25)])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    tips = TextAreaField('Tips')
    submit = SubmitField('Submit Recipe')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
