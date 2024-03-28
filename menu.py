import helper
import arcade

class Menu(helper.Page):
    def __init__(self, app):
        super().__init__(app)

        # Play button for solitaire. FYI lambdda expression makes it a bit easier to change the page and define what page to pass in before we want to execute the function.
        self.solitaire_button = helper.ClassicButton(app.buttons, 250, 250, 200, 75, "SOLITAIRE", lambda: app.change_page("SOLITAIRE"), arcade.color.FOREST_GREEN)
        self.loldle_button = helper.ClassicButton(app.buttons, 750, 250, 200, 75, "LOLDLE", lambda: app.change_page("LOLDLE"), arcade.color.FOREST_GREEN)

        
        self.spriteList = arcade.SpriteList()
        self.title = arcade.Sprite("arcade.png", center_x=500, center_y=500)
        self.spriteList.append(self.title)

    def draw(self):
        arcade.draw_rectangle_filled(500, 325, 1000, 650, arcade.color.WHITE)  # Background color
        self.solitaire_button.draw()  # Draws solitaire play button
        self.loldle_button.draw()
        self.spriteList.draw()


