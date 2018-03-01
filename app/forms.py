#This is where we can create forms for flask
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField as ff

class Login(FlaskForm):
    email = StringField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Login")

class Signup(FlaskForm):
    fname = StringField("First Name",validators=[DataRequired()])
    lname = StringField("Last Name",validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired(),Email()])
    birthday = DateField("Birthdate",validators=[DataRequired()])
    country = StringField("Country", validators=[DateField()])
    gender = SelectField("Gender",validators=[DataRequired()],choices=[(0,"Male"),(1,"Female"),(2,"Other")])
    state = StringField("State",validators=[DataRequired()])
    city = StringField("City",validators=[DataRequired()])
    zipcode = StringField("Zipcode")
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()]) 
    interest = StringField("Interest")
    avail_mentee = BooleanField("Would you like to be mentored?")
    photo = ff("Upload a file")
    submit = SubmitField("Signup")

class Skills(FlaskForm):
    skills = StringField("Skills")
    submit = SubmitField("Save")

class ApplyForm(FlaskForm):
    show_blogs = BooleanField("Would you like to send info on blogs you've written?")
    notify_mentor = BooleanField("Would you like to notify your mentor of this application?")
    description = TextAreaField("Please leave a note about yourself")
    submit = SubmitField("Apply")

class WriteBlog(FlaskForm):
    title = StringField("Blog Title")
    content = TextAreaField("Blog Content")
    submit = SubmitField("Post!")

class Company_Signup(FlaskForm):
    name = StringField("Name of Company",validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired(),Email()])
    state = StringField("State",validators=[DataRequired()])
    city = StringField("City",validators=[DataRequired()])
    zipcode = StringField("Zipcode")
    website = StringField("Website",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()]) 
    address = StringField("Address",validators=[DataRequired()])
    submit = SubmitField("Signup")

class PostJob(FlaskForm):
    title = StringField("Title of Job",validators=[DataRequired()])
    description = StringField("Description of Job",validators=[DataRequired()])
    rate = IntegerField("Hourly Rate",validators=[DataRequired()])
    due = DateField("When applications are due",validators=[DataRequired()])
    submit = SubmitField("Post Job")


class ScheduleInterview(FlaskForm):
    name = StringField("Interviewer Name")
    time = DateTimeField("What Day and Time?")
    comment = StringField("Attached Comments")
    submit = SubmitField("Send Interview Details")

class Delete(FlaskForm):
    iid = HiddenField("Interview Id")
    submit = SubmitField("Delete")


