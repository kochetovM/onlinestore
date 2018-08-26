from app import app, db
import os
from flask import render_template, redirect, url_for, session, flash, request
from app.forms import RegistrationForm, LoginForm, ProfileForm, ProductForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User
from werkzeug.urls import url_parse
import time
from app.models import Product
import stripe
from app.stripe_info import stripe_keys

@app.route('/')
@app.route('/index', methods=('GET', 'POST'))
def index(): 
    #print(os.getenv('STRIPE_PUBLISHABLE_KEY'))
    # print(os.getenv('STRIPE_SECRET_KEY'))
    products = Product.query.all()
    return render_template('index.html', products=products)
  
@app.route('/404')
def eror404():
    return render_template('404.html')

@app.route('/emptycart')
def emptycart():
    return render_template('emptycart.html')

@app.route('/cart')
def cart():
  if "cart" not in session or not session["cart"]:
    return redirect(url_for('emptycart'))
  items = session["cart"]
  dict_of_items = {}
  totalPrice = 0
  for item in items:
        product = Product.query.get(item)
        totalPrice+=product.price
        if product.id in dict_of_items:
            dict_of_items[product.id]["qty"] += 1
        else:
            dict_of_items[product.id] = {
                "id": product.id,
                "image": product.image,
                "name": product.name,
                "qty": 1,
                "price": product.price
            }
  session["paymentTotal"] = totalPrice
  session["shopping_cart"] = dict_of_items
  context = {
    'title': 'Shopping Cart',
    'display_cart': dict_of_items,
    'total': totalPrice,
    'key': stripe_keys['publishable_key']
  }
  return render_template('cart.html', **context)


@app.route('/charge', methods=['POST'])
def charge():
  amount = session["paymentTotal"]  
  stripe.api_key = "sk_test_s8zCASFgKidV07WleXsXxrzj"
#   customer = stripe.Customer.create(
#     description="Customer for jenny.rosen@example.com",
#     source=request.form[stripe_token]
#   )

  charge = stripe.Charge.create(
    #customer=customer.id,
    amount=int(amount),
    currency='usd',
    source="tok_visa",
    description='This is a test charge with Flask'
  )
  session['chargeAmount'] = int(amount)
  return redirect(url_for('thanks'))


@app.route('/thanks')
def thanks():
  context = {
    'amount': session['chargeAmount']
  }
  return render_template('thanks.html', **context)

@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
  if "cart" not in session:
    session["cart"] = []
  session["cart"].append(id)
  flash("Item added to cart")
  product = Product.query.get(id)
  return render_template('single.html', product=product)
  

@app.route('/remove_item/<int:id>')
def remove_item(id):
  session["cart"].remove(id)
  flash("Item removed from cart")
  return redirect(url_for('cart'))

@app.route('/clear_cart')
def clear_cart():
  session["cart"].clear()
  flash("All items removed from cart")
  return redirect(url_for('cart'))




@app.route('/single/<int:id>')
def single(id):
    product = Product.query.get(id)
    return render_template('single.html', product=product)

    
@app.route('/products', methods=('GET', 'POST'))
def products():
    products = Product.query.all()
    return render_template('products.html',products=products)

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form=LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user is None or not user.check_password(form.password.data):
      flash("The email or password did not match. Try again!")
      return redirect(url_for('index'))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('index')
    return redirect(next_page)
  return render_template('login.html', form=form)

@app.route('/logout')
def logout():
  logout_user()
  flash("You are logged out!")
  return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form=RegistrationForm()
  if form.validate_on_submit() and form.validate_email_username(form.email.data,form.username.data) :
    user = User(email=form.email.data,username=form.username.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash("You are now registered")
    return redirect(url_for('login'))
  return render_template('register.html', form=form)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    context = { 
        'form': ProductForm()
    }
    form = ProductForm()
    if form.validate_on_submit():
        filename = time.strftime("%Y%m%d%H%M%S") + '.png'
        new_product = Product(name=form.name.data, image=filename, price=form.price.data, inventory=form.inventory.data,pr_type=form.pr_type.data, description=form.description.data)
        file = request.files['image']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db.session.add(new_product)
        db.session.commit()
        flash("Added new product to database")
        return redirect(url_for('admin'))
    return render_template('admin.html', **context)

@app.route('/delete_user/<int:id>')
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin'))