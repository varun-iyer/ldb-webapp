from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import User, Collection, Document
from app import app, db
from app.forms import LoginForm, SignupForm, CollectionForm, DocumentForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is None:
            flash('Invalid email!')
            return redirect(url_for('login'))
        if not user.check_password(form.password.data):
            flash('Incorrect password!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
 
@app.route('/collections')
@login_required
def collections():
    return render_template('collections.html')
 
@app.route('/signup', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, name=form.name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you’re all signed up!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up for LDB', form=form)
 
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_collection():
    form = CollectionForm()
    if form.validate_on_submit():
        coll = Collection(name=form.name.data, description=form.description.data)
        current_user.add_collection(coll)
        db.session.commit()
        return redirect(url_for('collections'))
    return render_template('create_collection.html', form=form)
 
 
@app.route('/collection/<int:cid>', methods=['GET'])
@login_required
def collection(cid):
    if current_user not in Collection.query.get(cid).users:
        return abort(404)
    return render_template('collection.html', collection=Collection.query.get(cid))


@app.route('/404')
@app.errorhandler(404)
def http_404(e):
    return render_template('404.html'), 404
 
 
@app.route('/collection/<int:cid>/documentadd', methods=['GET', 'POST'])
@login_required
def add_document(cid):
    coll = Collection.query.get(cid)
    if current_user not in coll.users:
        return abort(404)
    form = DocumentForm()
    if form.validate_on_submit():
        doc = Document(name=form.name.data)
        coll.add_document(doc)
        db.session.commit()
        return redirect(url_for('collection', cid=cid))
    return render_template('add_document.html', form=form)
