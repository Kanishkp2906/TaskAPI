from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload
from fastapi import APIRouter, HTTPException, Depends
from models import Users, Tasks
from schemas.users import UserResponse, UserUpdate, UserTaskResponse, UserRole
from schemas.tasks import TaskResponse
from auth import get_current_user
from database import get_db
from typing import List

router = APIRouter(tags=['Admin Panel'])

# Role checker for admin routes.
class Role_checker:
    def __init__(self, required_role):
        self.role = required_role

    def __call__(self, user: Users = Depends(get_current_user)):
        if user.role != self.role:
            raise HTTPException(status_code=403, detail='Not Authorized!')
        return user

# Admin route to see all the tasks from all users.
@router.get('/admin/tasks', response_model=List[UserTaskResponse])
def get_all_tasks(
    current_user: Users = Depends(Role_checker(UserRole.admin)), 
    db: Session = Depends(get_db)
):
    all_users = db.query(Users).options(joinedload(Users.tasks)).all()

    return all_users

# Route to delete all the tasks.
@router.delete('/delete/{email}/{task_id}/task', response_model=TaskResponse)
def delete_task(
    email: str,
    task_id: int,
    current_user: Users = Depends(Role_checker(UserRole.admin)),
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter(Users.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not Found')
    
    del_task = db.query(Tasks).filter(Tasks.id == task_id, Tasks.user_id == user.id).first()

    if del_task is None:
        raise HTTPException(status_code=404, detail='Task not found or not Authorized!')
    
    db.delete(del_task)
    db.commit()

    return del_task
    
