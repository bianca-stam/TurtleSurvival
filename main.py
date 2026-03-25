from Scenes.MenuView import MenuView
from constants import *

def main():
    window = arcade.Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, title=WINDOW_TITLE)
    window.high_score = 0
    window.center_window()

    game = MenuView()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()
