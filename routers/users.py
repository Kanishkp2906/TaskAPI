from sqlalchemy.orm.session import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from schemas.users import UserCreate, UserResponse, UserUpdate
from auth import hash_password, verify_password, get_current_user, create_access_token
from database import get_db
from models import Users
from utils.notification import send_notification

router = APIRouter(tags=['User Sign Up'])

# Register a new user.
@router.post('/register', response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(Users.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=409, deatil='User already exists!')
    
    hashed_pwd = hash_password(user.password)
    
    new_user = Users(
        username = user.username,
        email = user.email,
        password = hashed_pwd,
        role = user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Login user for jwt token
@router.post('/login')
def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == form_data.username).first()
    if user is None:
        raise HTTPException(status_code=400, detail='Invalid Credentials')
    
    verification = verify_password(form_data.password, user.password)

    if not verification:
        raise HTTPException(status_code=400, detail='Invalid credentials')
    
    token = create_access_token({'sub': user.email, 'role': user.role})

    return {'access_token': token, 'token_type': 'bearer'}

# Delete user through user_email.
@router.delete('/delete/{user_email}/user', response_model=UserResponse)
def delete_user(
    user_email: str,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
    ):
    
    user_del = db.query(Users).filter(Users.email == user_email).first()

    if user_del is None:
        raise HTTPException(statuss_code=404, detail='user not found!')
    
    if current_user.email != user_email and current_user.role != "Admin":
        raise HTTPException(status_code=403,detail="Not authorized to delete this user")
    
    db.delete(user_del)
    db.commit()
    
    return user_del

# Update user information,
@router.put('/update/user', response_model=UserResponse)
def user_update(
    update_user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
    ):

    db_user = db.query(Users).filter(Users.email == current_user.email).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found!')
    
    update_data = update_user.model_dump(exclude_unset=True)

    if 'password' in update_data:
        update_data['password'] = hash_password(update_data['password'])
    
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user

@router.post('/notify')
def notify(email: str, backgorundTask: BackgroundTasks):
    backgorundTask.add_task(send_notification, email)
    return {'message': 'You will receive an email.'}