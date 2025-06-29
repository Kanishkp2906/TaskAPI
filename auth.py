from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from database import get_db
from models import Users
from config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRY_MINS

pwd_content = CryptContext(schemes=['argon2'], deprecated='auto')

def hash_password(password: str) -> str:
    return pwd_content.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_content.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    expiry = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=TOKEN_EXPIRY_MINS))
    to_encode.update({'exp': expiry})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

OAuth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

def get_current_user(token: str = Depends(OAuth2_scheme), db: Session = Depends(get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid token or credentials',
        headers={'WWW_Authenticate': 'Bearer'}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
    except JWTError:
        print('JWT Error:',)
        raise credentials_exception
    
    user = db.query(Users).filter(Users.email == email).first()

    if user is None:
        raise credentials_exception
    
    return user