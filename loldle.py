import helper
import arcade
import pandas as pd
import matplotlib.pyplot as plt
import math

class Champion():
    def __init__(self, name, gender, positon, species, resources, range_type, region):
        self.name = name
        self.gender = gender
        self.position = positon
        self.species = species
        self.resource = resources
        self.range_type = range_type
        self.region = region
    
    def setup(self, name, gender, positon, species, resources, range_type, region):
        self.name = name
        self.gender = gender
        self.position = positon
        self.species = species
        self.resource = resources
        self.range_type = range_type
        self.region = region
    
    def getName(self):
        return self.name

    def getGender(self):
        return self.gender
    
    def getPosition(self):
        return self.position
    
    def getSpecies(self):
        return self.species
    
    def getResources(self):
        return self.resource
    
    def getRange_type(self):
        return self.range_type
    
    def getRegion(self):
        return self.region


class Loldle(helper.Page):
    def __init__(self, app):
        super().__init__(app)
        self.answer = Champion("Aatrox","Male","Top","Darkin","Manaless","Melee","Runeterra")
        
        self.champ_list = [Champion("Alistar","Male","Support","Minotaur","Mana","Melee","Runeterra"),
                           Champion("Aatrox","Male","Top","Darkin","Manaless","Melee","Runeterra"),
                           Champion("Ashe","Female","Bottom","IceBorn","Mana","Ranged","Frejlord")]
        self.pastguess = []
        self.autofillguess = []
        self.current_guess = ""

        self.win = False
        self.attempts = 0
        self.submitButton = helper.ClassicButton(buttonList=app.buttons, center_x=100,center_y=200,width=50,height=50,text="Submit Guess",func=self.submit())
    
    def setup(self):
        self.answer = self.answer.setup("Aatrox","Male","Top","Darkin","Manaless","Melee","Runeterra") #Get from CSV File


    def update(self, mouse: helper.Mouse):
        self.autofill()
        print("updating")


    def draw(self):
        arcade.draw_rectangle_filled(500, 325, 1000, 650, arcade.color.OCEAN_BOAT_BLUE)# Background color
        arcade.draw_text(text=self.current_guess, start_x=100, start_y=100, color=arcade.color.BLACK, font_name= "Times New Roman")
        self.submitButton.draw()
        print(len(self.autofillguess))
        #for champ in self.autofillguess:
            #arcade.draw_text(text=champ, start_x=400, start_y=400, color=arcade.color.BLACK, font_name= "Times New Roman")


        if self.win:

            arcade.draw_text(text=f"Congrats, you got the right champion Attempts:{self.attempts}", start_x=100, start_y=100, color=arcade.color.BLACK, font_name= "Times New Roman")
            quit()

    def guess_champion(self, guess):
        if guess.upper() == self.answer[0].uppder():
            self.attempts += 1
            self.pastguess.append(self.answer)
            self.win = True
            return None
        else:
            self.attempts += 1
            for champ in self.champ_list:
                if guess.upper() == champ[0]:
                    self.pastguess.apend(champ)
                    return None
    
    def submit(self):
        for champ in self.champ_list:
            if self.current_guess.upper() == champ.getName().upper():
                self.guess_champion(self.current_guess)

    def display_guess(self):
        arcade.draw_text(text=self.current_guess, start_x=100, start_y=100, color=arcade.color.BLACK, font_name= "Times New Roman")

    def addLetter(self,letter):
        self.current_guess += letter
        self.autofillguess = []

    def removeLetter(self):
        print("Removed Letters")
        self.current_guess = ""
        self.autofillguess = []

    def autofill(self):
        counter = 0
        if len(self.current_guess) > 0:
            for champ in self.champ_list:
                if len(self.autofillguess) >= 3:
                    return None
                elif self.current_guess.upper() == champ.getName().upper()[0:len(self.current_guess)]:
                    
                    self.autofillguess.append(champ.getName())
                    counter += 1
                
    


