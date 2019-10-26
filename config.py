import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Ko89OD9PjEF+FrX5AvjlrnWHrqXjjG2IXaqY2rxo/yz0Vf7o/Dx8Mg=='
     
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FILES_DEST = '/home/varun/ldb/storage/'
    UPLOADED_FILES_ALLOW = ''
