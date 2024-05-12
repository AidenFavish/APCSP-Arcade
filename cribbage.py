import helper
import arcade
import math
import random
from typing import List
from time import sleep

class Card:
    def __init__(self, value, suit, center_x, center_y):
        self.value = value  # 1-13
        self.suit = suit  # 0-3
        self.x = (self.value - 1) * 4 + self.suit
        self.on_back = True
        self.sprite = helper.TimeBasedSprite(f"back_card.png", scale=0.5, start_center_x=center_x, start_center_y=center_y, duration=0.0, end_center_x=center_x, end_center_y=center_y)
    
    def __init__(self, x, center_x, center_y):
        self.value = x // 4 + 1  # 1-13
        self.suit = x - (self.value - 1) * 4  # 0-3
        self.x = x
        self.on_back = True
        self.sprite = helper.TimeBasedSprite(f"back_card.png", scale=0.5, start_center_x=center_x, start_center_y=center_y, duration=0.0, end_center_x=center_x, end_center_y=center_y)

    def flip(self):
        self.on_back = not self.on_back
        if self.on_back:
            self.sprite = helper.TimeBasedSprite(f"back_card.png", scale=0.5, start_center_x=self.sprite.center_x, start_center_y=self.sprite.center_y, duration=0.0, end_center_x=self.sprite.end_center_x, end_center_y=self.sprite.end_center_y)
        else:
            self.sprite = helper.TimeBasedSprite(f"{self.value}_{self.suit}.png", scale=0.5, start_center_x=self.sprite.center_x, start_center_y=self.sprite.center_y, duration=0.0, end_center_x=self.sprite.end_center_x, end_center_y=self.sprite.end_center_y)

class Player:
    def __init__(self, x, y, buttonList):
        self.state = "Locked"
        self.hand: List[Card] = []
        self.hand_pos = (x, y)
        self.increment = 30
        self.button_list = buttonList
        self.reveal_button = helper.ClassicButton(buttonList, x + self.increment * 2.5, y, 225, 50, "Click to Reveal", self.reveal)

        # Crib discard
        self.crib_discard = []
        self.crib_chosen = False
        self.done_button = helper.ClassicButton(buttonList, x + self.increment * 2.5, y + 150, 250, 50, "Done", self.done)

    def update(self, dt):
        for card in self.hand:
            card.sprite.move(dt)

            if self.state == "Hidden" and card.sprite.elapsed_time > card.sprite.duration:  # If cards aren't animating then display button
                self.state = "To be revealed"

    def draw(self):
        for card in self.hand:
            card.sprite.draw()

        if self.state == "To be revealed":
            self.reveal_button.draw()

        if self.state == "Revealed" and len(self.crib_discard) == 2:
            self.done_button.draw()

    def new_hand(self, hand: List[Card]):
        self.hand = hand
        for i in range(len(hand)):
            hand[i].sprite.move_to(self.hand_pos[0] + self.increment * i, self.hand_pos[1], 2)

    def reveal(self):
        if self.state == "To be revealed":
            for card in self.hand:
                card.flip()
            self.state = "Revealed"
            temp = []
            for i in range(len(self.hand)):
                button = helper.ClassicButton(temp, self.hand_pos[0] + self.increment * i, self.hand_pos[1], self.hand[i].sprite.width, self.hand[i].sprite.height, "", lambda x=i: self.clicked(x))
                self.button_list.insert(0,button)

    def clicked(self, index):
        print(f"Clicked: {index}")
        if self.state == "Revealed":
            if index in self.crib_discard:
                self.crib_discard.remove(index)
                self.hand[index].sprite.move_to(self.hand[index].sprite.end_center_x, self.hand[index].sprite.end_center_y - 25, 0.5)
            else:
                self.crib_discard.append(index)
                self.hand[index].sprite.move_to(self.hand[index].sprite.end_center_x, self.hand[index].sprite.end_center_y + 25, 0.5)
                if len(self.crib_discard) > 2:
                    temp = self.crib_discard.pop(0)
                    self.hand[temp].sprite.move_to(self.hand[temp].sprite.end_center_x, self.hand[temp].sprite.end_center_y - 25, 0.5)

    def done(self):
        if len(self.crib_discard) == 2:
            self.crib_chosen = True
            temp = [self.hand[self.crib_discard[0]], self.hand[self.crib_discard[1]]]
            self.hand.remove(temp[0])
            self.hand.remove(temp[1])
            self.organize()
            self.state = "Done"
            for card in self.hand:
                card.flip()

    def organize(self):
        for i in range(len(self.hand)):
            self.hand[i].sprite.move_to(self.hand_pos[0] + self.increment * i, self.hand_pos[1], 1.0)

class CribbageGame():
    def __init__(self, app):
        # Set up the game
        self.deck_pos = (800, 500)
        self.shuffled_cards: List[Card] = self.get_shuffled_deck()
        self.freeze_scene = 5.0  # Seconds to display dealer decision drawing
        self.currrent_task = "Pick Dealer"
        self.dealer = 0  # Will hold 1 or 2 depending on who the dealer is
        self.player1 = Player(145, 100, app.buttons)
        self.player2 = Player(630, 100, app.buttons)

        # Sets up the initial scene
        self.shuffled_cards[-1].flip()
        self.shuffled_cards[-2].flip()
        self.shuffled_cards[-1].sprite.move_to(100, 100, 2)
        self.shuffled_cards[-2].sprite.move_to(900, 100, 2)

    def update(self, dt):
        # Update all the cards
        for card in self.shuffled_cards:
            card.sprite.move(dt)

        # Update the players
        self.player1.update(dt)
        self.player2.update(dt)
        # print(f"player 1 state: {self.player1.state}")
        # print(f"buttons: {self.player1.button_list}")
        # print(f"task: {self.dealer}")
        
        # Update the current task
        if self.currrent_task == "Pick Dealer":
            temp = self.freeze_scene - dt
            if temp < 0:
                if self.shuffled_cards[-1].value == self.shuffled_cards[-2].value:  # Redraw
                    self.freeze_scene = 5.0
                    self.shuffled_cards[-1].flip()
                    self.shuffled_cards[-2].flip()
                    self.shuffled_cards[-1].sprite.move_to(100, 100, 2)
                    self.shuffled_cards[-2].sprite.move_to(900, 100, 2)
                elif self.shuffled_cards[-1].value > self.shuffled_cards[-2].value:  # Lowest value deals
                    self.dealer = 2  # player 2 is the dealer
                    self.currrent_task = "Draw Hand"
                else:
                    self.dealer = 1  # player 1 is the dealer
                    self.currrent_task = "Draw Hand"
                self.shuffled_cards = self.get_shuffled_deck()  # Reshuffle deck
            elif temp < 2 and not self.shuffled_cards[-1].on_back:
                # Bring cards back to deck
                self.shuffled_cards[-1].flip()
                self.shuffled_cards[-2].flip()
                self.shuffled_cards[-1].sprite.move_to(self.deck_pos[0], self.deck_pos[1], 2)
                self.shuffled_cards[-2].sprite.move_to(self.deck_pos[0], self.deck_pos[1], 2)
            self.freeze_scene -= dt
        elif self.currrent_task == "Draw Hand":
            # Give the players their cards
            self.player1.new_hand(self.shuffled_cards[46:])
            self.player2.new_hand(self.shuffled_cards[40:46])
            self.currrent_task = "Player 1 Discard"
        elif self.currrent_task == "Player 1 Discard":
            if self.player1.state == "Locked":
                self.player1.state = "Hidden"  # Unlock player 1's cards
            elif self.player1.state == "Done":
                self.currrent_task = "Player 2 Discard"
        elif self.currrent_task == "Player 2 Discard":
            if self.player2.state == "Locked":
                self.player2.state = "Hidden"
            elif self.player2.state == "Done":
                self.currrent_task = "Pegging"

    def draw(self):
        if self.currrent_task == "Pick Dealer" or self.currrent_task == "Draw Hand":
            for i in range(39, len(self.shuffled_cards)):  # Only draw the cards that are actually going to be used
                self.shuffled_cards[i].sprite.draw()
        else:
            self.shuffled_cards[0].sprite.draw()

        # Draw the players
        self.player1.draw()
        self.player2.draw()

    def get_shuffled_deck(self):
        deck = []
        for i in range(52):
            deck.append(Card(i, self.deck_pos[0], self.deck_pos[1]))

        shuffled: List[Card] = []
        while len(deck) > 0:
            shuffled.append(deck.pop(random.randint(0, len(deck) - 1)))

        return shuffled

class Cribbage(helper.Page):
    def __init__(self, app):
        super().__init__(app)
        self.game = CribbageGame(app)

    def update(self, mouse: helper.Mouse, dt):
        self.game.update(dt)

    def draw(self):
        arcade.draw_rectangle_filled(500, 325, 1000, 650, arcade.color.FOREST_GREEN)
        self.game.draw()
