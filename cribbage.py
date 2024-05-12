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
            self.sprite = helper.TimeBasedSprite(f"back_card.png", scale=0.5, start_center_x=self.sprite.center_x, start_center_y=self.sprite.center_y, duration=self.sprite.duration - self.sprite.elapsed_time, end_center_x=self.sprite.end_center_x, end_center_y=self.sprite.end_center_y)
        else:
            self.sprite = helper.TimeBasedSprite(f"{self.value}_{self.suit}.png", scale=0.5, start_center_x=self.sprite.center_x, start_center_y=self.sprite.center_y, duration=self.sprite.duration - self.sprite.elapsed_time, end_center_x=self.sprite.end_center_x, end_center_y=self.sprite.end_center_y)

    def clipped_value(self):
        if self.value > 10:
            return 10
        return self.value

class Player:
    def __init__(self, x, y, buttonList):
        self.state = "Locked"
        self.hand: List[Card] = []
        self.hand_pos = (x, y)
        self.increment = 30
        self.button_list: List[helper.Button] = buttonList
        self.reveal_button = helper.ClassicButton(buttonList, x, y, 225, 50, "Click to Reveal", self.reveal, hidden=True)

        # Crib discard
        self.crib_discard = []
        self.crib_chosen = False
        self.done_button = helper.ClassicButton(buttonList, x, y + 150, 250, 50, "Done", self.done, hidden=True)
        self.task = "Discard"

        # Pegging
        self.going = False
        self.select_button = helper.ClassicButton(buttonList, x, y + 150, 250, 50, "Select", self.select, hidden=True)
        self.go_button = helper.ClassicButton(buttonList, x, y + 150, 250, 50, "Go", self.go, hidden=True)
        

    def update(self, dt):
        for card in self.hand:
            card.sprite.move(dt)

            if self.state == "Hidden" and card.sprite.elapsed_time > card.sprite.duration:  # If cards aren't animating then display button
                self.state = "To be revealed"

    def draw(self):
        for card in self.hand:
            card.sprite.draw()

        if self.state == "To be revealed":
            self.reveal_button.hidden = False
            self.reveal_button.draw()

        if self.state == "Revealed" and len(self.crib_discard) == 2 and self.task == "Discard":
            self.done_button.hidden = False
            self.done_button.draw()
        elif self.state == "Revealed" and len(self.crib_discard) == 1 and self.task == "Pegging":
            self.select_button.hidden = False
            self.select_button.draw()
        elif self.state == "Revealed" and self.task == "Going" and not self.going:
            self.go_button.hidden = False
            self.go_button.draw()

    def new_hand(self, hand: List[Card]):
        self.hand = hand
        start_x = self.hand_pos[0] - self.increment * (len(hand) / 2 - 0.5)
        for i in range(len(hand)):
            hand[i].sprite.move_to(start_x + self.increment * i, self.hand_pos[1], 2)

    def reveal(self):
        if self.state == "To be revealed":
            for card in self.hand:
                card.flip()
            self.state = "Revealed"
            self.reveal_button.hidden = True
            self.fresh_buttons()

    def clicked(self, index):
        if self.state == "Revealed":
            if index in self.crib_discard:
                self.crib_discard.remove(index)
                self.hand[index].sprite.move_to(self.hand[index].sprite.end_center_x, self.hand[index].sprite.end_center_y - 25, 0.5)
            else:
                self.crib_discard.append(index)
                self.hand[index].sprite.move_to(self.hand[index].sprite.end_center_x, self.hand[index].sprite.end_center_y + 25, 0.5)
                if (self.task == "Discard" and len(self.crib_discard) > 2) or (self.task == "Pegging" and len(self.crib_discard) > 1):
                    temp = self.crib_discard.pop(0)
                    self.hand[temp].sprite.move_to(self.hand[temp].sprite.end_center_x, self.hand[temp].sprite.end_center_y - 25, 0.5)

    def done(self):
        if len(self.crib_discard) == 2:
            self.done_button.hidden = True
            self.crib_chosen = True
            self.crib_discard = [self.hand[self.crib_discard[0]], self.hand[self.crib_discard[1]]]
            self.hand.remove(self.crib_discard[0])
            self.hand.remove(self.crib_discard[1])
            self.clip_buttons(6)
            self.organize()
            self.state = "Done"
            for card in self.hand:
                card.flip()

    def organize(self):
        start_x = self.hand_pos[0] - self.increment * (len(self.hand) / 2 - 0.5)
        for i in range(len(self.hand)):
            self.hand[i].sprite.move_to(start_x + self.increment * i, self.hand_pos[1], 1.0)

    def select(self):
        if len(self.crib_discard) == 1:
            self.select_button.hidden = True
            self.crib_discard = [self.hand[self.crib_discard[0]]]
            self.state = "Selected"

    def confirm(self):
        self.hand.remove(self.crib_discard[0])
        self.clip_buttons(len(self.hand) + 1)
        self.organize()

    def deny(self):
        self.crib_discard[0].sprite.move_to(self.crib_discard[0].sprite.end_center_x, self.crib_discard[0].sprite.end_center_y - 25, 0.5)
        self.crib_discard = []

    def flip_hand(self):
        for card in self.hand:
            card.flip()

    def fresh_buttons(self):
        temp = []
        start_x = self.hand_pos[0] - self.increment * (len(self.hand) / 2 - 0.5)
        for i in range(len(self.hand)):
            button = helper.ClassicButton(temp, start_x + self.increment * i, self.hand_pos[1], self.hand[i].sprite.width, self.hand[i].sprite.height, "", lambda x=i: self.clicked(x))
            self.button_list.insert(0,button)

    def go(self):
        self.going = True
        self.go_button.hidden = True

    def clip_buttons(self, x):
        temp = self.button_list[x:]
        self.button_list.clear()
        for button in temp:
            self.button_list.append(button)

class CribbageGame():
    def __init__(self, app):
        # Set up the game
        self.deck_pos = (800, 550)
        self.shuffled_cards: List[Card] = self.get_shuffled_deck()
        self.freeze_scene = 5.0  # Seconds to display dealer decision drawing
        self.currrent_task = "Pick Dealer"
        self.dealer = None  # Will hold the dealer
        self.non_dealer = None  # Will hold the non-dealer
        self.turn = None  # Will hold the current player
        self.non_turn = None  # Will hold the non-current player
        self.player1 = Player(250, 100, app.buttons)
        self.player2 = Player(750, 100, app.buttons)
        self.crib: List[Card] = []
        self.player1_total = 0
        self.player1_round = 0
        self.player2_total = 0
        self.player2_round = 0
        self.peg_pot = 0
        self.peg_pot_history = []
        self.player1_hand_history = []
        self.player2_hand_history = []
        self.p1_peg = []
        self.p2_peg = []
        self.increment = 30
        self.p1_progress = helper.ProgressBar(175, 575, 300, 45, arcade.color.BLUE, arcade.color.LIGHT_BLUE)
        self.p2_progress = helper.ProgressBar(175, 475, 300, 45, arcade.color.RED, arcade.color.LIGHT_APRICOT)
        self.p1_label = arcade.Text(f"{0}", 335, 575, arcade.color.WHITE, 25, align="left", width=100, anchor_y="center")
        self.p2_label = arcade.Text(f"{0}", 335, 475, arcade.color.WHITE, 25, align="left", width=100, anchor_y="center")

        # Sets up the initial scene
        self.shuffled_cards[-1].flip()
        self.shuffled_cards[-2].flip()
        self.shuffled_cards[-1].sprite.move_to(250, 100, 2)
        self.shuffled_cards[-2].sprite.move_to(750, 100, 2)

    def update(self, dt):
        # Update all the cards
        for card in self.shuffled_cards:
            card.sprite.move(dt)

        # Update the players
        self.player1.update(dt)
        self.player2.update(dt)

        # Update crib
        for card in self.crib:
            card.sprite.move(dt)

        # Debug
        print(f"current task: {self.currrent_task}")
        if self.currrent_task == "Placing" or self.currrent_task == "Going" or self.currrent_task == "Pegging" or self.currrent_task == "Clear run":
            print(f"turn state: {self.turn.state}")
            print(f"non-turn state: {self.non_turn.state}")
            print(f"turn task: {self.turn.task}")
            print(f"non-turn task: {self.non_turn.task}")
            print(f"peg pot: {self.peg_pot}")
            print(f"peg pot history: {len(self.peg_pot_history)}")
            print(f"player 1 score: {self.player1_round}")
            print(f"player 2 score: {self.player2_round}")
            print(f"buttons: {len(self.player1.button_list)}")

        # Update the current task
        if self.currrent_task == "Pick Dealer":
            temp = self.freeze_scene - dt
            if temp < 0:
                if self.shuffled_cards[-1].value == self.shuffled_cards[-2].value:  # Redraw
                    self.shuffled_cards = self.get_shuffled_deck()  # Reshuffle deck
                    self.freeze_scene = 5.0
                    self.shuffled_cards[-1].flip()
                    self.shuffled_cards[-2].flip()
                    self.shuffled_cards[-1].sprite.move_to(250, 100, 2)
                    self.shuffled_cards[-2].sprite.move_to(750, 100, 2)
                elif self.shuffled_cards[-1].value > self.shuffled_cards[-2].value:  # Lowest value deals
                    self.dealer = self.player2  # player 2 is the dealer
                    self.non_dealer = self.player1  # player 1 is the non-dealer
                    self.currrent_task = "Draw Hand"
                    self.shuffled_cards = self.get_shuffled_deck()  # Reshuffle deck
                else:
                    self.dealer = self.player1  # player 1 is the dealer
                    self.non_dealer = self.player2  # player 2 is the non-dealer
                    self.currrent_task = "Draw Hand"
                    self.shuffled_cards = self.get_shuffled_deck()  # Reshuffle deck

            elif temp < 2 and not self.shuffled_cards[-1].on_back:
                # Bring cards back to deck
                self.shuffled_cards[-1].flip()
                self.shuffled_cards[-2].flip()
                self.shuffled_cards[-1].sprite.move_to(self.deck_pos[0], self.deck_pos[1], 2)
                self.shuffled_cards[-2].sprite.move_to(self.deck_pos[0], self.deck_pos[1], 2)
            self.freeze_scene -= dt

        elif self.currrent_task == "Draw Hand":  # Give players their 6 cards
            # Give the players their cards
            self.player1.new_hand(self.shuffled_cards[46:])
            self.player2.new_hand(self.shuffled_cards[40:46])
            self.currrent_task = "Player 1 Discard"

        elif self.currrent_task == "Player 1 Discard":  # Have player 1 discard 2 cards to the crib
            if self.player1.state == "Locked":
                self.player1.state = "Hidden"  # Unlock player 1's cards
            elif self.player1.state == "Done":
                self.crib.append(self.player1.crib_discard[0])
                self.crib.append(self.player1.crib_discard[1])
                self.player1.crib_discard[0].flip()
                self.player1.crib_discard[1].flip()
                self.player1.crib_discard[0].sprite.move_to(500, 225, 1)
                self.player1.crib_discard[1].sprite.move_to(500, 225, 1)
                self.player1.crib_discard = []

                self.player1.state = "Locked"
                self.currrent_task = "Player 2 Discard"

        elif self.currrent_task == "Player 2 Discard":  # Have player 2 discard 2 cards to the crib
            if self.player2.state == "Locked":
                self.player2.state = "Hidden"
            elif self.player2.state == "Done":
                self.crib.append(self.player2.crib_discard[0])
                self.crib.append(self.player2.crib_discard[1])
                self.player2.crib_discard[0].flip()
                self.player2.crib_discard[1].flip()
                self.player2.crib_discard[0].sprite.move_to(500, 225, 1)
                self.player2.crib_discard[1].sprite.move_to(500, 225, 1)
                self.player2.crib_discard = []

                self.player2.state = "Locked"
                self.currrent_task = "Draw Crib Card"

        elif self.currrent_task == "Draw Crib Card":  # Draw the crib card
            self.crib.append(self.shuffled_cards[39])
            self.shuffled_cards[39].flip()
            self.shuffled_cards[39].sprite.move_to(500, 550, 1)

            # Give dealer his nibs
            if self.shuffled_cards[39].value == 11:  # If the crib card is a jack
                self.add_points(self.dealer, 2)

            self.currrent_task = "Pegging"
            self.turn = self.non_dealer
            self.non_turn = self.dealer
            self.player1_hand_history = self.player1.hand.copy()
            self.player2_hand_history = self.player2.hand.copy()

        elif self.currrent_task == "Pegging":  # Start the pegging
            temp = False
            for card in self.turn.hand:
                if card.clipped_value() + self.peg_pot <= 31:
                    temp = True
                    break
            if temp:  # Place allowed card
                self.turn.task = "Pegging"
                self.currrent_task = "Placing"
                self.turn.state = "To be revealed"
            elif self.turn.going or self.turn.hand == []:  # "Go" to next player
                self.turn.going = False
                self.turn.flip_hand()
                self.turn.clip_buttons(len(self.turn.hand))
                self.turn.state = "Locked"
                self.currrent_task = "Going"
                self.non_turn.state = "To be revealed"
            elif self.turn.task != "Going": 
                self.turn.state = "To be revealed"
                self.turn.task = "Going"

        elif self.currrent_task == "Placing":  # Place a card
            if self.turn.state == "Selected" and self.turn.crib_discard[0].clipped_value() + self.peg_pot <= 31:
                self.peg_pot += self.turn.crib_discard[0].clipped_value()
                self.turn.confirm()
                self.turn.flip_hand()
                self.add_p_peg(self.turn, self.turn.crib_discard[0])
                #self.turn.crib_discard[0].sprite.move_to(250 if self.turn == self.player1 else 750, 365, 1)
                self.peg_pot_history.append((self.turn, self.turn.crib_discard[0].value))
                
                # Check for points save in history
                self.check_for_points()

                if self.peg_pot == 31:
                    self.add_points(self.turn, 2)
                    self.currrent_task = "Clear run"
                else:
                    self.currrent_task = "Next turn"

                self.turn.crib_discard = []
                self.turn.state = "Locked"
            elif self.turn.state == "Selected":
                self.turn.state = "Revealed"
                self.turn.deny()

        elif self.currrent_task == "Going":  # "Go" to next player
            self.non_turn.task = "Pegging"
            temp = False
            for card in self.non_turn.hand:
                if card.clipped_value() + self.peg_pot <= 31:
                    temp = True
                    break

            if not temp:  # Finish going
                if self.peg_pot == 31:
                    self.add_points(self.non_turn, 2)
                else:
                    self.add_points(self.non_turn, 1)  # Gives go points

                
                self.non_turn.state = "Locked"
                if self.non_turn.hand != [] and not self.non_turn.hand[0].on_back:
                    self.non_turn.clip_buttons(len(self.non_turn.hand))
                    self.non_turn.flip_hand()
                self.currrent_task = "Clear run"

            elif self.non_turn.state == "Selected" and self.non_turn.crib_discard[0].clipped_value() + self.peg_pot <= 31:
                self.peg_pot += self.non_turn.crib_discard[0].clipped_value()
                self.non_turn.confirm()
                self.add_p_peg(self.non_turn, self.non_turn.crib_discard[0])
                #self.non_turn.crib_discard[0].sprite.move_to(250 if self.non_turn == self.player1 else 750, 365, 1)
                self.peg_pot_history.append((self.non_turn, self.non_turn.crib_discard[0].value))

                # Check for points save in history
                self.check_for_points()

                self.non_turn.crib_discard = []
                self.non_turn.state = "Revealed"
                self.non_turn.fresh_buttons()
            elif self.non_turn.state == "Selected":
                self.non_turn.state = "Revealed"
                self.non_turn.deny()
        elif self.currrent_task == "Next turn":
            if self.player1.hand == [] and self.player2.hand == []:
                self.currrent_task = "Clear run"
                return

            if self.turn == self.player1:
                self.turn = self.player2
                self.non_turn = self.player1
            else:
                self.turn = self.player1
                self.non_turn = self.player2
            self.currrent_task = "Pegging"
        elif self.currrent_task == "Clear run":
            if self.player1.hand == [] and self.player2.hand == []:
                self.add_points(self.peg_pot_history[-1][0], 1)  # Gives last card points
                self.currrent_task = "Counting"
                self.player1.state = "Locked"
                self.player2.state = "Locked"
            else:
                # Switch turns
                if self.player1 == self.peg_pot_history[-1][0]:  # Whoever put the last card down is non-turn
                    self.turn = self.player2
                    self.non_turn = self.player1
                else:
                    self.turn = self.player1
                    self.non_turn = self.player2
                self.currrent_task = "Pegging"

            self.peg_pot = 0
            self.peg_pot_history = []
            self.clear_p_peg()

    def draw(self):
        if self.currrent_task == "Pick Dealer" or self.currrent_task == "Draw Hand":
            for i in range(39, len(self.shuffled_cards)):  # Only draw the cards that are actually going to be used
                self.shuffled_cards[i].sprite.draw()
        else:
            self.shuffled_cards[0].sprite.draw()

        # Draw the players
        self.player1.draw()
        self.player2.draw()

        # Draw the crib
        for card in self.crib:
            card.sprite.draw()

        # Draw the progress bars
        self.p1_progress.on_draw()
        self.p2_progress.on_draw()

        # Draw the pegged cards
        for card in self.p1_peg:
            card.sprite.draw()
        for card in self.p2_peg:
            card.sprite.draw()

        # Draw the labels
        self.p1_label.draw()
        self.p2_label.draw()

    def get_shuffled_deck(self):
        deck = []
        for i in range(52):
            deck.append(Card(i, self.deck_pos[0], self.deck_pos[1]))

        shuffled: List[Card] = []
        while len(deck) > 0:
            shuffled.append(deck.pop(random.randint(0, len(deck) - 1)))

        return shuffled
    
    def add_points(self, player, points):
        if player == self.player1:
            self.player1_round += points
            self.p1_label.text = f"{self.player1_round + self.player1_total}"
            self.p1_progress.set_progress2((self.player1_round + self.player1_total) / 121)
            if self.player1_round + self.player1_total >= 121:
                pass  # Player 1 wins
        else:
            self.player2_round += points
            self.p2_label.text = f"{self.player2_round + self.player2_total}"
            self.p2_progress.set_progress2((self.player2_round + self.player2_total) / 121)
            if self.player2_round + self.player2_total >= 121:
                pass # Player 2 wins

    def confirm_points(self):
        self.player1_total += self.player1_round
        self.player2_total += self.player2_round
        self.player1_round = 0
        self.player2_round = 0
        self.p1_progress.set_progress((self.player1_total) / 121)
        self.p2_progress.set_progress((self.player2_total) / 121)

    def add_p_peg(self, player, card):
        if player == self.player1:
            self.p1_peg.append(card)
            start_x = 250 - self.increment * (len(self.p1_peg) / 2 - 0.5)
            for i in range(len(self.p1_peg)):
                self.p1_peg[i].sprite.move_to(start_x + self.increment * i, 365, 1.0)
        else:
            self.p2_peg.append(card)
            start_x = 750 - self.increment * (len(self.p2_peg) / 2 - 0.5)
            for i in range(len(self.p2_peg)):
                self.p2_peg[i].sprite.move_to(start_x + self.increment * i, 365, 1.0)

    def clear_p_peg(self):
        self.p1_peg = []
        self.p2_peg = []

    def check_for_points(self):
        player = self.peg_pot_history[-1][0]
        if self.peg_pot == 15:
            self.add_points(player, 2)
        
        # Check for runs
        if len(self.peg_pot_history) > 1:
            for i in range(len(self.peg_pot_history) - 2):
                if self.check_for_run(self.peg_pot_history[i:]):
                    self.add_points(player, len(self.peg_pot_history[i:]))
                    break

        # Check for pairs
        for i in range(len(self.peg_pot_history) - 4, len(self.peg_pot_history) - 1):
            if len(self.peg_pot_history) >= len(self.peg_pot_history) - i and self.check_for_pairs(self.peg_pot_history[i:]):
                if i == len(self.peg_pot_history) - 4:
                    self.add_points(player, 12)
                elif i == len(self.peg_pot_history) - 3:
                    self.add_points(player, 6)
                elif i == len(self.peg_pot_history) - 2:
                    self.add_points(player, 2)
                break

    def check_for_run(self, x):
        smallest = x[0][1]
        for i in x:
            if i[1] < smallest:
                smallest = i[1]
        
        for i in range(len(x)):
            temp = False
            for j in x:
                if j[1] == smallest + i:
                    temp = True
                    break
            if not temp:
                return False
        return True
    
    def check_for_pairs(self, x):
        temp = x[0][1]
        for i in x:
            if i[1] != temp:
                return False
        return True

class Cribbage(helper.Page):
    def __init__(self, app):
        super().__init__(app)
        self.game = CribbageGame(app)
        self.label1 = arcade.Text("Player 1", 175, 620, arcade.color.WHITE, 20, 200, "center", anchor_x="center", anchor_y="center")
        self.label2 = arcade.Text("Player 2", 175, 520, arcade.color.WHITE, 20, 200, "center", anchor_x="center", anchor_y="center")
        self.p1 = arcade.Text("Player 1", 250, 10, arcade.color.WHITE, 10, 100, "center", anchor_x="center", anchor_y="center")
        self.p2 = arcade.Text("Player 2", 750, 10, arcade.color.WHITE, 10, 100, "center", anchor_x="center", anchor_y="center")
        self.quit = helper.ClassicButton(app.buttons, 25, 625, 20, 20, "X", lambda: app.change_page("MENU"), font_size=15)

    def update(self, mouse: helper.Mouse, dt):
        self.game.update(dt)

    def draw(self):
        arcade.draw_rectangle_filled(500, 325, 1000, 650, arcade.color.FOREST_GREEN)
        arcade.draw_rectangle_filled(500, 225, 147, 196.5, arcade.color.WHITE)
        arcade.draw_rectangle_filled(500, 225, 132, 181.5, arcade.color.FOREST_GREEN)
        self.p1.draw()
        self.p2.draw()
        self.label1.draw()
        self.label2.draw()
        self.game.draw()
        self.quit.draw()
