from flask import Flask, render_template, request, redirect, url_for
import os
import json
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# flask run --host=0.0.0.0

app = Flask(__name__)

SAVE_FOLDER = 'registered_users'
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Email config
EMAIL_SENDER = os.environ.get('EMAIL_SENDER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_RECEIVER = os.environ.get('EMAIL_RECEIVER')



# Test print statements
print("Sender:", EMAIL_SENDER)
print("Receiver:", EMAIL_RECEIVER)
print("Password loaded:", bool(EMAIL_PASSWORD))

def send_email(name, phone, selections):
    subject = "New Registration Submitted"
    body = f"""
    A new registration has been submitted:\n
    Name: {name}
    Phone: {phone}
    Selections: {', '.join(selections)}
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        selections = request.form.getlist('options')

        data = {
            'name': name,
            'phone': phone,
            'selections': selections,
            'timestamp': datetime.now().isoformat()
        }

        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}{name.replace(' ', '')}.json"
        # send filename to an email account
        filepath = os.path.join(SAVE_FOLDER, filename)

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
            
        # Send the data via email
        send_email(name, phone, selections)

        return redirect(url_for('register', success='true'))

    # Check if success flag exists in query params
    success = request.args.get('success') == 'true'
    return render_template('register.html', success=success)

if __name__ == '__main__':
    app.run(debug=True)
