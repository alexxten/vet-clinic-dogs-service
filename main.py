import datetime
from enum import Enum
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.engine import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker, Session

from db import models
from envars import DATABASE_URL

app = FastAPI()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class OrmBaseModel(BaseModel):
    class Config:
        orm_mode = True


class DogType(str, Enum):
    terrier = 'terrier'
    bulldog = 'bulldog'
    dalmatian = 'dalmatian'


class Dog(OrmBaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(OrmBaseModel):
    id: int
    timestamp: int


# dogs_db = {
#     0: Dog(name='Bob', pk=0, kind='terrier'),
#     1: Dog(name='Marli', pk=1, kind='bulldog'),
#     2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
#     3: Dog(name='Rex', pk=3, kind='dalmatian'),
#     4: Dog(name='Pongo', pk=4, kind='dalmatian'),
#     5: Dog(name='Tillman', pk=5, kind='bulldog'),
#     6: Dog(name='Uga', pk=6, kind='bulldog')
# }
#
# post_db = [
#     Timestamp(id=0, timestamp=12),
#     Timestamp(id=1, timestamp=10)
# ]


@app.get('/')
def root():
    return {
        'hello': (
            'Это сервис на FastApi, возвращающий информацию по собакам для ветклиники'
        ),
        'problems': (
            'У него есть проблемы с pk модели Dogs, тк он вроде должен быть'
            ' автоинкрементируемым, но в тоже время он обязателен в модели pydantic'
        ),
        'some-smiles': '༼ つ ⚈⚬⚈ ༽つ  ᓚᘏᗢ'
    }


@app.post('/post')
def get_post(db: Session = Depends(get_db)) -> Timestamp:
    db_val = models.Timestamps(timestamp=int(datetime.datetime.now().timestamp()))
    db.add(db_val)
    db.commit()
    db.refresh(db_val)
    return db_val


@app.get('/dog', response_model=List[Dog])
def get_dogs(
        kind: DogType | None = None,
        db: Session = Depends(get_db),
) -> List[Dog]:
    result = db.query(models.Dogs)
    if kind:
        result = db.query(models.Dogs).filter(models.Dogs.kind == kind)
    # тут и ниже где результат возвращается из бд не поняла,
    # нужно ли преобразовывать модель таблицы в pydantic
    # кажется что тк они одинаковые смысла нет, но ide понятно ругается на типы((
    return result.all()


@app.post('/dog', response_model=Dog)
def create_dog(dog: Dog, db: Session = Depends(get_db)) -> Dog:
    existing_dog = db.query(models.Dogs).filter(models.Dogs.pk == dog.pk).first()
    if dog.pk < 0:
        raise HTTPException(
            status_code=400,
            detail='Please stop killing me. Use pk >= 0',
        )
    if existing_dog:
        max_pk = db.query(func.max(models.Dogs.pk)).first()
        raise HTTPException(
            status_code=409,
            detail=(
                f'Dog with pk {dog.pk} already exists. You can use pk more than {max_pk}'
            ),
        )
    db_dog = models.Dogs(**dog.model_dump())
    db.add(db_dog)
    db.commit()
    db.refresh(db_dog)
    return db_dog


@app.get('/dog/{pk}', response_model=Dog)
def get_dog_by_pk(pk: int, db: Session = Depends(get_db)) -> Dog:
    db_dog = db.query(models.Dogs).filter(models.Dogs.pk == pk).first()
    if not db_dog:
        raise HTTPException(status_code=404, detail=f'No dog with {pk=}')
    return db_dog


@app.patch('/dog/{pk}')
def update_dog_by_pk(pk: int, dog: Dog, db: Session = Depends(get_db)) -> Dog:
    dog_query = db.query(models.Dogs).filter(models.Dogs.pk == pk)
    db_dog = dog_query.first()
    if not db_dog:
        raise HTTPException(status_code=404, detail=f'No dog with {pk=}')
    if pk != dog.pk:
        raise HTTPException(
            status_code=400,
            detail=(
                f"That's not fair. Your pk in request - {pk}, but pk in body - {dog.pk}. "
                f"They should be the same",
            ),
        )
    update = dog.model_dump()
    dog_query.update(update, synchronize_session=False)
    db.commit()
    db.refresh(db_dog)
    return db_dog
