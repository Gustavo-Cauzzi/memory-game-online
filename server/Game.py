
from Utils import AppException, AppResponse, find
import random
import uuid
import copy
import json

CARD_PAIRS_QUANTITY = 20
games = []

def generate_card_map():
	def generate_card_pair(i):
		card = { "card_id": str(uuid.uuid4()), "card_pair": i, "turn_turned": False }
		cp = card.copy()
		cp['card_id'] = str(uuid.uuid4())
		return [card, cp]

	cards = [generate_card_pair(i + 1) for i in range(CARD_PAIRS_QUANTITY)]
	cards = [card for card_pair in cards for card in card_pair] # Flatten

	for i in range(len(cards)):
		random_index = random.randint(0, len(cards) - 1)
		card_to_shuffle_with = cards[random_index]
		cards[random_index] = cards[i]
		cards[i] = card_to_shuffle_with

	return cards

class Game:
	def __init__(self, game_id, creator_player_id):
		self.game_id = game_id
		self.connected_players = [creator_player_id]
		self.cards = generate_card_map()
		
		self.started = False
		self.current_player_turn = None 
		self.has_a_card_turned = False
		
		for j in range(8):
			for i in range(5):
				print(self.cards[j * 5 + i]['card_pair'], end=" ")
			print("")

	def as_dict(self):
		cp = copy.copy(self)
		return cp.__dict__
	
	def get_other_player_id(self, client_id):
		other_player_id = find(lambda c_id: c_id != client_id, self.connected_players)
		if not other_player_id:
			raise AppException("[FATAL ERROR] Não foi possível encontrar o outro jogador da partida")
		return other_player_id
	
	def initialize_game(self):
		if len(self.connected_players) != 2:
			raise AppException("Não há jogadores suficientes para começar a partida")
		self.current_player_turn = random.choice(self.connected_players)
		self.started = True
	
	def turn_card(self, card_id, client_id):
		if self.current_player_turn != client_id:
			raise AppException("Não é a sua vez!")
		
		if not find(lambda card: card['card_id'] == card_id, self.cards):
			raise AppException(f"Cartda de id {card_id} não existe")

		if self.has_a_card_turned:
			other_player_id = self.get_other_player_id(client_id)
			self.current_player_turn = other_player_id
		
		self.has_a_card_turned = not self.has_a_card_turned
		return self


def get_game_list():
	return [{"game_id": game.game_id, "connected_players": game.connected_players} for game in games]

def find_game(game_id) -> Game:
	return find(lambda game: game.game_id == game_id, games)

def find_game_or_raise(game_id) -> Game:
	game = find_game(game_id)
	if not game:
		raise AppException(f'Jogo com id {game_id} não encontrado')
	return game

# --------------------------------

def get_games_info(connection_data):
	return AppResponse(
		payload={"games": get_game_list()},
		connection_data=connection_data
	).response

# --------------------------------

def game_create(connection_data):
	game_id = connection_data['payload']['game_id']
	game_exists = find_game(game_id)
	if game_exists:
		raise AppException("Id já existe")
	game = Game(game_id, connection_data['client_id'])
	games.append(game)
	return AppResponse(
		payload=game.as_dict(), 
		server_emit_route="/game/update", 
		server_emit_payload=get_game_list(),
		connection_data=connection_data
	).response

def game_join(connection_data):
	game_id = connection_data['payload']['game_id']
	game = find_game_or_raise(game_id)
	
	if len(game.connected_players) == 2:
		raise AppException("Número de jogadores máximo alcançado")
	
	game.connected_players.append(connection_data['client_id'])

	game.initialize_game()

	return AppResponse( 
		payload=game.as_dict(), 
		server_emit_route=["/game/update", "/game/start/" + game_id], 
		server_emit_payload=[get_game_list(), game.as_dict()],
		connection_data=connection_data
	).response

def game_card_turned(connection_data):
	client_id = connection_data['client_id']
	game_id = connection_data['payload']['game_id']
	card_id = connection_data['payload']['card_id']
	game = find_game_or_raise(game_id)

	game.turn_card(card_id, client_id)

	return AppResponse(
		payload=None, 
		server_emit_payload={ 'card_id': card_id, 'turn_changed': client_id != game.current_player_turn },
		server_emit_route=f'/game/{game_id}/turn',
		to=game.get_other_player_id(client_id),
		connection_data=connection_data
	).response
