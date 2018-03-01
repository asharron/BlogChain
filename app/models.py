#This is where we define our database models such as tables
#Basically the schema
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer(),primary_key=True)
    fname = db.Column(db.String(70))
    lname = db.Column(db.String(70))
    email = db.Column(db.String(70))
    birthday = db.Column(db.Date())
    country = db.Column(db.String(70))
    gender = db.Column(db.Integer())
    state = db.Column(db.String(70))
    city = db.Column(db.String(70))
    zipcode = db.Column(db.Integer())
    username = db.Column(db.String(70))
    password_hash = db.Column(db.String(128))
    trust_index = db.Column(db.Integer())
    skills = db.Column(db.String(70))
    interest = db.Column(db.String(70))
    mentor_uid = db.Column(db.Integer(),db.ForeignKey('user.uid'))
    avail_mentee = db.Column(db.Boolean())
    comid = db.Column(db.Integer(),db.ForeignKey('community.comid'))
    user_type = db.Column(db.Boolean())
    photo = db.Column(db.String(200))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribtue')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Company(db.Model):
    __tablename__= 'company'
    cid = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(70))
    state = db.Column(db.String(40))
    city = db.Column(db.String(70))
    website = db.Column(db.String(70))
    email = db.Column(db.String(70))
    password_hash = db.Column(db.String(128))
    comid = db.Column(db.Integer(),db.ForeignKey('community.comid'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribtue')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Job(db.Model):
    __tablename__ = 'job'
    jid = db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String(70))
    description = db.Column(db.String(300))
    rate = db.Column(db.Float())
    due = db.Column(db.Date())
    cid = db.Column(db.Integer(),db.ForeignKey('company.cid'))


class Community(db.Model):
    __tablename__ = 'community'
    comid = db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String(70))
    description = db.Column(db.String(150))

class Skill(db.Model):
    __tablename__ = 'skill'
    sid = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(70))

class Application(db.Model):
    __tablename__ = 'application'
    aid = db.Column(db.Integer(),primary_key=True)
    uid = db.Column(db.Integer(),db.ForeignKey('user.uid'))
    cid = db.Column(db.Integer(),db.ForeignKey('company.cid'))
    jid = db.Column(db.Integer(),db.ForeignKey('job.jid'))
    description = db.Column(db.String(200))

class Interview(db.Model):
    __tablename__ = 'interview'
    iid = db.Column(db.Integer(),primary_key=True)
    jid = db.Column(db.Integer(),db.ForeignKey('job.jid'))
    uid = db.Column(db.Integer(),db.ForeignKey('user.uid'))
    cid = db.Column(db.Integer(),db.ForeignKey('company.cid'))
    time = db.Column(db.Date())
    interviewer = db.Column(db.String(150))
    comment = db.Column(db.String(200))
    





