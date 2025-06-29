from sqlalchemy.orm.session import Session
from fastapi import APIRouter, HTTPException, Depends
from schemas.tasks import TaskCreate, TaskResponse, TaskUpdate
from auth import get_current_user
from models import Tasks, Users
from database import get_db
from typing import List

router = APIRouter(tags=['User Tasks'])

#Create a task for current user.
@router.post('/create/task', response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    current_user: Users = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):

    db_task = Tasks(**task.model_dump())

    current_user.tasks.append(db_task)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task

# Show all the tasks from the current user.
@router.get('/user/tasks', response_model=List[TaskResponse])
def user_tasks(current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):

    user_tasks = db.query(Tasks).filter(Tasks.user_id == current_user.id).all()

    return user_tasks

# Update a task from the current user.
@router.put('/update/{task_id}/task', response_model=TaskResponse)
def task_update(
    task_id: int,
    update_task: TaskUpdate,
    current_user: Users = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    
    db_task = db.query(Tasks).filter(Tasks.id == task_id, Tasks.user_id == current_user.id).first()

    if db_task is None:
        raise HTTPException(status_code=404, detail='Task not found or not Authorized!')
    
    update_data = update_task.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)

    return db_task

# Delete a task by current user.
@router.delete('/delete/{task_id}/task', response_model=TaskResponse)
def task_delete(
    task_id: int,
    current_user: Users = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    del_task = db.query(Tasks).filter(Tasks.id == task_id, Tasks.user_id == current_user.id).first()

    if del_task is None:
        raise HTTPException(status_code=404, detail='Task not found or not Authorized!')
    
    db.delete(del_task)
    db.commit()

    return del_task