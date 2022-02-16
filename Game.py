"""
Module to be imported in BlackjackGUI.py
"""

from tkinter import *                                       # python GUI library
from tkinter import ttk
from PIL import ImageTk, Image                              # python imaging library

# assignments to create a pack of cards which are to be used in the entire game
suits = ['Hearts', 'Clubs', 'Spades', 'Diamonds']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
value = {ranks[k]: int('1234567899990'[k]) + 1 for k in range(13)}
pack = []

for n in range(0, 4):
    k = 0
    for j in range(n * 13, n * 13 + 13):

        pack.append((ranks[k], suits[n]))                   # pack created
        k += 1


class Game:
    """
    Class to create the user objects which are to be used in the game i.e. dealer,player.
    """
    def __init__(self, name, tag, cards, chips=0):
        """
        Default Game class constructor.
        INPUT: Game Object and it's attributes
        OUTPUT: No output
        """
        self.name = name
        self.tag = tag
        self.cards = cards
        self.chips = chips

    def betStats(self, bet, gui, win=True):
        """
        To manage the no. of chips.
        INPUT: Game Object, player's bet, player's chips, gui object which displays function's result
               and win variable which indicates player's luck on the bet
        OUTPUT: Prints the status of chips.
        """
        if win == True:                                     # if player won the bet

            self.chips += bet

        else:                                               # if player lost the bet

            self.chips -= bet

        if type(self.chips) == float:                       # if chips are of float type, convert it to integer

            self.chips = int(self.chips)

        if self.chips > 0:                                  # if player has enough chips

            gui.canvas.create_text(1250, 200, text=f"Now, you have {self.chips} chips.", font='Nunito 12 bold',
                                   fill='WHITE')

        if self.chips == 0:                                 # if chips have reduced to zero

            gui.bet = 0                                     # reset the bet

            gui.canvas.create_text(1250, 230, text="You have no chips now. You can't play another hand.",
                                   font='Nunito 12 bold', fill='WHITE')
            gui.canvas.create_window(1250, 300, window=Button(gui.canvas, text='QUIT', bg='DARKBLUE', fg='WHITE',
                                     font='Arial 15 bold', width=15, command=gui.exitGame))
            self.canvas.create_text(750, 30, text=f" ", font=('Nunito 20 bold'),
                                    fill='GREEN')
            self.canvas.create_text(750, 40, text=f" ", font=('Nunito 20 bold'),
                                    fill='GREEN')

        if self.chips < 0:                                  # if player has been debted

            gui.bet = 0                                     # reset the bet

            gui.canvas.create_text(1250, 203, text=f"Your chips are over.", font='Nunito 12 bold', fill='WHITE')
            gui.canvas.create_window(1250, 300, window=Button(gui.canvas, text='QUIT', bg='DARKBLUE', fg='WHITE',
                                     font='Arial 15 bold', width=20, command=gui.exitGame))

    def blackjack(self):
        """
        Checks if the user has a blackJack or not.
        INPUT: Game Object
        OUTPUT: Returns a boolean
        """
        for i in range(0, 2):                               # loop to check for blackJack
            # if one of the cards is Ace, and the other card has a value 10, then return True
            if self.cards[i][0] == 'Ace':

                if i == 0:

                    if value[self.cards[1][0]] == 10:

                        return True

                if i == 1:

                    if value[self.cards[0][0]] == 10:

                        return True

        return False                                        # if not a blackJack, return False

    def cardSum(self):
        """
        Calculates the sum of the user's cards ranks.
        INPUT: Game Object and user's cards
        OUTPUT: Returns the sum
        """
        sum_var = 0                                         # stores the sum

        for i in range(len(self.cards)):

            sum_var += value[self.cards[i][0]]

        for i in range(len(self.cards)):
            # if any card is an Ace, adjust the sum using its value as either 1 or 11 to make the sum maximum and <= 21
            if self.cards[i][0] == 'Ace' and sum_var + 10 <= 21:
                sum_var += 10

        return sum_var                                      # returns the sum

    def cardImages(self):
        """
        To return a list of required images of cards
        INPUT: Game Object
        OUTPUT: Returns list of card images
        """

        # various lists to generate the required cards
        num_list = []
        suit_list = []
        card_list = []

        for i in range(len(self.cards)):  # loop to fill the above lists
            # if rank is either 'Jack','Queen','King' or 'Ace, append its initial letter to the num_list
            if self.cards[i][0] in list(value.keys())[9:]:

                num_list.append(self.cards[i][0][0])
            # else append the ranks as they are
            else:

                num_list.append(value[self.cards[i][0]])

            # append the initials of suits to suit_list
            suit_list.append(self.cards[i][1][:1])

        # an object is given a tag which determines whether the card is required to be shown or not. It has
        # significance in the dealer's case as he/she has to hide the second card in some situations.
        # Default tag provided to the dealer is 'd'. Whenever the tag is changed to 'D', it gives the green
        # signal to the dealer's second card to be shown.

            # if dealer's second card is not needed to be shown
            if self.tag == 'd':

                num_list.append('#')
                suit_list.append('#')

                break

        for i in range(len(num_list)):
            # if dealer's second card is hidden
            if num_list[i] == '#':

                card_img = Image.open(f"./Cards/back_side.jpg")
            # fetch the card images which are to be showm
            else:

                card_img = Image.open(f"./Cards/{num_list[i]}"
                                      f"{suit_list[i]}.jpg")

            # resize the image
            card_img = card_img.resize((150, 200), Image.ANTIALIAS)
            # append the image to the list of cards
            card_list.append(ImageTk.PhotoImage(card_img))

        return card_list                                    # returns the list of cards
