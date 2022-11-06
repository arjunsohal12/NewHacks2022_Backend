import json
import csv
from flask import Flask, request, send_file
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

def Create_Account_Dict(database):
    output = dict({})
    with open(database) as f:
        reader = csv.reader(f, delimiter=',')
        # Skip the first header row.
        # next(reader)

        for account in reader:
            output[account[0]] = (account[1], account[2], account[3])
    return output


@app.route('/login', methods=['POST'])
def account_verify():
    request_data = request.get_json()
    email = request_data['email']
    password = request_data['password']
    account_data = Create_Account_Dict('dummy_accounts.csv')
    User_Exists = False
    Password_Correct = False
    id = ''
    if email in account_data:
        User_Exists = True
        id = account_data[email][2]
        if password == account_data[email][0]:
            Password_Correct = True

    return json.dumps({"email": email, "user_exists": User_Exists, "password": Password_Correct, "id": id})


if __name__ == "__main__":
    app.run(debug=True, port=3001)
