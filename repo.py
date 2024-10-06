import dao
import models


class GameRepo:
    __dao = dao.GameDao()

    def save_entry(self, entry: models.Game):
        self.__dao.save_entry(entry)

    def delete_entry(self, entry: models.Game):
        self.__dao.delete_entry(entry)

    def get_entry_by_token(self, token: str) -> models.Game | None:
        return self.__dao.get_entry_by_token(token)

    def get_entry_by_device(self, device: str) -> models.Game | None:
        return self.__dao.get_entry_by_device(device)


class StatRepo:
    __dao = dao.StatDao()

    def save_entry(self, entry: models.Stat):
        self.__dao.save_entry(entry)

    def get_entry(self, device: str) -> models.Stat | None:
        return self.__dao.get_entry(device)
