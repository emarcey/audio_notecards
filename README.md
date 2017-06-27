# audio_notecards

# Overview
Create and store Q&A flashcards that generate audio recordings so the flashcards can be read back to you. The idea comes from someone asking for a flashcard app they could use while driving.

# Files
Notecards.py:
  - The main file to be used is Notecards. This initializes the notecard window, allows you to:
    - edit settings
    - create/edit/delete cards and decks
    - Run through a deck of cards
  - The interface is built in tkinter, with data stored in a SQLite instance, and audio generated and played back by pydub.
  
# Notecards_Setup.py:
  - Should be run prior to running Notecards.py
  - Ensures that all Python packages are installed
  - Creates home C:\\Notecards\ directory
  - Creates database and tables, populates sample records
 
# Notecards.sqlite
  - SQLite database used to store setting information, flashcards and decks.
  - See schema for more information
  
# Limitations
  - Cards will throw an error if you try to use an apostrophe in the text. This is just due to how the SQL is written. Change forthcoming.
