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


@app.route('/create_account', methods = ['POST'])
def create_account():
    filename = 'dummy_accounts.csv'
    request_data = request.get_json()
    email = request_data['email']
    password = request_data['password']
    
    account_info = []
    account_exists = False
    key = random.randint(0, 9999)
    
    keylist = []
    with open (filename) as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            if line != [''] or line != ['\n']:
                for item in line:
                    item = item.strip()
                if line != [''] and line !=['\n'] and line != []:
                    print(line)
                    keylist.append(line[-1])
                if email in line:
                    account_exists = True
    while key in keylist:
        key = random.randint(0, 9999)
    if account_exists == False:
        account_info.append(email)
        account_info.append(password)
        account_info.append([])
        account_info.append(key)
    
        
        with open(filename, 'a') as f_object:
         
            # Pass this file object to csv.writer()
            # and get a writer object
            writer_object = writer(f_object)
         
            # Pass the list as an argument into
            # the writerow()
            writer_object = csv.writer(f_object, lineterminator='\n')
            writer_object.writerow(account_info)
         
            # Close the file object
            f_object.close()
        return json.dumps(True)
    else:
        return json.dumps(False)

if __name__ == "__main__":
    app.run(debug=True, port=3001)
