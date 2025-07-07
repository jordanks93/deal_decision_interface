from flask import Flask, request, render_template, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets setup
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Credit Decisions").sheet1  # Ensure this sheet name matches yours

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = [
        request.form['date'],
        request.form['customer_name'],
        request.form['vendor_location'],
        request.form['salesperson'], # do we need this?
        request.form['lease_rep'],
        request.form['finance_type'],
        request.form['vehicle_type'],
        request.form['vehicle_year'],
        request.form['vehicle_make'],
        request.form['vehicle_model'],
        request.form['sale_price'],
        request.form['term'],
        request.form['rate'],
        request.form['down_payment'],
        request.form['security_deposit'], # do we need this?
        request.form['residual_value'], # do we need this?
        request.form['payment'],
        request.form['cost_of_funds'],
        request.form['credit_decision'],
        request.form['notes']
    ]
    sheet.append_row(data)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)