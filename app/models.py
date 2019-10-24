from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

user_collection = db.Table('user_collection',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('collection_id', db.Integer, db.ForeignKey('collection.id'))
)
 
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(64), index=True, unique=False)
    password_hash = db.Column(db.String(128))
    collections = db.relationship('Collection', secondary=user_collection)

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
         
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_collection(self, collection):
        return self.collections.append(collection)

 
class Collection(db.Model):
    __tablename__ = 'collection'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(1024), index=True);
    documents = db.relationship('Document', backref='collection', lazy='dynamic')

    def __repr__(self):
        return '<Collection {}>'.format(self.name)


class Document(db.Model):
    # TODO how to correlate documents that are the same in diff. collections?
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))

 
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
