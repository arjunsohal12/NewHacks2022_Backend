import requests
import csv
from dataclasses import dataclass

@dataclass
# [[name, (longitude, latitude), time, etc..]]
class Event:
    name: str
    location: tuple
    time: str

def format_data(database) -> list[Event]:
    output = []
    with open(database) as f:
        reader = csv.reader(f, delimiter=',')
        # Skip the first header row.
        # next(reader)
        for event in reader:
            output.append(Event(event[0], (event[1], event[2]), event[3]))
    return output


def distance(longitude, latitude, event_longitude, event_latitude) -> float:
    distance_output = 0

    return distance_output


def is_in_range(longitude, latitude, database_list, range) -> list:
    output_list = []
    for event in database_list:
        if distance(longitude, latitude, ) <= range:
            output_list.append(event)

    return output_list

data = 'dummy_data.csv'
print(format_data(data))
