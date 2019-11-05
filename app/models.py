from app import db, login
from sqlalchemy import JSON
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

reference = db.Table('reference',
    db.Column('paper', db.Integer, db.ForeignKey('document.doi')),
    db.Column('reference', db.Integer, db.ForeignKey('document.doi'))
)
 
 
class Document(db.Model):
    __tablename__ = 'document'

    id = db.Column(db.Integer, primary_key=True)
    doi = db.Column(db.String(64), index=True, unique=True)
    references = db.relationship('Document', secondary=reference, backref='referenced_by')
    queried = db.Column(db.Boolean, default=False)
    meta = db.Column(JSON, default=None)

    def __getitem__(self, key):
        return self.meta[key].astext

    def __hash__(self):
        try:
            return self['DOI'][0].__hash__()
        except (KeyError, IndexError):
            try:
                return self['key'].__hash__()
            except (KeyError, IndexError):
                return self['title'][0].__hash__()

    def __str__(self):
        try:
            return self['title'][0]
        except (KeyError, IndexError):
            try:
                return self['DOI'][0]
            except (KeyError, IndexError):
                return self['key']

    def __repr__(self):
        try:
            return self['DOI'][0]
        except (KeyError, IndexError):
            return self['key']
