from flask import Flask, request, render_template, redirect, flash
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Google Sheets setup
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
client = gspread.authorize(creds)
main_sheet = client.open("Credit Decisions").worksheet("Main")
loc_sheet = client.open("Credit Decisions").worksheet("LOC")

def validate_fields(form, required_fields):
    errors = []
    for field in required_fields:
        if not form.get(field):
            errors.append(f"{field.replace('_', ' ').title()} is required.")
    return errors

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return None
    except (ValueError, KeyError):
        return "Invalid date format."

def validate_number_fields(form, fields):
    errors = []
    for field in fields:
        try:
            float(form[field])
        except (ValueError, KeyError):
            errors.append(f"{field.replace('_', ' ').title()} must be a number.")
    return errors

def validate_vehicle_year(vehicle_year):
    if vehicle_year == "Real Estate":
        return None
    try:
        year = int(vehicle_year)
        if year < 2000 or year > 2026:
            return "Vehicle Year must be between 2000 and 2026, or 'Real Estate'."
    except (ValueError, KeyError):
        return "Vehicle Year must be a valid year or 'Real Estate'."
    return None

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    required_fields = [
        'date', 'customer_name', 'vendor_location', 'lease_rep', 'finance_type',
        'vehicle_type', 'vehicle_year', 'vehicle_make', 'vehicle_model',
        'sale_price', 'term', 'rate', 'down_payment', 'cost_of_funds',
        'credit_grade', 'credit_decision'
    ]
    errors = validate_fields(request.form, required_fields)
    date_error = validate_date(request.form.get('date', ''))
    if date_error:
        errors.append(date_error)
    errors += validate_number_fields(request.form, ['sale_price', 'term', 'rate', 'down_payment', 'cost_of_funds'])
    year_error = validate_vehicle_year(request.form.get('vehicle_year', ''))
    if year_error:
        errors.append(year_error)

    if errors:
        for error in errors:
            flash(error)
        return render_template('form.html')

    try:
        sale_price = float(request.form['sale_price'])
        sale_price_formatted = "${:,.2f}".format(sale_price)
    except (ValueError, KeyError):
        sale_price_formatted = request.form.get('sale_price', '')

    data = [
        request.form['date'],
        request.form['customer_name'],
        request.form['vendor_location'],
        request.form['lease_rep'],
        request.form['finance_type'],
        request.form['vehicle_type'],
        request.form['vehicle_year'],
        request.form['vehicle_make'],
        request.form['vehicle_model'],
        sale_price_formatted,
        request.form['term'],
        float(request.form['rate']) / 100,
        float(request.form['down_payment']) / 100,
        request.form['cost_of_funds'],
        request.form['credit_grade'],
        request.form['credit_decision'],
        request.form.get('notes', '')
    ]
    main_sheet.append_row(data)
    flash("Submission successful!")
    return redirect('/')

@app.route('/submit_loc', methods=['POST'])
def submit_loc():
    required_fields = ['date', 'customer_name', 'lease_rep', 'amount']
    errors = validate_fields(request.form, required_fields)
    date_error = validate_date(request.form.get('date', ''))
    if date_error:
        errors.append(date_error)
    try:
        amount = float(request.form['amount'])
        amount_formatted = "${:,.2f}".format(amount)
    except (ValueError, KeyError):
        errors.append("Amount must be a number.")
        amount_formatted = request.form.get('amount', '')

    if errors:
        for error in errors:
            flash(error)
        return render_template('form.html')

    loc_data = [
        request.form['date'],
        request.form['customer_name'],
        request.form['lease_rep'],
        amount_formatted,
        request.form.get('notes', '')
    ]
    loc_sheet.append_row(loc_data)
    flash("LOC submission successful!")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)