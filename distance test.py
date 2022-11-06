import csv
from dataclasses import dataclass
from flask import Flask, request
import json
from math import radians, cos, sin, asin, sqrt

app = Flask(__name__)


def format_data(database):
    output = []
    with open(database) as f:
        reader = csv.reader(f, delimiter=',')
        # Skip the first header row.
        # next(reader)
        for event in reader:
            output.append([event[0], (event[1], event[2]), event[3]])
    return output


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
    a = sin(dlat / 2) ** 2 + cos(location_lat) * cos(event_lat) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    return c * r


@app.route('/is_in_range', methods=['POST'])
def is_in_range():
    request_data = request.get_json()

    longitude = request_data['longitude']
    latitude = request_data['latitude']
    location_cords = (latitude, longitude)

    range = int(request_data['range'])

    database_list = format_data('dummy_data.csv')

    output_list = []

    for event in database_list:
        if distance(location_cords, event[1]) <= range:
            output_list.append(event)

    return json.dumps(output_list)


if __name__ == "__main__":
    app.run(debug=True)
