import redis
client = redis.Redis(host="localhost")

def islimiter(key, limit):
    req = client.incr(key)
    if req == 1:
        client.expire(key, 3600)
        ttl = 3600
    else:
        ttl = client.ttl(key)
    if req > limit:
        return False
    else:
        return True