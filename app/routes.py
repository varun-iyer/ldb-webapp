import flask
from app.models import Document
from app import app, db
from app.forms import GraphForm

@app.route('/')
@app.route('/index')
def index():
    form = GraphForm()
    if form.validate_on_submit():
        return flask.render_template('index.html')
    return flask.render_template('index.html')
