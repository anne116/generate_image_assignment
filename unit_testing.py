from fastapi.testclient import TestClient
from generate_image import app, MAX_HEIGHT, MAX_WIDTH

client = TestClient(app)

def test_valid_input():
    response = client.get("/generate_image?width=200&height=100")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

def test_valid_large_num():
    response = client.get("/generate_image?width=10000&height=5000")
    assert response.status_code == 400
    assert response.json() == {"detail": f"Height and Width must be less than or equal to {MAX_HEIGHT} and {MAX_WIDTH}"}

def test_invalid_zero_input():
    response = client.get("/generate_image?width=0&height=50")
    assert response.status_code == 400
    assert response.json() == {"detail": "Height and Width must be positive integers."}
    
def test_invalid_negative_num_input():
    response = client.get("/generate_image?width=-200&height=100")
    assert response.status_code == 400
    assert response.json() == {"detail": "Height and Width must be positive integers."}

def test_invalid_nan_input():
    response = client.get("/generate_image?width=1de&height=abc")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid integer, unable to parse string as an integer"

def test_invalid_special_character():
    response = client.get("/generate_image?width=#$&height=&*")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid integer, unable to parse string as an integer"

def test_invalid_empty_input():
    response = client.get("/generate_image?width=&height=100")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid integer, unable to parse string as an integer"