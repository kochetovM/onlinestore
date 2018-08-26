import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  UPLOAD_FOLDER = basedir + os.path.join('/app/static/images/products/')
  STRIPE_SECRET_KEY = os.getenv('sk_test_s8zCASFgKidV07WleXsXxrzj')
  STRIPE_PUBLISHABLE_KEY = os.getenv('pk_test_yS1w7tqtVE0gHbgHdjY957To')


