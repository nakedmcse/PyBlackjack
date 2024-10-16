import json
import os
import time
import uuid

from dotenv import load_dotenv
from flasgger import Swagger, swag_from
from flask import Flask, request, Response
from waitress import serve

import gamelogic
import service
import utils
from db.models import Game, ResponseMsg, ErrorMsg, StatsMsg
from swagger.config import template

load_dotenv()

game_service = service.ServiceGame()
stat_service = service.ServiceStat()

blackjack_api = Flask(__name__)
blackjack_api.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
swagger = Swagger(blackjack_api, template=template)


# Disable Cache
@blackjack_api.after_request
def no_cache(req):
    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    return req


# Deal endpoint
@blackjack_api.route('/deal', methods=['POST'])
@swag_from('swagger/deal.yml')
def deal():
    device_id = utils.device_hash(request)
    ret_game = game_service.get_device(device_id)

    if ret_game is None:
        ret_game = Game(token=str(uuid.uuid4()), device=device_id, status="playing", startedOn=int(time.time()),
                        deck=[], dealerCards=[], playerCards=[])
        gamelogic.create_deck(ret_game)
        gamelogic.deal(ret_game)
        game_service.save_game(ret_game)
        print(f'Created new game for {device_id}')

    resp = ResponseMsg(token=ret_game.token, device=ret_game.device, cards=ret_game.playerCards, dealerCards=[],
                       handValue=gamelogic.score(ret_game.playerCards), dealerValue=0, status=ret_game.status)
    return Response(json.dumps(resp.__dict__, ensure_ascii=False), content_type="application/json; charset=utf-8")


# Hit endpoint
@blackjack_api.route('/hit', methods=['POST'])
@swag_from('swagger/hit.yml')
def hit():
    device_id = utils.device_hash(request)
    token = request.args.get('token', '')
    ret_game = game_service.get_active_game(token=token, device=device_id)
    if ret_game is None:
        return Response(json.dumps(ErrorMsg(status=400, message="Missing Game").__dict__),
                        content_type="application/json; charset=utf-8", status=400)
    resp = gamelogic.hit(ret_game)
    return Response(json.dumps(resp.__dict__, ensure_ascii=False), content_type="application/json; charset=utf-8")


# Stay endpoint
@blackjack_api.route('/stay', methods=['POST'])
@swag_from('swagger/stay.yml')
def stay():
    device_id = utils.device_hash(request)
    token = request.args.get('token', '')
    ret_game = game_service.get_active_game(token=token, device=device_id)
    if ret_game is None:
        return Response(json.dumps(ErrorMsg(status=400, message="Missing Game").__dict__),
                        content_type="application/json; charset=utf-8", status=400)
    resp = gamelogic.stay(ret_game)
    return Response(json.dumps(resp.__dict__, ensure_ascii=False), content_type="application/json; charset=utf-8")


# Stats endpoint
@blackjack_api.route('/stats', methods=['GET'])
@swag_from('swagger/stats.yml')
def stats():
    device_id = utils.device_hash(request)
    user_stats = gamelogic.stats(device_id)
    if user_stats is None:
        return Response(json.dumps(ErrorMsg(status=400, message="Missing Device").__dict__),
                        content_type="application/json; charset=utf-8", status=400)
    resp = StatsMsg(wins=user_stats.wins, loses=user_stats.loses, draws=user_stats.draws)
    return Response(json.dumps(resp.__dict__, ensure_ascii=False), content_type="application/json; charset=utf-8")


# History endpoint
@blackjack_api.route('/history', methods=['GET'])
@swag_from('swagger/history.yml')
def history():
    device_id = utils.device_hash(request)
    start = request.args.get('start', '')
    games = game_service.get_history(device_id, start)
    resp = [ResponseMsg(x.token, x.device, x.playerCards, x.dealerCards,
                        gamelogic.score(x.playerCards), gamelogic.score(x.dealerCards), x.status).__dict__
            for x in games]
    return Response(json.dumps(resp, ensure_ascii=False), content_type="application/json; charset=utf-8")


# Delete endpoint
@blackjack_api.route('/delete', defaults={'token': None}, methods=['DELETE'])
@blackjack_api.route('/delete/<token>', methods=['DELETE'])
@swag_from('swagger/delete.yml')
def delete(token):
    device_id = utils.device_hash(request)
    sure = request.args.get('sure', '')
    if sure != 'true':
        return Response(json.dumps(ErrorMsg(status=400, message="Sure must be set to true").__dict__),
                        content_type="application/json; charset=utf-8", status=400)
    resp = game_service.delete_history(device_id, token)
    return Response(json.dumps(resp, ensure_ascii=False), content_type="application/json; charset=utf-8")


if __name__ == '__main__':
    if os.getenv('ENV').upper() == 'DEV':
        blackjack_api.run(port=os.getenv('PORT'), debug=(os.getenv('DEBUG') == 'true'))
    else:
        serve(blackjack_api, port=os.getenv('PORT'))
