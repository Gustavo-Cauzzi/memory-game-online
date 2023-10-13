import tkinter as tk
import controller.GameController as GameController
from view.GameView import GameView
from view.MenuView import MenuView

root = tk.Tk()
root.title("Memória online")

def go_to_game_view():
    print('go_to_game_view')
    menu.destroy()
    GameView(root)

def exit_game():
    GameController.exit_game()
    root.destroy()

menu = MenuView(root, on_game_joined=go_to_game_view)
root.protocol('WM_DELETE_WINDOW', exit_game)

tk.mainloop()