from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User
from app import db
from flask import flash

class RegistrationForm(FlaskForm):
  username = StringField('UserName', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Register')

  def validate_email_username(self, email_check, username_check):
      user = User.query.filter_by(email=email_check).first()
      if user is not None:
        flash("That username already exists. Choose another one.")
        return False
      user = User.query.filter_by(username=username_check).first()
      if user is not None:
        flash("That username already exists. Choose another one.")
        return False
      return True

class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Log In')

class ProfileForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Add User')

class ProductForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  image = FileField('Image', validators=[DataRequired()])
  price = FloatField('Price', validators=[DataRequired()])
  inventory = IntegerField('Inventory', validators=[DataRequired()])
  description=StringField('Description')
  pr_type = StringField('Type', validators=[DataRequired()])

  submit = SubmitField('Add Product')