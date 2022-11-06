import json
import csv
from flask import Flask, request, send_file
from flask_cors import CORS
import requests
import random
from typing import TextIO
from csv import writer
from math import radians, cos, sin, asin, sqrt

app = Flask(__name__)
CORS(app)

def Create_Account_Dict(database):
    output = dict({})
    with open(database) as f:
        reader = csv.reader(f, delimiter=',')
        # Skip the first header row.
        # next(reader)

        for account in reader:
            output[account[0]] = (account[1], account[2])
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
                    keylist.append(line[2])
                if email in line:
                    account_exists = True
    while key in keylist:
        key = random.randint(0, 9999)
    if account_exists == False:
        account_info.append(email)
        account_info.append(password)
        account_info.append(key)
        account_info.append([])
        
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
        return json.dumps({"email": email, "user_exists": True, 
                           "password": True, "id": key})
    else:
        account_data = Create_Account_Dict('dummy_accounts.csv')
        id = account_data[email][3]
        return json.dumps({"email": email, "user_exists": True, 
                           "password": True, "id": id})
@app.route('/return_events', methods = ['POST'])
def return_events():
    filename = 'dummy_accounts.csv'
    events = []
    with open (filename) as f:
        reader = csv.reader(f)
        for line in reader:
            if int(line[2]) == int(id):
                for i in range(len(line)):
                    if i not in (0, 1, 2):
                        events.append(line[i])
    output = []
    filename3 = 'dummy_data.csv'
    with open (filename2) as wf:
        reader = csv.reader(wf)
        for line in reader:
            if line[0] in events:
                output.append(line)
    return json.dumps({"Events": output})

def distance(location_coord, event_coord):
    location_lat = float(location_coord[0])
    location_lon = float(location_coord[1])
    event_lat = float(event_coord[0])
    event_lon = float(event_coord[1])
     
    # The math module contains a function named
    # radians which converts from degrees to radians.
    location_lon = radians(location_lon)
    event_lon = radians(event_lon)
    location_lat = radians(location_lat)
    event_lat = radians(event_lat)

    # Haversine formula
    dlon = event_lon - location_lon
    dlat = event_lat - location_lat
    a = sin(dlat / 2)**2 + cos(location_lat) * cos(event_lat) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
      
    # calculate the result
    return(c * r)



def is_in_range(location_coord: tuple, event_coord: tuple, event_radius: float):
    distance_calc = distance((location_coord[0], location_coord[1]), (event_coord[0], event_coord[1]))
    if distance_calc <= event_radius:
        return True
    else:
        return False
    

@app.route('/event_in_range', methods = ['GET'])
def event_in_range():
    request_data = request.get_json()
    longitude = request_data['lon']
    latitude = request_data['lat']
    location_coords = (float(latitude), float(longitude))
    output = []
    filename = 'spoof.csv'
    with open (filename) as f:
        reader = csv.reader(f)
        for line in reader:
            if is_in_range(location_coords, (float(line[1]), float(line[2])), 10.0):
                output.append(line)
                
    return json.dumps({"Events_in_range": output})
    
    
                
    
    
if __name__ == "__main__":
    app.run(debug=True, port=3001)
