import time
import uuid

import gamelogic
import models
import service

game_service = service.ServiceGame()
stat_service = service.ServiceStat()

# Add some games
token_1 = str(uuid.uuid4())
new_game_1 = models.Game(token=token_1, device="device_1", status="playing", startedOn=int(time.time()),
                         deck=[], dealerCards=[], playerCards=[])
gamelogic.create_deck(new_game_1)
gamelogic.deal(new_game_1)
game_service.save_game(new_game_1)

token_2 = str(uuid.uuid4())
new_game_2 = models.Game(token=token_2, device="device_2", status="playing", startedOn=int(time.time()),
                         deck=[], dealerCards=[], playerCards=[])
gamelogic.create_deck(new_game_2)
gamelogic.deal(new_game_2)
game_service.save_game(new_game_2)

token_3 = str(uuid.uuid4())
new_game_3 = models.Game(token=token_3, device="device_3", status="playing", startedOn=int(time.time()),
                         deck=[], dealerCards=[], playerCards=[])
gamelogic.create_deck(new_game_3)
gamelogic.deal(new_game_3)
game_service.save_game(new_game_3)

# Add some stats
stat_1 = models.Stat(device="device_1", wins=1, loses=1, draws=1)
stat_service.save_stat(stat_1)
stat_service.update_stat("device_2","win")

# Get game by token
game_by_token = game_service.get_token(token_3)
print(game_by_token)

# Get game by device
game_by_device = game_service.get_device("device_2")
print(game_by_device)

# Get stats
stats_dev1 = stat_service.get_stat("device_1")
print(stats_dev1)
stats_dev2 = stat_service.get_stat("device_2")
print(stats_dev2)