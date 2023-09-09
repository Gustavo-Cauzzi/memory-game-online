import tkinter as tk

class MenuView:
    def __init__(self, root, on_game_started):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.on_game_started = on_game_started
        self.render()

    def render(self):
        label = tk.Label(self.frame, text="Aguardando outro jogador...")
        label.pack()
        button = tk.Button(self.frame, text="Jogar", command=self.on_game_started)
        button.pack()
        self.frame.pack()
    
    def destroy(self):
        self.frame.destroy()