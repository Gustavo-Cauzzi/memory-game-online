import controller.client_socket as socket
import uuid

current_game = {
    'cards': []
}

def exit_game():
    print("1")
    socket.close_socket()
    print("2")

# --------------

def get_games():
    response = socket.send_data('/game')
    return response['games']

# --------------

def create_game(game_id):
    response = socket.send_data('/game/create', { 'game_id': game_id })
    current_game['cards'] = response['cards']

def join_game(game_id):
    response = socket.send_data('/game/join', { 'game_id': game_id })
    current_game['cards'] = response['cards']

    