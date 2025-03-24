# Importing Packages we Need
from flask import Flask, render_template, request, redirect, url_for, flash, session
import pandas as pd
# import uuid
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# This is how you can simply create users
users = {
    "testuser": "123456",
    "admin": "123456",
    "kenneth": "123456"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # username = request.form['username']
        # password = request.form['password']
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and users[username] == password:
            session['user'] = username
            # 200 response from the API = success
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            # 40x is failure/error
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

# Route for Home Page
@app.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html', username=session['user'])
    else:
        flash('You need to log in first!', 'error')
        return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Route for adding entries
@app.route('/add-entry')
def add_entry():
    if 'user' in session:
        # Placeholder for add entry logic
        return "<h2>Add Entry Page (Coming soon)</h2>"
    else:
        flash('You need to log in first!', 'error')
        return redirect(url_for('login'))

# Route for data summary/graphs
# Summary / Graphs route (stub for future)
@app.route('/summary')
def summary():
    if 'user' in session:
        # Placeholder for summary page
        return "<h2>Summary & Graphs Page (Coming soon)</h2>"
    else:
        flash('You need to log in first!', 'error')
        return redirect(url_for('login'))


# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)