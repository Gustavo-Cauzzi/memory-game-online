import controller.socket as socket
import uuid

current_game = {
    'cards': []
}

def create_game(game_id):
    response = socket.send_data('/game/create', { 'game_id': game_id })
    current_game['cards'] = response['cards']

def join_game(game_id):
    response = socket.send_data('/game/join', { 'game_id': game_id })
    current_game['cards'] = response['cards']

    