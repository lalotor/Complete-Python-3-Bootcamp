# %% [markdown]
# Constants and global variables 

# %%
import random

INITIAL_MONEY_AMOUNT = 50
BUSTED_LIMIT = 21
ACE = "Ace"
ACE_ALTERNATE_VALUE = 1

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen',
         'King', ACE)
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9,
          'Ten':10, 'Jack':10, 'Queen':10, 'King':10, ACE:11}

# %% [markdown]
# Classes

# %%
class CustomError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

# %%
class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit} ({self.value})"

# %%
# ten_diamonds = Card(suits[1], ranks[8])
# print(ten_diamonds)

# %%
class Deck:
    def __init__(self):
        self.all_cards = [] 
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit,rank))

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()

# %%
# deck = Deck()
# print(len(deck.all_cards))
# print(deck.deal_one())
# print(deck.deal_one())
# print(len(deck.all_cards))

# deck = Deck()
# deck.shuffle()
# print(deck.deal_one())
# print(deck.deal_one())

# %%
class Hand:

    def __init__(self):
        self.cards = []
        self.total = 0
        self.busted = False

    def receive_card(self, card):
        self.cards.append(card)
        self.total += card.value
        if self.total > BUSTED_LIMIT:
            aces_found = self.update_aces_value()
            if not aces_found:
              self.busted = True

    def clear(self):
        self.cards = []
        self.total = 0
        self.busted = False

    def show_cards(self):
        for card in self.cards:
            print(f"{card}, ", end="")
        print()

    def show_last_card(self):
        print(self.cards[-1])

    def update_aces_value(self):
        ace_found = False
        for card in self.cards:
            if card.rank == ACE and card.value == values[ACE]:
                self.total = self.total - card.value + ACE_ALTERNATE_VALUE
                card.value = ACE_ALTERNATE_VALUE
                ace_found = True
                break

        return ace_found

    def __str__(self):
        return f"{len(self.cards)} cards, for {self.total} total. Is busted? {self.busted}"

# %%
# deck = Deck()
# deck.shuffle()

# hand = Hand()
# hand.receive_card(deck.deal_one())
# hand.receive_card(deck.deal_one())
# print(hand)
# hand.show_cards()

# hand.clear()
# print(hand)

# #ACE SPECIAL LOGIC
# nine_diamonds = Card(suits[1], ranks[7])
# ace_diamonds = Card(suits[1], ranks[12])
# seven_diamonds = Card(suits[1], ranks[5])
# five_diamonds = Card(suits[1], ranks[3])

# hand.receive_card(nine_diamonds)
# hand.receive_card(ace_diamonds)
# print(hand)
# hand.show_cards()
# hand.receive_card(seven_diamonds)
# print(hand)
# hand.show_cards()
# hand.receive_card(five_diamonds)
# print(hand)
# hand.show_cards()

# %%
class Player:

    def __init__(self, hand, name, money = 0):
        self.hand = hand
        self.name = name
        self.money = money

    def __str__(self):
        return f"Name: {self.name}, money: {self.money}, hand: {self.hand}"

# %%
class Game:

    def __init__(self):
        self.dealer = None
        self.player = None
        self.deck = Deck()
        self.deck.shuffle()

    def start(self):
        self.dealer = Player(Hand(), "Dealer")
        self.player = Player(Hand(), "Player", INITIAL_MONEY_AMOUNT)

    def deal_cards(self):
        self.player.hand.clear()
        self.dealer.hand.clear()
        self.player.hand.receive_card(self.deck.deal_one())
        self.dealer.hand.receive_card(self.deck.deal_one())
        self.player.hand.receive_card(self.deck.deal_one())
        self.dealer.hand.receive_card(self.deck.deal_one())

    def show_state(self, show_dealer_full_hand = False):
        print("-------------------------")
        print("--------DEALER HAND------")
        if show_dealer_full_hand:
            print(self.dealer)
            self.dealer.hand.show_cards()
        else:
            self.dealer.hand.show_last_card()
        print("--------PLAYER HAND------")
        print(self.player)
        self.player.hand.show_cards()
        print("-------------------------")


# %% [markdown]
# Functions

# %%
def ask_for_player_bet(player):

    print("-------PLAYER BET--------")
    bet = 0

    while bet <= 0 or bet > player.money:
        try:
            bet = int(input(f"{player.name} place your bet: "))
            if bet <= 0 or bet > player.money:
                raise CustomError("Bet less than zero or greater than available money")
        except ValueError:
            print("Please enter a numeric value")
        except CustomError as err:
            print(f"Please check: {err}")

    return bet

# %%
# player = Player(Hand(), "test", INITIAL_MONEY_AMOUNT)
# bet = ask_for_player_bet(player)
# print(f"Bet {bet}")
# print(player)

# %%
def ask_for_player_action(player, deck):

    print("------PLAYER ACTION------")
    keep_playing = True
    is_busted = False

    while keep_playing:
        try:
            action = input(f"{player.name} choose Hit (h/H) or Stay (s/S): ")
            if action.lower() not in  ["h", "s"]:
                raise CustomError("Only enter Hit (h/H) or Stay (s/S)")
            if action.lower() == "h":
                print("-----------HIT-----------")
                player.hand.receive_card(deck.deal_one())
                print(player)
                if player.hand.busted:
                    print("--->>>PLAYER BUSTED, DEALER WINS<<<---")
                    is_busted = True
                    keep_playing = False
                else:
                    keep_playing = True
            elif action.lower() == "s":
                print("-----------STAY----------")
                keep_playing = False
        except CustomError as err:
            print(f"Please check: {err}")
            keep_playing = True

    return is_busted

# %%
def dealer_action(dealer, player, deck):

    print("------DEALER ACTION------")
    keep_playing = True
    dealer_wins = True

    while keep_playing:
        if dealer.hand.total > player.hand.total:
            print("-------DEALER WINS-------")
            keep_playing = False
        else:
            dealer.hand.receive_card(deck.deal_one())
            print(dealer)
            if dealer.hand.busted:
                print("--->>>DEALER BUSTED, PLAYER WINS<<<---")
                dealer_wins = False
                keep_playing = False

    return dealer_wins

# %%
def ask_for_keep_playing():

    valid_input = False
    keep_playing = True

    while not valid_input:
        try:
            action = input("Do you want to keep playing? Yes (y/Y) or No (n/N): ")
            if action.lower() not in  ["y", "n"]:
                raise CustomError("Only enter Yes (y/Y) or No (n/N)")
            if action.lower() == "y":
                keep_playing = True
            elif action.lower() == "n":
                keep_playing = False
            valid_input = True
        except CustomError as err:
            print(f"Please check: {err}")
            valid_input = False

    return keep_playing

# %%
def update_money(game, dealer_wins):
    if dealer_wins:
        game.dealer.money += bet
        game.player.money -= bet
    else:
        game.player.money += bet
        game.dealer.money -= bet

# %% [markdown]
# Run game

# %%
game = Game()
game.start()

game_on = True

while game_on:
    print("---------NEW PLAY--------")
    game.deal_cards()
    game.show_state()

    bet = ask_for_player_bet(game.player)
    print(f"Bet {bet}")
    print(game.player)

    is_busted = ask_for_player_action(game.player, game.deck)

    dealer_wins = True
    if not is_busted:
        dealer_wins = dealer_action(game.dealer, game.player, game.deck)

    update_money(game, dealer_wins)

    print("-------PLAY SUMMARY------")
    game.show_state(True)

    if game.player.money == 0:
        print("-PLAYER RAN OUT OF MONEY-")
        game_on = False
    else:
        game_on = ask_for_keep_playing()

print("--------GAME OVER--------")