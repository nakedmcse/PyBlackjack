from sqlalchemy import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    pass


# Entities
class Game(BaseModel):
    __tablename__ = "games"
    token: Mapped[str] = mapped_column(primary_key=True)
    device: Mapped[str]
    status: Mapped[str]
    startedOn: Mapped[int]
    deck: Mapped[list] = mapped_column(JSON)
    dealerCards: Mapped[list] = mapped_column(JSON)
    playerCards: Mapped[list] = mapped_column(JSON)

    def __repr__(self):
        return f'token:{self.token}, device:{self.device}, status:{self.status}, startedOn:{self.startedOn},\ndeck:{self.deck},\nplayerCards:{self.playerCards}'


class Stat(BaseModel):
    __tablename__ = "stats"
    device: Mapped[str] = mapped_column(primary_key=True)
    wins: Mapped[int]
    loses: Mapped[int]
    draws: Mapped[int]

    def __repr__(self):
        return f'device:{self.device}, wins:{self.wins}, loses:{self.loses}, draws:{self.draws}'


# Messages
class ErrorMsg:
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message


class ResponseMsg:
    def __init__(self, token: str, device: str, cards: list[str], dealerCards: list[str], handValue: int, dealerValue: int, status: str):
        self.token = token
        self.device = device
        self.cards = cards
        self.dealerCards = dealerCards
        self.handValue = handValue
        self.dealerValue = dealerValue
        self.status = status


class StatsMsg:
    def __init__(self, wins: int, loses: int, draws: int):
        self.wins = wins
        self.loses = loses
        self.draws = draws