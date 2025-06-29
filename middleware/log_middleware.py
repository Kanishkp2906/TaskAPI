import time
import logging
from fastapi import Request
from config import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(
    level=logging.INFO,
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('FastAPI')

class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        user_info = 'anonynous'
        role = 'unknown'

        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer'):
            token = auth_header.split(' ')[1]

            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user_info = payload.get('sub', 'unknown')
                role = payload.get('role', 'unknown')
            except JWTError:
                user_info = "Invalid token!"

        # logger.info(f'{request.method} {request.url.path} - Client: {request.client.host}')

        response = await call_next(request)

        duration = round(time.time() - start_time, 4)

        log_msg = (
            f'{request.method} {request.url.path} - '
            f'User: {user_info} ({role}) - '
            f'{response.status_code} {duration}s'
        )

        logger.info(log_msg)

        return response
