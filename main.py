import arcade
import helper
import menu
import solitaire
import loldle
from typing import List
import random

# Set up the constants
SCREEN_TITLE = "Arcade"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

RECT_WIDTH = 50
RECT_HEIGHT = 50

class MyApplication(arcade.Window):
    def __init__(self, width, height, theTitle):
        super().__init__(width, height, title=theTitle)
        self.mouse: helper.Mouse = None
        self.buttons: List[helper.Button] = None
        self.page: helper.Page = None

    def setup(self):
        # Creates game objects
        self.mouse = helper.Mouse()
        self.buttons = []  # Holds all buttons
        self.page = menu.Menu(self)  # Landing page

    def update(self, dt):
        # Make visual and background calculations
        self.page.update(self.mouse)

    def on_draw(self):
        # Draw visuals to screen
        arcade.start_render()
        self.page.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse.setLocation(x, y)
        #print(random.randint(10, 20))

    def on_mouse_press(self, x: float, y: float, button, modifiers):
        #print(f"press {random.randint(0, 3)}")
        self.mouse.up = False
        for b in self.buttons:
            if b.in_bounds(x, y):
                b.clicked()
                break

    def on_mouse_release(self, x, y, button, modifiers):
        self.mouse.up = True
        for b in self.buttons:
            if b.in_bounds(x, y):
                b.released()
                break
            
    def on_key_press(self, key, modifiers):
        print("Key is being pressed")
        print(key)
        if key != arcade.key.BACKSPACE:
            self.current_guess += key
        else:
            self.current_guess = ""
        

    def change_page(self, page):
        self.buttons = []  # Needs to reset buttons for new page
        if page == "SOLITAIRE":
            self.page = solitaire.Solitaire(self)
        elif page == "LOLDLE":
            self.page = loldle.Loldle(self)
        else:
            self.page = menu.Menu(self)


def main():
    window = MyApplication(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

main()
