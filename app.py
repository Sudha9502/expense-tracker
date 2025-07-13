from flask import Flask, render_template, redirect, url_for, flash
from extensions import db, login_manager
from models import User
from forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# ✅ Configuration must come BEFORE initializing db
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ Initialize extensions with the app
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

# 🔁 User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- ROUTES (same as before) ---
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Try again.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

from datetime import date
from models import Expense
from forms import ExpenseForm

# @app.route('/dashboard', methods=['GET', 'POST'])
# @login_required
# def dashboard():
#     form = ExpenseForm()
#     if form.validate_on_submit():
#         new_expense = Expense(
#             title=form.title.data,
#             amount=form.amount.data,
#             category=form.category.data,
#             date=form.date.data,
#             user_id=current_user.id
#         )
#         db.session.add(new_expense)
#         db.session.commit()
#         flash('Expense added successfully!', 'success')
#         return redirect(url_for('dashboard'))

#     expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
#     return render_template('dashboard.html', form=form, expenses=expenses, name=current_user.username)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = ExpenseForm()
    if form.validate_on_submit():
        new_expense = Expense(
            title=form.title.data,
            amount=form.amount.data,
            category=form.category.data,
            date=form.date.data,
            user_id=current_user.id
        )
        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added!', 'success')
        return redirect(url_for('dashboard'))

    expenses = Expense.query.filter_by(user_id=current_user.id).all()

    # Group expenses by category
    category_totals = {}
    for expense in expenses:
        category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount

    labels = list(category_totals.keys())
    values = list(category_totals.values())

    return render_template(
        'dashboard.html',
        form=form,
        expenses=expenses,
        name=current_user.username,
        labels=labels,
        values=values
    )


# 🔧 Run the app

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
