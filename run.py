import pytest
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicles.db' 
app.config['TESTING'] = True
db = SQLAlchemy(app)


class Vehicle(db.Model):
    vin = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    manufacturer_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    horse_power = db.Column(db.Integer, nullable=False)
    model_name = db.Column(db.String, nullable=False)
    model_year = db.Column(db.Integer, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    fuel_type = db.Column(db.String, nullable=False)

    # Convert object to dictionary
    def to_dict(self):
        vehicle_data = {
            "vin": self.vin,
            "manufacturer_name": self.manufacturer_name,
            "description": self.description,
            "horse_power": self.horse_power,
            "model_name": self.model_name,
            "model_year": self.model_year,
            "purchase_price": self.purchase_price,
            "fuel_type": self.fuel_type
        }
        return vehicle_data

with app.app_context():
    db.create_all()

# API routes
@app.route('/vehicle', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    vehicle_list = [vehicle.to_dict() for vehicle in vehicles]
    return jsonify(vehicle_list)

@app.route('/vehicle', methods=['POST'])
def add_vehicle():

    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad Request"}), 400

    try:
 
        vehicle = Vehicle(**data)
        db.session.add(vehicle)
        db.session.commit()

        return jsonify({"message": "Vehicle added", "vehicle": vehicle.to_dict()}), 201
    except Exception as e:
        error_message = {"error": "Unprocessable Entity", "details": str(e)}
        return jsonify(error_message), 422

@app.route('/vehicle/<vin>', methods=['GET'])
def get_vehicle(vin):
    vehicle = Vehicle.query.filter_by(vin=vin).first()
    if vehicle:
        return jsonify(vehicle.to_dict())
    return jsonify({"error": "Vehicle not found"}), 404
  

@app.route('/vehicle/<vin>', methods=['DELETE'])
def delete_vehicle(vin):
    print("The VIN number is: ", vin)
    vehicle = Vehicle.query.filter_by(vin=vin).first()
    if vehicle:
        db.session.delete(vehicle)
        db.session.commit()
        return jsonify({"message": f"Vehicle with VIN {vin} deleted"}), 200

    return jsonify({"error": "Vehicle not found"}), 404

@app.route('/vehicle/<vin>', methods=['PUT'])
def update_vehicle(vin):
 
    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad Request"}), 400

    vehicle = Vehicle.query.filter_by(vin=vin).first()
    if not vehicle:
 
        return jsonify({"error": "Vehicle not found"}), 404

    try:
        for key, value in data.items():
            if hasattr(vehicle, key):
                setattr(vehicle, key, value)
  
        db.session.commit()
        return jsonify({"message": "Vehicle updated", "vehicle": vehicle.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": "Unprocessable Entity", "details": str(e)}), 422

# Pytest fixtures
@pytest.fixture
def client():
    client = app.test_client()
    with app.app_context():
        db.create_all()
        yield client

    with app.app_context():
        db.drop_all()

# Tests
def test_get_vehicles(client):
    response = client.get('/vehicle')
    assert response.status_code == 200

def test_add_vehicle(client):
    with app.app_context():
        Vehicle.query.delete()
        db.session.commit()

    # Send a POST request to /vehicle
    vehicle_data = {
        "vin": "1HGCM82633A123456",
        "manufacturer_name": "Honda",
        "description": "Sedan",
        "horse_power": 180,
        "model_name": "Accord",
        "model_year": 2020,
        "purchase_price": 20000.0,
        "fuel_type": "Gasoline"
    }
    response = client.post('/vehicle', json=vehicle_data)
    assert response.status_code == 201

    invalid_json = "hello"
    response = client.post('/vehicle', json=invalid_json)
    assert response.status_code == 422

    empty_json = ""
    response = client.post('/vehicle', json=empty_json)
    assert response.status_code == 400

def test_get_vehicle_by_vin(client):
    first_vin = "1HGCM82633A123456"
    vehicle_data_1 = {
        "vin": first_vin,
        "manufacturer_name": "Honda",
        "description": "Sedan",
        "horse_power": 180,
        "model_name": "Accord",
        "model_year": 2020,
        "purchase_price": 20000.0,
        "fuel_type": "Gasoline"
    }
    client.post('/vehicle', json=vehicle_data_1)
    response = client.get('/vehicle/'+ first_vin)
    assert response.status_code == 200
    second_vin = "1HGCM82633A123457"
    vehicle_data_2 = {
        "vin": second_vin,
        "manufacturer_name": "Honda",
        "description": "Sedan",
        "horse_power": 180,
        "model_name": "Accord",
        "model_year": 2020,
        "purchase_price": 20000.0,
        "fuel_type": "Gasoline"
    }
    client.post('/vehicle', json=vehicle_data_2)
    response = client.get('/vehicle/'+ second_vin)
    assert response.status_code == 200
    invalid_vin = "1HGC"
    invalid_vin_data = {
        "vin": invalid_vin,
        "manufacturer_name": "Honda",
        "description": "Sedan",
        "horse_power": 180,
        "model_name": "Accord",
        "model_year": 2020,
        "purchase_price": 20000.0,
        "fuel_type": "Gasoline"
    }
    response = client.get('/vehicle/'+ invalid_vin)
    assert response.status_code == 404

def test_delete_vehicle(client):
    vehicle_data = {
        "vin": "1HGCM82633A123456",
        "manufacturer_name": "Honda",
        "description": "Sedan",
        "horse_power": 180,
        "model_name": "Accord",
        "model_year": 2020,
        "purchase_price": 20000.0,
        "fuel_type": "Gasoline"
    }
    client.post('/vehicle', json=vehicle_data)

    # Delete the vehicle
    response = client.delete('/vehicle/1HGCM82633A123456')
    assert response.status_code == 200
    assert response.json['message'] == "Vehicle with VIN 1HGCM82633A123456 deleted"

    response = client.get('/vehicle/1HGCM82633A123456')
    assert response.status_code == 404

def test_update_vehicle(client):
    vehicle_data = {
        "vin": "1HGCM82633A123456",
        "manufacturer_name": "Honda",
        "description": "Sedan",
        "horse_power": 180,
        "model_name": "Accord",
        "model_year": 2020,
        "purchase_price": 20000.0,
        "fuel_type": "Gasoline"
    }
    client.post('/vehicle', json=vehicle_data)
    updated_data = {
        "description": "Updated Sedan",
        "horse_power": 200
    }
    response = client.put('/vehicle/1HGCM82633A123456', json=updated_data)
    assert response.status_code == 200
    response = client.get('/vehicle/1HGCM82633A123456')
    assert response.json['description'] == "Updated Sedan"
    assert response.json['horse_power'] == 200

# Run tests manually
if __name__ == '__main__':
    # Create a test client
    with app.test_client() as client:
        print("Running test: test_add_vehicle")
        test_add_vehicle(client)

        print("Running test: test_get_vehicles")
        test_get_vehicles(client)

        print("Running test: test_get_vehicle_by_vin")
        test_get_vehicle_by_vin(client)

        print("Running test: test_update_vehicle")
        test_update_vehicle(client)

        print("Running test: test_delete_vehicle")
        test_delete_vehicle(client)
