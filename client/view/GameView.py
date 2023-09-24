import tkinter as tk
import threading
import controller.GameController as GameController
from itertools import tee
from config.constants import Results, results_text, CARD_COLUMNS, CARD_PAIRS_QUANTITY

class GameView:
    def __init__(self, root):
        # TK
        self.root = root
        self.cards_frame = None
        self.points_frame = None
        self.frames = [self.cards_frame, self.points_frame]

        # Game
        self.game = GameController.current_game['game']

        # UI Behaviours
        self.block_actions = not self.game['started']

        self.current_player_turn = True
        self.has_chosen_a_card = False
        self.chosen_card = None
        self.current_player_points = 0
        self.other_player_points = 0

        self.setup_game_socket_events()
        self.render()

    def setup_game_socket_events(self):
        if not self.game['started']:
            GameController.on_player_joined(
                self.game['game_id'], 
                lambda game: self.other_player_joined(game)
            )
        # GameController.

    # Listeners ----------

    def other_player_joined(self, updated_game):
        self.game = updated_game
        self.render()

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
            text = card['card_pair'] if card['turn_turned'] else 'X'
            tk.Button(self.cards_frame, text=text, padx=10, pady=10, command=lambda idx=idx: self.card_click(idx)) \
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
        self.points_frame = tk.Frame(self.root)
        self.cards_frame = tk.Frame(self.root)
       
        if not self.game['started']:
            label = tk.Label(self.points_frame, text="Aguardando outro jogador...")
            label.pack()
        else: 
            result = self.check_for_winner()
            self.render_points(result)
            if result:
                self.block_actions = True

        self.render_cards()


        for i in range(CARD_COLUMNS):
            self.cards_frame.grid_columnconfigure(i, minsize=40)
            self.cards_frame.grid_rowconfigure(i, minsize=40)

        self.points_frame.pack()
        self.cards_frame.pack()

    def card_click(self, card_index):
        if not self.current_player_turn or self.block_actions:
            return

        card = self.game['cards'][card_index]
        if card['turn_turned']:
            return
        
        card['turn_turned'] = not card['turn_turned']

        if self.has_chosen_a_card: # Player already turned one card and this is the second one
            self.has_chosen_a_card = False
            if card['card_pair'] == self.chosen_card['card_pair']:
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
