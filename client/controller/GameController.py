import controller.client_connection as connection
import uuid

current_game = {
    'cards': [],
    'game': None
}

def exit_game():
    connection.close_connection()

# --------------

def create_game(game_id):
    response = connection.send_data('game_create', { 'game_id': game_id })
    print(f'response: {response}')
    current_game['game'] = response  # TODO use only current_game['game']
    current_game['cards'] = response['cards']

def join_game(game_id):
    response = connection.send_data('game_join', { 'game_id': game_id })
    current_game['game'] = response
    current_game['cards'] = response['cards'] # TODO use only current_game['game']

def card_turn(game_id, card_id):
    connection.send_data("game_card_turn", { 'game_id': game_id, "card_id": card_id })

# --------------

def get_games():
    response = connection.send_data('game')
    return response['games']

def on_new_game(on_new_game_added):
    connection.on('/game/update', on_new_game_added)

def on_player_joined(game_id, event):
    connection.on("/game/start/" + game_id, event)

def on_card_turned(game_id, event):
    connection.on(f"/game/{game_id}/turn", event)

