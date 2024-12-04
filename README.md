# Vehicle Management API

A RESTful web service that provides CRUD operations for vehicle data management. Built with Flask and SQLAlchemy, this API allows you to store and manage vehicle information in a SQLite database.

## Features

- Create, Read, Update, and Delete vehicle records
- SQLite database storage
- JSON-formatted request/response handling
- Comprehensive error handling
- Built-in unit tests
- Case-insensitive VIN handling

## Tech Stack

- Python 3.x
- Flask
- SQLAlchemy
- pytest
- SQLite

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /vehicle | Retrieve all vehicles |
| POST | /vehicle | Create a new vehicle |
| GET | /vehicle/{vin} | Retrieve a specific vehicle |
| PUT | /vehicle/{vin} | Update a specific vehicle |
| DELETE | /vehicle/{vin} | Delete a specific vehicle |

## Data Model

Vehicle attributes:
- VIN (Vehicle Identification Number) - Primary Key, Unique
- manufacturer_name (string)
- description (string)
- horse_power (integer)
- model_name (string)
- model_year (integer)
- purchase_price (decimal)
- fuel_type (string)

## Setup and Installation

1. Clone the repository
```bash
git clone <repository-url>
```

## Install dependencies

```bash

pip install -r requirements.txt
```

## Run the application

```bash

python run.py
```

## Testing

Run the tests using pytest:
```bash

pytest
```

The test suite includes:

    Vehicle creation tests
    Vehicle retrieval tests
    Vehicle update tests
    Vehicle deletion tests
    Error handling tests

## API Usage Examples
Create a Vehicle
```bash

POST /vehicle
Content-Type: application/json

{
    "vin": "1HGCM82633A123456",
    "manufacturer_name": "Honda",
    "description": "Sedan",
    "horse_power": 180,
    "model_name": "Accord",
    "model_year": 2020,
    "purchase_price": 20000.0,
    "fuel_type": "Gasoline"
}
```

### Get All Vehicles
```bash

GET /vehicle
```

### Get Specific Vehicle
```bash

GET /vehicle/1HGCM82633A123456
```
### Update Vehicle
```bash

PUT /vehicle/1HGCM82633A123456
Content-Type: application/json

{
    "description": "Updated Sedan",
    "horse_power": 200
}
```
### Delete Vehicle
```bash

DELETE /vehicle/1HGCM82633A123456
```

## Error Handling

The API includes comprehensive error handling:

    400 Bad Request - Invalid JSON format
    404 Not Found - Vehicle not found
    422 Unprocessable Entity - Invalid data format or validation failure

## Local Development

The application runs on localhost by default. The SQLite database file (vehicles.db) will be created automatically in the project directory.
Contributing

    Fork the repository
    Create a feature branch
    Commit your changes
    Push to the branch
    Create a Pull Request
