import arcade.color
import helper
import arcade
import pandas as pd
import matplotlib.pyplot as plt
import math
import random
from time import sleep

class Champion():
    def __init__(self, name: str, gender: str, positon: list, species: list, resources: str, range_type:str, region: list):
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
    
    def toString(self):
        return (f"{self.name}, {self.gender}, {self.position}, {self.species}, {self.resource}, {self.range_type}, {self.region}")


class Loldle(helper.Page):
    def __init__(self, app):
        super().__init__(app)
        self.champ_list = self.import_characters("league_characters.csv")
        """self.champ_list = [Champion("Alistar","Male",["Support"],["Minotaur", "Human"],"Mana","Melee",["Runeterra"]),
                           Champion("Aatrox","Male",["Top"],["Darkin"],"Manaless","Melee",["Runeterra"]),
                           Champion("Ashe","Female",["Bottom"],["IceBorn", "Darkin"],"Mana","Ranged",["Frejlord"]),
                           Champion("Blitzcrank","Other",["Support"],["Golem"],"Mana","Melee",["Zaun"]),
                           Champion("Bard","Male",["Support"],["Celestial"],"Mana","Ranged",["Runeterra"])]
        """

        self.answer = random.choice(self.champ_list)
        print(self.answer)
        self.pastguess = []
        self.autofillguess = []
        self.current_guess = arcade.Text("",100,100)
        self.guess_string = ""
        self.color_box = arcade.color.BLACK

        self.win = False
        self.attempts = 0
        self.submitButton = helper.ClassicButton(buttonList=app.buttons, center_x=50,center_y=50,width=100,height=100,text="Submit Guess",func=self.submit)

        self.temp_name = arcade.Text("",100,100)
        self.temp_gender = arcade.Text("",100,100)
        self.temp_position = arcade.Text("",100,100)
        self.temp_species = arcade.Text("",100,100)
        self.temp_resource = arcade.Text("",100,100)
        self.temp_range = arcade.Text("",100,100)
        self.temp_region = arcade.Text("",100,100)

    def setup(self):
        pass

    def update(self, mouse: helper.Mouse):
        pass
    
    def import_characters(self, filename):
        characters = []
        data = pd.read_csv(filename, header=0)
        for i in range(len(data)):
            name = data["Name"][i]
            gender = data["Gender"][i]
            position = data["Position(s)"][i]
            species = data["Species"][i]
            resource = data["Resource"][i]
            range_type = data["Range type"][i]
            reigons = data["Region(s)"][i]

            position = position.replace("|", "")
            species = species.replace("|", "")
            reigons = reigons.replace("|", "")
            position = position.split("-")
            species = species.split("-")
            reigons = reigons.split("-")

            champ = Champion(name, gender, position, species, resource, range_type, reigons)
            #print(champ.toString())
            characters.append(champ)

        return characters



    def draw(self):
        marginx = 0
        marginy = 0
        ctr = 0
        arcade.draw_rectangle_filled(500, 325, 1000, 650, arcade.color.OCEAN_BOAT_BLUE)# Background color
        

        if self.win:
            arcade.draw_text(text=f"Congrats, you got the right champion Attempts:{self.attempts}", start_x=100, start_y=100, color=arcade.color.BLACK, font_name= "Times New Roman")
        else:
            self.current_guess.draw()
            self.submitButton.draw()
            #print(len(self.autofillguess))
            #print(self.autofillguess)
             
            for champ in self.autofillguess:
                arcade.draw_text(text=champ, start_x=5, start_y=300 + marginx, color=arcade.color.BLACK, font_name= "Times New Roman", font_size= 18)
                marginx -= 25

            marginx = 0
            #Display each trait in a box to indicate wrong or right
            for champ in self.pastguess:
                self.draw_guessed(champ,400 - marginx, 600 - marginy)
                marginx -= 180
                ctr += 1
                if ctr % 2 == 0:
                    marginy += 150
                    marginx = 0
            

    def guess_champion(self, guess):
        if guess.upper() == self.answer.getName().upper():
            self.attempts += 1
            self.pastguess.append(self.answer)
            self.win = True
            return None
        else:
            #print("guessinggggg")
            for champ in self.champ_list:
                #print(guess.upper())
                #print(champ.getName().upper())
                if guess.upper() == champ.getName().upper():
                    self.pastguess.append(champ)
                    self.attempts += 1
                    #print(f"added to list, attempts:{self.attempts}")
                    return None
    
    def submit(self):
        for champ in self.champ_list:
            if self.guess_string.upper() == champ.getName().upper():
                #print("Submit guess")
                self.guess_champion(self.guess_string)

    def addLetter(self,letter):
        self.guess_string += letter
        self.current_guess = arcade.Text(self.guess_string, 5, 111)
        self.autofillguess = []
        self.autofill()

    def removeLetter(self):
        #print("Removed Letters")
        self.guess_string = ""
        self.current_guess = arcade.Text(self.guess_string, 100, 100)
        self.autofillguess = []

    def autofill(self):
        if len(self.guess_string) > 0:
            for champ in self.champ_list:
                if len(self.autofillguess) >= 3:
                    return None
                elif self.guess_string.upper() == champ.getName().upper()[0:len(self.guess_string)]:
                    
                    self.autofillguess.append(champ.getName())
                    
                
    #Colors when guess is correct incorrect or close

    def draw_guessed(self, champ: Champion, x, y):
        self.temp_name = arcade.Text(champ.getName(), x+10, y+20)
        self.temp_gender = arcade.Text(champ.getGender(), x+10, y)
        self.temp_position = arcade.Text(str(champ.getPosition()), x+10, y-20)
        self.temp_species = arcade.Text(str(champ.getSpecies()), x+10, y-40)
        self.temp_resource = arcade.Text(champ.getResources(), x+10, y-60)
        self.temp_range = arcade.Text(champ.getRange_type(), x+10, y-80)
        self.temp_region = arcade.Text(str(champ.getRegion()), x+10, y-100)

        
        self.temp_name.draw()

        self.check_correctness(champ.getGender(),self.answer.getGender())
        arcade.draw_rectangle_filled(center_x= x+5, center_y= y, width= 10, height= 20, color= self.color_box)
        self.temp_gender.draw()

        self.check_correctness_list(champ.getPosition(),self.answer.getPosition())
        arcade.draw_rectangle_filled(center_x= x+5, center_y= y-20, width= 10, height= 20, color= self.color_box)
        self.temp_position.draw()

        self.check_correctness_list(champ.getSpecies(),self.answer.getSpecies())
        arcade.draw_rectangle_filled(center_x= x+5, center_y= y-40, width= 10, height= 20, color= self.color_box)
        self.temp_species.draw()

        self.check_correctness(champ.getResources(),self.answer.getResources())
        arcade.draw_rectangle_filled(center_x= x+5, center_y= y-60, width= 10, height= 20, color= self.color_box)
        self.temp_resource.draw()

        self.check_correctness(champ.getRange_type(),self.answer.getRange_type())
        arcade.draw_rectangle_filled(center_x= x+5, center_y= y-80, width= 10, height= 20, color= self.color_box)
        self.temp_range.draw()
        
        self.check_correctness_list(champ.getRegion(),self.answer.getRegion())
        arcade.draw_rectangle_filled(center_x= x+5, center_y= y-100, width= 10, height= 20, color= self.color_box)
        self.temp_region.draw()

    
    def check_correctness(self, check1: str, check2: str):
        if check1 == check2:
            self.color_box = arcade.color.GREEN
        else:
            self.color_box = arcade.color.RED
    
    def check_correctness_list(self, check1: list, check2: list):
        ctr = 0
        for temp1 in check1:
            for temp2 in check2:
                if temp1 == temp2:
                    ctr += 1
        
        if ctr == len(check1):
            self.color_box = arcade.color.GREEN
            #print("GREEN")
        elif ctr > 0:
            self.color_box = arcade.color.ORANGE
            #print("ORANGE")
        else:
            self.color_box = arcade.color.RED
            #print("RED")


                
                
        


