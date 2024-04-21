import requests
import time

# URL of the Flask application
url = 'http://127.0.0.1:5000/'

# Make multiple requests to test rate limiting
for i in range(15):
    response = requests.get(url)
    print(f"Request {i+1}: Status {response.status_code}")
    time.sleep(0.5)  # Adjust based on your rate limit settings
