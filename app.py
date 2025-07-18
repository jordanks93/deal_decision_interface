from flask import Flask, request, render_template, redirect, flash
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Google Sheets setup
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Credit Decisions").worksheet("Main")  # Ensure this sheet name matches yours

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    required_fields = [
        'date', 'customer_name', 'vendor_location',
        'lease_rep', 'finance_type', 'vehicle_type', 'vehicle_year',
        'vehicle_make', 'vehicle_model', 'sale_price', 'term', 'rate',
        'down_payment', 'cost_of_funds', 'credit_grade', 'credit_decision'
    ]
    errors = []

    # Check required fields
    for field in required_fields:
        if not request.form.get(field):
            errors.append(f"{field.replace('_', ' ').title()} is required.")

    # Validate date
    try:
        datetime.strptime(request.form['date'], '%Y-%m-%d')
    except (ValueError, KeyError):
        errors.append("Invalid date format.")

    # Validate numbers
    number_fields = [ 'sale_price', 'term', 'rate', 'down_payment', 'cost_of_funds']
    for field in number_fields:
        try:
            float(request.form[field])
        except (ValueError, KeyError):
            errors.append(f"{field.replace('_', ' ').title()} must be a number.")

    # Validate vehicle year
    try:
        year = int(request.form['vehicle_year'])
        if year < 2000 or year > 2026:
            errors.append("Vehicle Year must be between 2000 and 2026.")
    except (ValueError, KeyError):
        errors.append("Vehicle Year must be a valid year.")

    if errors:
        for error in errors:
            flash(error)
        return render_template('form.html')

    # Format sale price as $X,XXX.XX
    try:
        sale_price_raw = float(request.form['sale_price'])
        sale_price_formatted = "${:,.2f}".format(sale_price_raw)
    except (ValueError, KeyError):
        sale_price_formatted = request.form['sale_price']  # fallback

    # If all validations pass, save to sheet
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
        sale_price_formatted,  # use formatted price here
        request.form['term'],
        float(request.form['rate']) / 100,  # Convert rate to decimal
        float(request.form['down_payment']) / 100,  # Convert down payment to decimal
        request.form['cost_of_funds'],
        request.form['credit_grade'],
        request.form['credit_decision'],
        request.form.get('notes', '')
    ]
    sheet.append_row(data)
    flash("Submission successful!")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)