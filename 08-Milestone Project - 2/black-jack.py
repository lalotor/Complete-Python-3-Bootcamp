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
    def __init__(self, message):
        self.value = message

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
        self.all_cards = [Card(suit, rank) for suit in suits for rank in ranks]

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
            if not self.adjust_for_ace():
                self.busted = True

    def adjust_for_ace(self):
        for card in self.cards:
            if card.rank == ACE and card.value == values[ACE]:
                card.value = ACE_ALTERNATE_VALUE
                self.total -= (values[ACE] - ACE_ALTERNATE_VALUE)
                return True
        return False

    def clear(self):
        self.cards.clear()
        self.total = 0
        self.busted = False

    def show_cards(self):
        print(', '.join(str(card) for card in self.cards))

    def show_last_card(self):
        print(self.cards[-1])

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
        for _ in range(2):
            self.player.hand.receive_card(self.deck.deal_one())
            self.dealer.hand.receive_card(self.deck.deal_one())

    def show_state(self, reveal_dealer = False):
        print("-------------------------")
        print("--------DEALER HAND------")
        if reveal_dealer:
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
def ask_for_bet(player):

    print("-------PLAYER BET--------")
    while True:
        try:
            bet = int(input(f"{player.name}, place your bet: "))
            if 0 < bet <= player.money:
                print(f"Bet {bet}")
                print(player)
                return bet
            else:
              raise CustomError("Bet must be greater than zero and less than or equal to your current money.")
        except ValueError:
            print("Please enter a numeric value")
        except CustomError as err:
            print(f"Please check: {err}")


# %%
# player = Player(Hand(), "test", INITIAL_MONEY_AMOUNT)
# bet = ask_for_bet(player)

# %%
def player_turn(player, deck):

    print("-------PLAYER TURN-------")
    while True:
        action = input(f"{player.name}, choose Hit (h/H) or Stay (s/S): ").lower()
        if action == "h":
            print("-----------HIT-----------")
            player.hand.receive_card(deck.deal_one())
            print(player)
            if player.hand.busted:
                print("--->>>PLAYER BUSTED<<<---")
                return True
        elif action == "s":
            print("-----------STAY----------")
            return False
        else:
            print("Invalid action. Only enter Hit (h/H) or Stay (s/S)")

# %%
def dealer_turn(dealer, player, deck):

    print("-------DEALER TURN-------")
    while dealer.hand.total <= player.hand.total and not dealer.hand.busted:
        dealer.hand.receive_card(deck.deal_one())
        print(dealer)

    return dealer.hand.total > player.hand.total and not dealer.hand.busted

# %%
def ask_for_keep_playing():

    while True:
          action = input(f"Do you want to keep playing? Yes (y/Y) or No (n/N): ").lower()
          if action == "y":
              return True
          elif action == "n":
              return False
          else:
              print("Invalid action. Only enter Yes (y/Y) or No (n/N)")

# %%
def update_money(game, bet, dealer_wins):
    if dealer_wins:
        game.dealer.money += bet
        game.player.money -= bet
    else:
        game.player.money += bet
        game.dealer.money -= bet

# %% [markdown]
# Run game

# %%
def main():
    game = Game()
    game.start()

    while True:
        print("---------NEW PLAY--------")
        game.deal_cards()
        game.show_state()

        bet = ask_for_bet(game.player)
        player_busted = player_turn(game.player, game.deck)
        dealer_wins = dealer_turn(game.dealer, game.player, game.deck) if not player_busted else True
        update_money(game, bet, dealer_wins)
        
        print("-------PLAY SUMMARY------")
        if dealer_wins:
            print("--->>>DEALER WINS<<<---")
        else:
            print("--->>>PLAYER WINS<<<---")
        game.show_state(True)

        if game.player.money == 0:
            print("-PLAYER IS OUT OF MONEY. GAME OVER-")
            break
        
        if not ask_for_keep_playing():
            print("--------GAME OVER--------")
            break

if __name__ == "__main__":
    main()



