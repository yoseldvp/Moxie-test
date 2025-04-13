from sqlmodel import Session, create_engine, select
from sqlmodel.main import SQLModel
from config import config
import typer

# Not pretty. But needed due the order of operations by SQLModel
from models import *


# To be honest, I'm just showing off. It is always cool to have a CLI Tool :)
app = typer.Typer()
engine = create_engine(str(config.SQLALCHEMY_DATABASE_URI), echo=True)

@app.command()
def create() -> None:
  try:
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
      session.exec(select(1))
  except Exception as e:
    print("Hey!, what's going on here?.........")
    raise e


@app.command()
def drop() -> None:
  try:
    SQLModel.metadata.drop_all(engine)
  except Exception as e:
    print("Hey!, what's going on here?.........")
    raise e


if __name__ == "__main__":
  app()
