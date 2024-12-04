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
