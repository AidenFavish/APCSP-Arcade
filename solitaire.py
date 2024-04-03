import helper
import arcade
import random

class Card(helper.Button):
    # Free public card images link: https://tekeye.uk/playing_cards/svg-playing-cards
    def __init__(self, spriteList: arcade.SpriteList, buttonList, game, face, suit, center_x, center_y, scale=0.3):
        super().__init__(buttonList)
        self.on_back = True
        self.face = self.decode_face(face)
        self.suit = self.decode_suit(suit)
        self.sprite_list: arcade.SpriteList = spriteList
        self.game = game
        self.suit_color = 0 if self.suit < 2 else 1

        self.center_x = center_x
        self.center_y = center_y
        self.scale = scale
        self.snap_position = (center_x, center_y)

        self.src = f"{self.face}_{self.suit}.png"
        self.back = "back_card.png"
        self.front_sprite = arcade.Sprite(self.src, self.scale, center_x=self.center_x, center_y=self.center_y)
        self.back_sprite = arcade.Sprite(self.back, self.scale, center_x=self.center_x, center_y=self.center_y)
        self.shown_sprite = self.back_sprite
        spriteList.append(self.shown_sprite)

    def in_bounds(self, x: float, y: float) -> bool:
        width = self.shown_sprite.width
        height = self.shown_sprite.height
        return (self.center_x - width / 2 <= x <= self.center_x + width / 2) and (self.center_y - height / 2 <= y <= self.center_y + height / 2)
    
    def clicked(self):
        self.game.clicked(self)

    def released(self):
        self.game.released(self)

    def decode_face(self, face):
        if type(face) != int:
            try:
                face = int(face)
            except Exception as e:
                face = face.upper()
                if face == "A" or face == "ACE":
                    face = 1
                elif face == "J" or face == "JACK":
                    face = 11
                elif face == "Q" or face == "QUEEN":
                    face = 12
                elif face == "K" or face == "KING":
                    face = 13
                else:
                    raise TypeError("Unrecognized card. Enter a number or allowed card face.")
        return face
    
    def snap(self):
        self.snap_position = (self.center_x, self.center_y)


    def decode_suit(self, suit):
        if type(suit) != int:
            suit = suit.upper()
            if suit == "H" or suit == "HEARTS":
                suit = 0
            elif suit == "D" or suit == "DIAMONDS":
                suit = 1
            elif suit == "C" or suit == "CLUBS":
                suit = 2
            elif suit == "S" or suit == "SPADES":
                suit = 3
            else:
                raise TypeError("Unrecognized suit.")
        return suit
    
    def to_back(self, x=True):
        self.on_back = x
        index = self.sprite_list.index(self.shown_sprite)
        if x:
            self.shown_sprite = self.back_sprite
        else:
            self.shown_sprite = self.front_sprite

        # Change the sprite in the list
        self.sprite_list.pop(index)
        self.sprite_list.insert(index, self.shown_sprite)

    def append_to_new_list(self, newSpriteList: arcade.SpriteList):
        self.sprite_list.remove(self.shown_sprite)
        newSpriteList.append(self.shown_sprite)
        self.sprite_list = newSpriteList

    def update(self, mouse):
        if self.center_x != self.back_sprite.center_x or self.center_y != self.back_sprite.center_y:
            self.back_sprite.center_x = self.center_x
            self.back_sprite.center_y = self.center_y
            self.front_sprite.center_x = self.center_x
            self.front_sprite.center_y = self.center_y

class SolitaireGame:
    def __init__(self, mainSpriteList: arcade.SpriteList, buttonList):
        self.mainSpriteList = mainSpriteList
        self.buttonList = buttonList

        self.deck_pos = (75, 450)
        self.revealed = []
        self.revealed_pos = (75, 300)
        
        self.deck = self.get_fresh_shuffled_deck()
        self.dragging = []

        self.foundation = [[], [], [], []]
        self.foundation_x = 900
        self.foundation_y = [550, 420, 290, 160]

        self.tableau_centers = [200, 300, 400, 500, 600, 700, 800]
        self.tableau_y_top = 550
        self.tableau_spacing = 25
        self.tableau = self.make_tableau(self.deck)

        self.cover = arcade.Sprite("cover.png")

        self.decidied = None

    def make_tableau(self, deck):
        centers = self.tableau_centers
        y_top = self.tableau_y_top
        tableau = []
        for col in range(7):
            temp = []
            for card in range(col+1):
                if card == col:
                    deck[0].to_back(False)
                deck[0].center_x = centers[col]
                deck[0].center_y = y_top - card * self.tableau_spacing
                deck[0].snap()
                temp.append(deck.pop(0))
            tableau.append(temp)

        return tableau

    def get_fresh_shuffled_deck(self):
        deck = []
        for face in range(1, 14):
            for suit in range(4):
                deck.append(Card(self.mainSpriteList, self.buttonList, self, face, suit, self.deck_pos[0], self.deck_pos[1]))
        random.shuffle(deck)

        self.mainSpriteList.clear()
        self.buttonList.clear()
        for card in range(0, len(deck)):
            self.mainSpriteList.append(deck[card].shown_sprite)
            self.buttonList.append(deck[len(deck) - 1 - card])

        return deck
    
    def update(self, mouse):
        temp = None
        if self.dragging != []:
            temp = self.dragging[0].center_y
        for i in self.dragging:
            i.center_x = mouse.x
            i.center_y = mouse.y - (temp - i.center_y)

        if self.dragging != [] and mouse.up:
            self.released(None)

        self.in_placeable_bounds(mouse.x, mouse.y)

        # Update sprite locations
        for i in self.deck:
            i.update(mouse)

        for i in self.revealed:
            i.update(mouse)

        for i in self.tableau:
            for j in i:
                j.update(mouse)

        for i in self.foundation:
            for j in i:
                j.update(mouse)

        self.mainSpriteList.update()

    def clicked(self, card:Card):

        if self.dragging != []:
            return

        index = -1
        for i in range(0, len(self.tableau)):
            if card in self.tableau[i]:
                index = i


        if index != -1 and not card.on_back:
            for i in range(self.tableau[index].index(card), len(self.tableau[index])):
                self.dragging.append(self.tableau[index][i])
                self.mainSpriteList.remove(self.tableau[index][i].shown_sprite)
                self.mainSpriteList.append(self.tableau[index][i].shown_sprite)
                self.buttonList.remove(self.tableau[index][i])
                self.buttonList.insert(0, self.tableau[index][i])

        elif card in self.deck:
            # Draw a card
            self.deck.remove(card)
            self.revealed.append(card)
            self.mainSpriteList.remove(card.shown_sprite)
            self.mainSpriteList.append(card.shown_sprite)
            self.buttonList.remove(card)
            self.buttonList.insert(0, card)
            card.snap_position = (self.revealed_pos[0], self.revealed_pos[1])
            card.center_x = card.snap_position[0]
            card.center_y = card.snap_position[1]
            card.to_back(False)
            

        elif card in self.revealed:
            self.dragging.append(card)
            self.mainSpriteList.remove(card.shown_sprite)
            self.mainSpriteList.append(card.shown_sprite)
            self.buttonList.remove(card)
            self.buttonList.insert(0, card)

    def released(self, card: Card):
        if card != None and len(self.dragging) > 0:
            card = self.dragging[0]
            placeable, p_index = self.in_placeable_bounds(card.center_x, card.center_y)
        else:
            placeable = None
        
        if placeable != None:
            card_loc = self.find_card_loc(card)
            tempT = ""
            for g in placeable:
                tempT += str(g.face) + ", "
            

            if card not in placeable:
                
                if placeable in self.tableau and self.tableau[p_index] is placeable:
                    
                    if len(placeable) == 0 and card.face == 13:
                        tempX = p_index
                        for i in range(len(self.dragging)):
                            card_loc.remove(self.dragging[i])
                            placeable.append(self.dragging[i])
                            self.dragging[i].snap_position = (self.tableau_centers[tempX], self.tableau_y_top - i * self.tableau_spacing)
                    elif placeable != [] and placeable[-1].face - 1 == card.face and placeable[-1].suit_color != card.suit_color:
                        tempX = p_index
                        
                        for i in range(len(self.dragging)):
                            
                            card_loc.remove(self.dragging[i])
                            placeable.append(self.dragging[i])
                            self.dragging[i].snap_position = (self.tableau_centers[tempX], self.tableau_y_top - (len(placeable) - 1) * self.tableau_spacing)
                    if card_loc in self.tableau and len(card_loc) > 0 and card_loc[-1].on_back:
                        card_loc[-1].to_back(False)
                elif placeable in self.foundation:
                    
                    if len(self.dragging) == 1:
                        
                        suit_pile = p_index
                        if suit_pile == card.suit:
                            
                            if (placeable == [] and card.face == 1) or (placeable != [] and card.face == placeable[-1].face + 1):
                                
                                placeable.append(card)
                                card_loc.remove(card)
                                card.snap_position = (self.foundation_x, self.foundation_y[suit_pile])
                                if card_loc in self.tableau and len(card_loc) > 0 and card_loc[-1].on_back:
                                    card_loc[-1].to_back(False)
                            
                                





        for card in self.dragging:
            card.center_x = card.snap_position[0]
            card.center_y = card.snap_position[1]
        self.dragging = []

        self.check_win()

    def find_card_loc(self, card: Card):
        for i in self.foundation:
            if card in i:
                return i
            
        for i in self.tableau:
            if card in i:
                return i
            
        if card in self.deck:
            return self.deck
        
        if card in self.revealed:
            return self.revealed

    def in_placeable_bounds(self, x, y):
        width = 70.2
        height = 100

        if self.dragging == []:
            if self.cover in self.mainSpriteList:
                self.mainSpriteList.remove(self.cover)
            return None, None

        # Check foundation
        for i in range(len(self.foundation_y)):
            if (self.foundation_x - width / 2 <= x <= self.foundation_x + width / 2) and (self.foundation_y[i] - height / 2 <= y <= self.foundation_y[i] + height / 2):
                if self.cover not in self.mainSpriteList:
                    self.cover.set_position(self.foundation_x, self.foundation_y[i])
                    self.insert_cover(len(self.mainSpriteList) - len(self.dragging))
                return self.foundation[i], i
            
        for i in range(len(self.tableau_centers)):
            tx = self.tableau_centers[i]

            if self.dragging[0] in self.tableau[i]:
                ty = self.tableau_y_top - (len(self.tableau[i]) - len(self.dragging)) * self.tableau_spacing  # Aligns already picked up cards
            else:
                ty = self.tableau_y_top - len(self.tableau[i]) * self.tableau_spacing

            if (tx - width / 2 <= x <= tx + width / 2) and (ty - height / 2 <= y <= ty + height / 2):
                if self.cover not in self.mainSpriteList:
                    self.cover.set_position(tx, ty)
                    self.insert_cover(len(self.mainSpriteList) - len(self.dragging))
                return self.tableau[i], i
            
        if self.cover in self.mainSpriteList:
            self.mainSpriteList.remove(self.cover)
            
        return None, None

    def insert_cover(self, index):
        temp = []
        for i in range(len(self.mainSpriteList) - index):
            temp.append(self.mainSpriteList.pop())
        self.mainSpriteList.append(self.cover)
        for i in range(len(temp)):
            self.mainSpriteList.append(temp[len(temp) - 1 - i])

    def reshuffle_deck(self):
        for index in range(len(self.revealed)):
            i = self.revealed[len(self.revealed) - 1 - index]
            self.deck.append(i)
            self.buttonList.remove(i)
            self.buttonList.insert(0, i)
            i.to_back(True)
            i.center_x = self.deck_pos[0]
            i.center_y = self.deck_pos[1]
            i.snap()
            self.mainSpriteList.remove(i.shown_sprite)
            self.mainSpriteList.append(i.shown_sprite)
        self.revealed = []

    def check_win(self):
        for i in self.foundation:
            if not (len(i) > 0 and i[-1].face == 13):
                return

        self.decidied = True



class Solitaire(helper.Page):
    def __init__(self, app):
        super().__init__(app)
        self.mainSpriteList = arcade.SpriteList()

        self.smallSpriteList = arcade.SpriteList()
        self.smallSpriteList.append(arcade.Sprite("heartsCover.png", center_x=900, center_y=550))
        self.smallSpriteList.append(arcade.Sprite("DiamondsCover.png", center_x=900, center_y=420))
        self.smallSpriteList.append(arcade.Sprite("ClubsCover.png", center_x=900, center_y=290))
        self.smallSpriteList.append(arcade.Sprite("SpadesCover.png", center_x=900, center_y=160))
        
        self.game = SolitaireGame(self.mainSpriteList, app.buttons)
        self.reshuffle = helper.ClassicButton(app.buttons, self.game.deck_pos[0], self.game.deck_pos[1], 65, 75, "Reshuffle", self.game.reshuffle_deck, arcade.color.GRAY, font_size=12)
        self.restart = helper.ClassicButton(app.buttons, 825, 45, 85, 35, "Restart", self.restartFunc, arcade.color.MAROON, font_size=12)
        self.menu = helper.ClassicButton(app.buttons, 925, 45, 85, 35, "Menu", self.menuFunc, arcade.color.BLACK, font_size=12)
        self.you_won = arcade.Text("YOU WON!", 300, 45,font_size=24)
        self.you_lost = arcade.Text("YOU LOST!", 300, 45, font_size=24)

    def update(self, mouse: helper.Mouse):
        self.game.update(mouse)
        self.reshuffle.update(mouse)
        self.restart.update(mouse)
        self.menu.update(mouse)

    def draw(self):
        arcade.draw_rectangle_filled(500, 325, 1000, 650, arcade.color.FOREST_GREEN)
        if self.game.decidied != None:
            if self.game.decidied:
                self.you_won.draw()
            else:
                self.you_lost.draw()
        
        self.reshuffle.draw()
        self.restart.draw()
        self.menu.draw()
        self.smallSpriteList.draw()
        self.mainSpriteList.draw()

    def restartFunc(self):
        self.app.buttons = []
        self.mainSpriteList = arcade.SpriteList()
        self.game = SolitaireGame(self.mainSpriteList, self.app.buttons)
        self.reshuffle = helper.ClassicButton(self.app.buttons, self.game.deck_pos[0], self.game.deck_pos[1], 65, 75, "Reshuffle", self.game.reshuffle_deck, arcade.color.GRAY, font_size=12)
        self.app.buttons.append(self.restart)
        self.app.buttons.append(self.menu)

    def menuFunc(self):
        self.app.change_page("MENU")
