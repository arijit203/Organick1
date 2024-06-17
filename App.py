from flask import Flask,session, abort,render_template, redirect, url_for, request,flash,jsonify
from wtforms.validators import InputRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exists
from sqlalchemy.exc import SQLAlchemyError
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,ValidationError,IntegerField,FloatField,SelectField,RadioField
from wtforms.validators import DataRequired,EqualTo,Length,NumberRange,Email
from flask_wtf.csrf import generate_csrf
from functools import wraps
import matplotlib
matplotlib.use('Agg')
from flask_wtf.csrf import CSRFProtect
import matplotlib.pyplot as plt
from datetime import datetime
from pytz import timezone
from sqlalchemy import asc,desc
indian_timezone = timezone('Asia/Kolkata')
from email.message import EmailMessage
import ssl
import smtplib
from jinja2 import Environment, FileSystemLoader
from email.message import EmailMessage
import smtplib
from flask import Flask, render_template_string,render_template
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart





from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, login_user,LoginManager, login_required, logout_user,current_user


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(os.getcwd(),"instance","grocery.db")
app.config['SECRET_KEY']="my secret key"

db=SQLAlchemy(app)
csrf = CSRFProtect(app)

#Flask Login Stuff
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

class Users(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(200),nullable=False,unique=True)
    name=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(200),nullable=False,unique=True)
    password_hash=db.Column(db.String(128))
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password) 
    #create string
    def __repr__(self):
        return '<Name %r>' %self.name

   


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))




@app.route('/home')
def home():
    form=UserForm()
    cartform=Cart()
    username = request.args.get('username')
    email = request.args.get('email')

    categories = Category.query.all()
    category_items_dict = {}
    for category in categories:
        items = Order_items.query.filter_by(category_id=category.category_id).all()
        category_items_dict[category.category_id] = items

    if current_user.is_authenticated:
        cart_items = db.session.query(Cart, Order_items, Category)\
        .join(Order_items, Cart.item_id == Order_items.id)\
        .join(Category, Order_items.category_id == Category.category_id)\
        .filter(Cart.user_id == current_user.id)\
        .all()
        total_price = 0
        for cart_item, item, category in cart_items:
            total_price += item.price * cart_item.quantity
        print(total_price)  
        return render_template('index.html',categories=categories , cart_items=cart_items,category_items_dict=category_items_dict,username=current_user.username, email=current_user.email,form=form,cartform=cartform,total_price=total_price)
    return render_template('index.html',categories=categories , category_items_dict=category_items_dict,username=username, form=form,cartform=cartform,email=email)
    

@app.route('/about')
def about():
    form=UserForm()
    cartform=Cart()
    username = request.args.get('username')
    email = request.args.get('email')

    categories = Category.query.all()
    category_items_dict = {}
    for category in categories:
        items = Order_items.query.filter_by(category_id=category.category_id).all()
        category_items_dict[category.category_id] = items

    if current_user.is_authenticated:
        cart_items = db.session.query(Cart, Order_items, Category)\
        .join(Order_items, Cart.item_id == Order_items.id)\
        .join(Category, Order_items.category_id == Category.category_id)\
        .filter(Cart.user_id == current_user.id)\
        .all()
        total_price = 0
        for cart_item, item, category in cart_items:
            total_price += item.price * cart_item.quantity
        print(total_price)  
        return render_template('about.html',categories=categories , cart_items=cart_items,category_items_dict=category_items_dict,username=current_user.username, email=current_user.email,form=form,cartform=cartform,total_price=total_price)
    return render_template('about.html',categories=categories , category_items_dict=category_items_dict,username=username, form=form,cartform=cartform,email=email)
    

@app.route('/shop')
def shop():
    # Access form information from the URL parameters
    form=UserForm()
    cartform=Cart()
    username = request.args.get('username')
    email = request.args.get('email')

    categories = Category.query.all()
    category_items_dict = {}
    for category in categories:
        items = Order_items.query.filter_by(category_id=category.category_id).all()
        category_items_dict[category.category_id] = items

    if current_user.is_authenticated:
        cart_items = db.session.query(Cart, Order_items, Category)\
        .join(Order_items, Cart.item_id == Order_items.id)\
        .join(Category, Order_items.category_id == Category.category_id)\
        .filter(Cart.user_id == current_user.id)\
        .all()
        total_price = 0
        for cart_item, item, category in cart_items:
            total_price += item.price * cart_item.quantity
        print(total_price)  
        return render_template('shop.html',categories=categories , cart_items=cart_items,category_items_dict=category_items_dict,username=current_user.username, email=current_user.email,form=form,cartform=cartform,total_price=total_price)


    # Render the shop.html template with the form information
    return render_template('shop.html',categories=categories , category_items_dict=category_items_dict,username=username, form=form,cartform=cartform,email=email)
   


@app.route('/portfolio')
def portfolio():
    form=UserForm()
    cartform=Cart()
    username = request.args.get('username')
    email = request.args.get('email')

    categories = Category.query.all()
    category_items_dict = {}
    for category in categories:
        items = Order_items.query.filter_by(category_id=category.category_id).all()
        category_items_dict[category.category_id] = items

    if current_user.is_authenticated:
        cart_items = db.session.query(Cart, Order_items, Category)\
        .join(Order_items, Cart.item_id == Order_items.id)\
        .join(Category, Order_items.category_id == Category.category_id)\
        .filter(Cart.user_id == current_user.id)\
        .all()
        total_price = 0
        for cart_item, item, category in cart_items:
            total_price += item.price * cart_item.quantity
        print(total_price)  
        return render_template('portfolio.html',categories=categories , cart_items=cart_items,category_items_dict=category_items_dict,username=current_user.username, email=current_user.email,form=form,cartform=cartform,total_price=total_price)
    return render_template('portfolio.html',categories=categories , category_items_dict=category_items_dict,username=username, form=form,cartform=cartform,email=email)
    # return render_template('portfolio.html')

@app.route('/blog')
def blog():
    form=UserForm()
    cartform=Cart()
    username = request.args.get('username')
    email = request.args.get('email')

    categories = Category.query.all()
    category_items_dict = {}
    for category in categories:
        items = Order_items.query.filter_by(category_id=category.category_id).all()
        category_items_dict[category.category_id] = items

    if current_user.is_authenticated:
        cart_items = db.session.query(Cart, Order_items, Category)\
        .join(Order_items, Cart.item_id == Order_items.id)\
        .join(Category, Order_items.category_id == Category.category_id)\
        .filter(Cart.user_id == current_user.id)\
        .all()
        total_price = 0
        for cart_item, item, category in cart_items:
            total_price += item.price * cart_item.quantity
        print(total_price)  
        return render_template('blog.html',categories=categories , cart_items=cart_items,category_items_dict=category_items_dict,username=current_user.username, email=current_user.email,form=form,cartform=cartform,total_price=total_price)
    return render_template('blog.html',categories=categories , category_items_dict=category_items_dict,username=username, form=form,cartform=cartform,email=email)
    # return render_template('blog.html')

@app.route('/contact')
def contact():
    form=UserForm()
    cartform=Cart()
    username = request.args.get('username')
    email = request.args.get('email')

    categories = Category.query.all()
    category_items_dict = {}
    for category in categories:
        items = Order_items.query.filter_by(category_id=category.category_id).all()
        category_items_dict[category.category_id] = items

    if current_user.is_authenticated:
        cart_items = db.session.query(Cart, Order_items, Category)\
        .join(Order_items, Cart.item_id == Order_items.id)\
        .join(Category, Order_items.category_id == Category.category_id)\
        .filter(Cart.user_id == current_user.id)\
        .all()
        total_price = 0
        for cart_item, item, category in cart_items:
            total_price += item.price * cart_item.quantity
        print(total_price)  
        return render_template('contact.html',categories=categories , cart_items=cart_items,category_items_dict=category_items_dict,username=current_user.username, email=current_user.email,form=form,cartform=cartform,total_price=total_price)
    return render_template('contact.html',categories=categories , category_items_dict=category_items_dict,username=username, form=form,cartform=cartform,email=email)
    






 
class LoginForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    password_hash=PasswordField("Password",validators=[DataRequired()])
    submit=SubmitField("Login")

#create the Register Form Class
class UserForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired()])
    name=StringField("Name",validators=[DataRequired()])
    email=StringField("Email",validators=[DataRequired()])
    password_hash=PasswordField('Password',validators=[DataRequired()])
    password_hash2=PasswordField('Confirm Password',validators=[DataRequired()])
    submit=SubmitField("Sign Up")

# New route for checking if the email is in the database
@app.route('/check_email', methods=['POST'])
def check_email():
    try:
        email = request.json.get('email')
        print(email)
        user = Users.query.filter_by(email=email).first()
        print(user)
        if user:
            return jsonify({'exists': False})
        else:
            return jsonify({'exists': True})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'An error occurred'})



@app.route('/reset_password', methods=['POST'])
def reset_password():
   
    new_password = request.form.get('newPassword')
    userEmail=request.form.get('userEmail')

    # Update the user's password in the database
    user = Users.query.filter_by(email=userEmail).first()  # Replace with actual email
    if user:
        hashed_pw = generate_password_hash(new_password)
        user.password_hash = hashed_pw
        db.session.commit()
        print(new_password)
        print(hashed_pw)
        flash('Password reset successfully! Please log in.')
        return redirect(url_for('login'))  # Redirect to login page after successful password reset
    else:
        flash('User not found!')
    


@app.route('/user_register', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    
    if form.validate_on_submit():
        print(form.email.data,"** $$")
        print("Hi there but there")
        existing_user = Users.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username is already taken. Please choose a different username.")
            return render_template("user_register.html", name=name, form=form)
        
        user = Users.query.filter_by(email=form.email.data).first()
        
        if user is None:
            # hash the password!!!
            hashed_pw = generate_password_hash(form.password_hash.data)
            user = Users(username=form.username.data, name=form.name.data, email=form.email.data, password_hash=hashed_pw)

            
            db.session.add(user)
            db.session.commit()
            flash("Registration Complete!")
            print("Commited")
            login_user(user)
            return redirect(url_for('shop',username=form.username.data))
        else:
            print("already commited")
            flash("Email is already registered. Please use a different email.")
            return render_template("user_register.html", username=form.username.data, form=form, our_users=existing_user,name=name)
    
    if form.errors:
        print("Form errors:", form.errors)    
    username = form.username.data
    form.username.data = ''
    form.name.data = ''
    form.email.data = ''
    form.password_hash.data = ''

    smtp_token = os.getenv("smtp_token")
    return render_template("user_register.html", name=name, form=form, username=username,smtp_token=smtp_token)


def user_profile_access_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # Get the username from the URL parameters or wherever you store it
        username = kwargs.get('username')  # Adjust this based on your route definition
        
        # Check if the current user is authenticated and matches the target user
        if current_user.is_authenticated   and current_user.username == username:
            # and session['is_user']
            return func(*args, **kwargs)  # User is authorized, proceed with the view
        else:
            # User is not authorized, you can handle this case (e.g., redirect)
            return "Access Denied: You are not authorized to view this page", 403  # 403 Forbidden status code

    return decorated_view

#Create Login Page
@app.route('/user_login',methods=['GET','POST'])

def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()
        
        if user:
            #check the hash
            
            if check_password_hash(user.password_hash,form.password_hash.data):
                login_user(user) #creates the session
                session['is_user']=True
                
                flash('Login successful!', 'success')
                next_url = request.args.get('next')
                print("Gone to :",next_url)
                return redirect(next_url or url_for('home'))

            else:
                flash('Invalid or Wrong Password - Try Again!!')    
        else:
            flash("That User doesn't exist! Try Again...")   
    smtp_token = os.getenv("smtp_token")         
    return render_template('user_login.html',form=form,smtp_token=smtp_token)

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    

    if form.validate_on_submit():
        # Here you can add logic to handle the forgot password functionality.
        # For simplicity, let's assume you have a User model with an email field.
        # You might want to generate a token for resetting the password and send an email.
        # For now, let's just display a flash message.
        flash(f"A password reset link has been sent to {form.email.data}.", 'success')
        return redirect(url_for('login'))  # Redirect to the login page after handling the forgot password request

    return render_template('forgot_password.html', form=form)


@app.route('/user',methods=["GET","POST"])
@login_required
@user_profile_access_required
def user_dashboard(username):
    # name=request.args.get('username')
    categories = Category.query.all()
    category_items_dict = {}
    for category in categories:
        items = Order_items.query.filter_by(category_id=category.category_id).all()
        category_items_dict[category.category_id] = items

    return render_template('user_dashboard.html', categories=categories, category_items_dict=category_items_dict,username=username)

class Cart(db.Model):
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('order_items.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Cart cart_id={self.cart_id} item_id={self.item_id} user_id={self.user_id} username={self.username} quantity={self.quantity}>'

class CartForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])

class BuyForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    

@app.route('/check_availability', methods=['GET'])
def check_availability():
   
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    all_available = "True"

    for cart_item in cart_items:
        item_id = cart_item.item_id
        quantity = cart_item.quantity

        # Retrieve the item from the database
        item = Order_items.query.get(item_id)

        if item is not None:
            # Check if the available quantity is sufficient
            if item.quantity < quantity:
                all_available = str(quantity) + item.unit.split('/')[1] +" of " + item.name + " not available in store. Only up to " + str(item.quantity) + item.unit.split('/')[1] + " Available"                
                break
        else:
            # Item not found in the database
            all_available = "Item removed from database"
            break

    return jsonify({'allAvailable': all_available})


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if not current_user.is_authenticated:
        # Return a JSON response indicating authentication failure
        return jsonify({'error': 'User not authenticated'}), 401

    item_id = request.form.get('item_id')
    category_id = request.form.get('category_id')
    quantity = request.form.get('quantity')  
    print(quantity)
    if quantity=='':
        return jsonify({'Item could not be added!'})
    
    quantity=int(quantity)

    item = Order_items.query.get_or_404(item_id)
    cart_item = Cart.query.filter_by(item_id=item_id, category_id=category_id, user_id=current_user.id).first()
    
    if cart_item:
        if int(cart_item.quantity) + int(quantity) > int(item.quantity):
            # Return a JSON response indicating failure due to insufficient stock
            return jsonify({'error': 'Item could not be added to your cart due to insufficient stock'}), 400
        else:
            cart_item.quantity += int(quantity)
            
           
            db.session.commit()
            # Return a JSON response indicating success
            return jsonify({'success': 'Item added to your cart'}), 200
    else:
        new_cart_item = Cart(category_id=category_id, item_id=item_id, user_id=current_user.id, username=current_user.username, quantity=quantity)
        db.session.add(new_cart_item)
        db.session.commit()
        # Return a JSON response indicating success
        return jsonify({'success': 'Item added to your cart'}), 200

@app.route('/get_cart_content', methods=['GET'])
@login_required
def get_cart_content():
    # Get the current user's cart
    user_cart = Cart.query.filter_by(user_id=current_user.id).first()

    if user_cart:
        # Get the cart items
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()

        # Fetch detailed product information for each item in the cart
        cart_content = []
        for cart_item in cart_items:
            product_info = Order_items.query.filter_by(id=cart_item.item_id).first()
            if product_info:
                cart_content.append({
                    'item_id': cart_item.item_id,
                    'name': product_info.name,
                    'price': product_info.price,
                    'quantity': cart_item.quantity,
                    'category_id': product_info.category_id,
                    'unit': product_info.unit,
                    # Add more fields as needed
                })
       
        return jsonify(cart_content)
    else:
        # No cart for the user
        return jsonify([])


@app.route('/fetch_items', methods=['GET'])
def fetch_items():
    search_term = request.args.get('searchTerm')
    category_id = request.args.get('categoryId')

    # Assuming you have a function to fetch items from the database based on search term and category
    items = get_items_from_database(search_term, category_id)

    # Render the product cards HTML using a template
    html = render_template('product_cards_template.html', items=items)

    return jsonify({'html': html})

@app.route('/search_items', methods=['GET'])
def search_items():
    search_term = request.form.get('search_term')
    
    # Perform the search in the database based on the search term
    results = Order_items.query.filter(Order_items.name.ilike(f'%{search_term}%')).all()
    
    # Convert the results to a list of dictionaries or a format suitable for JSON
    items = [{'id': item.id, 'name': item.name, 'price': item.price} for item in results]
    print(items)
    return jsonify(items)


def get_items_from_database(search_term, category_id):
    # Implement your logic to query the database and retrieve items
    # This is just a placeholder, replace it with your actual database query logic
    items = Order_items.query.filter(Order_items.category_id == category_id, Order_items.name.ilike(f"%{search_term}%")).all()

    return items

# @app.route("/delete_from_cart/<int:item_id>",methods=['GET','POST'])
# def delete_from_cart(item_id):
#     cart_item = Cart.query.filter_by(username=current_user.username, item_id=item_id).first()

#     if cart_item:
#         try:
#             # Update the Order_items table and add the quantity back
#             # item = Order_items.query.get_or_404(item_id)
#             # item.quantity += cart_item.quantity

            
#             db.session.delete(cart_item)
#             db.session.commit()

#             flash("Item deleted from the cart.", "success")
#         except:
#             flash("Error occurred while deleting the item from the cart. Please try again later.", "danger")
#     else:
#         flash("Item not found in the cart.", "danger")
#     categories = Category.query.all()
#     cart_items = db.session.query(Cart, Order_items, Category)\
#         .join(Order_items, Cart.item_id == Order_items.id)\
#         .join(Category, Order_items.category_id == Category.category_id)\
#         .filter(Cart.user_id == current_user.id)\
#         .all()
#     total_price = 0
#     for cart_item, item, category in cart_items:
#         total_price += item.price * cart_item.quantity
#     category_items_dict = {}
#     for category in categories:
#         items = Order_items.query.filter_by(category_id=category.category_id).all()
#         category_items_dict[category.category_id] = items    
#     # return redirect(url_for('shop', username=username))
#     form=UserForm()
#     cartform=CartForm()    
#     return redirect(url_for('shop',categories=categories , cart_items=cart_items,category_items_dict=category_items_dict,username=current_user.username, email=current_user.email,form=form,cartform=cartform,total_price=total_price))
 
@app.route("/delete_from_cart/<int:item_id>", methods=['POST'])
def delete_from_cart_ajax(item_id):
    cart_item = Cart.query.filter_by(username=current_user.username, item_id=item_id).first()

    if cart_item:
        try:
            print(cart_item)
            db.session.delete(cart_item)
            db.session.commit()

            return jsonify({'success': True, 'message': 'Item deleted from the cart.'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
    else:
        return jsonify({'success': False, 'message': 'Item not found in the cart.'})

# Save address respective to a particular User
class User_address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(10), nullable=False)
    receiver_name = db.Column(db.String(100), nullable=False)
    delivery_address = db.Column(db.String(255), nullable=False)
    address_type = db.Column(db.String(10), nullable=False)

class AddressForm(FlaskForm):
    title = SelectField('Title', choices=[('','Title') ,('1', 'Mr.'), ('2', 'Mrs'), ('3', 'Miss')], validators=[InputRequired()])
    receiver_name = StringField('Receiver\'s Name', validators=[InputRequired()])
    delivery_address = StringField('Delivery Address', validators=[InputRequired()])
    save_address_as = RadioField('Save Address as', choices=[('Home', 'Home'), ('Work', 'Work'), ('Other', 'Other')], validators=[InputRequired()])


    
@app.route("/cart",methods=["GET","POST"])
def cart():
    cart_items = db.session.query(Cart, Order_items, Category)\
        .join(Order_items, Cart.item_id == Order_items.id)\
        .join(Category, Order_items.category_id == Category.category_id)\
        .filter(Cart.user_id == current_user.id)\
        .all()
    addresses = db.session.query(User_address).filter_by(user_id=current_user.id).all()
    form=AddressForm()
    google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    print(google_maps_api_key,"****")
    return render_template("cart.html",username=current_user.username,cart_items=cart_items,addresses=addresses,form=form,google_maps_api_key=google_maps_api_key)


@app.route("/delete/<int:item_id>",methods=['GET'])
def delete(item_id):
    cart_item = Cart.query.filter_by(username=current_user.username, item_id=item_id).first()

    if cart_item:
        try:
            # Update the Order_items table and add the quantity back
            # item = Order_items.query.get_or_404(item_id)
            # item.quantity += cart_item.quantity

            
            db.session.delete(cart_item)
            db.session.commit()
            return jsonify({"success": True, "message": "Item successfully removed"})
            
        except:
            return jsonify({"success":False,"mesaage":"Error occurred while deleting the item from the cart. Please try again later."}),404
    else:
        return jsonify({"success": False, "message": "Item not found in the cart"}), 404
        
@app.route('/increase_quantity/<int:item_id>', methods=['GET'])
def increase_quantity(item_id):
    # Find the item in the cart
    cart_item = Cart.query.filter_by(username=current_user.username, item_id=item_id).first()

    if cart_item:
        # Ensure the quantity doesn't go below 1
        cart_item.quantity += 1
        db.session.commit()
        return jsonify({"success": True, "message": "Quantity increased successfully"})
    else:
        return jsonify({"success": False, "message": "Item not found in the cart"}), 404

@app.route('/decrease_quantity/<int:item_id>', methods=['GET'])
def decrease_quantity(item_id):
    # Find the item in the cart
    print("Increase")
    cart_item = Cart.query.filter_by(username=current_user.username, item_id=item_id).first()

    if cart_item:
        # Ensure the quantity doesn't go below 1
        cart_item.quantity = max(cart_item.quantity - 1, 1)
        db.session.commit()
        return jsonify({"success": True, "message": "Quantity decreased successfully"})
    else:
        return jsonify({"success": False, "message": "Item not found in the cart"}), 404
    
    

def user_address_to_dict(user_address):
    return {
        'id': user_address.id,
        'user_id': user_address.user_id,
        'title': user_address.title,
        'receiver_name': user_address.receiver_name,
        'delivery_address': user_address.delivery_address,
        'address_type': user_address.address_type,
        # Add more fields as needed
    }

@app.route('/save_address', methods=['POST'])
def save_address():
    
    form = AddressForm()

    if form.validate_on_submit():
        # Create a new user address instance
        new_user_address = User_address(
            user_id=current_user.id,
            title=form.title.data,
            receiver_name=form.receiver_name.data,
            delivery_address=form.delivery_address.data,
            address_type=form.save_address_as.data
        )

        # Add the user address to the database
        db.session.add(new_user_address)
        db.session.commit()
        
        # Fetch addresses and convert them to dictionaries
        addresses = User_address.query.filter_by(user_id=current_user.id).all()
        # addresses_data = [user_address_to_dict(address) for address in addresses]
        
        return jsonify({'success': True, 'message': 'Address added successfully', 'address': user_address_to_dict(new_user_address)})
    else:
        # Handle form validation errors
        flash('Form validation error. Please check your input.', 'error')
        return jsonify({'success': False, 'message': 'Form validation error'})
# @app.route('/save_address', methods=['POST'])
# def save_address():
   
#     form = AddressForm()

#     if form.validate_on_submit():
#         # Create a new user address instance
#         new_user_address = User_address(
#             user_id=current_user.id,  # Assuming user_id is associated with the current user
#             title=form.title.data,
#             receiver_name=form.receiver_name.data,
#             delivery_address=form.delivery_address.data,
#             address_type=form.save_address_as.data
#         )

#         # Add the user address to the database
#         db.session.add(new_user_address)
#         db.session.commit()
#         flash("Address added, now Proceed to Payment")

#         # Fetch and return all addresses after adding
#         addresses = User_address.query.filter_by(user_id=current_user.id).all()
#         return jsonify({'success': True, 'message': 'Address added successfully', 'addresses': addresses})
#     else:
#         # Handle form validation errors
#         flash('Form validation error. Please check your input.', 'error')
#         return jsonify({'success': False, 'message': 'Form validation error'})    
@app.route('/get_all_addresses', methods=['GET'])
def get_all_addresses():
    try:
        # Fetch addresses for the current user
        addresses = User_address.query.filter_by(user_id=current_user.id).all()

        # Transform addresses to a format suitable for JSON
        addresses_data = [{
            'id': address.id,
            'title': address.title,
            'receiver_name': address.receiver_name,
            'delivery_address': address.delivery_address,
            'address_type': address.address_type
        } for address in addresses]

        return jsonify({'success': True, 'address_details': addresses_data})
    except Exception as e:
        # Handle exceptions appropriately
        print(f"Error: {str(e)}")
        return jsonify({'success': False, 'message': 'Error fetching addresses'})




@app.route('/get_address_details/<int:address_id>', methods=['GET'])
def get_address_details(address_id):
    address = User_address.query.get(address_id)

    if address:
        # Convert the address object to a dictionary
        address_details = user_address_to_dict(address)
        return jsonify({'success': True, 'address_details': address_details})
    else:
        return jsonify({'success': False, 'message': 'Address not found'})


# @app.route('/edit_address/<int:address_id>', methods=['GET'])
# def edit_address(address_id):
   
#     # Fetch the address details from the database based on the address_id
#     address = User_address.query.get(address_id)
#     print("Fetching from edit_address GET")
#     # Return the address details as JSON

#     return jsonify({
#         'id': address.id,
#         'user_id': address.user_id,
#         'title': address.title,
#         'receiver_name': address.receiver_name,
#         'delivery_address': address.delivery_address,
#         'address_type': address.address_type,
#         'edit_mode':True
#     })


# @app.route('/update_address/<int:address_id>', methods=['POST'])
# def update_address(address_id):
#     edit_mode = request.form.get('edit_mode', 'false').lower() == 'true'

#     if edit_mode:
#         # Update the existing address with the new information
#         address = User_address.query.get(address_id)
#         address.title = request.form['title']
#         address.receiver_name = request.form['receiver_name']
#         address.delivery_address = request.form['delivery_address']
#         address.address_type = request.form['save_address_as']
#         print("Updated")
        
#         db.session.commit()

#         # Return success response
#         flash('Address updated successfully')

#         return redirect(url_for('cart'))
#         # return jsonify({'message': 'Address updated successfully', 'redirect_url': url_for('cart')})
#     else:
#         # Handle the case where edit_mode is not set
       
#         flash('Invalid request. Please try again.', 'error')
#         return redirect(url_for('cart'))
    
    # Redirect to a relevant page (e.g., cart or a confirmation page)
    # flash('Address updated successfully')
      # Change 'cart' to the appropriate endpoint


@app.route('/update_address/<int:address_id>', methods=['POST'])
def update_address(address_id):
    try:
        # Fetch the existing address
        address = User_address.query.get(address_id)

        # Update the fields based on the form data
        address.title = request.form['title']
        address.receiver_name = request.form['receiver_name']
        address.delivery_address = request.form['delivery_address']
        address.address_type = request.form['save_address_as']

        # Commit changes to the database
        db.session.commit()

        # Return success response
        
        return jsonify({'message': 'Address updated successfully', 'success': True})
    except Exception as e:
        # Handle exceptions appropriately
        print(f"Error: {str(e)}")
        flash('Error updating address', 'error')
        return jsonify({'message': 'Error updating address', 'success': False})
@app.route('/delete_address/<int:address_id>', methods=["POST"])
def delete_address(address_id):
    # Find the address in the database
    address = User_address.query.filter_by(id=address_id).first()

    if address:
        try:
            # Update the Order_items table and add the quantity back
            # item = Order_items.query.get_or_404(item_id)
            # item.quantity += cart_item.quantity

            print("***************",address.id)
            db.session.delete(address)
            db.session.commit()
            return jsonify({"success": True, "message": "Address successfully removed"})
            
        except:
            return jsonify({"success":False,"mesaage":"Error occurred while deleting the address from the table. Please try again later."}),404
    else:
        return jsonify({"success": False, "message": "Address not found in the table"}), 404
# Add this route in your Flask app
# @app.route('/delete_address/<int:address_id>', methods=['GET'])
# def delete_address(address_id):
#     # Find the address in the database
#     address = User_address.query.filter_by(id=address_id).first()

#     if address:
#         # Delete the address
#         db.session.delete(address)
#         db.session.commit()

#         # Return a success JSON response
#         return jsonify({'message': 'Address deleted successfully'})
#     else:
#         # Return an error JSON response if the address is not found
#         return jsonify({'error': 'Address not found'}), 404
    
@app.route('/checkout/<int:address_id>',methods=['GET','POST'])
def checkout(address_id):
    # Handle the payment logic with the selected address ID
    # For demonstration, just render a template
    payment_form = PaymentForm()
    total_price = 0
    cart_items = db.session.query(Cart, Order_items, Category)\
        .join(Order_items, Cart.item_id == Order_items.id)\
        .join(Category, Order_items.category_id == Category.category_id)\
        .filter(Cart.user_id == current_user.id)\
        .all()
    
    address=User_address.query.filter_by(id=address_id).first()
    num_items_in_cart = len(cart_items)
    for cart_item, item, category in cart_items:
        total_price += item.price * cart_item.quantity
    
    
    return render_template('checkout.html',address=address,cart_items=cart_items,num=num_items_in_cart,total_price=total_price, form=payment_form)



class Discount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(200), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __init__(self, code, amount):
        self.code = code
        self.amount = amount

@app.route('/get_discount/<string:promo_code>/<string:totalAmount>' ,methods=['GET'])
def get_discount(promo_code,totalAmount):
    discount = Discount.query.filter_by(code=promo_code).first()
    
    if discount and discount.amount > 0:
        if int(totalAmount) >= 150:
            return jsonify({'success': True, 'amount': discount.amount})
        else:
            return jsonify({'success': False, 'message': "Minimum Amount of Purchase to avail this discount should be ₹150"})
        # return jsonify({'success': True, 'amount': discount.amount})
    else:
        return jsonify({'success': False, 'message': 'Invalid Discount Code'})


    
def get_user_orders(user_id):
    orders = Placed_orders.query.filter_by(user_id=user_id).all()
    return orders

def get_user_details(username):
    user = Users.query.filter_by(username=username).first()
    return user

@app.route("/<username>/user_profile")
@login_required
@user_profile_access_required
def user_profile(username):
    user = get_user_details(username)
    orders = get_user_orders(user.id)
    return render_template("user_profile.html", user=user, orders=orders, username=username)


class User_buy(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('placed_orders.order_id'),nullable=False)
    category_name = db.Column(db.String(200), nullable=False)
    item_name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    

    

class Placed_orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True ,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.now(indian_timezone))
    total_price = db.Column(db.Float, nullable=False)
    mode_of_payment=db.Column(db.String(200),nullable=False)
    address=db.Column(db.String(200),nullable=False)
    promoCode=db.Column(db.String(200))

    def __repr__(self):
        return f'<Placed_Orders order_id={self.order_id} user_id={self.user_id} order_date={self.order_date} total_price={self.total_price}>'
    
class PaymentForm(FlaskForm):
    addressId = StringField('AddressId')
    totalAmount = IntegerField('totalAmount')
    mode_of_payment =StringField ('mode_of_Payment')
    promo_code = StringField('promo_code')
    submit = SubmitField('Pay Now')    

@app.route('/placed_order', methods=['POST'])
def placed_order():
    
    try:
        # Retrieve form data
       
        payment_method = request.form.get('mode_of_payment')
        total_amount = int(request.form.get('totalAmount'))
        address_id = int(request.form.get('addressId'))
        address = User_address.query.get(address_id)
        promoCode=request.form.get('promo_code')

        # Step 1: Create the Order
        new_order = Placed_orders(user_id=current_user.id, order_date=datetime.now(indian_timezone), total_price=total_amount, mode_of_payment=payment_method, address=address.delivery_address,promoCode=promoCode)
        db.session.add(new_order)
        db.session.commit()
        
        # Step 2: Retrieve Cart Items
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        # Update the Order_items table and subtract the ordered quantity
        for cart_item in cart_items:
            item = Order_items.query.filter_by(id=cart_item.item_id).first()

            category = Category.query.filter_by(category_id=item.category_id).first()
            user_buyer = User_buy(
                order_id=new_order.order_id,
                category_name=category.category_name,
                item_name=item.name,
                quantity=cart_item.quantity,
                price=item.price
            )
           
            db.session.add(user_buyer)
            db.session.commit()

            item.quantity -= cart_item.quantity
            db.session.delete(cart_item)
            db.session.commit()

            order_id = new_order.order_id
            user_email=Users.query.filter_by(id=current_user.id).first().email

        send_order_details_email(user_email,order_id)
        print("User Email:", user_email)    
        # send_order_details_email(user_email,order_id)
        flash("Order Placed Successfully! Arriving in 20mins")
        # Redirect to the shop.html page upon successful order placement
        return redirect(url_for('shop'))

    except Exception as e:
        # Handle any exceptions
        print(e)
        # Redirect to an error page or display an error message
        return redirect(url_for('error_page'))
    


def send_order_details_email(email_receiver, order_id):
    print("Entered")
    try:
        subject = "Your Organick Order #ORD" +str(order_id)  +" was successfully delivered!"
        order = Placed_orders.query.get(order_id)

        # Fetch items for the order
        items = User_buy.query.filter_by(order_id=order_id).all()
        
        # Convert data to JSON
        MRP=0
        discountCode=order.promoCode
        print(discountCode)
        if len(discountCode)!=0:
            discountValue=Discount.query.filter_by(code=discountCode).first().amount
        else:
            discountValue=''    
        print(order)
        items_str=""
        for item in items:
            MRP+=item.quantity*item.price
            items_str+=item.item_name+", "
        items_str= items_str[:-2]
        
        
        order_info = {
            'order_id': order.order_id,
            'total_price': order.total_price,
            'MRP':MRP,
            'paymentMode':order.mode_of_payment,
            'Address':order.address,
            'discountCode':discountCode,
            'discountValue':discountValue,
            'formatted_order_date': order.order_date.strftime("%A, %d %b'%y, %I:%M%p"),
            'items_str': items_str,
            'items': [{'item_name': item.item_name, 'item_price': item.price,'item_quantity':item.quantity} for item in items],
        }


        

        # Calculate the length of the items list
        items_length = len(order_info['items'])
        no_of_items = 'item' if items_length == 1 else 'items'

        

        with app.app_context():
            rendered_html = render_template('send-email.html', order_info=order_info, items_length=items_length,no_of_items=no_of_items)
        em = EmailMessage()
        em['From'] = 'organick.groc@gmail.com'  # Update with your email address
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(rendered_html, subtype='html')

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()  # Start TLS encryption
            smtp.login('organick.groc@gmail.com', 'xkfk iglo sddh zabh')  # Update with your email and password
            smtp.sendmail('organick.groc@gmail.com', email_receiver, em.as_string())

    except Exception as e:
        # Print error details
        print(f"An error occurred: {e}")
       


@app.route('/error_page',methods=['GET'])
def error_page():
    return render_template('404.html')

@app.route('/user_orders',methods=['GET'])
def user_orders():
    orders = Placed_orders.query.filter_by(user_id=current_user.id).order_by(desc(Placed_orders.order_date)).all()
    for order in orders:
        order.formatted_order_date = order.order_date.strftime("%A, %d %b'%y, %I:%M%p")

    return render_template('user_orders.html',orders=orders)


@app.route('/order_details/<int:order_id>')
def order_details(order_id):
    try:
        order = Placed_orders.query.get(order_id)

        # Fetch items for the order
        items = User_buy.query.filter_by(order_id=order_id).all()
        for item in items:
            item.image_url = f'/static/images/items/{item.item_name.replace(" ", "_")}.png'
            order_item=Order_items.query.filter_by(name=item.item_name).first()
            item.unit=order_item.unit.split('/')[1]
            if(item.unit=='kg'):
                item.unit='1Kg'
            elif(item.unit=='L'):
                item.unit='1L' 

            elif(item.unit=='unit'):
                item.unit='1unit' 

        # Convert data to JSON
        MRP=0
        discountCode=order.promoCode
        print(discountCode)
        if len(discountCode)!=0:
            discountValue=Discount.query.filter_by(code=discountCode).first().amount
        else:
            discountValue=' - '    
        print(order)
        for item in items:
            MRP+=item.quantity*item.price
        data = {
            'order_id': order.order_id,
            'total_price': order.total_price,
            'MRP':MRP,
            'paymentMode':order.mode_of_payment,
            'Address':order.address,
            'discountCode':discountCode,
            'discountValue':discountValue,
            'formatted_order_date': order.order_date.strftime("%A, %d %b'%y, %I:%M%p"),
            'items': [{'item_name': item.item_name, 'item_price': item.price,'item_quantity':item.quantity,'img_url':item.image_url,'unit':item.unit} for item in items]
        }

        return jsonify(data)
    except Exception as e:
        print(f"Error in order_details route: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500
    


@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        # Get form data
        full_name = request.form['full_name']
        user_email = request.form['user_email']
        company = request.form['company']
        subject = request.form['subject']
        message = request.form['message']

        # Set up the email content
        sender_email = user_email# Replace with your email address
        receiver_email = "organick.groc@gmail.com"
        email_subject = f"New Inquiry - {subject}"

        email_body = f"Full Name: {full_name}\nEmail: {user_email}\nCompany: {company}\n\nMessage:\n{message}"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = email_subject
        msg.attach(MIMEText(email_body, 'plain'))

        print(email_subject," sending OTP * ")

        # Set up the SMTP server and send the email
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, 'your_password')  # Use your 'App Password' for Gmail
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            flash("Feedback sent successfully!")
            redirect(url_for('home'))
        except Exception as e:
            return f"Error sending email: {str(e)}"




# #create Logout page
@app.route('/user_logout',methods=['GET','POST'])
@login_required

def user_logout():
    logout_user()
    session['is_user']=False
    session.clear()
    flash("You have been Logged Out!  Thanks for Stopping By...")
    return redirect(url_for('shop'))

#####################################################################################################################################

def manager_access_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        
        is_manager = session.get('is_manager', False)
        
        # Check if the current user is authenticated and matches the target user
        
        if  is_manager:
            return func(*args, **kwargs)  # User is authorized, proceed with the view
        else:
            abort(403)  # 403 Forbidden status code for unauthorized access

    return decorated_view

def is_manager(username):
    manager = Managers.query.filter_by(username=username).first()
    return manager is not None


class Managers(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(200),nullable=False,unique=True)
    password_hash=db.Column(db.String(200),nullable=False)
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    def __repr__(self):
        return '<Name %r>' %self.name



class ManagerForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired()])
    password_hash=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField("Login")


# login_manager.login_view='manager'

# @login_manager.user_loader
# def load_user(id):
#     # Replace this with your logic to retrieve the user based on user_id
#     return Managers.query.get(int(id))

@app.route('/manager_login', methods=['GET', 'POST'])
def manager():
    form = ManagerForm()
    if form.validate_on_submit():
        user = Managers.query.filter_by(username=form.username.data).first()
        if user:
            if user.password_hash == form.password_hash.data:
                login_user(user)# Creates the session
                session['is_manager']=True
                return redirect(url_for('manager_dashboard',name=form.username.data))
            else:
                flash('Wrong Password - Try Again!!')
        else:
            flash("That manager doesn't exist! Try Again...")
    return render_template('manager_login.html', form=form)


@app.route("/<name>/manager_dashboard", methods=["GET","POST"])
@manager_access_required
def manager_dashboard(name):
    
    if is_manager(name):
        categories = Category.query.all()
        csrf_token = generate_csrf()
        # Create a dictionary to store items for each category
        category_items_dict = {}
        for category in categories:
            # Fetch items associated with the current category
            items = Order_items.query.filter_by(category_id=category.category_id).all()
            category_items_dict[category.category_id] = items
        
        return render_template("manager_dashboard.html", categories=categories, category_items_dict=category_items_dict, name=name, csrf_token=csrf_token)
    else:
        abort(403)


@app.route('/<name>/summary')
@manager_access_required
def summary(name):
    if is_manager(name):
        categories = Category.query.all()
        user_buys = User_buy.query.all()

        # Process data for the first graph (category-wise utilization)
        category_utilization = {category.category_name: 0 for category in categories}

        for buy in user_buys:
            if buy.category_name in category_utilization:
                category_utilization[buy.category_name] += buy.quantity
            else:
                category_utilization[buy.category_name] = buy.quantity

        # Process data for the second graph (range of products bought in the present week)
        current_week = datetime.now().isocalendar()[1]
        price_ranges = [0, 10, 20, 30, 40, 50, 100, 200, 500, 1000]
        products_in_ranges = [0] * (len(price_ranges) - 1)
        for buy in user_buys:
            for i in range(len(price_ranges) - 1):
                if price_ranges[i] < buy.price <= price_ranges[i + 1]:
                    products_in_ranges[i] += 1
                    break

        # Plot the first graph (category-wise utilization)
        plt.figure(figsize=(10, 7))
        bar_width = 0.5
        plt.bar(category_utilization.keys(), category_utilization.values(), width=bar_width)
        plt.xlabel('Category', fontsize=12)
        plt.ylabel('Total Quantity', fontsize=12)
        plt.title('Category-wise Utilization', fontsize=14)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()
        plt.savefig('./static/images/category_utilization.png')
        plt.close()

        # Plot the second graph (summary of items purchased)
        data = db.session.query(User_buy.item_name, db.func.sum(User_buy.quantity)).group_by(User_buy.item_name).all()
        item_names, quantities = zip(*data) if data else ([], [])

        plt.figure(figsize=(10, 8))
        bar_height = 0.5
        plt.barh(item_names, quantities, height=bar_height)
        plt.ylabel("Item Name", fontsize=12)
        plt.xlabel("Quantity Purchased", fontsize=12)
        plt.title("Summary of Items Purchased", fontsize=14)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()
        plt.savefig('./static/images/summary.png')
        plt.close()

        out_of_stock = [item.name for item in Order_items.query.all() if item.quantity == 0]

        return render_template('summary.html', name=name, out_of_stock=out_of_stock)
    else:
        abort(403)

        
@app.route('/logout',methods=['GET','POST'])

def logout():
    logout_user()
    session['is_manager']=False
    flash("You have been Logged Out!  Thanks for Stopping By...")
    return redirect(url_for('manager'))

class Category(db.Model):
    category_id=db.Column(db.Integer,primary_key=True)
    category_name=db.Column(db.String(200),nullable=False,unique=True)

class CreateCategoryForm(FlaskForm):
    category_name = StringField('Category Name : ', validators=[DataRequired()])
    submit = SubmitField('Save')    

@app.route('/<name>/create_category',methods=["GET","POST"])

def create_category(name):
    if is_manager(name):
        form = CreateCategoryForm()

        if form.validate_on_submit():
            

            # Check if the manager is authorized to create a category (you'll need to implement this logic)
            # For simplicity, let's assume any logged-in user is considered a manager
            # You can enhance this by using Flask-Login or any other authentication mechanism.
            # if current_user.is_authenticated:
            # Create the category object
            existing_category = Category.query.filter_by(category_name=form.category_name.data).first()
            if existing_category:
                flash('A category with the same name already exists.', 'danger')
            else:
                # Create the category object
                new_category = Category(category_name=form.category_name.data)
                db.session.add(new_category)
                # Add the category to the database
                flash('Category created successfully!', 'success')
                db.session.commit()
                return redirect(url_for('manager_dashboard',name=name))  # Redirect to the home page or any other page
            

                
            # else:
            #     flash('You are not authorized to create a category.', 'danger')
        category_name = form.category_name.data
        form.category_name.data=''
        return render_template('create_category.html', category_name=category_name,form=form,name=name)
    else:
        abort(403)


#for items class
class Order_items(db.Model):
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(200), nullable=False,unique=True)
    unit=db.Column(db.String(20), nullable=False)
    MFD=db.Column(db.DateTime,default=datetime.now(indian_timezone))


class CreateItemForm(FlaskForm):
    product_name = StringField('Product Name :', validators=[DataRequired()])
    unit = SelectField('Unit :', choices=[('Rs/kg', 'Rs/kg'), ('Rs/L', 'Rs/L'), ('Rs/dozen', 'Rs/dozen'), ('Rs/500 gram', 'Rs/500 gram'),('Rs/unit','Rs/unit'),('Rs/500 ml','Rs/500 ml')], validators=[DataRequired()])
    rate_per_unit = FloatField('Rate/Unit :', validators=[DataRequired()])
    quantity = IntegerField('Quantity :', validators=[DataRequired(), NumberRange(min=0)])
    save_button = SubmitField('Save')


@app.route("/<name>/create_item/<int:category_id>", methods=["GET", "POST"])
@manager_access_required
def create_item(name,category_id):
    if is_manager(name):
        form = CreateItemForm()

        if form.is_submitted():
                # Get the form data
            product_name = form.product_name.data
            unit = form.unit.data
            rate_per_unit = form.rate_per_unit.data
            quantity = form.quantity.data

            # Create an entry in the OrderItem table or perform other actions as needed
            # For example:
            existing_item = Order_items.query.filter_by(name=product_name).first()
            if existing_item:
                flash(f'The product "{product_name}" already exists in the order_items table!', 'failure')
            else:    
                order_item = Order_items(name=product_name, unit=unit, price=rate_per_unit, quantity=quantity, category_id=category_id)
                # Save the order_item to the database (assuming OrderItem is your SQLAlchemy model)
                db.session.add(order_item)
                db.session.commit()

                # Redirect to the manager dashboard or any other page as needed
                return redirect(url_for('manager_dashboard',name=name))

        return render_template("create_item.html", form=form,name=name)
    else:
        abort(403)

class EditItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    unit = SelectField('Unit :', choices=[('Rs/kg', 'Rs/kg'), ('Rs/L', 'Rs/L'), ('Rs/dozen', 'Rs/dozen'), ('Rs/500 gram', 'Rs/500 gram'),('Rs/unit','Rs/unit'),('Rs/500ml','Rs/500ml')], validators=[DataRequired()])
    category_id = IntegerField('Category ID', validators=[DataRequired()])

@app.route("/<name>/edit_item/<int:item_id>", methods=["GET", "POST"])
@manager_access_required
def edit_item(name,item_id):
    if is_manager(name):
        item = Order_items.query.get_or_404(item_id)
        form = EditItemForm(obj=item)
        
        if form.validate_on_submit():
            form.populate_obj(item)
            db.session.commit()
            return redirect(url_for('manager_dashboard',name=name))

        return render_template("edit_item.html", form=form,name=name)

        # Route to delete an item

    else:
        abort(403)
    
@app.route("/<name>/delete_item/<int:item_id>", methods=["GET","POST"])
@manager_access_required
def delete_item(name, item_id):
    if is_manager(name):
        item = Order_items.query.get(item_id)
        if not item:
            flash("Item not found.", "error")
            return redirect(url_for("manager_dashboard", name=name))

        try:
            db.session.delete(item)
            db.session.commit()
            flash("Item deleted successfully.", "success")
            return redirect(url_for("manager_dashboard", name=name))
        except Exception as e:
            db.session.rollback()
            flash("Error deleting item.", "error")
            return redirect(url_for("manager_dashboard", name=name))
        
    else:
        abort(403)




#now category

class EditCategoryForm(FlaskForm):
    category_name = StringField('Category Name', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Save')

@app.route("/<name>/edit_category/<int:category_id>", methods=["GET", "POST"])
@manager_access_required
def edit_category(name,category_id):

    if is_manager(name):
        category = Category.query.get_or_404(category_id)
        form = EditCategoryForm()
        old_name=category.category_name
        if request.method == "POST" and form.validate_on_submit():
            new_category_name = form.category_name.data
            
            # Check if the new category name collides with any existing category name
            if category.category_name != new_category_name and db.session.query(exists().where(Category.category_name == new_category_name)).scalar():
                flash("A category with the same name already exists.", "danger")
            else:

                category.category_name = new_category_name
                db.session.commit()
                flash("Category name updated successfully!", "success")
                return redirect(url_for("manager_dashboard",name=name))

        return render_template("edit_category.html", form=form,name=name,category_name=old_name)
    else:
        abort(403)


@app.route("/<name>/delete_category/<int:category_id>", methods=["GET","POST"])
@manager_access_required
def delete_category(name,category_id):
    # Fetch the category to delete
    if is_manager(name):
        category = Category.query.get(category_id)
        print(category_id)
        if not category:
            flash("Category not found.", "error")
            return redirect(url_for("manager_dashboard",name=name))

        try:
            # Delete the items associated with the category
            Order_items.query.filter_by(category_id=category_id).delete()

            # Delete the category
            db.session.delete(category)
            db.session.commit()

            flash("Category  and it's associated Items deleted successfully.", "success")
            return redirect(url_for("manager_dashboard",name=name))
        except Exception as e:
            db.session.rollback()
            flash("Error deleting category and items.", "error")
            return redirect(url_for("manager_dashboard",name=name))
    else:
        abort(403)



# app.run(debug=True)

# Set the port from the environment variable, default to 10000

port = int(os.environ.get('PORT', 10000))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)