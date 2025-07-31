import os
import time
import uuid
import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse
from typing import Optional

import gamelogic
import service
import utils
from db.models import Game, ResponseMsg, ErrorMsg, StatsMsg

load_dotenv()

game_service = service.ServiceGame()
stat_service = service.ServiceStat()

blackjack_api = FastAPI()

# Deal endpoint
@blackjack_api.post('/deal')
def deal(request: Request):
    device_id = utils.device_hash(request)
    utils.log('DEAL', device_id)
    ret_game = game_service.get_device(device_id)

    if ret_game is None:
        ret_game = Game(token=str(uuid.uuid4()), device=device_id, status="playing", startedOn=int(time.time()),
                        deck=[], dealerCards=[], playerCards=[])
        gamelogic.create_deck(ret_game)
        gamelogic.deal(ret_game)
        game_service.save_game(ret_game)
        print(f'Created new game for {device_id}')

    return ResponseMsg(token=ret_game.token, device=ret_game.device, cards=ret_game.playerCards, dealerCards=[],
                       handValue=gamelogic.score(ret_game.playerCards), dealerValue=0, status=ret_game.status)


# Hit endpoint
@blackjack_api.post('/hit')
@blackjack_api.post('/hit/{token}')
def hit(request: Request, token: Optional[str] = ''):
    device_id = utils.device_hash(request)
    utils.log('HIT', device_id, token)
    ret_game = game_service.get_active_game(token=token, device=device_id)
    if ret_game is None:
        return JSONResponse(status_code = 400, content = ErrorMsg(status=400, message="Missing Game").__dict__)
    return gamelogic.hit(ret_game)


# Stay endpoint
@blackjack_api.post('/stay')
@blackjack_api.post('/stay/{token}')
def stay(request: Request, token: Optional[str] = ''):
    device_id = utils.device_hash(request)
    utils.log('STAY', device_id, token)
    ret_game = game_service.get_active_game(token=token, device=device_id)
    if ret_game is None:
        return JSONResponse(status_code = 400, content=ErrorMsg(status=400, message="Missing Game").__dict__)
    return gamelogic.stay(ret_game)


# Stats endpoint
@blackjack_api.get('/stats')
def stats(request: Request):
    device_id = utils.device_hash(request)
    utils.log('STATS', device_id)
    user_stats = gamelogic.stats(device_id)
    if user_stats is None:
        return JSONResponse(status_code = 400, content = ErrorMsg(status=400, message="Missing Device").__dict__)
    return StatsMsg(wins=user_stats.wins, loses=user_stats.loses, draws=user_stats.draws)


# History endpoint
@blackjack_api.get('/history')
def history(request: Request, start: str = Query('')):
    device_id = utils.device_hash(request)
    utils.log('HISTORY', device_id, '', start)
    games = game_service.get_history(device_id, start)
    resp = [ResponseMsg(x.token, x.device, x.playerCards, x.dealerCards,
                        gamelogic.score(x.playerCards), gamelogic.score(x.dealerCards), x.status)
            for x in games]
    return resp


# Delete endpoint
@blackjack_api.delete('/delete')
@blackjack_api.delete('/delete/{token}')
def delete(request: Request, token: Optional[str] = '', sure: str = Query(None)):
    device_id = utils.device_hash(request)
    if sure != 'true':
        return JSONResponse(status_code = 400, content = ErrorMsg(status=400, message="Sure must be set to true").__dict__)
    utils.log('DELETE', device_id, token)
    return game_service.delete_history(device_id, token)


if __name__ == '__main__':
    if os.getenv('ENV').upper() == 'DEV':
        uvicorn.run("blackjack:blackjack_api", port=int(os.getenv('PORT')), log_level="trace")
    else:
        uvicorn.run("blackjack:blackjack_api", port=int(os.getenv('PORT')))
