import arcade
import helper
from typing import List

# Set up the constants
SCREEN_TITLE = "Arcade"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

RECT_WIDTH = 50
RECT_HEIGHT = 50

class MyApplication(arcade.Window):
    def __init__(self, width, height, theTitle):
        super().__init__(width, height, title=theTitle)
        self.mouse_loaded = True  # Boolean valuable that restricts holding mouse down for multiple clicks
        self.mouse_up = True
        self.mouse_location = [0, 0]
        self.buttons: List[helper.Button] = []  # Holds all buttons
        self.test = helper.ClassicButton(self.buttons, 250, 250, 300, 100, "Test", print, color=arcade.color.RED)

    def setup(self):
        # Create arcade objects
        pass

    def update(self, dt):
        # Make visual and background calculations
        pass

    def on_draw(self):
        # Draw visuals to screen
        self.test.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_location[0] = x
        self.mouse_location[1] = y

    def on_mouse_press(self, x: float, y: float, button, modifiers):
        self.mouse_up = False
        if self.mouse_loaded:  # Only register a single click
            for b in self.buttons:
                if b.in_bounds(x, y):
                    b.clicked()
            self.mouse_loaded = False

    def on_mouse_release(self, x, y, button, modifiers):
        self.mouse_up = True
        self.mouse_loaded = True

    def change_page(self, page):
        pass


def main():
    window = MyApplication(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

main()
