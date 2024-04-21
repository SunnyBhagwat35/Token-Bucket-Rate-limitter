const express = require('express');
const app = express();
const PORT = 5000;

class TokenBucket {
    constructor(tokens, fillRate) {
      this.capacity = tokens;
      this.tokens = tokens;
      this.fillRate = fillRate;
      this.lastTimestamp = Date.now();
    }
  
    consume(tokens = 1) {
      this._addNewTokens();
      if (this.tokens >= tokens) {
        this.tokens -= tokens;
        return true;
      }
      return false;
    }
  
    _addNewTokens() {
      const now = Date.now();
      const elapsed = (now - this.lastTimestamp) / 1000; // convert to seconds
      this.lastTimestamp = now;
      this.tokens = Math.min(this.capacity, this.tokens + elapsed * this.fillRate);
    }
  }
  

const rateLimitBucket = new TokenBucket(10, 10/60);

// Middleware for rate limiting
function rateLimit(req, res, next) {
  if (rateLimitBucket.consume()) {
    next();
  } else {
    res.status(429).send('Rate limit exceeded');
  }
}

app.use(rateLimit);

app.get('/', (req, res) => {
  res.send('Hello, World!');
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
