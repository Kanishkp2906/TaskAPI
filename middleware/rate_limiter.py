from fastapi import Request
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM
from starlette.middleware.base import BaseHTTPMiddleware
import redis

redis_client = redis.Redis(host='localhost', port='6379', decode_responses=True)

class RedisRateLimiter(BaseHTTPMiddleware):
    def __init__(self, app, limit=5, window=60):
        super().__init__(app)
        self.limit = limit
        self.window = window

    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get('Authorization')
        user_id = 'unknown'

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user_id = payload.get('sub', 'unknown')
            except JWTError:
                user_id = 'Invalid Token!'

        redis_key = f'ratelimiting: {user_id}'
        request_count = redis_client.get(redis_key)

        if request_count is None:
            redis_client.set(redis_key, 1, ex=self.window)
        elif int(request_count) < self.limit:
            redis_client.incr(redis_key)
        else:
            ttl = redis_client.ttl(redis_key)
            return JSONResponse(
                status_code=429,
                content = {'message': f'Rate limit exceeded. Try again after {ttl} seconds.'}
            )
        
        return await call_next(request)
