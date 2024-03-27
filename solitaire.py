import helper
import arcade

class Solitaire(helper.Page):
    def __init__(self, app):
        super().__init__(app)

    def update(self, mouse: helper.Mouse):
        pass

    def draw(self):
        arcade.draw_rectangle_filled(500, 325, 1000, 650, arcade.color.FOREST_GREEN)
