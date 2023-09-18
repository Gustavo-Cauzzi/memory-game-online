import tkinter as tk
from view.GameView import GameView
from view.MenuView import MenuView
# Create the master object
root = tk.Tk()
root.title("Memória online")

def go_to_game_view():
    menu.destroy()
    GameView(root)

menu = MenuView(root, on_game_joined=go_to_game_view)

tk.mainloop()