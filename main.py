from flask import Flask, render_template, request, redirect, url_for, flash
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

DATA_FILE = "data.json"

# Load data from JSON
try:
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {"transactions": []}

# Save data to JSON
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@app.route('/')
def index():
    total_income = sum(item['amount'] for item in data['transactions'] if item['type'] == 'income')
    total_expenses = sum(item['amount'] for item in data['transactions'] if item['type'] == 'expense')
    balance = total_income - total_expenses
    return render_template('index.html', data=data, balance=balance)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    try:
        description = request.form['description']
        amount = float(request.form['amount'])
        transaction_type = request.form['type']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['transactions'].append({
            "description": description,
            "amount": amount,
            "type": transaction_type,
            "timestamp": timestamp
        })
        save_data()
        flash(f"{transaction_type.capitalize()} added successfully!", "success")
    except ValueError:
        flash("Invalid amount entered.", "error")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
