from flask import Flask, request, jsonify
import pandas as pd
from create_sheet import main
from mail import mail_it
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

def generate_excel_sheet():
    # Call the main function to generate the Excel sheet
    excel_sheet_path = main()
    return excel_sheet_path

@app.route('/api/generate-excel', methods=['POST'])
def generate_excel():
    excel_sheet_path = generate_excel_sheet()
    print(excel_sheet_path)
    # Return the path or URL of the generated Excel sheet
    return jsonify({'sheetUrl': str(excel_sheet_path)})
    
    
@app.route('/api/send-mail', methods=['POST'])
def send_mail():
    # Get the data from the request
    data = request.get_json()
    # Get the email address from the data
    email = data['email']
    excel_sheet_path = data['path']
    # Send the mail
    print(email)
    print(excel_sheet_path)
    mail_it(email, excel_sheet_path)
    # Return the success message
    return jsonify({'message': 'Mail sent successfully!'})



if __name__ == '__main__':
    app.run()
