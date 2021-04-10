from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db, login_manager, app
from flask_login import UserMixin
from flask_admin import Admin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(20),unique=True, nullable=False)
    email_address = db.Column(db.String(120),unique=True, nullable=False)
    image_file = db.Column(db.String(20),nullable=False, default='default.jpg' )
    password = db.Column(db.String(60),nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    order = db.relationship('ShoppingOrder', backref='order', lazy=True)
    address = db.relationship('AccountAddress', backref='address', lazy=True)
    isaadminUser = db.Column(db.Boolean(),default=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email_address}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted =db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id =db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Violin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100),nullable=False)
    product_images = db.Column(db.String(20),nullable=False)
    product_date =db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    price = db.Column(db.Integer,nullable=False)
    shopping_order = db.relationship('ShoppingOrder', backref='product', lazy=True)

class ShoppingOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    violin_id = db.Column(db.Integer, db.ForeignKey('violin.id'), nullable=False)
    order_date =db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user =  db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

class AccountAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(120),unique=False, nullable=False)
    city = db.Column(db.String(120),unique=False, nullable=False)
    street = db.Column(db.String(120),unique=False, nullable=False)
    postcode = db.Column(db.String(120),unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
