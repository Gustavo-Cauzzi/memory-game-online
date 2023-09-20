import controller.client_socket as socket
import uuid

current_game = {
    'cards': []
}

def exit_game():
    socket.close_socket()

# --------------

def get_games():
    response = socket.send_data('/game')
    return response['games']

def on_new_game(on_new_game_added):
    socket.on('/game/update', on_new_game_added)

# --------------

def create_game(game_id):
    response = socket.send_data('/game/create', { 'game_id': game_id })
    current_game['cards'] = response['cards']

def join_game(game_id):
    response = socket.send_data('/game/join', { 'game_id': game_id })
    current_game['cards'] = response['cards']

    