from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

import models

# Datasource
engine = create_engine("sqlite://", echo=False)
models.BaseModel.metadata.create_all(bind=engine)


# Game Dao
class GameDao:
    def save_entry(self, entry: models.Game):
        global engine
        with Session(engine) as session:
            session.add(entry)
            session.commit()

    def delete_entry(self, entry: models.Game):
        global engine
        with Session(engine) as session:
            session.delete(entry)
            session.commit()

    def get_entry_by_token(self, token: str) -> models.Game | None:
        global engine
        retval = None
        with Session(engine) as session:
            stmt = select(models.Game).where(models.Game.token == token)
            retval = session.scalars(stmt).first()
        return retval

    def get_entry_by_device(self, device: str) -> models.Game | None:
        global engine
        retval = None
        with Session(engine) as session:
            stmt = select(models.Game).where(models.Game.device == device)
            retval = session.scalars(stmt).first()
        return retval


# Stat Dao
class StatDao:
    def save_entry(self, entry: models.Stat):
        global engine
        with Session(engine) as session:
            session.add(entry)
            session.commit()

    def get_entry(self, device: str) -> models.Stat | None:
        global engine
        retval = None
        with Session(engine) as session:
            stmt = select(models.Stat).where(models.Stat.device == device)
            retval = session.scalars(stmt).first()
        return retval
