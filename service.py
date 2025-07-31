import db.repo as repo
import utils
from db.models import Game, Stat


class ServiceGame:
    __repo = repo.GameRepo()

    def save_game(self, game: Game):
        self.__repo.save_entry(game)

    def delete_game(self, game: Game):
        self.__repo.delete_entry(game)

    def get_token(self, token: str) -> Game | None:
        return self.__repo.get_entry_by_token(token)

    def get_device(self, device: str) -> Game | None:
        return self.__repo.get_entry_by_device(device)

    def get_active_game(self, device: str, token: str) -> Game | None:
        return self.get_device(device) if token == "" else self.get_token(token)

    def get_history(self, device: str, start: str) -> list[Game]:
        epoch = utils.string_epoch(start)
        return self.__repo.get_history(device, epoch)

    def delete_history(self, device: str, token: str | None) -> bool:
        return self.__repo.delete_history(device, token)


class ServiceStat:
    __repo = repo.StatRepo()

    def save_stat(self, stat: Stat):
        self.__repo.save_entry(stat)

    def get_stat(self, device: str) -> Stat | None:
        return self.__repo.get_entry(device)

    def update_stat(self, device: str, action: str):
        userStat = self.get_stat(device)

        if userStat is None:
            userStat = Stat(device=device, wins=0, loses=0, draws=0)

        match action:
            case "win":
                userStat.wins += 1
            case "loss":
                userStat.loses += 1
            case "draw":
                userStat.draws += 1

        self.save_stat(userStat)

