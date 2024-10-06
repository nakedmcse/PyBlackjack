from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session

import models

# Datasource
engine = create_engine("sqlite:///main.sqlite", echo=False)
models.BaseModel.metadata.create_all(bind=engine)


# Game Dao
class GameDao:
    def save_entry(self, entry: models.Game):
        global engine
        with Session(engine) as session:
            session.merge(entry)
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
            stmt = select(models.Game).where(and_(models.Game.token == token, models.Game.status == "playing"))
            retval = session.scalars(stmt).first()
        return retval

    def get_entry_by_device(self, device: str) -> models.Game | None:
        global engine
        retval = None
        with Session(engine) as session:
            stmt = select(models.Game).where(and_(models.Game.device == device, models.Game.status == "playing"))
            retval = session.scalars(stmt).first()
        return retval


# Stat Dao
class StatDao:
    def save_entry(self, entry: models.Stat):
        global engine
        with Session(engine) as session:
            session.add(entry)
            session.commit()
            session.refresh(entry)

    def get_entry(self, device: str) -> models.Stat | None:
        global engine
        retval = None
        with Session(engine) as session:
            stmt = select(models.Stat).where(models.Stat.device == device)
            retval = session.scalars(stmt).first()
        return retval
