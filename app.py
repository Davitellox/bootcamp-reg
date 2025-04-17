from flask import Flask, render_template, request, redirect, url_for
import os
import json
from datetime import datetime


# flask run --host=0.0.0.0

app = Flask(__name__)

SAVE_FOLDER = 'registered_users'
os.makedirs(SAVE_FOLDER, exist_ok=True)

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
        filepath = os.path.join(SAVE_FOLDER, filename)

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

        return redirect(url_for('register', success='true'))

    # Check if success flag exists in query params
    success = request.args.get('success') == 'true'
    return render_template('register.html', success=success)

if __name__ == '__main__':
    app.run(debug=True)