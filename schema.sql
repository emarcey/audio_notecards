-- each row corresponds to a deck of cards
CREATE TABLE Deck {
	deck_id		INTEGER,
	deck_name	TEXT
};

-- each row corresponds to a flashcard within a deck. Question/Answer are the text inputs for each card.
CREATE TABLE Card {
	card_id 	INTEGER,
	deck_id 	INTEGER,
	question	TEXT,
	answer		TEXT
};

-- each row corresponds to a setting that can be changed from the settings menu
CREATE TABLE Settings {
	settings_id	INTEGER,
	setting		TEXT,
	value		INTEGER
};
