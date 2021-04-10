import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_script import Manager, prompt, prompt_pass

app = Flask(__name__)

app.config['SECRET_KEY']= 'b11b1e24e2639c068cebaf50d2e5912f'
app.config['SQLALCHEMY_DATABASE_URI'] =  "mysql+pymysql://root@localhost/205CDE"
app.config['UPLOAD_FOLDER'] = 'app/static/products/'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'violinfactoryhouse@gmail.com'
app.config['MAIL_PASSWORD'] = 'Mnb12345!'
mail = Mail(app)


from app.models import *
manager = Manager(app)
admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Violin, db.session))
admin.add_view(ModelView(ShoppingOrder, db.session))

class UserView(ModelView):



    def is_accessible(self):
        return(login.current_user.is_authenticated and current_user.AdminUser)


    def inaccessible_callback(self, username, **kwargs):

        return redirect(url_for('login', next=request.url))

    column_exclude_list = ('password')
isSuperUser = db.Column(db.Boolean(),default=False)

from app import routes, db









@manager.command
def admin_create():

    username = prompt('admin_username')
    email_address = prompt('admin_email')
    password = prompt_pass('admin_password')
    confirm_password = prompt_pass('confrim_admin_password')
    

    if not password == confirm_password:
        sys.exit('\n sorry password is not correct!!!!!!')

    hash_password = bcrypt.generate_password_hash(confirm_password).decode('utf-8')
    admin = User(username = username, email_address= email_address, password = hash_password, isaadminUser = True)

    db.session.add(admin)
    db.session.commit()