import time

class TTLCache:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl = ttl_seconds
        self.store = {}

    def get(self, key):
        item = self.store.get(key)
        if not item:
            return None

        value, expiry = item
        if time.time() > expiry:
            del self.store[key]
            return None

        return value

    def set(self, key, value):
        self.store[key] = (value, time.time() + self.ttl)

    def invalidate(self, key: str = None):
        if key:
            self.store.pop(key, None)
        else:
            self.store.clear()
