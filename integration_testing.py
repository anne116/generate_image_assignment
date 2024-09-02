from fastapi.testclient import TestClient
from concurrent.futures import ThreadPoolExecutor
from generate_image import app, MAX_HEIGHT, MAX_WIDTH
from PIL import Image
import time
import io

client = TestClient(app)

def test_generate_image_valid_input_success():
    start_time = time.time()
    response = client.get("/generate_image?width=200&height=100")
    end_time = time.time()
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

    image = Image.open(io.BytesIO(response.content))
    assert image.size == (200, 100)

    assert (end_time - start_time) < 0.7, f"Response took too long: {end_time - start_time} seconds"

def test_boundary_values():
    response = client.get(f"/generate_image?width={MAX_WIDTH}&height={MAX_HEIGHT}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

def test_generate_image_invalid_zero_input():
    response = client.get("/generate_image?width=0&height=50")
    assert response.status_code == 400
    assert response.json() == {"detail": "Height and Width must be positive integers."}

def test_generate_image_invalid_negative_input():
    response = client.get("/generate_image?width=-100&height=-50")
    assert response.status_code == 400
    assert response.json() == {"detail": "Height and Width must be positive integers."}

def test_generate_image_invalid_nan_input():
    response = client.get("/generate_image?width=abc&height=de")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == 'Input should be a valid integer, unable to parse string as an integer'

def test_generate_image_invalid_special_character_input():
    response = client.get("/generate_image?width=@#$&height=%^")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == 'Input should be a valid integer, unable to parse string as an integer'

def test_generate_image_invalid_empty_input():
    response = client.get("/generate_image?width= &height=500")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == 'Input should be a valid integer, unable to parse string as an integer'

def test_over_size():
    response = client.get(f"/generate_image?width={MAX_WIDTH + 1}&height={MAX_HEIGHT + 1}")
    assert response.status_code == 400
    assert response.json() == {"detail": f"Height and Width must be less than or equal to {MAX_HEIGHT} and {MAX_WIDTH}"}

def test_concurrent_requests():
    def send_request(_):
        response = client.get("/generate_image?width=20&height=10")
        assert response.status_code == 200
        return response.elapsed.total_seconds()

    with ThreadPoolExecutor(max_workers=10) as executor:
        times = list(executor.map(send_request, range(10)))

    for elapsed_time in times:
        assert elapsed_time < 0.7, f"Response time is too long: {elapsed_time} seconds"
