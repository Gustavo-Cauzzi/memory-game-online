import controller.client_socket as socket
import uuid

current_game = {
    'cards': [],
    'game': None
}

def exit_game():
    socket.close_socket()

# --------------

def create_game(game_id):
    response = socket.send_data('/game/create', { 'game_id': game_id })
    current_game['game'] = response  # TODO use only current_game['game']
    current_game['cards'] = response['cards']

def join_game(game_id):
    response = socket.send_data('/game/join', { 'game_id': game_id })
    current_game['game'] = response
    current_game['cards'] = response['cards'] # TODO use only current_game['game']

def card_turn(game_id, card_id):
    socket.send_data("/game/card/turn", { 'game_id': game_id, "card_id": card_id })

# --------------

def get_games():
    response = socket.send_data('/game')
    return response['games']

def on_new_game(on_new_game_added):
    socket.on('/game/update', on_new_game_added)

def on_player_joined(game_id, event):
    socket.on("/game/start/" + game_id, event)

def on_card_turned(game_id, event):
    socket.on(f"/game/{game_id}/turn", event)

