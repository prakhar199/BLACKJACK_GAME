"""
Blackjack game main module
"""
from time import sleep                                      # to delay execution
from tkinter import *                                       # python gui library
from tkinter import ttk
from PIL import ImageTk, Image                              # python imaging library
from random import shuffle                                  # to shuffle elements
from Game import *                                          # objects of Game.py imported


class BlackjackGUI:
    """
    Class to create the GUI of the game
    """
    # variables independent of object
    dealer, player = Game, Game                             # instances of class Game to be used
    index = 0                                               # to store the  pack's index
    few = False                                             # to be changed when few cards are left in the pack
    bytes = 0                                               # to indicate progress of the progress bar
    canvas_cards = []                                       # to keep track of cards displayed on the canvas

    def __init__(self):
        """
        Default BlackjackGUI class constructor
        INPUT: BlackjackGUI Object
        OUTPUT: No output
        """

        self.root = Tk()                                    # stores a tkinter window
        self.root.title('BlackJack')                        # sets title of the tkinter window
        self.root.resizable(0, 0)                           # window can't be maximised
        self.root.iconbitmap(False, "icon.ico")
        # opens and resize the image to be set as background. This image is further needed to be stored in a variable,
        # so that python's garbage collector doesn't collect it
        bj_img = Image.open('blackjack_lc.jpg')
        bj_img = bj_img.resize((1500, 780), Image.ANTIALIAS)

        self.img = ImageTk.PhotoImage(bj_img)               # stores the background image

    # label which sets the background image
        Label(self.root, image=self.img).place(x=0, y=0, relwidth=1, relheight=1)
    # creates, stores and pack the canvas in the root tkinter window
        self.canvas = Canvas(self.root, width=1000, height=500)
        self.canvas.pack(expand=YES, fill=BOTH)
    # sets the background image of canvas
        self.canvas.create_image(0, 0, anchor=NW, image=self.img)
    # progress bar to simulate loading the next screen
        self.progress_bar = ttk.Progressbar(orient='horizontal', length=200, mode='determinate')
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = 100

        self.name = Entry(self.canvas)                      # Entry widget to input and store the name
        self.enter_chips = Entry(self.canvas)               # Entry widget to input and store the no. of chips
        self.enter_bet = Entry(self.canvas)                 # Entry widget to input and store the n. of chips to bet

    # assign various bindings to the entry widgets
        self.name.bind('<Return>', lambda event: self.enter_chips.focus_set())
        self.enter_chips.bind('<Return>', lambda event: self.betInfo())
        self.enter_bet.bind('<Return>', lambda event: self.playHand())

    # variables to store the no. of chips and bet contained by their entry widgets as a integer
        self.chips = 0
        self.bet = 0

    def clear(self):
        """
        Clears the root window except the background image
        INPUT: BlackjackGUI Object
        OUTPUT: No Output
        """
        for grid_slave in self.root.grid_slaves():          # loop to access items in the root managed by grid geometry

            grid_slave.grid_forget()                        # temporarily forgets the widget managed by grid geometry

        pack_slaves = self.root.pack_slaves()               # stores the list of widgets managed by pack geometry

        if pack_slaves:                                     # if there is atleast one widget in pack_slaves

            pack_slaves.pop()                               # preserves the background image

        for pack_slave in pack_slaves:                      # loop to access items in the root managed by pack geometry

            pack_slave.pack_forget()                        # temporarily forgets the widget managed by pack geometry

        place_slaves = self.root.place_slaves()             # stores the list of widgets managed by place geometry

        if place_slaves:                                    # if there is atleast one widget in place_slaves

            place_slaves.pop()                              # preserves the background image

        for place_slave in place_slaves:                    # loop to access items in the root managed by place geometry

            place_slave.place_forget()                      # temporarily forgets the widget managed by place geometry

    def createBackground(self):
        """
        To create the background of the canvas for further execution
        INPUT: BlackjackGUI Object
        OUTPUT: Clears(preserving background image) and creates the background
        """

        canvas_widgets = list(self.canvas.find_all())       # stores the list of all widgets on the canvas

        if canvas_widgets:                                  # if there is atleast one widget in canvas_widgets

            canvas_widgets.pop(0)                           # preserves the background image

        for item in canvas_widgets:                         # loop to access items in canvas_widgets

            self.canvas.delete(item)                        # removes the item

    # required to remove widgets managed by geometries other than pack
        self.clear()

        self.canvas.pack(expand=YES, fill=BOTH)             # packs the canvas over root


    def submitInfo(self, *args):
        """
        To display a page which inputs the name of the player and no. of chips
        INPUT: BlackjackGUI object
        OUTPUT: Creates the page
        """
        if args:
            self.table(self.player.chips, self.combinedSums(), True)
        else:
            self.createBackground()
        # creates the label and entry for name
            self.canvas.create_text(740, 450, text="What's your name? ", font='Nunito 12 bold', fill='WHITE')
            self.canvas.create_window(910, 450, window=self.name)
            self.name.focus_set()                           # sets the cursor focus on name entry
        # creates the label and entry for no. of chips
            self.canvas.create_text(705, 500, text="How many chips you have? ", font='Nunito 12 bold', fill='WHITE')
            self.canvas.create_window(910, 500, window=self.enter_chips)
        # creates the buttons to control the flow of the program
            self.canvas.create_window(900, 600, window=Button(self.canvas, text='BACK', bg='DARKBLUE', fg='WHITE',
                                      width=15, font='Arial 15 bold', command=self.run))
            self.canvas.create_window(700, 600, window=Button(self.canvas, text='SUBMIT', bg='DARKBLUE', fg='WHITE',
                                                              width=15, font='Arial 15 bold', command=self.betInfo))

        self.root.mainloop()

    def betInfo(self, *args):
        """
        To display a page which inputs the no. of chips the player wants to bet
        INPUT: BlackjackGUI object
        OUTPUT: Creates the page
        """
        try:                                                # checks if player has entered valid entry for chips

            int(self.enter_chips.get())                     # this raises an error if data type is other than integer

        except ValueError:                                  # if error is raised by try block

            # displays 'invalid entry' and retries
            self.canvas.create_text(1060, 435, text=" Invalid Entry! ", font='Nunito 12 bold', fill='WHITE')
    # else continues execution
        else:

            self.chips = int(self.enter_chips.get())        # gets the integer value of chips

            if self.few == True:                            # if few cards are left in the pack

                self.fewCards()

            else:                                           # else continues execution

                self.createBackground()

            # sets the widgets on the page
                self.canvas.create_text(740 + len(self.name.get()), 450, text=f"{self.name.get().capitalize()}, You "
                                                                              f"have {self.enter_chips.get()} chip(s)."
                                                                              f" ", font='Nunito 12 bold', fill='WHITE')
                self.canvas.create_text(705, 500, text="How many chips you want to bet? ", font='Nunito 12 bold',
                                        fill='WHITE')

                self.canvas.create_window(910, 500, window=self.enter_bet)
                self.enter_bet.focus_set()
                if args:
                    self.canvas.create_window(900, 600, window=Button(self.canvas, text='BACK', bg='DARKBLUE',
                                                                      fg='WHITE',
                                                                      width=15, font='Arial 15 bold',
                                                                      command=lambda: self.submitInfo(args[0])))
                else:
                    self.canvas.create_window(900, 600, window=Button(self.canvas, text='BACK', bg='DARKBLUE',
                                                                      fg='WHITE',
                                                                      width=15, font='Arial 15 bold',
                                                                      command=self.submitInfo))
                self.canvas.create_window(700, 600, window=Button(self.canvas, text='CONTINUE', bg='DARKBLUE',
                                                                  fg='WHITE', width=15, font='Arial 15 bold',
                                                                  command=self.playHand))

        self.root.mainloop()

    def combinedSums(self):
        """
        Recieves the dealer's cards sum and player's cards sum separately by calling cardSum() and
        then returns them combined in a list.
        INPUT: Game objects(dealer and player)
        OUTPUT: Returns the created list
        """
        d_sum = self.dealer.cardSum()                      # Dealer's card sum
        p_sum = self.player.cardSum()                      # Player's card sum

        return [d_sum, p_sum]  # Returns sum as a list

    def hit(self, chips):
        """
        To perform the hit operation for the player and update the table
        INPUT: BlackjackGUI object, Game objects(dealer and player) and player's chips
        OUTPUT: No specific output
        """
        if self.index > 50:                                 # if cards are over

            self.canvas.create_text(770, 830, text="You can't hit more.", font='Nunito 12 bold', fill='WHITE')
            self.few = False

        else:                                               # else continues execution

            self.player.cards.append(pack[self.index])      # appends one card to the player's cards
            self.index += 1                                 # updates the index
        # stores the updated sum
            sum_list = self.combinedSums()
        # displays the updated table
            self.table(chips, sum_list, False)

    def stand(self, chips, sum_list):
        """
        To perform the stand operation for the player and update the table
        INPUT: BlackjackGUI object, Game objects(dealer and player), player's chips and sum_list
        """
    # while sum of cards of dealer becomes 17 or greater than 17, dealer hits
        while sum_list[0] < 17:

            if self.index <= 50:
                # append one card to the player's cards
                self.dealer.cards.append(pack[self.index])
                self.index += 1                             # update the index

            sum_list = self.combinedSums()
    # changes the dealer tag to 'D' so that his all cards can be shown
        self.dealer.tag = 'D'
    # displays the updated table
        self.table(chips, sum_list, False)

    def busted(self, sum_list):
        """
        Check whether dealer or player is busted or not, updates the chips by calling Game.betStats()
        and prints the result.
        INPUT: BlackjackGUI object, Game objects(dealer and player), list of their cards' sum, player's bet
        OUTPUT: Displays the result on GUI
        """
    # if dealer's cards' sum is greater than 21
        if sum_list[0] > 21:

            self.canvas.create_text(930, 665, text="Dealer is busted. You won this hand. ", font='Nunito 20 bold',
                                    fill='WHITE')
        # updates the no. of chips
            self.player.betStats(self.bet, gui)
    # if player's cards' sum is greater than 21
        elif sum_list[1] > 21:

            self.canvas.create_text(930, 665, text="You are busted. Dealer won this hand. ", font='Nunito 20 bold',
                                    fill='RED')
        # updates the no. of chips, False indicates that the player lost the bet
            self.player.betStats(self.bet, gui, False)

    def whoWon(self, sum_list, bust):
        """
        Check whether dealer or player won, updates the chips by calling Game.betStats() and prints the
        result
        INPUT: BlackjackGUI object, Game objects(dealer and player), list of their cards' sum, player's bet
        OUTPUT: Displays the result on GUI
        """
    # if dealer's cards' sum is greater than player's cards' sum and no one is busted
        if sum_list[0] > sum_list[1] and not bust:

            self.canvas.create_text(930, 665, text="Dealer won this hand. You lost the bet. ", font='Nunito 20 bold',
                                    fill='RED')

            self.player.betStats(self.bet, gui, False)

    # if dealer's cards' sum is equal to player's cards' sum and no one is busted
        elif sum_list[0] == sum_list[1] and not bust:

            self.canvas.create_text(930, 665, text="No one won this hand. You lose half the chip(s).",
                                    font='Nunito 20 bold', fill='WHITE')
    # bet is divided between dealer and player
            self.bet = self.bet / 2
            self.player.betStats(self.bet, gui, False)
    # if player's cards' sum is greater than dealer's cards' sum and no one is busted
        elif sum_list[0] < sum_list[1] and not bust:

            self.canvas.create_text(930, 665, text=" You won this hand. ", font='Nunito 20 bold', fill='GREEN')     ########################...iiiiii....#######################################################

            self.player.betStats(self.bet, gui)

    def fewCards(self):
        """
        To display a page asking the player whether he/she wants to continue playing or not when few cards are left.
        When cards are over, it displays a page which displays quit button with a message.
        INPUT: BlackjackGUI object
        OUTPUT: Displays the page
        """
    # if index is more than 40, asks the player to continue or not
        if self.index > 40 and self.index <= 48:

            self.createBackground()

            self.canvas.create_text(740, 450, text="Few cards left in the pack. You may or may not hit. Do you want to"
                                                   " continue?  ", font='Nunito 20 bold', fill='WHITE')
            self.canvas.create_window(700, 600, window=Button(self.canvas, text='YES', bg='DARKBLUE', fg='WHITE',
                                      width=15, font='Arial 15 bold', command=self.betInfo))
            self.canvas.create_window(900, 600, window=Button(self.canvas, text='NO', bg='DARKBLUE', fg='WHITE',
                                      width=15, font='Arial 15 bold', command=self.exitGame))
        # sets few variable to false because if user continues, then this function need not to be called again as now
        # index remains greater than 40
            self.few = False

    # if index is more than 48, quit the game or go back to the home page
        if self.index > 48:

            self.createBackground()

            self.canvas.create_text(800, 435, text="Can't play another hand. See you next time. ",
                                    font='Nunito 12 bold', fill='WHITE')
            self.canvas.create_window(800, 500, window=Button(self.canvas, text='QUIT', bg='DARKBLUE', fg='WHITE',
                                      width=15, font='Arial 15 bold', command=self.exitGame))

            self.few = False

    def animate(self, obj, i):
        """
        To animate the cards.
        INPUT: BlackjackGUI object, an integer value to specify the position of the card
        OUTPUT: Moves the card to the required position
        """
        # loop to change the coordinates periodically to show motion
        for p in range(0, 4-i):

            x = self.canvas.coords(obj)[0]                  # stored previous x coordinate
            y = self.canvas.coords(obj)[1]                  # stored previous y coordinate

            self.canvas.coords(obj, x-120, y)               # sets the new coordinates
            self.canvas.move(obj, 0, 0)                     # moves the card to new coordinates
            self.canvas.update()                            # updates the canvas

            sleep(0.05)                                     # this makes updating of the canvas slower to achieve motion

    def table(self, chips, sum_list, hand):
        """
        Displays the GUI table made up by cards,dealer,player and their cards' sum.
        INPUT: BlackjackGUI object, Game objects(dealer and player), list of their cards' sum and a variable to
               indicate if it's a new hand or not.
        OUTPUT: Displays the table
        """
    # if not a new hand, then clear the canvas leaving the cards
        if hand == False:

            canvas_widgets = list(self.canvas.find_all())

            canvas_widgets.pop(0)

            if self.canvas_cards:

                for i in self.canvas_cards:

                    canvas_widgets.remove(i)                # preserves the cards

            for item in canvas_widgets:

                self.canvas.delete(item)                    # deletes all the items except the cards

        else:                                               # if a new hand, clear the whole canvas(except bg of course)

            self.createBackground()
    # assignments to indicate various situations in the game
        over = False                                        # changes to True if the hand is over
        bust = False                                        # changes to True if anyone is busted
        bj = False                                          # changes to True if anyone has a blackjack
        show = False                                        # changes to True if all cards showed up
    # sets the widgets to form the table on the canvas
        if self.bet == 0:
            self.canvas.create_text(750, 40, text=f"{self.enter_bet.get()} chip(s) are on bet. ", font=('Nunito 20 bold'),fill='GREEN')
        else:
            self.canvas.create_text(750, 30, text=f"{self.bet} chip(s) are on bet. ", font=('Nunito 20 bold'),
                                    fill='GREEN')
        self.canvas.create_text(200, 130, text="DEALER", font='Nunito 20 bold', fill='YELLOW')

        if self.index > 50:                                 # if all cards showed up

            over = True
            bust = True
            bj = True


        if sum_list[0] > 21 or sum_list[1] > 21:            # if anyone is busted

            self.dealer.tag = 'D'                           # allows dealer cards to show
            bust = True
            over = True                                     # hand is over

        if self.player.blackjack() == True or self.dealer.blackjack() == True:
            self.dealer.tag = 'D'
    # store the list of card images for both the users
        d_card_list = self.dealer.cardImages()
        p_card_list = self.player.cardImages()

        if hand == True:                                    # if new hand

            for i in d_card_list:                           # loop to display dealer's cards
                # display and animate the card
                obj = self.canvas.create_window(600, 150, anchor=NW, window=Label(self.canvas, image=i))      ########################################################################################
                self.canvas_cards.append(obj)

                self.animate(obj, d_card_list.index(i))

        elif self.dealer.tag == 'D':                        # if current hand is not over

                self.canvas.create_window(600, 150, anchor=NW, window=Label(self.canvas, image=d_card_list[1]))
                # animate the next card(s) if it's after dealer's second card
                if len(d_card_list) > 2:

                    for i in d_card_list[2:]:

                        obj = self.canvas.create_window(640, 150, anchor=NW, window=Label(self.canvas, image=i))
                        self.canvas_cards.append(obj)

                        self.animate(obj, d_card_list.index(i))
    # if dealer's second card is shown, display his/her cards' sum
        if self.dealer.tag == 'D':

            self.canvas.create_text(1250, 160, text=f"Dealer's card sum: {sum_list[0]} ", font='Nunito 20 bold',
                                    fill='WHITE')
    # displays player's cards' sum
        self.canvas.create_text(1250, 130, text=f"Your card sum: {sum_list[1]} ", font='Nunito 20 bold', fill='WHITE')

        if hand == True:

            for i in range(len(p_card_list)):               # loop to display player's cards

                obj = self.canvas.create_window(700, 400, anchor=NW, window=Label(self.canvas, image=p_card_list[i]))
                self.canvas_cards.append(obj)

                self.animate(obj, i)
        else:

            obj = self.canvas.create_window(700, 400, anchor=NW, window=Label(self.canvas, image=p_card_list[-1]))
            self.canvas_cards.append(obj)

            self.animate(obj, p_card_list.index(p_card_list[-1]))

        self.canvas.create_text(200, 380, text=f"{self.name.get().upper()}", font='Nunito 20 bold', fill='YELLOW')    #####################################################################################

        if self.player.blackjack() == True:                 # if player has a blackjack

            # display message
            self.canvas.create_text(910, 650, text="You have a BlackJack. ", font='Nunito 12 bold', fill='WHITE')
            self.canvas.create_text(950, 600, text="Congratulations! You have won 2.5 times the bet. ",
                                    font='Nunito 20 bold', fill='WHITE')

            self.bet = self.bet + self.bet / 2              # increases the bet by 1.5 times to be won by player
            self.player.betStats(self.bet, gui)
        # hand is over
            over = True
            bust = True
            bj = True

        elif self.dealer.blackjack() == True:               # if dealer has a blackjack

            self.canvas.create_text(950, 650, text="Dealer has a BlackJack. You lost 1.5 times the bet. ",
                                    font='Nunito 12 bold', fill='WHITE')

            self.bet = self.bet + self.bet / 2              # increases the bet by 1.5 times to be lost by player
            self.player.betStats(self.bet, gui, False)

            over = True
            bust = True
            bj = True

        # both have a blackjack
        elif self.dealer.blackjack() == True and self.player.blackjack() == True:

            self.canvas.create_text(950, 650, text="Both have a blackjack",
                                    font='Nunito 12 bold', fill='WHITE')
            self.canvas.create_text(910, 650, text="No one won this hand. You lose half the chip(s).",
                                    font='Nunito 12 bold', fill='WHITE')
            # bet is divided between dealer and player
            self.bet = self.bet / 2
            self.player.betStats(self.bet, gui, False)

        if self.index > 50 and over and bust and bj:        # if hand is over and all cards showed up
            # displays message
            self.canvas.create_text(950, 630, text="All cards showed up. Game over. ", font='Nunito 12 bold',
                                    fill='WHITE')
            self.canvas.create_window(900, 665, window=Button(self.canvas, text='QUIT', bg='DARKBLUE', fg='WHITE',                    #########################################################################
                                      width=15, font='Arial 15 bold', command=self.exitGame))

            show = True

    # if hand is not over and neither anyone is busted nor anyone has a blackjack
        if self.dealer.tag != 'D' and not over and not bust and not bj:
            # displays hit and stand buttons
            self.canvas.create_text(295, 650, text="Select your move: ", font=('Nunito 12 bold',17), fill='BLACK')
            self.canvas.create_window(300, 700, window=Button(self.canvas, text='HIT', bg='DARKBLUE', fg='WHITE',                         #####################################################################
                                                              width=15, font='Arial 15 bold',
                                                              command=lambda: self.hit(chips)))
            self.canvas.create_window(475, 700, window=Button(self.canvas, text='STAND', bg='DARKBLUE', fg='WHITE',
                                                              width=15, font='Arial 15 bold',
                                                              command=lambda: self.stand(chips, sum_list)))

        if self.index > 40:                                 # if few cards are left

            self.few = True                                 # few variable is set to True

        self.busted(sum_list)
    # if no one is busted and no one has a blackjack, then decides who won the hand
        if self.dealer.tag == 'D' and not bj and not bust:

            self.whoWon(sum_list, bust)
    # updates the chips
        chips = self.player.chips
        self.enter_chips.delete(0, END)
        self.enter_chips.insert(0, self.player.chips)
    # if hand is over and cards are left in the pack, asks whether to play again or not
        if self.dealer.tag == 'D' and chips > 0 and not show and self.index < 52:

            self.canvas.create_text(870, 700, text="Wanna play another hand: ", font='Nunito 12 bold', fill='WHITE')

            self.bet = 0                                # resets the bet
            self.canvas.create_window(900, 750, window=Button(self.canvas, text='YES', bg='DARKBLUE', fg='WHITE',
                                                              width=15, font='Arial 15 bold',
                                                              command=lambda: self.betInfo(False)))
            self.canvas.create_window(1075, 750, window=Button(self.canvas, text='NO', bg='DARKBLUE', fg='WHITE',
                                                               width=15, font='Arial 15 bold',
                                                               command=self.exitGame))

        self.root.mainloop()

    def playHand(self):
        """
        To set the variables and conditions to play a hand
        INPUT: BlackjackGUI object
        OUTPUT: No specific output
        """
        try:                                                # checks if player has entered valid entry for chips

            int(self.enter_bet.get())

        except ValueError:

            self.canvas.create_text(800, 435, text=" Invalid Entry! ", font='Nunito 12 bold', fill='WHITE')

        else:                                               # else continues execution

            self.bet = int(self.enter_bet.get())
        # checks if the player has entered more value of bet than chips
            try:

                if self.bet > self.chips:

                    raise ValueError

            except ValueError:

                self.canvas.create_text(810, 800, text="Can't bet more than available chips. ", font='Nunito 12 bold',
                                        fill='WHITE')

            else:                                          # else continues execution
                # gets and stores the name and no. of chips
                name = self.name.get()
                chips = self.chips
                # creates the Game objects to be used in the entire game
                self.player = Game(name, 'p', [pack[self.index], pack[self.index+1]], chips)
                self.dealer = Game('Dealer', 'd', [pack[self.index+2], pack[self.index+3]])

                self.index = self.index + 4                 # update the index as cards are drawn

                self.canvas_cards = []                      # clear the canvas cards for a new hand

                sum_list = self.combinedSums()

                self.table(chips, sum_list, True)           # display the table

    def exitGame(self):
        """
        To display the main exit window where the player can navigate to home or can quit the game
        INPUT: BlackjackGUI object, and *args which signify when to display BACK button
        """
        self.createBackground()

    # displays the window
        self.canvas.create_text(800, 400, text="Exit Game?  ", font='Nunito 20 bold', fill='WHITE')

        self.canvas.create_window(600, 450, window=Button(self.canvas, text='YES', bg='DARKBLUE', fg='WHITE',
                                                          width=15, font='Arial 15 bold',
                                                          command=self.root.destroy))
        self.canvas.create_window(800, 450, window=Button(self.canvas, text='BACK', bg='DARKBLUE', fg='WHITE',
                                                          width=15, font='Arial 15 bold',
                                                          command=lambda: self.table(self.player.chips,
                                                                                     self.combinedSums(), True)))
        self.canvas.create_window(1000, 450, window=Button(self.canvas, text='HOME', bg='DARKBLUE', fg='WHITE',
                                                           width=15, font='Arial 15 bold', command=self.run))

    def run(self):
        """
        To run the entire GUI, this the first function to be called
        INPUT: BlackjackGUI object
        OUTPUT: Runs the GUI window
        """

        self.clear()
    # clears the bytes, list of cards on canvas, name, no. of chips and bet
        self.bytes = 0
        self.canvas_cards = []
        self.name.delete(0, END)
        self.enter_chips.delete(0, END)
        self.enter_bet.delete(0, END)

        shuffle(pack)                                       # shuffles the pack of cards

        self.root.geometry("1500x780+170+70")               # sets the geometry of the root window
        #self.root.geometry("1500x780")
    # opens, resize and stores the introduntion image to be shown on the home page
        bj_img = Image.open('Blackjack.png')
        bj_img = bj_img.resize((1500, 800), Image.ANTIALIAS)
        intro_img = ImageTk.PhotoImage(bj_img)
    # sets the root window
        Label(self.root, image=intro_img).place(x=0, y=0, relwidth=1, relheight=1)
        Button(self.root, text='PLAY', fg='WHITE', bg='DARKRED', width=10, font='Ariel 20 bold',
               command=self.submitInfo).place(x=700, y=400)
        # get screen width and height
        #ws = self.root.winfo_screenwidth()
        #hs = self.root.winfo_screenheight()
        # calculate position x, y
        #self.x = (ws/2) - (w/2)
        #self.y = (hs/2) - (h/2)
        #self.root.geometry("1500x780"+self.x+self.y)               # sets the geometry of the root window
        self.root.mainloop()


if __name__ == '__main__':                                  # if this module is the GUI module

    gui = BlackjackGUI()                                    # creates the GUI object
    gui.run()                                               # runs the game
