from core.cache import TTLCache

symbols_cache = TTLCache(ttl_seconds=3600)   # 1 hour
data_cache = TTLCache(ttl_seconds=300)       # 5 minutes
