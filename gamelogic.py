import random
import re

import models
import service

suits = ['\u2660', '\u2663', '\u2665', '\u2666']
faces = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A', 'J', 'Q', 'K']

game_service = service.ServiceGame()
stat_service = service.ServiceStat()


def create_deck(game: models.Game):
    for suit in suits:
        for face in faces:
            game.deck.append(face + suit)
    for i in range(len(game.deck)):
        j = random.randrange(0,len(game.deck))
        game.deck[i], game.deck[j] = game.deck[j], game.deck[i]


def deal(game: models.Game):
    game.playerCards.append(game.deck.pop())
    game.dealerCards.append(game.deck.pop())
    game.playerCards.append(game.deck.pop())
    game.dealerCards.append(game.deck.pop())


def hit(game: models.Game) -> models.ResponseMsg:
    game.playerCards.append(game.deck.pop())
    print(f'HIT: {game.token}')
    if score(game.playerCards) > 21:
        game.status = "Bust"
        print('BUST')

    resp = models.ResponseMsg(game.token, game.device, game.playerCards, [], score(game.playerCards), 0, game.status)
    if game.status == "Bust":
        stat_service.update_stat(game.device, "loss")
    game_service.save_game(game)
    return resp


def stay(game: models.Game) -> models.ResponseMsg:
    while score(game.dealerCards < 17):
        game.dealerCards.append(game.deck.pop())

    print(f'STAY: {game.token}')
    playerScore = score(game.playerCards)
    dealerScore = score(game.dealerCards)
    if dealerScore > 21:
        game.status = "Dealer Bust"
        print("DEALER BUST")
        stat_service.update_stat(game.device, "win")
    else:
        totalScore = playerScore - dealerScore
        gameState = "draw" if totalScore == 0 else "win" if totalScore > 0 else "loss"
        game.status = "Draw" if gameState == "draw" else "Player Wins" if gameState == "win" else "Dealer Wins"
        print(game.status.upper())
        stat_service.update_stat(game.device, gameState)

    resp = models.ResponseMsg(game.token, game.device, game.playerCards, game.dealerCards, score(game.playerCards), score(game.dealerCards), game.status)
    game_service.save_game(game)
    return resp


def score(cards: list[str]) -> int:
    retval = 0
    hasAce = False
    for card in cards:
        retval += card_value(card)
        if 'A' in card:
            hasAce = True
    if hasAce:
        for card in cards:
            if 'A' in card:
                retval += 1 if retval + 11 > 21 else 11
    return retval


def card_value(card: str) -> int:
    numeric = ''.join(re.findall(r'\d+',card))
    if numeric:
        return int(numeric)
    elif any(char in card for char in ['J','Q','K']):
        return 10