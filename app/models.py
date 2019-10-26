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
    doi = db.Column(db.String(64), index=True)
    meta = db.Column(JSON)

    def __getitem__(self, key):
        return self.meta[key].astext
