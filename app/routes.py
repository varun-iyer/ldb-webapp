import flask
from app.models import Document
from app import app, db
from app.forms import GraphForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = GraphForm()
    if form.validate_on_submit():
        return flask.render_template('index.html', form=form)
    return flask.render_template('index.html', form=form)
