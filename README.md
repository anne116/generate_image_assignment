# Image Generation and Testing Project

This project includes a set of Python scripts for generating images, performing arithmetic operations, and running unit and integration tests. The main API server is built using FastAPI, with integration for Google Cloud Logging and Google Analytics event tracking.

## Table of Contents

- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Testing](#testing)
- [Google Cloud Logging and Google Analytics Integration](#google-cloud-logging-and-google-analytics-integration)

## Project Structure
  ├── .gitignore # Git ignore file
  ├── string_arithmetic.py # Python implementation for string arithmetic operations 
  ├── generate_image.py # FastAPI implementation for image generation API 
  ├── find_max_image_size.py # Script to test the maximum image size that can be generated
  ├── unit_testing.py # Unit testing script 
  └── integration_testing.py # Integration testing script

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your_username/your_repository.git
   cd your_repository
   ```
2. Create a virtual environment and install the required dependencies:
    ```
    python -m venv venv
    source venv/bin/activate  # For Windows, use venv\Scripts\activate
    pip install -r requirements.txt
    ```
3. Set up Google Cloud Logging and Google Analytics:
    I. Place the google_cloud_logging.json credentials file in the project root directory.
    II. Configure the .env file with MEASUREMENT_ID and API_SECRET.

## Usage

Run generate_image.py to start the FastAPI server:
    ```
    uvicorn generate_image:app --reload
    ```
You can test the API endpoint via browser or Postman:
    ```
    http://127.0.0.1:8000/generate_image?width=100&height=100
    ```
Run string_arithmetic.py to perform arithmetic calculations from a string input.

## Features

1. string_arithmetic.py: Safely evaluates arithmetic expressions from strings using Python.
2. generate_image.py: Provides an API endpoint using FastAPI to generate PNG images based on user-provided width and height.
3. find_max_image_size.py: Tests the performance of image generation for various sizes to find the maximum stable size.
4. unit_testing.py: Performs unit tests on the API endpoints, checking response status and performance metrics.
5. integration_testing.py: Runs integration tests, including concurrency testing to evaluate API performance and stability.

## Testing

Run the following command to execute unit tests:
    ```
    pytest unit_testing.py
    ```
Run the following command to execute integration tests:
    ```
    pytest integration_testing.py
    ```

## Google Cloud Logging and Google Analytics Integration

The API usage and execution events have been successfully logged to Google Cloud Logging and Google Analytics. Below are the steps and configurations:

1. **Google Cloud Logging**: Configured using `google_cloud_logging.json` and Python's Google Cloud Client.
2. **Google Analytics**: Implemented event tracking using Measurement Protocol with the correct `MEASUREMENT_ID` and `API_SECRET`.

![Google Cloud Logging Screenshot](screenshots/cloud_logging.png)
![Google Analytics Screenshot](screenshots/google_analytics.png)
