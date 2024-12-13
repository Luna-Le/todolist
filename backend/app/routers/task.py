from fastapi import APIRouter, Depends, Response, status, HTTPException
from .. import schemas, models
from typing import List
from ..oauth2 import get_current_user
from ..database import get_db
from sqlalchemy.orm import Session
router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TaskOut)
def create_task(task: schemas.Task, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    task_data = task.model_dump()
    new_task = models.Task(owner_id=current_user.id, **task_data)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    #final_task = db.query(models.Task).outerjoin(models.Category).filter(models.Task.id == new_task.id).first()
    return new_task


@router.get("/", response_model=List[schemas.TaskOut])
def get_tasks(current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
    return tasks



@router.get("/{id}", response_model=schemas.TaskOut)
def get_task(id: int, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {id} was not found")
    
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    return task


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    task_query = db.query(models.Task).filter(models.Task.id == id)
    task = task_query.first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {id} was not found")
    
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    task_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.TaskOut)
def update_task(id: int, updated_task: schemas.Task, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    task_query = db.query(models.Task).filter(models.Task.id == id)
    existing_task = task_query.first()
    
    if not existing_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {id} was not found")
    
    if existing_task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    

    
    # Update task with excluded fields and set category
    task_data = updated_task.model_dump()
    task_query.update(task_data, synchronize_session=False)
    
    db.commit()
    db.refresh(existing_task)
    return existing_task