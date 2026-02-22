from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User, db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('login4.html')

@main.route('/dashboard')
def dashboard():
    return render_template('dashboard4.html')

@main.route('/admin')
def admin():
    return render_template('admin.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Registration logic here
        flash('Registration successful!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register4.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Login logic here
        flash('Login successful!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('login4.html')