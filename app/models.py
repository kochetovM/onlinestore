from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))
  description = db.Column(db.String, nullable=False)
  image = db.Column(db.String(255), default="http://placehold.it/400x400")
  price = db.Column(db.Float)
  inventory = db.Column(db.Integer)
  pr_type = db.Column(db.String(50))

  def __repr__(self):
    return f"Product({self.id}) {self.name} - {self.image} - price: {self.price}, inventory: {self.inventory})"

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(100), index=True, unique=True)
  password_hash = db.Column(db.String(100))
  admin = db.Column(db.Boolean, default=True)
  username = db.Column(db.String, nullable=False)

  # fname = db.Column(db.String(50))
  # lname = db.Column(db.String(50))
  # address = db.Column(db.String(255))

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def set_admin(self):
    self.admin=True

  def __repr__(self):
    return f"Client({self.email}), admin: {self.admin}"


@login.user_loader
def load_user(id):
  return User.query.get(int(id))

