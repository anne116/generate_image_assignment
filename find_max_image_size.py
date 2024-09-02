from PIL import Image
import io
import gc
import time

def test_max_image_size():
    max_width = 5000
    max_height = 5000
    increment = 10

    while True:
        try:
            start_time = time.time()
            gc.collect()
            print(f"Testing with width={max_width}, height={max_height}")
            with io.BytesIO() as buffer:
                image = Image.new("RGB", (max_width, max_height), (0, 0, 255))
                buffer = io.BytesIO()
                image.save(buffer, format="PNG")
                buffer.seek(0)
            end_time = time.time()
            elapsed_time = end_time - start_time

            print(f"Success with width={max_width}, height={max_height} in {elapsed_time:.2f} seconds")

            if elapsed_time > 0.7:
                print(f"Time exceeds 0.7 seconds at width={max_width}, height={max_height}. Therefore stopping test.")
                break

            max_width += increment
            max_height += increment
        except MemoryError:
            print(f"MemoryError encountered at width={max_width}, height={max_height}")
            break
        except Exception as err:
            print(f"Error encountered at width={max_width}, height={max_height}: {err}")
            break

    print(f"Maximum image size: width={max_width-increment}, height={max_height-increment}")

if __name__ == "__main__":
    test_max_image_size()

