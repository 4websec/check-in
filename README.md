# General Flask Idea


## models.py

```python
# user model exmaple:

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    ivr_code = db.Column(db.String(20), nullable=False)
	
	def __repr__(self):
    return f'<User {self.username}>'
	
```

## signup.py
```python
# signup.py form (maybe move phone, last_name, ivr_code to user settings)

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    phone = StringField('Phone Number', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    ivr_code = StringField('PIN', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

```


```sql
-- schema.sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    phone TEXT NOT NULL,
    last_name TEXT NOT NULL,
    ivr_code TEXT NOT NULL
);
```



* * *

## Revised 'app.py':

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
		# may want to 
    phone = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    ivr_code = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
```



```python

# app.py example

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
# from your_project.models import User, db
# from your_project.forms import LoginForm, SignupForm, ContactForm, ProfileForm

app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///path/to/dailycomply.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance and initialize it with the app
db = SQLAlchemy(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Secret key for session management and CSRF protection
app.secret_key = '9278f9a09c156eacc18f2123037924a6' # <- example

@login_manager.user_loader
def load_user(user_id):
    # Replace with your method of getting a user by ID
    return User.query.get(int(user_id))

@app.teardown_appcontext
def teardown_appcontext(exception=None):
    db.session.remove()

# Define your routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        # Signup logic
        pass  # Replace with your signup logic
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Login logic
        pass  # Replace with your login logic
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        # Profile update logic
        pass  # Replace with your profile update logic
    return render_template('profile.html', form=form)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Contact form logic
        pass  # Replace with your contact form logic
    return render_template('contact.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
```

