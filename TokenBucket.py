import time
import threading

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


# Bucket with capacity of 10 tokens, refilling 1 token per second
bucket = TokenBucket(tokens=1, fill_rate=1)  

# mimicing request handling
def handle_request(request_id, token_required=1):
    if bucket.consume(tokens=token_required):
        print(f"Request {request_id} handled.")
    else:
        print(f"Request {request_id} denied due to rate limiting.")

# Simulating incoming requests
for i in range(15):
    handle_request(i)
    time.sleep(0.3)
