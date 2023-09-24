import tkinter as tk
import controller.GameController as GameController

class MenuView:
    def __init__(self, root, on_game_joined):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.on_game_joined = on_game_joined
        self.error = None
        self.game_list = GameController.get_games()
        self.set_socket_listeners()
        self.render()

    def update_list(self, payload):
        if self.frame.winfo_exists():
            self.game_list = payload
            self.render()

    def set_socket_listeners(self): 
        GameController.on_new_game(self.update_list)

    def render(self):
        if self.frame:
            self.frame.destroy()
            self.frame = tk.Frame(self.root)

        game_list_container = tk.Frame(self.frame)

        label = tk.Label(self.frame, text="Lista de jogos:")
        label.pack()
        if len(self.game_list) == 0:
            label = tk.Label(self.frame, text="Nenhum jogo encontrado")
            label.pack()

        for idx, game in enumerate(self.game_list):
            connected_players = len(game['connected_players'])
            label = tk.Label(game_list_container, text=game["game_id"])
            label.grid(row=idx, column=0)

            label = tk.Label(game_list_container, text=f'{connected_players}/2')
            label.grid(row=idx, column=1)

            if connected_players != 2:
                button_or_nothing = tk.Button(game_list_container, text="Entrar", command=lambda game=game: self.connect_to_game(game['game_id']) if connected_players == 1 else None)
            else:
                button_or_nothing = tk.Label(game_list_container, text=" ")

            button_or_nothing.grid(row=idx, column=3)

        game_list_container.pack()

        label = tk.Label(self.frame, text="-----------------------------------------")
        label.pack()
        
        label = tk.Label(self.frame, text="Crie um jogo")
        label.pack()

        entry = tk.Entry(self.frame, width=20)
        entry.pack()

        button = tk.Button(self.frame, text="Criar", command=lambda: self.create_game(entry.get()))
        button.pack()

        if self.error:
            label = tk.Label(self.frame, text=self.error, fg="red")
            label.pack()

        self.frame.pack()
    
    def connect_to_game(self, game_id):
        try:
            GameController.join_game(game_id)
            self.on_game_joined()
            self.destroy()
        except:
            self.error = "Não foi possível encontrar o jogo " + game_id
            self.render()

    def create_game(self, game_id):
        print('game_id: ', game_id)
        if not game_id or len(game_id) == 0:
            self.error = 'Informe um nome ao jogo'
            self.render()
            return
        GameController.create_game(game_id)
        self.on_game_joined()
        self.destroy()

    def destroy(self):
        self.frame.destroy()