
# CSV Analyzer FastAPI Application

## Overview

The CSV Analyzer is a FastAPI-based web service designed for data analysts to upload CSV files and run analyses based on various filters. This service includes user authentication to ensure secure access to the functionalities.

## Deployement

The CSV Analyzer is deployed on Render: https://csv-analysis-1f0a.onrender.com/docs

## Screenshots

![image](https://github.com/Addy-codes/csv-analysis/assets/72205091/ed4616b1-3961-4413-a982-8e25310b2db6)

![image](https://github.com/Addy-codes/csv-analysis/assets/72205091/e0d1a3c1-f405-4047-b40c-70c2e0b82d60)

![image](https://github.com/Addy-codes/csv-analysis/assets/72205091/70a7d75d-7746-4fc0-8aac-4a523db5a62d)

## Features

- **CSV Upload**: Allows users to upload a CSV file and save its contents to an SQLite database.
- **Data Analysis**: Provides endpoints to query the uploaded CSV data based on various filters.
- **User Authentication**: Secure user registration and authentication to access the main features.

## Requirements

- Docker
- Python 3.8+

## Installation

### Docker Setup

1. **Clone the Repository**

   ```sh
   git clone https://github.com/Addy-codes/csv-analysis
   cd csv-analysis
   ```

2. **Build the Docker Image**

   ```sh
   docker build -t csv_analyzer .
   ```

3. **Run the Docker Container**

   ```sh
   docker run -d -p 8000:8000 csv_analyzer
   ```

### Local Setup

1. **Clone the Repository**

   ```sh
   git clone https://github.com/Addy-codes/csv-analysis
   cd csv-analysis
   ```

2. **Create a virtual env & Install Dependencies**

   ```sh
   python -m venv venv
   venv/Scripts/activate
   pip install -r requirements.txt
   ```

3. **Run the Application**

   ```sh
   uvicorn app.main:app --reload
   ```

## Usage

### Accessing the Application

After starting the application, you can access the following endpoints:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc UI**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Note

Before using the endpoints, make sure you authorize yourself with a registered email and password:
- **Sample**:
  ```json
  {
    "username": "addy@gmail.com",
    "password": "123456"
  }
  ```

### Endpoints

#### Register User

- **URL**: `/register/`
- **Method**: `POST`
- **Description**: Registers a new user.
- **Payload**:
  ```json
  {
    "username": "Shobhit",
    "email": "shobhit@gmail.com",
    "password": "123456"
  }
  ```

#### Upload CSV

- **URL**: `/upload/`
- **Method**: `POST`
- **Description**: Uploads a CSV file from a given URL.
- **Payload**:
  ```json
  {
    "file_url": "https://docs.google.com/spreadsheets/d/1ShbFMzRUuIJY8amTA58UuEHwsc3UmAnd_LzduBwcBhE/edit?usp=sharing"
  }
  ```
- **Headers**: `Authorization: Bearer <JWT_TOKEN>`

#### Analyze Data

- **URL**: `/analyze/`
- **Method**: `POST`
- **Description**: Analyzes the uploaded CSV data based on the provided filters.
- **Payload**:
  ```json
  {
      "Name": "of"
  }
  ```
- **Headers**: `Authorization: Bearer <JWT_TOKEN>`

## Authentication

### Obtain JWT Token

1. **Login User**

   - **URL**: `/token/`
   - **Method**: `POST`
   - **Description**: Authenticates a user and returns a JWT token.
   - **Payload**:
     ```json
     {
       "username": "addy@gmail.com",
       "password": "123456"
     }
     ```

2. Use the returned `access_token` to authenticate requests to the `/upload/` and `/analyze/` endpoints.

## Development

### Database Migration

To ensure the database schema is up to date, the application will automatically create the necessary tables on startup.


## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.
