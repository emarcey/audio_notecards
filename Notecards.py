
# coding: utf-8

# In[3]:

# imports
from tkinter import *
from tkinter import ttk
import os
import csv
import sqlite3
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import sys
import random
import time

CHUNK = 1024

# initialize config locations
homeDirectory = "C:\\Notecards\\"

sqliteFile = 'Notecards.sqlite'

class main_menu(Frame):
    
    # initializes program and runs subprocesses
    def __init__(self,master=None):
        
        maxDeck = 0
        maxCard = 0
        
        Frame.__init__(self, master)
        master.title("Flashcards are Fun!")
        
        #set window size
        root.minsize(600,500)
        root.maxsize(600,500)
        
        test = main_menu.createMainMenu(root)

    def createMainMenu(master):
                #create menu
        menubar = Menu(master)
        master.config(menu=menubar,bd=5)
        menubar.add_command(label="Settings",
                            command=main_menu.openSettings)
        menubar.add_command(label="Quit",
                            command=master.quit)
        
        #display decks
        deckFrame = Frame(master)
        deckFrame.grid(row=1,column=0)
        deckFrame.grid_rowconfigure(0)

        w = Label(deckFrame,
                  text ='Available Decks',
                  anchor=NW, justify=LEFT,
                  bd=5,
                  bg='lightgray',
                  font=("Arial",16)).grid(row=0,sticky=N+W,ipadx=200)
         
        
        maxDeck = main_menu.getMaxDeck()
        deckList = Listbox(deckFrame,selectmode=SINGLE)
        
        def deckListInsert():
            decks = main_menu.getDecks()
            deckList.delete(0,END)
            for deck in decks:
                deckList.insert(END, deck[1])
            return decks
            
        decks = deckListInsert()

        deckList.grid(row=1,sticky=N+W,ipadx=219)
        
        #deck buttons
        #play deck
        def setPlayDeck():
            deck_Name = deckList.get(ACTIVE)
            deckID = 0
            for deck in decks:
                if deck_Name == deck[1]:
                    deckID = deck[0]
            main_menu.playDeck(root,deck_Name,deckID,deckFrame)
        
        playDeckButton = Button(deckFrame, 
                                text='Play Deck', 
                                command=setPlayDeck,
                                bg='Green').grid(row=2,
                                                 column=0, 
                                                 sticky=S,
                                                 ipadx=250)
        #edit deck
        def editDeck():
            deck_Name = deckList.get(ACTIVE)
            deckID = 0
            for deck in decks:
                if deck_Name == deck[1]:
                    deckID = deck[0]
            main_menu.openDeck(root,decks,deckID,deck_Name,deckFrame)

        editDeckButton = Button(deckFrame, 
                                text='Edit Deck', 
                                command=editDeck).grid(row=3,
                                                                 column=0,
                                                                 sticky=S+W,
                                                                 ipadx=62)
        
        #delete deck
        def getDeleteDeck():
            main_menu.deleteDeck(deckList)
            
            #temp = main_menu.saveDecks(decks)
            
        deleteDeckButton = Button(deckFrame, 
                                  text='Delete Deck', 
                                  command=getDeleteDeck).grid(row=3,
                                                                     column=0,
                                                                     sticky=S,
                                                                     ipadx=55)
        #create deck
        def createDeck():
            main_menu.openDeck(root,decks,maxDeck+1,'Sample',deckFrame)

                
        createDeckButton = Button(deckFrame, 
                                text='Create Deck', 
                                command=createDeck).grid(row=3,
                                                                   column=0,
                                                                   sticky=S+E,
                                                                   ipadx=55)
        
    # function checks if window is open. If not, then opens Settings window.
    def openSettings():
        children = root.winfo_children()
        swCounter = 0
        
        for child in children:
            swCounter+= 1
        if swCounter <= 3:
            sm = SettingsMenu(root)
        else:
            print('Window Already Open')

    # function checks if window is open. If not, then opens Create Deck Window.
    def openDeck(root,decks,deckID,deckName,deckFrame):
        deckFrame.destroy()
        sm = DeckView(root,decks,deckID,deckName)    
    # function gets list of all decks as nested array
    # uses home_dir file to get list of decks
    # returns deck array
    def getDecks():
        decks = []
        c.execute('SELECT * from {tn}'.                  format(tn='Deck'))
        decks = c.fetchall()
        return(decks)

    # function gets the current max deck id
    def getMaxDeck():
        maxDeck = 0
        c.execute("SELECT * FROM {tn}".                  format(tn='Deck'))
        decks = c.fetchall()
        for deck in decks:
            if int(deck[0]) > maxDeck:
                maxDeck = int(deck[0])
        return maxDeck
        
    def playDeck(root,deckName,deckID,deckFrame):
        deckFrame.destroy()
        sm = PlayView(root,deckName,deckID)
    
    def deleteDeck(deckList):
        deleteDeck = deckList.get(ACTIVE)
        deletes = deckList.curselection()[0]
        deckList.delete(deletes)
        decks = main_menu.getDecks()
        decksTemp = deckList.get(0,END)
        c.execute("DELETE FROM {tn} WHERE {idf} == '{v_id}'".                  format(tn='Deck', idf='name', v_id=deleteDeck))

        deckID = 0
        for deck in decks:
            if deleteDeck == deck[1]:
                deckID = deck[0]
        print(deckID)
        c.execute("DELETE FROM {tn} WHERE {idf} == '{v_id}'".                  format(tn='Card', idf='deck_id', v_id=deckID))
            
        conn.commit()
        
#creates frame with settings         
class SettingsMenu:

    v_shuffle = ' '
    v_delay = ' '
    
    def __init__(self,master):   
        settingsTop = Toplevel(master,width=335,height=200)
        settingsTop.minsize(335,200)
        
        settingsFrame = Frame(settingsTop)
        settingsFrame.grid(row=1,column=2)
        
        sw = Label(settingsFrame,
                   text='Settings',
                   anchor=NW, 
                   justify=LEFT,
                   bd=5,
                   bg='lightgray',
                   font=("Arial",16)).grid(row=0,
                                           sticky=N+W,
                                           ipadx=120)
        
        #get saved settings
        settings = SettingsMenu.getSavedSettings()
        for setting in settings:
            if setting[1] == 'Shuffle':
                v_shuffle = setting[2]
            elif setting[1] == 'Delay':
                v_delay = setting[2]
                
        v1 = StringVar()
        v2 = StringVar()
        #set saved shuffle
        shuffle_c = Checkbutton(settingsFrame,
                                variable=v2,
                                text='Shuffle')
        shuffle_c.grid(row=2,
                      sticky=W)
        
        if(v_shuffle) == 1:
            shuffle_c.select()
        else:
            shuffle_c.deselect()
        
        #set saved default
        delay_l = Label(settingsFrame,
                       text='Delay between Question and Answer').grid(row=3,sticky=W)
        
        delay_e = Entry(settingsFrame, textvariable=v1)
        delay_e.grid(row=3,sticky=E)
        if(v_delay != delay_e.get()):
            delay_e.insert(0,v_delay)
        
        exit_b = Button(settingsFrame,
                        text = 'Exit Without Saving',
                        fg='red',
                        command = settingsTop.destroy)
        exit_b.grid(row=4,
                   sticky=W)
        
        def SaveDefault():
            v_delay = delay_e.get()
            v_shuffle = v2.get()
            
            SettingsMenu.SaveAndExit(settings,v_delay,v_shuffle)
            settingsTop.destroy()
            
        save_b = Button(settingsFrame,
                        text = 'Save and Exit',
                        fg='green',
                        command = SaveDefault)
        save_b.grid(row=4,
                    sticky=E)
    # function returns saved settings from file
    def getSavedSettings():
        settings = []
        c.execute('SELECT * from {tn}'.                  format(tn='Settings'))
        settings = c.fetchall()
        return settings
      
    def SaveAndExit(settings,v_delay,v_shuffle):
        
        c.execute("UPDATE {tn} SET Value == {cq} WHERE Setting = 'Shuffle'".                  format(tn='Settings', cq=v_shuffle))
        
        c.execute("UPDATE {tn} SET Value == {cq} WHERE Setting = 'Delay'".                  format(tn='Settings', cq=v_delay))
        
        conn.commit()

# Deck class which contains a series of cards
class DeckView:

    #open existing deck
    def __init__(self,master,decks,deck_id,deck_name):
        test1 = DeckView.createDeckView(master,decks,deck_id,deck_name)
    
    def createDeckView(master,decks,deck_id,deck_name):
        
        v1 = StringVar()
        
        #Create deck frame
        cardFrame = Frame(master)
        cardFrame.grid(row=0,column=0)
        
        menubar = Menu(cardFrame)
        master.config(menu=menubar,bd=5)
        
        def deckBack():
            cardFrame.destroy()
            main_menu.createMainMenu(root)
            
        menubar.add_command(label="Back",
                            command=deckBack)
        
        #Name Label and Entry at top
        name_l = Label(cardFrame,
                       text='Deck Name:',
                       anchor=W,
                       bg='lightgray',
                       font=("Arial",12))
        name_l.grid(row=0,column=0,sticky=W)
        
        name_e = Entry(cardFrame,
                      textvariable=v1)
        name_e.grid(row=0,column=1,sticky=W)
        name_e.insert(0, deck_name)
        
        #List of Cards with question displayed
        card_l = Label(cardFrame,
                  text ='Cards',
                  anchor=NW, justify=LEFT,
                  bd=5,
                  bg='lightgray',
                  font=("Arial",12)).grid(row=1,columnspan=4,sticky=W,ipadx=233)
         
        cards = DeckView.getCards(deck_id)
        #maxDeck = main_menu.getMaxDeck(decks)
        cardList = Listbox(cardFrame,selectmode=SINGLE)

        for card in cards:
            cardList.insert(END, card[2])
            
        cardList.grid(row=2,sticky=N+W,columnspan=4,ipadx=200)
            
        #Can open/edit/delete/add Cards
        
        def playThisDeck():
            cardFrame.destroy()
            sm = PlayView(root,deck_name,deck_id)
            
        playDeckButton = Button(cardFrame, 
                                text='Play Deck', 
                                command=playThisDeck,
                                bg='Green').grid(row=3,
                                                 columnspan=4,
                                                 ipadx=230)
        
        #save deck
        def getSaveDeck():
            tempDeck = [name_e.get(),deck_id]
            DeckView.saveDeck(name_e.get(),deck_id,cards)

            #deckList.insert(tempDeck)
            conn.commit()
            cardFrame.destroy()
            main_menu.createMainMenu(root)
        
        saveDeckButton = Button(cardFrame,
                               text = 'Save Deck',
                               command=getSaveDeck).grid(row=4,
                                                         column=0,
                                                         sticky=S+W,
                                                         ipadx=32)
        
        #edit card
        def editCard():
            cardName = cardList.get(ACTIVE)
            tempCard = []
            for card in cards:
                if cardName == card[2]:
                    tempCard = card 
                        
            tempDeck = [name_e.get(),deck_id]
            DeckView.saveDeck(name_e.get(),deck_id,cards)
            
            DeckView.openCard(root,tempCard,cards,cardFrame)
        
        editCardButton = Button(cardFrame, 
                                text='Edit Card', 
                                command=editCard).grid(row=4,
                                                       column=1,
                                                       sticky=S,
                                                       ipadx=32)
        
        #delete card
        def getDeleteCard():
            DeckView.deleteCard(cardList)
        
        deleteCardButton = Button(cardFrame, 
                                  text='Delete Card', 
                                  command=getDeleteCard).grid(row=4,
                                                                    column=2,
                                                                    sticky=S,
                                                                    ipadx=28)
        #create deck
        def createCard():
            
            newCard = [DeckView.getMaxCardID()+1, 
                      deck_id,
                      'Question',
                      'Answer']
            cards.append(newCard)
            
            tempDeck = [name_e.get(),deck_id]
            print('TempDeck')
            print(tempDeck)
            DeckView.saveDeck(name_e.get(),deck_id,cards)
            
            DeckView.openCard(root,newCard,cards,cardFrame)
        
        createDeckButton = Button(cardFrame, 
                                text='Create Card', 
                                command=createCard).grid(row=4,
                                                         column=3,
                                                         sticky=S+E,
                                                         ipadx=28)  
    
    #saves the deck and its cards 
    def saveDeck(deck_name,deck_id,cards):
        
        #check if deck_name is unique
        maxID = main_menu.getMaxDeck()
        c.execute("SELECT * FROM {tn}".                  format(tn='Deck'))
        deckNames = c.fetchall()
        print(deckNames)
        deckError = 0
        deckExists = 0
        for deck in deckNames:
            if deck_name == deck[1] and deck_id != deck[0]:
                deckError += 1
            if deck_id == deck[0]:
                deckExists += 1
                
        if deckError == 1:
            print('error')
        else:
            c.execute("INSERT OR REPLACE INTO {tn} (deck_id, name) VALUES ({cq},'{ca}')".                      format(tn='Deck', cq=deck_id,ca=deck_name))

    def deleteCard(cardList):
        deleteCard = cardList.get(ACTIVE)
        deletes = cardList.curselection()[0]
        cardList.delete(deletes)
        c.execute("DELETE FROM {tn} WHERE {idf} == '{v_id}'".            format(tn='Card', idf='question', v_id=deleteCard))
        conn.commit()  

    #get all cards for current deck
    #in: deck_id - id of current deck
    #out: cards related to deck
    def getCards(deck_id):
        cards = []
        c.execute("SELECT * FROM {tn} WHERE deck_id = {cq}".                  format(tn='Card',cq=deck_id))
        cards = c.fetchall()
        return cards
    
    #get all cards
    #out: all cards
    def getAllCards():
        cards = []
        c.execute("SELECT * FROM {tn}".                  format(tn='Deck'))
        cards = c.fetchall()
        print(cards)
        return cards
    
    #gets greatest cardID
    #in: list of cards to use
    #out: maxID from input list
    def getMaxCardID():
        maxCard = 0
        c.execute("SELECT * FROM {tn}".                  format(tn='Card'))
        cards = c.fetchall()
        for card in cards:
            if int(card[0]) > maxCard:
                maxCard = int(card[0])
        return maxCard
    
    #creates CardView object using new card or edit card settings
    def openCard(root, card, cards,cardFrame):
        cardFrame.destroy()
        sm = CardView(root,card,cards)
        
        
class CardView:

    #open existing card
    def __init__(self,master,card,cards):
        
        test = CardView.createCardFrame(master,card,cards)
        
    def createCardFrame(master,card,cards):
        
        v_question = StringVar()
        v_answer = StringVar()
            
        oneCardFrame = Frame(master)
        oneCardFrame.grid(row=0,column=0)
        
        menubar = Menu(oneCardFrame)
        master.config(menu=menubar,bd=5)
        
        def cardBack():
            oneCardFrame.destroy()
            deckName = ''
            decks = main_menu.getDecks()
            for deck in decks:
                if card[1] == deck[0]:
                    deckName = deck[1]
            print(deckName)
            DeckView.createDeckView(root,decks,card[1],deckName)
        
        menubar.add_command(label="Back",
                            command=cardBack)
        
        #Question Label, Entry and Record
        question_l = Label(oneCardFrame,
                       text='Question',
                       anchor=W,
                       bg='lightgray',
                       font=("Arial",12))
        question_l.grid(row=0,column=0,sticky=W)
        
        question_e = Entry(oneCardFrame,
                      textvariable=v_question)
        question_e.grid(row=0,column=1,sticky=W)
        question_e.insert(0, card[2])
        
        def qRecordAudio():
            filename = homeDirectory + str(card[0]) + '_' + str(card[1]) + '_question'
            tts = gTTS(text=question_e.get(),lang='en')
            tts.save(filename + '.mp3')
        
        def qPlayAudio():
            filename = homeDirectory + str(card[0]) + '_' + str(card[1]) + '_question.mp3'
            mysong = AudioSegment.from_mp3(filename)
            play(mysong)
            
        def aRecordAudio():
            filename = homeDirectory + str(card[0]) + '_' + str(card[1]) + '_answer'
            tts = gTTS(text=answer_e.get(),lang='en')
            tts.save(filename + '.mp3')
        
        def aPlayAudio():
            filename = homeDirectory + str(card[0]) + '_' + str(card[1]) + '_answer.mp3'
            mysong = AudioSegment.from_mp3(filename)
            play(mysong)
            
        question_b = Button(oneCardFrame,
                           command=qRecordAudio,
                           text='Create Audio')
        question_b.grid(row=0,column=2,sticky=W)
        
        question_b1 = Button(oneCardFrame,
                           command=qPlayAudio,
                           text='Listen')
        question_b1.grid(row=0,column=3,sticky=W)
        
        #Answer Label, Entry and Record
        answer_l = Label(oneCardFrame,
                       text='Answer',
                       anchor=W,
                       bg='lightgray',
                       font=("Arial",12))
        answer_l.grid(row=1,column=0,sticky=W)
        
        answer_e = Entry(oneCardFrame,
                      textvariable=v_answer)
        answer_e.grid(row=1,column=1,sticky=W)
        answer_e.insert(0, card[3])
        
        answer_b = Button(oneCardFrame,
                           command=aRecordAudio,
                           text='Create Audio')
        answer_b.grid(row=1,column=2,sticky=W)
        
        answer_b1 = Button(oneCardFrame,
                           command=aPlayAudio,
                           text='Listen')
        answer_b1.grid(row=1,column=3,sticky=W)
        
        
        #Save 
        def getSaveCard():
            tempCard = [card[0],card[1],question_e.get(),answer_e.get()]
            CardView.saveCard(tempCard,cards)

            #deckList.insert(tempDeck)
            conn.commit()
            oneCardFrame.destroy()
            #DeckView.createMainMenu(root)
            deckName = ''
            decks = main_menu.getDecks()
            for deck in decks:
                if card[1] == deck[0]:
                    deckName = deck[1]
            DeckView.createDeckView(root,decks,card[1],deckName)
        
        save_b = Button(oneCardFrame,
                           command=getSaveCard,
                           text='Save And Quit')
        save_b.grid(row=2,column=0,columnspan=2,sticky=W)

    def saveCard(newCard,cards):
                
        #check if deck_name is unique
        maxCard = DeckView.getMaxCardID()
        c.execute("SELECT * FROM {tn}".                  format(tn='Card'))
        cardNames = c.fetchall()
        cardError = 0
        cardExists = 0
        for card in cardNames:
            if newCard[2] == card[2] and newCard[3] == card[3] and newCard[0] != card[0]:
                cardError += 1
            if newCard[0] == card[0]:
                cardExists += 1
                
        if cardError == 1:
            print('error')
        else:
            c.execute("INSERT OR REPLACE INTO {tn} (card_id,deck_id, question,answer) VALUES ({ci},{cq},'{ca}','{cf}')".                      format(tn='Card',ci=newCard[0],cq=newCard[1],ca=newCard[2],cf=newCard[3]))
            
class PlayView:
    
    #open existing card
    def __init__(self,master,deckName,deckID):
        
        test = PlayView.createPlayFrame(master,deckName,deckID)
        
    def createPlayFrame(master,deckName,deckID):
   
        playFrame = Frame(master)
        playFrame.grid(row=0,column=0)
        
        menubar = Menu(playFrame)
        master.config(menu=menubar,bd=5)
        
        def mainBack():
            playFrame.destroy()
            main_menu.createMainMenu(root)
            
        menubar.add_command(label="Main Menu",
                            command=mainBack)
        
        labell = Label(playFrame,
                       text='Deck:',
                       anchor=W,
                       bg='lightgray',
                       font=("Arial",12))
        labell.grid(row=0,column=0,sticky=W)
        
        label2 = Label(playFrame,
                       text=deckName,
                       anchor=W,
                       bg='white',
                       font=("Arial",12))
        label2.grid(row=0,column=1,sticky=W)
        
        def playDeck():
            cards_QA = DeckView.getCards(deckID)
            playCards = []
            for card in cards_QA:
                tempPlayCards = []
                tempPlayCards.append(card[0])
                tempPlayCards.append(card[1])
                tempPlayCards.append(card[2])
                tempPlayCards.append(card[3])
                tempPlayCards.append(homeDirectory + str(card[0]) + '_' + str(card[1]) + '_question.mp3')
                tempPlayCards.append(homeDirectory + str(card[0]) + '_' + str(card[1]) + '_answer.mp3')
                playCards.append(tempPlayCards)
                
            
            settings = SettingsMenu.getSavedSettings()
            for setting in settings:
                if setting[1] == 'Shuffle':
                    v_shuffle = setting[2]
                elif setting[1] == 'Delay':
                    v_delay = setting[2]
            
            if v_shuffle == 1:
                random.shuffle(playCards)
            PlayView.Play(master,playCards,playFrame,v_delay)
        
        button1 = Button(playFrame,
                         command=playDeck,
                         text='Begin')
        button1.grid(row=1,column=0,columnspan=2,ipadx=30)

        
        
    def Play(master,playCards,playFrame,delay):
        
        #oneCardFrame.destroy()
        #playTop = Toplevel(master,width=335,height=200)
        #playTop.minsize(335,200)
        v = StringVar()
        vTemp = ''
        textBox = Message(playFrame,
                          relief=RAISED,
                          justify=LEFT,
                          bg='white',
                          width=200,
                          textvariable=v).grid(row=1,columnspan=4,rowspan=10,sticky=NW)

        #playFrame = Frame(playTop)
        #playFrame.grid(row=0,column=0)
        #loop through cards
        card_ct = 1
        for card in playCards:
            #tempPlay = PlayView.playCard(playFrame,card,delay)
            PlayView.playAudio(card[4])
            vTemp += "Question " + str(card_ct) + ":\n"
            vTemp += "Q: " + card[2] + "\n"
            time.sleep(delay)
            PlayView.playAudio(card[5])
            vTemp += "A: " + card[3] + "\n"
            card_ct += 1
            v.set(vTemp)
            time.sleep(delay)
            
    
    def playCard(playFrame,card,delay):
        #display question
        labelq1 = Label(playFrame,
                        text='Question:',
                        anchor=W,
                        bg='lightgray',
                        font=("Arial",12))
        labelq1.grid(row=0,column=0,sticky=W)
        
        labelq2 = Label(playFrame,
                        text=card[2],
                        anchor=W,
                        bg='white',
                        font=("Arial",12))
        labelq2.grid(row=0,column=1,sticky=W)
        
        #play question audio
        PlayView.playAudio(card[4])
        #wait x seconds
        #time.sleep(delay)
        
    def playAudio(fileName):
        myQuestion = AudioSegment.from_mp3(fileName)
        play(myQuestion)

root = Tk()
conn = sqlite3.connect(sqliteFile)
c = conn.cursor()
mm = main_menu(master=root)
mm.mainloop()
conn.close()
root.destroy()

