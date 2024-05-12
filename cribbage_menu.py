import helper
import arcade
import pandas as pd
import matplotlib.pyplot as plt
import math
import random
from time import sleep

SCREEN_TITLE = "Arcade"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

RECT_WIDTH = 50
RECT_HEIGHT = 50


class Cribbage_Menu(helper.Page):
    def __init__(self, app):
        super().__init__(app)
        
        # Play button for solitaire. FYI lambdda expression makes it a bit easier to change the page and define what page to pass in before we want to execute the function.
        self.muggings = helper.ClassicButton(app.buttons, 250, 150, 200, 75, "Muggings", lambda: self.check("muggings"), arcade.color.FOREST_GREEN)
        self.player_player = helper.ClassicButton(app.buttons, 750, 150, 200, 75, "2 Player Mode", lambda: self.check("PVP"), arcade.color.FOREST_GREEN)
        self.player_bot = helper.ClassicButton(app.buttons, 250, 450, 200, 75, "Easy Ai Mode", lambda: self.check("PVE"), arcade.color.FOREST_GREEN)
        self.player_bot2 = helper.ClassicButton(app.buttons, 750, 450, 200, 75, "Hard Ai Mode", lambda: self.check("PVE2"), arcade.color.FOREST_GREEN)
        self.play_game = helper.ClassicButton(app.buttons, 500, 325, 200, 75, "Game On", lambda: app.change_page("CRIBBAGE"), arcade.color.FOREST_GREEN)

        
        self.spriteList = arcade.SpriteList()
        self.title = arcade.Sprite("Settings.png", center_x=500, center_y=500)
        self.spriteList.append(self.title)

        self.pillList = [[250,75,100,50,False],[750,75,100,50,False],[250,375,100,50,False],[750,375,100,50,False]]
        self.muggingsPill = False
        self.PVPPill = False
        self.PVEPill = False
        self.PVE2Pill = False
    
    def draw(self):
        arcade.draw_rectangle_filled(500, 325, 1000, 650, arcade.color.WHITE)  # Background color
        self.title.draw()
        self.muggings.draw()
        self.player_player.draw()
        self.player_bot.draw()
        self.player_bot2.draw()
        self.play_game.draw()
        for i in self.pillList:
            self.pill(i)
        
        
    def update(self, mouse: helper.Mouse, dt):
        pass

    def pill(self,param):
        if param[4]:
            arcade.draw_rectangle_filled(param[0],param[1],param[2],param[3],arcade.color.BLACK)
            arcade.draw_circle_filled(param[0]+(param[2]/2),param[1],param[3]/2,arcade.color.BLACK)
            arcade.draw_circle_filled(param[0]-(param[2]/2),param[1],param[3]/2,arcade.color.BLACK)
            arcade.draw_circle_filled(param[0]+(param[2]/2),param[1],param[3]/3,arcade.color.GREEN)
        else:
            arcade.draw_rectangle_filled(param[0],param[1],param[2],param[3],arcade.color.BLACK)
            arcade.draw_circle_filled(param[0]+(param[2]/2),param[1],param[3]/2,arcade.color.BLACK)
            arcade.draw_circle_filled(param[0]-(param[2]/2),param[1],param[3]/2,arcade.color.BLACK)
            arcade.draw_circle_filled(param[0]-(param[2]/2),param[1],param[3]/3,arcade.color.RED)

    def check(self,pill):
        if pill =="muggings":
            self.muggingsPill = not self.muggingsPill
            self.pillList[0][4] = self.muggingsPill
        elif pill == "PVP":
            self.PVPPill = not self.PVPPill
            self.PVEPill = False
            self.PVE2Pill = False
        elif pill == "PVE":
            self.PVEPill = not self.PVEPill
            self.PVPPill = False
            self.PVE2Pill = False
        elif pill == "PVE2":
            self.PVE2Pill = not self.PVE2Pill
            self.PVEPill = False
            self.PVPPill = False
            

        self.pillList[1][4] = self.PVPPill
        self.pillList[2][4] = self.PVEPill
        self.pillList[3][4] = self.PVE2Pill