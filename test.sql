DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS profile;
DROP TABLE IF EXISTS allergen;
DROP TABLE IF EXISTS allergenListItem;
DROP TABLE IF EXISTS allergenListProfile;
DROP TABLE IF EXISTS persist_item;
DROP TABLE IF EXISTS persist_allergenListItem;
DROP TABLE IF EXISTS itemdate;
DROP TABLE IF EXISTS doorLog;

CREATE TABLE persist_item (
	ID INTEGER PRIMARY KEY,
	GTIN TEXT,
	name TEXT,
	ingredients TEXT,
	qt INTEGER
	);

CREATE TABLE itemdate (
	ID INTEGER PRIMARY KEY,
	foodID INTEGER, 
	indate DATETIME,
	expdate DATETIME,
	outdate DATETIME DEFAULT NULL,
	FOREIGN KEY(foodID) REFERENCES persist_item(ID) ON DELETE CASCADE
	);

CREATE TABLE persist_allergenListItem (
	ID INTEGER PRIMARY KEY,
	foodID INTEGER,
	allergenID INTEGER,
	FOREIGN KEY(foodID) REFERENCES persist_item(ID) ON DELETE CASCADE,
	FOREIGN KEY(allergenID) REFERENCES allergen(ID)
	);

CREATE TABLE item (
	ID INTEGER PRIMARY KEY,
	GTIN TEXT,
	name TEXT,
	ingredients TEXT,
	indate DATETIME DEFAULT (datetime('now','localtime')),
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
	FOREIGN KEY(foodID) REFERENCES item(ID) ON DELETE CASCADE,
	FOREIGN KEY(allergenID) REFERENCES allergen(ID)
	);

CREATE TABLE allergenListProfile (
	ID INTEGER PRIMARY KEY,
	profileID INTEGER,
	allergenID INTEGER,
	FOREIGN KEY(profileID) REFERENCES profile(ID) ON DELETE CASCADE,
	FOREIGN KEY(allergenID) REFERENCES allergen(ID)
	);

CREATE TABLE doorLog (
	ID INTEGER PRIMARY KEY,
	opendate DATETIME DEFAULT (datetime('now','localtime')),
	closedate DATETIME DEFAULT NULL
	);
