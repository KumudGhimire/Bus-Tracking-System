from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Sample data for buses
buses = [
    {"id": 1, "route": "Route 1", "lat": 40.712776, "lng": -74.005974},
    
]

@app.route('/')
def index():
    return render_template('index.html', buses=buses)

@app.route('/mobile')
def mobile():
    return render_template('mobile.html')

@socketio.on('update_location')
def handle_update_location(data):
    bus_id = int(data['id'])  # Ensure bus_id is an integer
    for bus in buses:
        if bus['id'] == bus_id:
            bus['lat'] = float(data['lat'])  # Ensure latitude is a float
            bus['lng'] = float(data['lng'])  # Ensure longitude is a float
            break
    emit('location_update', data, broadcast=True)  # Broadcast the updated location to all connected clients

if __name__ == '__main__':
    socketio.run(app, debug=True)
