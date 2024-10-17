from sqlalchemy import create_engine, select, delete, and_
from sqlalchemy.orm import Session

from db.models import Game, BaseModel, Stat

# Datasource
engine = create_engine("sqlite:///main.sqlite", echo=False)
BaseModel.metadata.create_all(bind=engine)


# Game Dao
class GameDao:
    @staticmethod
    def save_entry(entry: Game):
        global engine
        with Session(engine) as session:
            session.merge(entry)
            session.commit()

    @staticmethod
    def delete_entry(entry: Game):
        global engine
        with Session(engine) as session:
            session.delete(entry)
            session.commit()

    @staticmethod
    def get_entry_by_token(token: str) -> Game | None:
        global engine
        retval = None
        with Session(engine) as session:
            stmt = select(Game).where(and_(Game.token == token, Game.status == "playing"))
            retval = session.scalars(stmt).first()
        return retval

    @staticmethod
    def get_entry_by_device(device: str) -> Game | None:
        global engine
        retval = None
        with Session(engine) as session:
            stmt = select(Game).where(and_(Game.device == device, Game.status == "playing"))
            retval = session.scalars(stmt).first()
        return retval

    @staticmethod
    def get_history(device: str, epoch: int) -> list[Game]:
        global engine
        retval = None
        with Session(engine) as session:
            stmt = select(Game).where(and_(Game.device == device, Game.startedOn >= epoch, Game.status != "playing"))
            retval = list(session.scalars(stmt))
        return retval

    @staticmethod
    def delete_history(device: str, token: str | None) -> bool:
        global engine
        with Session(engine) as session:
            if token is None:
                stmt = delete(Game).where(and_(Game.device == device, Game.status != "playing"))
            else:
                stmt = delete(Game).where(and_(Game.token == token, Game.status != "playing"))
            session.execute(stmt)
            session.commit()
        return True


# Stat Dao
class StatDao:
    @staticmethod
    def save_entry(entry: Stat):
        global engine
        with Session(engine) as session:
            session.add(entry)
            session.commit()
            session.refresh(entry)

    @staticmethod
    def get_entry(device: str) -> Stat | None:
        global engine
        retval = None
        with Session(engine) as session:
            stmt = select(Stat).where(Stat.device == device)
            retval = session.scalars(stmt).first()
        return retval
