import parameters
from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_mail import Mail
from datetime import datetime
import os
import json
import math

app = Flask(__name__)
app.secret_key = 'super-secret-key'

try:
    with open('config.json', 'r') as c:
        parameters = json.load(c)["parameters"]
except FileNotFoundError:
    print("Error: config.json file not found.")
    parameters = {}

app.config['UPLOAD_FOLDER'] = parameters["upload_location"]

local_server = True
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=parameters['gmail-user'],
    MAIL_PASSWORD=parameters['gmail-password']
)
mail = Mail(app)

if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = parameters['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = parameters['prod_uri']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Contacts(db.Model):
    """ sr_no , name , phone_number, message, date , email """
    sr_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)


class Posts(db.Model):
    """ sr_no , name , phone_number, message, date , email """
    sr_no = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    tagline = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    img_file = db.Column(db.String(12), nullable=True)


@app.route("/mock")
def home_page():
    page = request.args.get('page', 1, type=int)
    posts_per_page = int(parameters['no_of_posts'])
    offset = (page - 1) * posts_per_page

    posts = Posts.query.offset(offset).limit(posts_per_page).all()

    total_posts = Posts.query.count()
    total_pages = math.ceil(total_posts / posts_per_page)

    prev = None
    next = None
    if page > 1:
        prev = f"/mock?page={page - 1}"
    if page < total_pages:
        next = f"/mock?page={page + 1}"

    return render_template('mock-practice.html', parameters=parameters, posts=posts, prev=prev, next=next)


@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post_tb.html', parameters=parameters, post=post)


@app.route("/about")
def web_about():
    return render_template('about_tb.html', parameters=parameters)


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():

    if 'user' in session and session['user'] == parameters['admin_user']:
        posts = Posts.query.all()
        return render_template('dashboard.html', parameters=parameters, posts=posts)

    if request.method == 'POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if username == parameters['admin_user'] and userpass == parameters['admin_password'] :
            # set the session-variable
            session['user'] = username
            posts = Posts.query.all()
            return render_template('dashboard.html', parameters=parameters, posts=posts)
    return render_template('login_tb.html', parameters=parameters)


@app.route("/edit/<string:sr_no>", methods=['GET', 'POST'])
def edit_post(sr_no):
    if 'user' in session and session['user'] == parameters['admin_user']:
        if request.method == 'POST':
            box_title = request.form.get('title')
            tline = request.form.get('tline')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            date = datetime.now()

            if sr_no == '0':
                # Get the next available sr_no
                max_sr_no = db.session.query(db.func.max(Posts.sr_no)).scalar()
                next_sr_no = max_sr_no + 1 if max_sr_no is not None else 1

                post = Posts(title=box_title, slug=slug, content=content, tagline=tline, img_file=img_file, date=date)
                post.sr_no = next_sr_no  # Set the sr_no for the new post
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(sr_no=sr_no).first()
                post.title = box_title
                post.slug = slug
                post.content = content
                post.tagline = tline
                post.img_file = img_file
                post.date = date
                db.session.commit()
                return redirect('/edit/'+sr_no)
        post = Posts.query.filter_by(sr_no=sr_no).first()
        return render_template('edit.html', parameters=parameters, post=post, sr_no=sr_no)


@app.route("/contact", methods=['GET', 'POST'])
def web_contact():
    if request.method == 'POST':
        '''Add entry to the database, start searching for credentials..'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_number=phone, message=message, date=datetime.now(), email=email)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from '+name,
                          sender=email,
                          recipients=[parameters['gmail-user']],
                          body=message + "\n" + phone
                          )
    return render_template('contact_tb.html', parameters=parameters)


@app.route("/uploader", methods=['GET', 'POST'])
def uploader():
    if 'user' in session and session['user'] == parameters['admin_user']:
        if request.method == 'POST':
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return "Uploaded successfully"


@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/dashboard')


@app.route("/delete/<string:sr_no>", methods=['GET', 'POST'])
def delete(sr_no):
    if 'user' in session and session['user'] == parameters['admin_user']:
        post = Posts.query.filter_by(sr_no=sr_no).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/dashboard')


@app.route("/post")
def web_post():
    # For example, you can query for the latest post or any specific post you want to display as default
    default_post = Posts.query.order_by(Posts.date.desc()).first()
    return render_template('post_tb.html', parameters=parameters, post=default_post)


if __name__ == '__main__':
    app.run(debug=True)
