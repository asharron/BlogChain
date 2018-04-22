#this is where we cover all of our routes and what happens in the views that we render
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from app import app, db, mail
from .models import *
from .forms import *
from flask_mail import Message
import yaml
import requests
import json
import os
from werkzeug.utils import secure_filename

calendlyKey = "JHJEGBEAMJFPW4225EQBHPNTABQJN5TX"

#Route for the homepage
@app.route("/",methods=['GET'])
def home():
  return render_template("index.html")

app.route("/login",methods=['GET','POST']) #Route for Logging in the user
def login():
  form = Login() #Create form object
  #If the user submitted the form
  if request.method == 'POST' and form.validate():
    #Grab the user with the same email
    user = User.query.filter_by(email=form.email.data).first()
    #If the user exists
    if user:
      #verify passwordSIGN
      if user.verify_password(form.password.data):
        #set session data to know they are logged
        session['email'] = form.email.data
        session['name'] = user.fname
        session['id'] = user.uid
        flash("You were logged in!")
        return redirect(url_for('dashboard'))
      else:
        return render_template("login.html",form=form)
    else:
      return render_template("login.html",form=form)
  else:
    return render_template("login.html",form=form)

#Route for logging the user out
@app.route('/logout')
def logout():
  #Clear session info
  session.clear()
  flash("You were logged out!")
  return redirect(url_for('home'))

#Route for signing the user up
@app.route('/signup',methods=['GET','POST'])
def signup():
    #create the form object
    form = Signup()
    #If they are submitting the form and it is filled
    if request.method == 'POST':
      #Do logic for DB here
      #Create the user and set the attributes
      user = User()
      user.fname = form.fname.data
      user.lname = form.lname.data
      user.gender = form.gender.data
      user.birthday = form.birthday.data
      user.country = form.country.data
      user.state = form.state.data
      user.city = form.city.data
      user.interest = form.interest.data
      user.avail_mentee = form.avail_mentee.data
      #photo = form.photo.data
      #filename = secure_filename(photo.filename)
      #photo.save(os.path.join(app.instance_path,'photos',filename))
      #user.photo = os.path.join(app.instance_path,'photos',filename)
      user.email = form.email.data
      user.password = form.password.data

      #Add user to database
      db.session.add(user)
      db.session.commit()

      #Mark the user as logged
      session['email'] = form.email.data
      session['name'] = form.fname.data
      session['id'] = user.uid
      flash("Signup Successful!")

      #Redirect to home
      return redirect(url_for('home'))
    else:
      return render_template('sign_up.html',form=form)

#Route for the users profile
@app.route('/profile/<int:id>',methods=['GET','POST'])
def profile(id):
  form = Skills() #Create the skills form
  if 'email' in session:#Make sure the user is logged in
    #Grab the user from the database to get its data
    user = User.query.filter_by(uid=id).first()
    if user:
      if request.method=="POST":#If they are changing their skills
        #Change the skills and save
        user.skills = form.skills.data
        db.session.commit()
        form.skills.data = user.skills
        #list to hold the skill query objects
        skill_list = []
        #Grab the skill names
        if user.skills:
          skills = user.skills.split()
        #Grab each skill in the table that matches with the skillname
          for skillName in skills:
            skill_list.append(Skill.query.filter_by(name=skillName).first())
        return render_template('profile.html',user=user,form=form, skills=skill_list,id=id)
      else:
        #Just return the page if no changes
        form.skills.data = user.skills
        #list to hold the skill query objects
        skill_list = []
        #Grab the skill names
        if user.skills:
          skills = user.skills.split()
          #Grab each skill in the table that matches with the skillname
          for skillName in skills:
            skill_list.append(Skill.query.filter_by(name=skillName).first())
        return render_template('profile.html',user=user,form=form,skills=skill_list,id=id)
    else:
      return redirect(url_for('login'))
  else:
    return redirect(url_for('login'))

@app.route('/profile/<int:uid>')
def profile_photo(uid):
  photo = User.query.filter_by(uid=uid).first().photo
  return app.response_class(photo,mimetype='image/png')

#Route for finding available mentees
#Route is also paginated
@app.route('/findmentee')
@app.route('/findmentee/<int:page>', methods=['GET', 'POST'])
def findmentee(page=1):
  #Grab the mentess and paginate them

  mentees = User.query.filter_by(avail_mentee=True).paginate(page,10,False)
  return render_template('findmentees.html',page=page,mentees=mentees)

#Route for users blogs
@app.route("/blog",methods=['GET'])
def blog():
  #Query the blockchain for a specific blog
  data = s.get_content('tomshwom','tomshwom-s-advanced-crypto-security-guide-part-1-privacy-security-and-trust')
  headline = data['title'] #Access the response for the blog title
  blog = data['body'] #Access the response to get the body of the blog
  return render_template("blog.html",body=blog,title=headline)

#Route for faqs
@app.route("/faq",methods=['GET'])
def faq():
  return render_template("faq.html")

#route for dashboard
@app.route("/dashboard",methods=['GET', 'POST'])
def dashboard():
  if 'id' in session:
    return render_template("dashboard.html")
  else:
    return redirect( url_for("login"))

#route for dashboard
@app.route("/company_dashboard",methods=['GET', 'POST'])
def company_dashboard():
  if 'cid' in session:
    return render_template("company_dashboard.html")
  else:
    return redirect( url_for('company_login') )

#route for jobs page
@app.route("/jobs")
@app.route("/jobs/<int:page>",methods=['GET','POST'])
def jobs(page=1):
  jobs_list = Job.query.filter_by().paginate(page,10,False)
  return render_template("jobs.html",page=page,jobs=jobs_list)

#Route for the company to set up an interview with user and job
@app.route('/set_interview/<int:uid>/<int:jid>', methods=['GET','POST'])
def setInterview(uid,jid):
  form = ScheduleInterview()
  if request.method == 'POST':
    interview = Interview()
    interview.cid = session['cid']
    interview.uid = uid
    interview.jid = jid
    interview.time = form.time.data
    interview.interviewer = form.name.data
    interview.comment = form.comment.data 
    db.session.add(interview)
    db.session.commit()
    return redirect( url_for('applications') )
  return render_template('set_interview.html',uid=uid,jid=jid,form=form)

#Route for the user to view interviews
@app.route('/view_interviews', methods=['GET','POST'])
def view_interviews():
  form = Delete()
  if request.method == 'POST':
    interview = Interview.query.filter_by(iid=form.iid.data).first()
    db.session.delete(interview)
    db.session.commit()
  else:
    pass
  if 'id' in session:
    interviews = Interview.query.filter_by(uid=session['id']).all()
    return render_template('view_interviews.html',form=form,interviews=interviews,Company=Company,Job=Job)
  elif 'cid' in session:
    interviews = Interview.query.filter_by(cid=session['cid']).all()
    return render_template('view_interviews.html',form=form,interviews=interviews,Company=Company,Job=Job)
  else:
    return redirect( url_for('home'))

#route for account page
@app.route("/account",methods=['GET'])
def account():
  return render_template("account.html")

#Route for applying to a specific job
#job parameter is the jid of the job in the database
@app.route("/apply/<int:job>",methods=['GET','POST'])
def apply(job):
  #Create form for application
  form = ApplyForm()
  #Getting the job to fill out application database entry
  job = Job.query.filter_by(jid=job).first()
  if request.method == "POST" and form.validate():
    #Creation of entry in database
    application = Application()
    application.cid = job.cid
    application.jid = job.jid
    application.uid = session['id']
    application.description = form.description.data
    db.session.add(application)
    db.session.commit()
    flash("You have sucessfully applied")
    return redirect(url_for('home'))
  return render_template('application.html',form=form,company=company,job=job)
  
#route for write_blog
@app.route("/blog/write",methods=['GET','POST'])
def write_blog():
  form = WriteBlog() #Make the blog writing form
  if request.method == 'POST' and form.validate():
    #Do blockchain logic here
    pass
  else:
    pass
  return render_template('write_blog.html',form=form)

#route for community
@app.route("/community",methods=['GET'])
def community():
  return render_template("community.html")

#route for company
@app.route("/company",methods=['GET'])
def company():
  return render_template("company.html")


#route for professionals
@app.route("/professionals",methods=['GET'])
def professionals():
  return render_template("professionals.html")



#Redirect to home
#Route for signing up a company
@app.route('/company_signup',methods=['GET','POST'])
def company_signup():
    #create the form object
    form = Company_Signup()
    #If they are submitting the form and it is filled
    if request.method == 'POST':
      #Create the company and set the attributes
      company = Company()
      company.name = form.name.data
      company.address= form.address.data
      company.website = form.website.data
      company.state = form.state.data
      company.city = form.city.data
      company.website = form.website.data
      company.email = form.email.data
      company.password = form.password.data

      #Add company to database
      db.session.add(company)
      db.session.commit()

      #Mark the company as logged
      session['email'] = form.email.data
      session['name'] = form.name.data
      session["cid"] = company.cid
      flash("Sign up Successful!")

      #Redirect to home
      return redirect(url_for('company_dashboard'))
    else:
      return render_template('company_sign_up.html',form=form)

#Route for the company to views submitted applications
@app.route("/applications")
def applications():
  if 'cid' in session:
    applications = Application.query.filter_by(cid=session['cid']).all()
    return render_template('applications.html',applications=applications,User=User,Job=Job)

@app.route("/company_login",methods=['GET','POST']) #Route for Logging in the company
def company_login():
  form = Login() #Create form object
  #If the user submitted the form
  if request.method == 'POST' and form.validate():
    #Grab the user with the same email
    company = Company.query.filter_by(email=form.email.data).first()
    #If the user exists
    if company:
      #verify password
      if company.verify_password(form.password.data):
        #set session data to know they are logged in
        session['email'] = form.email.data
        session['name'] = company.name
        session['cid'] = company.cid
        flash("You were logged in!")
        return redirect(url_for('company_dashboard'))
      else:
        flash("Password was incorrect")
        return render_template("company_login.html",form=form)
    else:
      return render_template("company_login.html",form=form)
  else:
    return render_template("company_login.html",form=form)

#Route to join community
@app.route("/join_community",methods=['GET'])
def join_community():
  return render_template("join_community.html")

#route for community rules
@app.route("/community_rules",methods=['GET'])
def community_rules():
  return render_template("community_rules.html")

#route for request to create a community
@app.route("/community_request",methods=['GET'])
def community_request():
  return render_template("community_request.html")


#route for community_blogs
@app.route("/community_blog",methods=['GET', 'POST'])
def community_blog():
  return render_template("community_blog.html")


#route for community_faq
@app.route("/community_faq",methods=['GET', 'POST'])
def community_faq():
  return render_template("community_faq.html")

#route for community_categories
@app.route("/community_categories",methods=['GET', 'POST'])
def community_categories():
  return render_template("community_categories.html")

#route for community_general
@app.route("/community_general",methods=['GET', 'POST'])
def community_general():
  return render_template("community_general.html")


#route for community_cybersecurity
@app.route("/community_cybersecurity",methods=['GET', 'POST'])
def community_cybersecurity():
  return render_template("community_cybersecurity.html")

#route for post_job
@app.route("/post_job",methods=['GET', 'POST'])
def post_job():
  form = PostJob()
  if 'cid' in session:
    if request.method == 'POST':
      print("form was validated")
      job = Job()
      job.title = form.title.data
      job.cid = session['cid']
      job.description = form.description.data
      job.due = form.due.data
      job.rate = form.rate.data
      db.session.add(job)
      db.session.commit()
      return redirect( url_for('company_dashboard') )
    else:
      print("form was not validated") #Tell user that form was not validated
      return render_template("post_job.html",form=form)
  else:
    return redirect( url_for('company_login')) #Return the company url


#route for jobs_company
@app.route("/jobs_company",methods=['GET', 'POST'])
@app.route("/jobs_company/<int:page>")
def jobs_company(page=1):
  jobs = Job.query.filter_by().paginate(page,10,False)
  return render_template("jobs_company.html",jobs=jobs)

@app.route("/joinnetwork",methods=['GET', 'POST'])
def join_network():
    ip = request.remote_addr
    with open('nodes.yaml', 'r') as f:
        nodes = yaml.load(f)
    nodes.append(ip)
    with open('nodes.yaml', 'w') as f:
        f.write(yaml.dump(nodes))
    broadcast(nodes)

def broadcast(node_list):
    nodes = jsonify(node_list)
    for node in node_list:
        url = node + '/updatenodes'
        request.post(url, json=nodes)
