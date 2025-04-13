from fastapi import Depends
from sqlmodel import Session
from sqlalchemy import create_engine
from typing import Annotated

from .config import config

engine = create_engine(str(config.SQLALCHEMY_DATABASE_URI), echo=True)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
