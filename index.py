from flask import Flask,jsonify, render_template, send_from_directory
import requests
import redis
from pymongo import MongoClient
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)

# Redis connection
redis_host = 'redis-17570.c55.eu-central-1-1.ec2.redns.redis-cloud.com'
redis_port = 17570
redis_password = 'UQeA3BjJP99sdBLTxpz5aJ4LmQLY5L86'
redis_client = redis.StrictRedis(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    decode_responses=True
)


# Aviation Edge API details
aviation_edge_api_key = '4c3928-3500cc'
# https://aviation-edge.com/v2/public/flightsHistory?key=4c3928-3500cc&code=FRA&type=departure&date_from=2024-01-01&date_to=2024-01-30
aviation_edge_url = f'https://aviation-edge.com/v2/public/flights?key={aviation_edge_api_key}&depIcao=EDDF'
aviation_edge_url2 = f'https://aviation-edge.com/v2/public/flights?key=4c3928-3500cc&lat=50.0333&lng=8.5706&distance=500'
# https://aviation-edge.com/v2/public/flights?key=4c3928-3500cc&lat=50.0333&lng=8.5706&distance=100
# https://aviation-edge.com/v2/public/flights?key=4c3928-3500cc&depIcao=EDDH
aviation_edge_url22 = f'https://aviation-edge.com/v2/public/flights?key={aviation_edge_api_key}&arrIcao=EDDF'
aviation_edge_url3 = f'https://aviation-edge.com/v2/public/flights?key={aviation_edge_api_key}&depIcao=EDDM'
aviation_edge_url4 = f'https://aviation-edge.com/v2/public/flights?key={aviation_edge_api_key}&depIcao=EDDB'
print(aviation_edge_url4)



def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # Radius of the Earth in km
    return distance

# Fetch Flight Data Function
def fetch_flight_data():
    response = requests.get(aviation_edge_url)
    if response.status_code == 200:
        flight_data = response.json()
        # Cache the data in Redis for 2.6 minute (160 seconds)
        redis_client.setex('flight_data', 160, str(flight_data))
        return flight_data
    else:
        return []

def fetch_flight_data2():
    response = requests.get(aviation_edge_url2)
    if response.status_code == 200:
        flight_data = response.json()
        # Cache the data in Redis for 5 minute (300 seconds)
        redis_client.setex('flight_data2', 300, str(flight_data))
        return flight_data
    else:
        return []

def fetch_flight_data3():
    response = requests.get(aviation_edge_url3)
    if response.status_code == 200:
        flight_data = response.json()
        # Cache the data in Redis for 5 minute (300 seconds)
        redis_client.setex('flight_data3', 300, str(flight_data))
        return flight_data
    else:
        return []

def fetch_flight_data4():
    response = requests.get(aviation_edge_url4)
    if response.status_code == 200:
        flight_data = response.json()
        # Cache the data in Redis for 5 minute (300 seconds)
        redis_client.setex('flight_data4', 300, str(flight_data))
        return flight_data
    else:
        return []


# Get Flight Data Function
def get_flight_data():
    cached_data = redis_client.get('flight_data')
    if cached_data:
        return eval(cached_data)
    else:
        return fetch_flight_data()

def get_flight_data2():
        cached_data = redis_client.get('flight_data2')
        if cached_data:
            return eval(cached_data)
        else:
            return fetch_flight_data2()


def get_flight_data3():
    cached_data = redis_client.get('flight_data3')
    if cached_data:
        return eval(cached_data)
    else:
        return fetch_flight_data3()

def get_flight_data4():
    cached_data = redis_client.get('flight_data4')
    if cached_data:
        return eval(cached_data)
    else:
        return fetch_flight_data4()

@app.route('/fra')
def index():
    return render_template('index4.html')

@app.route('/all')
def index2():
    return render_template('index55.html')

@app.route('/api/flights')
def flights():
    flight_data = get_flight_data()
    return jsonify(flight_data)

@app.route('/api/flights2')
def flights2():
    flight_data = get_flight_data2()
    return jsonify(flight_data)

@app.route('/api/flights3')
def flights3():
    flight_data = get_flight_data3()
    return jsonify(flight_data)

@app.route('/api/flights4')
def flights4():
    flight_data = get_flight_data4()
    return jsonify(flight_data)


@app.route('/static/<path:filename>')
def serve_assets(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4080)
