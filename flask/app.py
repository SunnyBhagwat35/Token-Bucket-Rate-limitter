from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)

class TokenBucket:
    def __init__(self, tokens, fill_rate):
        self.capacity = tokens
        self._tokens = tokens
        self.fill_rate = fill_rate
        self.timestamp = time.time()
        self.lock = threading.Lock()

    def consume(self, tokens=1):
        with self.lock:
            self._add_new_tokens()
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False

    def _add_new_tokens(self):
        now = time.time()
        elapsed = now - self.timestamp
        self.timestamp = now
        self._tokens = min(self.capacity, self._tokens + elapsed * self.fill_rate)

# Initializing bucket with 10 requests per minute
rate_limit_bucket = TokenBucket(tokens=10, fill_rate=10/60)

# Decorator for rate limiting
def rate_limited(endpoint):
    def wrapper(*args, **kwargs):
        if rate_limit_bucket.consume():
            return endpoint(*args, **kwargs)
        else:
            return jsonify({"error": "Rate limit exceeded"}), 429
    return wrapper

# Apply the rate limiting decorator to endpoints
@app.route('/')
@rate_limited
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
