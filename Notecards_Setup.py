
# coding: utf-8

# In[15]:

#import statements
#install if not present
import os
import sys

try:
    from tkinter import *
    from tkinter import ttk
    print('Tkinter imported.')
except:
    print('Installing Tkinter...')
    os.system('pip install tkinter')
    print('Tkinter installed.')
    from tkinter import *
    from tkinter import ttk
    print('Tkinter imported.')
    
try:
    import csv
    print('csv imported.')
except:
    print('Installing csv...')
    os.system('pip install csv')
    print('csv installed.')
    import csv
    print('csv imported.')
    
try:
    import sqlite3
    print('sqlite3 imported.')
except:
    print('Installing sqlite3...')
    os.system('pip install sqlite3')
    print('sqlite3 installed.')
    import sqlite3
    print('sqlite3 imported.')
    
try:
    from gtts import gTTS
    print('gtts imported.')
except:
    print('Installing gtts...')
    os.system('pip install gtts')
    print('gtts installed.')
    from gtts import gTTS
    print('gtts imported.')
    
try:
    from pydub import AudioSegment
    from pydub.playback import play
    print('pydub imported.')
except:
    print('Installing pydub...')
    os.system('pip install pydub')
    print('pydub installed.')
    from pydub import AudioSegment
    from pydub.playback import play
    print('pydub imported.')
    
try:
    import random
    print('random imported.')
except:
    print('Installing random...')
    os.system('pip install random')
    print('random installed.')
    import random
    print('random imported.')

try:
    import time
    print('time imported.')
except:
    print('Installing time...')
    os.system('pip install time')
    print('time installed.')
    import time
    print('time imported.')

#create home directory
homeDirectory = "C:\\Notecards\\"

if not os.path.exists(homeDirectory):
    os.makedirs(homeDirectory)

#create db tables
sqliteFile = 'Notecards.sqlite'
tn_c = 'Card'
tn_d = 'Deck'
tn_s = 'Settings'
id_field1 = 'deck_id'
id_field2 = 'card_id'
id_field3 = 'settings_id'
deckName = 'name'
q = 'question'
a = 'answer'
s1 = 'setting'
s2 = 'value'
intType = 'INTEGER'
txtType = 'TEXT'

#open connection
conn = sqlite3.connect(sqliteFile)
c = conn.cursor()

#create settings table
c.execute("CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)"          .format(tn=tn_s,nf=id_field3,ft=intType))
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"          .format(tn=tn_s,cn=s1,ct=txtType))
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"          .format(tn=tn_s,cn=s2,ct=intType))

#create deck table
c.execute("CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)"          .format(tn=tn_d,nf=id_field1,ft=intType))
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"          .format(tn=tn_d,cn=deckName,ct=txtType))

#create card table
c.execute("CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)"          .format(tn=tn_c,nf=id_field2,ft=intType))
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"          .format(tn=tn_c,cn=id_field1,ct=intType))
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"          .format(tn=tn_c,cn=q,ct=txtType))
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"          .format(tn=tn_c,cn=a,ct=txtType))

#set default settings values
s1a = 1
s1b = 'Shuffle'
s1c = 1
s2a = 2
s2b = 'Delay'
s2c = 3
c.execute("INSERT INTO {tn} VALUES ({id2},'{cq}',{ca})".        format(tn=tn_s,id2=s1a, cq=s1b,ca=s1c))
c.execute("INSERT INTO {tn} VALUES ({id2},'{cq}',{ca})".        format(tn=tn_s,id2=s2a, cq=s2b,ca=s2c))

#insert sample deck
deck_ID = 1
deck_Name = 'Sample'
c.execute("INSERT INTO {tn} VALUES ({id2},'{cq}')".        format(tn=tn_d,id2=deck_ID, cq=deck_Name))

#add sample cards to deck
id1 = 1
id2 = 1
id3 = 2
q1 = 'Question'
a1 = 'Answer'
q2 = 'Is this thing on?'
a2 = 'That is a dumb question.'

c.execute("INSERT INTO {tn} VALUES ({id1},{id2},'{cq}','{ca}')".        format(tn=tn_c,id1=id1,id2=id2, cq=q1,ca=a1))
c.execute("INSERT INTO {tn} VALUES ({id1},{id2},'{cq}','{ca}')".        format(tn=tn_c,id1=id3,id2=id2, cq=q2,ca=a2))

conn.commit()
conn.close()

#create audio for sample cards
filename = homeDirectory + str(id2) + '_' + str(id1) + '_question'
tts = gTTS(text=q1,lang='en')
tts.save(filename + '.mp3')

filename = homeDirectory + str(id2) + '_' + str(id1) + '_answer'
tts = gTTS(text=a1,lang='en')
tts.save(filename + '.mp3')

filename = homeDirectory + str(id3) + '_' + str(id1) + '_question'
tts = gTTS(text=q2,lang='en')
tts.save(filename + '.mp3')

filename = homeDirectory + str(id3) + '_' + str(id1) + '_answer'
tts = gTTS(text=a2,lang='en')
tts.save(filename + '.mp3')


