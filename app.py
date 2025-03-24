# Importing Packages we Need
from flask import Flask, render_template, request, redirect, url_for, flash, session
import pandas as pd
import uuid
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# This is how you can simply create users
users = {
    "testuser": "123456",
    "admin": "123456",
    "kenneth": "123456"
}


# Data setup
DATA_PATH = 'data/'
CSV_FILE = 'transactions.csv'
CSV_FILE_PATH = os.path.join(DATA_PATH, CSV_FILE)

os.makedirs(DATA_PATH, exist_ok=True)

# Load or initialize DataFrame
if os.path.exists(CSV_FILE_PATH):
    df = pd.read_csv(CSV_FILE_PATH)
else:
    df = pd.DataFrame(columns=['UUID', 'Time', 'Amount', 'Transaction Type'])



@app.route('/', methods=['GET', 'POST'])
def index():
    global df
    if 'user' not in session:
        flash('You need to log in first!', 'error')
        print("[DEBUG] Not logged in — redirecting to login.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        print("[DEBUG] POST received at /")

        action_type = request.form.get('action_type', 'add')  # Default is add
        print(f"[DEBUG] action_type = {action_type}")

        if action_type == 'delete':
            uuid_to_delete = request.form.get('uuid_to_delete')
            print(f"[DEBUG] Deletion requested for UUID: {uuid_to_delete}")

            try:
                if os.path.exists(CSV_FILE_PATH):
                    df = pd.read_csv(CSV_FILE_PATH)
                else:
                    df = pd.DataFrame(columns=['UUID', 'Time', 'Amount', 'Transaction Type'])

                if uuid_to_delete in df['UUID'].values:
                    df = df[df['UUID'] != uuid_to_delete]
                    df.to_csv(CSV_FILE_PATH, index=False)
                    print(f"[DEBUG] Deleted UUID: {uuid_to_delete} and updated CSV.")
                    flash(f"Transaction with UUID {uuid_to_delete} deleted.", "success")
                else:
                    print(f"[DEBUG] UUID {uuid_to_delete} not found in DataFrame.")
                    flash("Selected UUID not found.", "error")

            except Exception as e:
                print(f"[ERROR] Exception during deletion: {e}")
                flash(f"Error deleting transaction: {e}", "error")

            return redirect(url_for('index'))

        else:
            # Handle Add Transaction
            try:
                time_str = request.form.get('time')
                amount = request.form.get('amount')
                transaction_type = request.form.get('transaction_type')

                print(f"[DEBUG] Received — Time: {time_str}, Amount: {amount}, Type: {transaction_type}")

                time_obj = datetime.strptime(time_str, '%Y-%m-%d')
                formatted_time = time_obj.strftime('%d/%m/%Y')
                transaction_id = str(uuid.uuid4())

                new_row = {
                    'UUID': transaction_id,
                    'Time': formatted_time,
                    'Amount': f"£{float(amount):.2f}",
                    'Transaction Type': transaction_type
                }
                print(f"[DEBUG] New row: {new_row}")

                if os.path.exists(CSV_FILE_PATH):
                    df = pd.read_csv(CSV_FILE_PATH)
                else:
                    df = pd.DataFrame(columns=['UUID', 'Time', 'Amount', 'Transaction Type'])

                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(CSV_FILE_PATH, index=False)
                print(f"[DEBUG] DataFrame saved to CSV: {CSV_FILE_PATH}")
                flash("Transaction added successfully.", "success")
            except Exception as e:
                print(f"[ERROR] Exception: {e}")
                flash(f"Error adding transaction: {e}", "error")
            return redirect(url_for('index'))

    # GET request: Always re-load the latest CSV here
    print("[DEBUG] GET — loading data from CSV")
    if os.path.exists(CSV_FILE_PATH):
        df = pd.read_csv(CSV_FILE_PATH)
        print(f"[DEBUG] DataFrame loaded from {CSV_FILE_PATH}, rows: {len(df)}")
    else:
        df = pd.DataFrame(columns=['UUID', 'Time', 'Amount', 'Transaction Type'])
        print("[DEBUG] No CSV file found, initialized empty DataFrame")

    return render_template('index.html', username=session['user'], data=df.to_dict(orient='records'))



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
            return redirect(url_for('index'))
        else:
            # 40x is failure/error
            flash('Invalid username or password.', 'error')
    return render_template('login.html')


# @app.route('/home)
# def home():
#     if 'user' not in session:
#         flash('You need to log in first!', 'error')
#         return redirect(url_for('login'))

#     if request.method == 'POST':
#         # handle form logic here
#         # optionally redirect after handling
#         flash("Transaction POST received on /home", "info")
#         return redirect(url_for('home'))

#     return render_template('home.html', username=session['user'])


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

# TO DO Add this in the future
@app.route('/summary')
def summary():
    if 'user' in session:
        # Placeholder for summary page
        return "<h2>Summary & Graphs Page</h2>"
    else:
        flash('You need to log in first!', 'error')
        return redirect(url_for('login'))


# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)