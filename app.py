from flask import Flask, request, redirect, url_for, render_template
import os
from datetime import datetime

app = Flask(__name__)

# Main folder where all reports are stored
BASE_REPORTS_FOLDER = "Crime Reports"

# Ensure the main "Crime Reports" folder exists
if not os.path.exists(BASE_REPORTS_FOLDER):
    os.makedirs(BASE_REPORTS_FOLDER)

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Retrieve form data
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        phonenumber = request.form.get('phonenumber')
        crimetype = request.form.get('crimetype')
        description = request.form.get('description')
        uploaded_file = request.files['uploadedphoto']

        # Create a new folder named with current date and time
        report_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Format: YYYY-MM-DD_HH-MM-SS
        report_folder = os.path.join(BASE_REPORTS_FOLDER, f"Report_{report_time}")
        os.makedirs(report_folder)  # Create a new folder for this report

        # Save uploaded file inside the report folder
        file_path = "No file uploaded"
        if uploaded_file and uploaded_file.filename:
            file_path = os.path.join(report_folder, uploaded_file.filename)
            uploaded_file.save(file_path)

        # Save form data as a text file inside the same folder
        report_data = f"""
        --- Crime Report ---
        Submitted at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        First Name: {firstname}
        Last Name: {lastname}
        Email: {email}
        Phone Number: {phonenumber}
        Crime Type: {crimetype}
        Description: {description}
        Uploaded File: {uploaded_file.filename if uploaded_file.filename else 'None'}
        ----------------------------
        """
        report_text_file = os.path.join(report_folder, "report.txt")
        with open(report_text_file, "w") as file:
            file.write(report_data)

        # Redirect to the thankyou.html page
        return redirect(url_for('thank_you'))

# Route to serve your custom thankyou.html
@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')

# Vercel handler for the serverless function
def handler(event, context):
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    return app
