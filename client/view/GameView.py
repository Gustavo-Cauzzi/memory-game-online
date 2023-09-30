import tkinter as tk
import threading
import controller.GameController as GameController
from config.constants import Results, results_text, CARD_COLUMNS, CARD_PAIRS_QUANTITY
from controller.client_socket import client_id

class GameView:
    def __init__(self, root):
        # TK
        self.root = root
        self.cards_frame = None
        self.points_frame = None
        self.turn_status_frame = None
        self.frames = [self.cards_frame, self.points_frame]

        # Game
        self.game = GameController.current_game['game']

        # UI Behaviours
        self.block_actions = not self.game['started']

        self.current_player_turn = False if not self.game['started'] else self.game['current_player_turn'] == client_id
        self.has_chosen_a_card = False
        self.chosen_card = None
        self.current_player_points = 0
        self.other_player_points = 0
        self.game_has_ended = False

        self.setup_game_socket_events()
        self.render()

    def setup_game_socket_events(self):
        if not self.game['started']:
            GameController.on_player_joined(self.game['game_id'], self.other_player_joined)
        GameController.on_card_turned(self.game['game_id'], self.on_card_clicked_remotely)  
        # GameController.

    # Listeners ----------

    def other_player_joined(self, updated_game):
        self.game = updated_game
        self.block_actions = not self.game['started']
        self.current_player_turn = self.game['current_player_turn'] == client_id
        self.render()

    def on_card_clicked_remotely(self, payload):
        self.current_player_turn = self.has_chosen_a_card
        self.card_click(payload['card_id'], remote_click=True)


    # --------------------

    def render_points(self, result):
        if result:
            label = tk.Label(self.points_frame, text=results_text[result])
            label.pack()
            return
            
        label = tk.Label(self.points_frame, text=f'Seus pontos: {self.current_player_points}')
        label.grid(row=0, column=0)
        label = tk.Label(self.points_frame, text=f'| Adversário: {self.other_player_points}')
        label.grid(row=0, column=1)

    def render_cards(self):
        for idx, card in enumerate(self.game['cards']):
            tk.Button(
                self.cards_frame, 
                text=card['card_pair'] if card['turn_turned'] else 'X', 
                padx=10, 
                pady=10, 
                command=lambda card_id=card['card_id']: self.card_click(card_id)
            )\
                .grid(row=idx // CARD_COLUMNS, column=idx % CARD_COLUMNS)

    def check_for_winner(self):
        if self.current_player_points + self.other_player_points == CARD_PAIRS_QUANTITY:
            if self.current_player_points == self.other_player_points:
                return Results.DRAW
            if self.current_player_points > self.other_player_points:
                return Results.YOU_WON
            return Results.OTHER_WON
        return None

    def render(self):
        def destroy_frame(frame):
            if frame is not None:
                frame.destroy()
        
        destroy_frame(self.points_frame)
        destroy_frame(self.cards_frame)
        destroy_frame(self.turn_status_frame)
        self.points_frame = tk.Frame(self.root)
        self.turn_status_frame = tk.Frame(self.root)
        self.cards_frame = tk.Frame(self.root)
       
        if not self.game['started']:
            label = tk.Label(self.points_frame, text="Aguardando outro jogador...")
            label.pack()
        else: 
            result = self.check_for_winner()
            self.render_points(result)
            if result:
                self.game_has_ended = True
                self.block_actions = True

        self.render_current_player_turn_status(self.turn_status_frame)
        self.render_cards()

        for i in range(CARD_COLUMNS):
            self.cards_frame.grid_columnconfigure(i, minsize=40)
            self.cards_frame.grid_rowconfigure(i, minsize=40)

        self.points_frame.pack()
        self.turn_status_frame.pack()
        self.cards_frame.pack()

    def render_current_player_turn_status(self, frame_to_append):
        if not self.game['started'] or self.game_has_ended:
            return
        label = tk.Label(frame_to_append, text="Sua vez" if self.current_player_turn else "Vez do outro jogador")
        label.pack()

    def card_click(self, card_id, remote_click = False):
        if not remote_click and (not self.current_player_turn or self.block_actions):
            return

        card = next(filter(lambda card: card['card_id'] == card_id, self.game['cards']))
        if not card:
            print(f"Não foi possível encontrar a carta {card_id}")
            return
        
        if card['turn_turned']:
            return

        if not remote_click:
            GameController.card_turn(self.game['game_id'], card['card_id'])        

        card['turn_turned'] = not card['turn_turned']

        if self.has_chosen_a_card: # Player already turned one card and this is the second one
            self.has_chosen_a_card = False

            if not remote_click:
                self.current_player_turn = False

            if card['card_pair'] == self.chosen_card['card_pair']:
                if remote_click:
                    self.other_player_points = self.other_player_points + 1
                else:
                    self.current_player_points = self.current_player_points + 1
            else:
                self.block_actions = True
                def reset_curently_turned_pair():
                    card['turn_turned'] = False
                    self.chosen_card['turn_turned'] = False
                    self.chosen_card = None
                    self.block_actions = False
                    self.render()

                timer = threading.Timer(2.0, reset_curently_turned_pair)
                timer.start() 
 
        else: # It is the first turned card
            self.chosen_card = card
            self.has_chosen_a_card = True

        self.render()
