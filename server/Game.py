
from Utils import ok_response, error_response, AppException, AppResponse
import random
import uuid
import copy
import json

CARD_PAIRS_QUANTITY = 20
games = []

def generate_card_map():
    def generate_card_pair(i):
        card = { "card_id": str(uuid.uuid4()), "card_pair": i, "turn_turned": False }
        return [card, card.copy()]

    cards = [generate_card_pair(i + 1) for i in range(CARD_PAIRS_QUANTITY)]
    cards = [card for card_pair in cards for card in card_pair] # Flatten

    for i in range(len(cards)):
        random_index = random.randint(0, len(cards) - 1)
        card_to_shuffle_with = cards[random_index]
        cards[random_index] = cards[i]
        cards[i] = card_to_shuffle_with

    return cards

class Game:
	def __init__(self, game_id, creator_player_id, creator_socket):
		self.game_id = game_id
		self.connected_players = [creator_player_id]
		self.players_sockets = [creator_socket]
		self.cards = generate_card_map()
		
		self.started = False
		self.current_player_turn = None 

		def initialize_game(self):
			if self.connected_players != 2:
				raise AppException("Não há jogadores suficientes para começar a partida")
			self.current_player_turn = random.choice(self.connected_players)
			self.started = True
        
		for j in range(8):
			for i in range(5):
				print(self.cards[j * 5 + i]['card_pair'], end=" ")
			print("")

	def as_dict(self):
		cp = copy.copy(self)
		cp.players_sockets = None
		return cp.__dict__

def get_game_list():
	return [{"game_id": game.game_id, "connected_players": game.connected_players} for game in games]
# --------------------------------

def get_games_info(socket_data):
	return AppResponse(payload={"games": get_game_list()})

# --------------------------------

def game_create(socket_data):
	print("Create")
	game = Game(socket_data['payload']['game_id'], socket_data['client_id'], socket_data['socket'])
	games.append(game)
	return AppResponse(payload=game.as_dict(), server_emit_route="/game/update", server_emit_payload=get_game_list())

def game_join(socket_data):
	print("Join")
	game_id = socket_data['payload']['game_id']
	game = next(filter(lambda game: game.game_id == game_id, games), None)
	if not game:
		raise AppException("Não foi possível encontrar o jogo")
	
	if len(game.connected_players) == 2:
		raise AppException("Número de jogadores máximo alcançado")
	
	game.connected_players.append(socket_data['client_id'])
	game.players_sockets.append(socket_data['socket'])

	game.initialize_game()

	return AppResponse( 
		payload=game, 
		server_emit_route=["/game/update", "/game/start/" + game_id], 
		server_emit_payload=[get_game_list(), game.as_dict()]
	)
