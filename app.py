#App.py 
from flask import Flask, render_template, redirect, url_for, g, request, session
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm
from functools import wraps

app = Flask(__name__)

#Set the secret key to enable CSRF protection
app.config['SECRET_KEY'] = 'secret_key_for_testing'

#Initialize the CSRFProtect object
csrf = CSRFProtect(app)

#Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) #Binds SQLAlchemy object to the app

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return '<User %r>' % self.username #Return a string representation of the object

# This runs before every request
@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None  # No user logged in
    else:
        # Load the user from the database and set it to g.user
        g.user = User.query.get(user_id)

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login_status", next=request.url))
        return view(*args, **kwargs)
    return wrapped_view

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        user_id = register_form.user_id.data
        password = register_form.password.data
        
        user = User.query.filter_by(username=user_id).first() 
        if user is not None:
            register_form.user_id.errors.append("User ID is already taken, please try another!")
        else:
            new_user = User(username=user_id, email=register_form.email.data, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html', register_form=register_form)    

@app.route('/Login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_id = login_form.user_id.data
        password = login_form.password.data

        # Retrieve the user from the database by username
        user = User.query.filter_by(username=user_id).first()

        if user is None:
            login_form.user_id.errors.append("User ID not found, please try again!")
        elif not check_password_hash(user.password, password):  # Compare the hashed password
            login_form.password.errors.append("Incorrect password, please try again!")
        else:
            session.clear()
            session['user_id'] = user.id
            # Login successful, redirect to the dashboard
            return redirect(url_for('home'))
    
    # Render the login page with the form
    return render_template('login.html', login_form=login_form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)