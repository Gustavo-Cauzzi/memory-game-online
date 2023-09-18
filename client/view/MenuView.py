import tkinter as tk
import controller.GameController as GameController

class MenuView:
    def __init__(self, root, on_game_joined):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.on_game_joined = on_game_joined
        self.render()

    def render(self):
        label = tk.Label(self.frame, text="Conecte-se a um jogo ou crie um")
        label.pack()

        entry = tk.Entry(self.frame, width=20)
        entry.pack()

        button = tk.Button(self.frame, text="Conectar", command=lambda: self.on_game_connect(entry.get()))
        button.pack()

        button = tk.Button(self.frame, text="Criar", command=lambda: self.on_game_create(entry.get()))
        button.pack()
        self.frame.pack()
    
    def on_game_connect(self, game_id):
        GameController.join_game(game_id)
        self.on_game_joined()
        self.destroy()

    def on_game_create(self, game_id):
        GameController.create_game(game_id)
        # print("Game" + str(GameController.cards))
        self.on_game_joined()
        self.destroy()

    def destroy(self):
        self.frame.destroy()