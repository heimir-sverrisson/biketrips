#!/usr/bin/env python3
#
# Use the Google Distance Matrix API for bike paths.
#
# Restartable, as outfile is read for already calculated
# paths and they are skipped on restart of this program.
#
# Heimir Sverrisson, October 2017
#
import json
import sys
import csv
from os import path, environ
import requests

BASE_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json'
API_KEY = environ['API_KEY']
MODE = "bicycling"

def parse_response(out):
    out_status = out['status']
    if out_status != 'OK':
        return out_status, '-1', '-1'
    status = out['rows'][0]['elements'][0]['status']
    if status == 'ZERO_RESULTS':
        dist = '-1'
        secs = '-1'
    else:
        dist = out['rows'][0]['elements'][0]['distance']['value']
        secs = out['rows'][0]['elements'][0]['duration']['value']
    return out_status, dist, secs

def get_distance_and_duration(origins, destinations):
    payload = {'origins': origins,
               'destinations': destinations,
               'mode': MODE,
               'key': API_KEY}
    r = requests.get(BASE_URL, params=payload)
    out_status, dist, secs = parse_response(json.loads(r.text))
    if out_status != 'OK':
        print('Did not get OK status:')
        print(r.text)
        raise Exception
    return dist, secs

def read_station_info(infile):
    stations = {}
    reader = csv.reader(open(infile, mode='r'))
    for row in reader:
        key, location, lat, lon = row
        stations[int(key)] = {'location': location, 'lat': lat, 'lon': lon}
    return stations

def calculate_and_write(writer, outfile_desc, existing, stations):
    for s_1 in stations:
        for s_2 in stations:
            if s_1 >= s_2: # Only need to calculate upper triangle array
                continue
            key = '{0},{1}'.format(s_1, s_2)
            if key in existing:
                continue
            coord_1 = '{0}, {1}'.format(stations[s_1]['lat'], stations[s_1]['lon'])
            coord_2 = '{0}, {1}'.format(stations[s_2]['lat'], stations[s_2]['lon'])
            distance, trip_time = get_distance_and_duration(
                coord_1,
                coord_2
            )
            writer.writerow(
                {'station_1': s_1, 'station_2': s_2,
                 'distance': distance, 'trip_time': trip_time}
            )
            outfile_desc.flush()


def read_existing(file):
    existing = {}
    reader = csv.reader(open(file, mode='r'))
    next(reader) # Skip header
    for row in reader:
        s_1, s_2, _distance, _time = row
        existing['{0},{1}'.format(int(s_1), int(s_2))] = True
    return existing

def make_writer(outfile):
    fieldnames = ['station_1', 'station_2', 'distance', 'trip_time']
    appending = path.isfile(outfile)
    existing = {}
    if appending:
        existing = read_existing(outfile)
    outfile_desc = open(outfile, mode='a')
    writer = csv.DictWriter(outfile_desc, fieldnames=fieldnames)
    if not appending:
        writer.writeheader()
    return writer, outfile_desc, existing

def main():
    if len(sys.argv) < 3:
        print('Please provide infile and outfile names on command line')
        exit(1)
    stations = read_station_info(sys.argv[1])
    writer, outfile_desc, existing = make_writer(sys.argv[2])
    calculate_and_write(writer, outfile_desc, existing, stations)

if __name__ == "__main__":
    main()
