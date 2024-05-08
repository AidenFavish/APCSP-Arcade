SCREEN_TITLE = "Arcade"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

RECT_WIDTH = 50
RECT_HEIGHT = 50


class Cribbage_Menu:
    def __init__(self, app):
        super().__init__(app)
        
        # Play button for solitaire. FYI lambdda expression makes it a bit easier to change the page and define what page to pass in before we want to execute the function.
        self.muggings = helper.ClassicButton(app.buttons, 250, 250, 200, 75, "SOLITAIRE", lambda: app.change_page("SOLITAIRE"), arcade.color.FOREST_GREEN)
        self.player_player = helper.ClassicButton(app.buttons, 750, 250, 200, 75, "LOLDLE", lambda: app.change_page("LOLDLE"), arcade.color.FOREST_GREEN)
        self.player_bot = 
        self.player_bot2

        
        self.spriteList = arcade.SpriteList()
        self.title = arcade.Sprite("arcade.png", center_x=500, center_y=500)
        self.spriteList.append(self.title)
