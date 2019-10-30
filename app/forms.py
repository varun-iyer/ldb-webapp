from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class GraphForm(FlaskForm):
    doi = StringField('DOI', validators=[DataRequired()])
    submit = SubmitField('Build Graph')
