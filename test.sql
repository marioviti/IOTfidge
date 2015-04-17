DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS profile;
DROP TABLE IF EXISTS allergen;
DROP TABLE IF EXISTS allergenListItem;
DROP TABLE IF EXISTS allergenListProfile;

PRAGMA foreign_keys = ON;

CREATE TABLE item (
	ID INTEGER PRIMARY KEY,
	GTIN TEXT,
	name TEXT,
	ingredients TEXT,
	indate DATETIME DEFAULT (datetime('now','localtime')),
	expdate DATETIME
	);

CREATE TABLE persist_item (
	ID INTEGER PRIMARY KEY,
	GTIN TEXT,
	name TEXT,
	qt INTEGER,
	ingredients TEXT,
	indate DATETIME,
	expdate DATETIME
	);

CREATE TABLE profile (
	ID INTEGER PRIMARY KEY,
	name TEXT,
	last_name TEXT
	);

CREATE TABLE allergen (
	ID INTEGER PRIMARY KEY,
	name TEXT
	);

CREATE TABLE allergenListItem (
	ID INTEGER PRIMARY KEY,
	foodID INTEGER,
	allergenID INTEGER,
	FOREIGN KEY(foodID) REFERENCES persist_item(ID) ON DELETE CASCADE,
	FOREIGN KEY(allergenID) REFERENCES allergen(ID)
	);

CREATE TABLE allergenListProfile (
	ID INTEGER PRIMARY KEY,
	profileID INTEGER,
	allergenID INTEGER,
	FOREIGN KEY(profileID) REFERENCES profile(ID) ON DELETE CASCADE,
	FOREIGN KEY(allergenID) REFERENCES allergen(ID)
	);
