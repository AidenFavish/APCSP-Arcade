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
        self.game.released()

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
        
        self.deck = self.get_fresh_shuffled_deck()
        self.dragging = []

        self.foundation = [[], [], [], []]
        self.foundation_x = 900
        self.foundation_y = [550, 410, 270, 130]

        self.tableau_centers = [200, 300, 400, 500, 600, 700, 800]
        self.tableau_y_top = 550
        self.tableau_spacing = 35
        self.tableau = self.make_tableau(self.deck)

        self.cover = arcade.Sprite("cover.png")

    def make_tableau(self, deck):
        centers = self.tableau_centers
        y_top = self.tableau_y_top
        tableau = []
        for i in range(7):
            temp = []
            for j in range(i):
                deck[0].center_x = centers[i]
                deck[0].center_y = y_top - j * self.tableau_spacing
                deck[0].snap()
                temp.append(deck.pop(0))
            deck[0].center_x = centers[i]
            deck[0].center_y = y_top - i * self.tableau_spacing
            deck[0].to_back(False)
            deck[0].snap()
            temp.append(deck.pop(0))
            tableau.append(temp)

        return tableau

    def get_fresh_shuffled_deck(self):
        deck = []
        for face in range(1, 14):
            for suit in range(4):
                deck.append(Card(self.mainSpriteList, self.buttonList, self, face, suit, 300, 300))
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
            self.released()

        self.in_placeable_bounds(mouse.x, mouse.y)

        # Update sprite locations
        for i in self.deck:
            i.update(mouse)

        for i in self.tableau:
            for j in i:
                j.update(mouse)

        self.mainSpriteList.update()

    def clicked(self, card):
        if self.dragging != []:
            return

        index = 0
        for i in range(0, len(self.tableau)):
            if card in self.tableau[i]:
                index = i

        for i in range(self.tableau[index].index(card), len(self.tableau[index])):
            self.dragging.append(self.tableau[index][i])
            self.mainSpriteList.remove(self.tableau[index][i].shown_sprite)
            self.mainSpriteList.append(self.tableau[index][i].shown_sprite)

    def released(self):
        for card in self.dragging:
            card.center_x = card.snap_position[0]
            card.center_y = card.snap_position[1]
        self.dragging = []

    def in_placeable_bounds(self, x, y):
        width = 70.2
        height = 100

        if self.dragging == []:
            if self.cover in self.mainSpriteList:
                self.mainSpriteList.remove(self.cover)
            return

        # Check foundation
        for i in self.foundation_y:
            if (self.foundation_x - width / 2 <= x <= self.foundation_x + width / 2) and (i - height / 2 <= y <= i + height / 2):
                if self.cover not in self.mainSpriteList:
                    self.cover.set_position(self.foundation_x, i)
                    self.insert_cover(len(self.mainSpriteList) - 1 - len(self.dragging))
                return
            
        for i in range(len(self.tableau_centers)):
            tx = self.tableau_centers[i]
            ty = self.tableau_y_top - len(self.tableau[i]) * self.tableau_spacing
            if (tx - width / 2 <= x <= tx + width / 2) and (ty - height / 2 <= y <= ty + height / 2):
                if self.cover not in self.mainSpriteList:
                    self.cover.set_position(tx, ty)
                    self.insert_cover(len(self.mainSpriteList) - 1 - len(self.dragging))
                return
            
        if self.cover in self.mainSpriteList:
            self.mainSpriteList.remove(self.cover)

    def insert_cover(self, index):
        temp = []
        for i in range(len(self.mainSpriteList) - index):
            temp.append(self.mainSpriteList.pop())
        self.mainSpriteList.append(self.cover)
        for i in range(len(temp)):
            self.mainSpriteList.append(temp[len(temp) - 1 - i])



class Solitaire(helper.Page):
    def __init__(self, app):
        super().__init__(app)
        self.mainSpriteList = arcade.SpriteList(use_spatial_hash=True)
        self.game = SolitaireGame(self.mainSpriteList, app.buttons)

    def update(self, mouse: helper.Mouse):
        self.game.update(mouse)

    def draw(self):
        arcade.draw_rectangle_filled(500, 325, 1000, 650, arcade.color.FOREST_GREEN)
        self.mainSpriteList.draw()
