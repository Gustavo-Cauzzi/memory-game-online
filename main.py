import tkinter as tk
from view.GameView import GameView
from view.MenuView import MenuView
# Create the master object
root = tk.Tk()
root.title("Memória online")

def start_game():
    print("dnisuo")
    menu.destroy()
    GameView(root)

menu = MenuView(root, on_game_started=start_game)

tk.mainloop()