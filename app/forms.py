from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User, ShoppingOrder, Violin

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length (min=2, max=25)])
    email_address = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email_address(self, email_address):
        user = User.query.filter_by(email_address=email_address.data).first()
        if user:
            raise ValidationError('That email address is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email_address = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length (min=2, max=25)])
    email_address = StringField('Email', validators=[DataRequired(),Email()], render_kw={"placeholder": "email"})
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    country = StringField('Country', validators=[DataRequired()], render_kw={"placeholder": "country"})
    city = StringField('City', validators=[DataRequired()], render_kw={"placeholder": "city"})
    street = StringField('Street', validators=[DataRequired()], render_kw={"placeholder": "street"})
    postcode = StringField('Post Code', validators=[DataRequired()], render_kw={"placeholder": "postcode"})
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email_address(self, email_address):
        if email_address.data != current_user.email_address:
            user = User.query.filter_by(email_address=email_address.data).first()
            if user:
                raise ValidationError('That email address is taken. Please choose a different one.')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class RequestResetForm(FlaskForm):
    email_address = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email_address(self, email_address):
        user = User.query.filter_by(email_address=email_address.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class ProductForm(FlaskForm):
    product_name = StringField('Name', validators=[DataRequired()])
    product_price = IntegerField('Price', validators=[DataRequired()])
    product_image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Create Product')
    