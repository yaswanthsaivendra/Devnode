from flask_wtf import FlaskForm
from wtforms.fields.core import SelectField, StringField
from wtforms.fields.simple import FileField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from devnode.models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import DateField




class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3,max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email is already registered. Headover to login')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with the email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')



class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3,max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about = TextAreaField('About',validators=[DataRequired()])
    designation = StringField('Designation', validators=[DataRequired()])
    branch = SelectField('Branch', choices=[None,'CSE','EE','ECE','MSC','ME','CE','M.TECH'])
    year = SelectField('Year', choices=[None,2021,2022,2023,2024,2025,2026,2027,2028])
    twitter_id = StringField('Twitter Id')
    github_id = StringField('Github Id')
    linkedin_id = StringField('Linkedin Id')
    discord_id = StringField('Discord Id')
    submit = SubmitField('Save')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken. Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('The email is already registered')


class UpdateProfilePicture(FlaskForm):
    profile_picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save')


class UpdateCoverPicture(FlaskForm):
    cover_picture = FileField('Update Cover Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save')

class AddSkill(FlaskForm):
    skill_name = StringField('Enter skill name', validators=[DataRequired()])
    submit = SubmitField("Add")


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()], choices= ['Hackathon', "Competetive Coding Contest", 'Opensource Project', 'other'])
    persons_required = SelectField('Number of Persons Required', validators=[DataRequired()], choices=[1,2,3,4,5,6,7,8])
    last_date = DateField('Last date', validators=[DataRequired()], format="%Y-%m-%d")
    submit = SubmitField('Post')