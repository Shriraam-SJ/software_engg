import os
import urllib.parse
from flask import Flask, request, redirect, url_for, session, render_template, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from backend.operations import add_user, authenticate_user, update_balance, get_balance, get_transaction_history, change_password, change_mpin

# MongoDB connection setup
username = "shriraamsj21"
password = "Sharan@123"
encoded_password = urllib.parse.quote_plus(password)

uri = f"mongodb+srv://{username}:{encoded_password}@cluster21.jhxmf.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.get_database('banking_system')
users_collection = db['users']

app = Flask(__name__)

# Generate and set the secret key
app.secret_key = os.urandom(24)

# Optionally, set session expiration time
app.permanent_session_lifetime = timedelta(days=1)

# Index route (Home page)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/adduser', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_id = request.form['user_id']
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        mtpin = request.form['mtpin']  # Store the mtpin instead of balance

        # Check if the user already exists
        if db.users.find_one({"user_id": user_id}):
            flash("User ID already exists.", "danger")
        else:
            # Insert the new user with mtpin as the initial value
            db.users.insert_one({
                "user_id": user_id,
                "username": username,
                "password": password,
                "mtpin": mtpin,  # Store mtpin as entered
                "balance":0
            })
            flash("User added successfully!", "success")
        return redirect(url_for('add_user'))

    return render_template('adduser.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        user = db.users.find_one({"user_id": user_id})
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user_id
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))  # Redirects to the dashboard after successful login
        else:
            flash("Invalid credentials. Please try again.", "danger")

    return render_template('login.html')

# Dashboard route (After login)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    balance = get_balance(session['user_id'])
    return render_template('dashboard.html', balance=balance)


@app.route('/credit_page', methods=['GET'])
def credit_page():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    return render_template('credit.html')

@app.route('/debit_page', methods=['GET'])
def debit_page():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    return render_template('debit.html')

@app.route('/netbanking_page', methods=['GET'])
def netbanking_page():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    return render_template('netbanking.html')  # Render the form for Net Banking

@app.route('/upi_page', methods=['GET'])
def upi_page():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    return render_template('upi.html')  # Render the form for UPI transaction

@app.route('/change_password_page', methods=['GET'])
def change_password_page():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    return render_template('change_password.html')  # Render the change password form
@app.route('/transaction_history_page', methods=['GET'])
def transaction_history_page():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    history = get_transaction_history(session['user_id'])
    return render_template('transaction_history.html', history=history)  # Render the transaction history

@app.route('/credit', methods=['POST'])
def credit():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    try:
        amount = float(request.form['amount'])
    except (ValueError, KeyError):
        flash("Invalid amount.", "danger")
        return redirect(url_for('credit_page'))

    success, message = update_balance(session['user_id'], amount, 'credit')
    flash(message, "success" if success else "danger")
    return redirect(url_for('dashboard'))

@app.route('/debit', methods=['POST'])
def debit():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    try:
        amount = float(request.form['amount'])
    except (ValueError, KeyError):
        flash("Invalid amount.", "danger")
        return redirect(url_for('debit_page'))

    success, message = update_balance(session['user_id'], amount, 'debit')
    flash(message, "success" if success else "danger")
    return redirect(url_for('dashboard'))

@app.route('/netbanking', methods=['POST'])
def netbanking():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    try:
        amount = float(request.form['amount'])  # Parse the amount
    except (ValueError, KeyError):  # Handle invalid input
        flash("Invalid amount entered.", "danger")
        return redirect(url_for('netbanking_page'))  # Redirect back to the form

    success, message = update_balance(session['user_id'], amount, 'net_banking')  # Call your function to process the balance
    flash(message, "success" if success else "danger")
    return redirect(url_for('dashboard'))  # Redirect to the dashboard after transaction

@app.route('/upi', methods=['POST'])
def upi():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    try:
        amount = float(request.form['amount'])  # Parse the amount
    except (ValueError, KeyError):  # Handle invalid input
        flash("Invalid amount entered.", "danger")
        return redirect(url_for('upi_page'))  # Redirect back to the form

    success, message = update_balance(session['user_id'], amount, 'upi')  # Call your function to process the balance
    flash(message, "success" if success else "danger")
    return redirect(url_for('dashboard'))  # Redirect to the dashboard after transaction

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    old_password = request.form['old_password']
    new_password = request.form['new_password']

    success = change_password(session['user_id'], old_password, generate_password_hash(new_password))
    if success:
        flash("Password changed successfully!", "success")
    else:
        flash("Old password is incorrect.", "danger")

    return redirect(url_for('dashboard'))

# Transaction History route (View past transactions)
@app.route('/transaction_history')
def transaction_history():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    history = get_transaction_history(session['user_id'])
    return render_template('transaction_history.html', history=history)

# Logout route (Log out the current user)
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
