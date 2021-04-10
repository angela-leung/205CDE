import os 
import secrets
from PIL import Image
from flask import render_template, request, flash, redirect, url_for, abort
from app import app, db, bcrypt, mail
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, ProductForm, RequestResetForm, ResetPasswordForm
from app.models import User, Post, Violin, ShoppingOrder, AccountAddress
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route("/")
@app.route("/home")
def home():
    return render_template('product.html')

@app.route("/index")
def index():
    posts= Post.query.all()
    return render_template('index.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User (username=form.username.data, email_address=form.email_address.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to login','success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
       
@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.isaadminUser:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('admin.index'))
            else:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('index'))
            
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/css/profile_pics', picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    #user = User (username=form.username.data, email_address=form.email_address.data)
    address = AccountAddress.query.filter_by(user_id=current_user.id).first()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        address = AccountAddress.query.filter_by(user_id=current_user.id).first()
        current_user.username = form.username.data
        current_user.email_address = form.email_address.data
        #address = AccountAddress(country=form.country.data, city = form.city.data, street = form.street.data, 
        #postcode = form.postcode.data, user_id=current_user.id)
        
        if address is True:
            address.country = form.country.data
            address.city = form.city.data
            address.street = form.street.data
            address.postcode = form.postcode.data
        else:
            latest_address = AccountAddress(country=form.country.data,city=form.city.data,
            street=form.street.data,postcode=form.postcode.data, user_id=current_user.id)
            db.session.add(latest_address)
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        address = AccountAddress.query.filter_by(user_id=current_user.id).first()
        form.username.data = current_user.username
        form.email_address.data = current_user.email_address
        if address:
            form.country.data = address.country
            form.city.data = address.city
            form.street.data = address.street
            form.postcode.data = address.postcode
        else:
            flash(f'no address here','danger')
        
    image_file = url_for('static', filename='css/profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route('/post/<int:post_id>/update', methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('index'))

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='violinfactoryhouse@gmail.com',
                  recipients=[user.email_address])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request_pw.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_pw.html', title='Reset Password', form=form)

@app.route ("/view_product",methods=['GET', 'POST'])
def view_product():
    product_images = Violin.query.all()
    return render_template('product.html', product_images=product_images)

@app.route("/upload_product/", methods=['GET', 'POST'])
def upload_product():
    form = ProductForm()
    if request.method == 'POST':
        file = request.files['violin_product']
        print(file.filename)
        path = (os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        file.save(path)
        #return redirect(url_for('uploaded_product',filename=filename))
        
        # check if the post request has the file part
        if 'violin_product' not in request.files:
            flash('No file part')
            return redirect(request.url)
            
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect('upload_product')
        
            
        if form.validate_on_submit():
            product = Violin(product_images=file.filename, product_name=form.product_name.data, price=form.product_price.data)
            db.session.add(product)
            db.session.commit()
            flash('Your picture has been created!', 'success')
            return redirect(url_for('view_product'))
    return render_template("create_product.html",form=form)

@app.route("/add_product_to_order", methods=['POST'])
@login_required
def add_to_order():
    if request.method == 'POST':
        print('entered')
        target_product = request.values.get("product_id")
        target_violin = Violin.query.filter_by(id=target_product).first()
        print(target_violin)
        if target_violin:
            add_to_order = ShoppingOrder(violin_id=target_product ,user=current_user.id)
            db.session.add(add_to_order)
            db.session.commit()
        else:
            flash("this product does not exist")

    return redirect(request.referrer)
    

@app.route("/order", methods=['GET'])
@login_required
def order():
    orders = ShoppingOrder.query.all()
    violins = Violin.query.all()
    return render_template('order.html', violins=violins ,orders=orders)

@app.route("/order/<int:shoppingorder_id>")
def order_item(shoppingorder_id):
    orders = ShoppingOrder.query.get_or_404(shoppingorder_id)
    
    return render_template('order.html', orders=orders)
#(shoppingorder_id)

@app.route("/order/<int:shoppingorder_id>/delete", methods=['POST'])
@login_required
def delete_order(shoppingorder_id):
    orders = ShoppingOrder.query.first()
    db.session.delete(orders)
    db.session.commit()
    flash('Your order has been deleted!', 'success')
    return redirect(url_for('order'))

@app.route('/search')
def search():
    search = request.args.get('search')

    if search:
        posts = Post.query.filter(Post.title.contains(search) |
        Post.content.contains(search))
    else:
        posts = Post.query.all()
    return render_template('product.html', posts=posts)


