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
        request.form['customer_name'],
        request.form['vehicle_make'],
        request.form['vehicle_model'],
        request.form['vehicle_year'],
        request.form['vin'],
        request.form['credit_decision'],
        request.form['credit_limit'],
        request.form['notes']
    ]
    sheet.append_row(data)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)