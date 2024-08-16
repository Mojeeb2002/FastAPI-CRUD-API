
from typing import List

from fastapi import FastAPI, APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import schemas, oauth2, models
from app.database import get_db
from app.models import Group

router = APIRouter(
    prefix="/group",
    tags=["group"],
)


@router.get("/", response_model=List[schemas.GroupResponse])
def get_groups(db: Session = Depends(get_db)):
    groups = db.query(Group).all()
    return groups


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.GroupResponse)
def create_group(group: schemas.CreateGroup, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_group = models.Group(owner_id=current_user.id, **group.dict())
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group


@router.get('/{id}', response_model=schemas.GroupResponse)
def get_group(id: int, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter(models.Group.id == id).first()

    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return group


@router.put('/{id}', response_model=schemas.GroupResponse)
def update_group(id: int, updated_group: schemas.CreateGroup, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    group_query = db.query(models.Group).filter(models.Group.id == id)
    group = group_query.first()

    if not group:
        raise HTTPException(status_code=404, detail="Post not found")

    if group.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    group_query.update(updated_group.dict(), synchronize_session=False)
    db.commit()
    return group_query.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_group(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    group_query = db.query(models.Group).filter(models.Group.id == id)
    group = group_query.first()

    if not group:
        raise HTTPException(status_code=404, detail="Post not found")

    if group.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    group_query.delete(synchronize_session=False)
    db.commit()
    return "Group deleted successfully"