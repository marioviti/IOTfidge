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
	item_name TEXT,
	ingredients TEXT,
	qt INTEGER
	);

CREATE TABLE itemdate (
	ID INTEGER PRIMARY KEY,
	item_ID INTEGER, 
	indate DATETIME,
	expdate DATETIME,
	outdate DATETIME DEFAULT NULL,
	FOREIGN KEY(item_ID) REFERENCES persist_item(ID) ON DELETE CASCADE
	);

CREATE TABLE persist_allergenListItem (
	ID INTEGER PRIMARY KEY,
	item_ID INTEGER,
	allergen_ID INTEGER,
	FOREIGN KEY(item_ID) REFERENCES persist_item(ID) ON DELETE CASCADE,
	FOREIGN KEY(allergen_ID) REFERENCES allergen(ID)
	);

CREATE TABLE item (
	ID INTEGER PRIMARY KEY,
	GTIN TEXT,
	item_name TEXT,
	ingredients TEXT,
	indate DATETIME DEFAULT (datetime('now','localtime')),
	expdate DATETIME
	);

CREATE TABLE profile (
	ID INTEGER PRIMARY KEY,
	profile_name TEXT,
	profile_last_name TEXT
	);

CREATE TABLE allergen (
	ID INTEGER PRIMARY KEY,
	allergen_name TEXT
	);

CREATE TABLE allergenListItem (
	ID INTEGER PRIMARY KEY,
	item_ID INTEGER,
	allergen_ID INTEGER,
	FOREIGN KEY(item_ID) REFERENCES item(ID) ON DELETE CASCADE,
	FOREIGN KEY(allergen_ID) REFERENCES allergen(ID)
	);

CREATE TABLE allergenListProfile (
	ID INTEGER PRIMARY KEY,
	profile_ID INTEGER,
	allergen_ID INTEGER,
	FOREIGN KEY(profile_ID) REFERENCES profile(ID) ON DELETE CASCADE,
	FOREIGN KEY(allergen_ID) REFERENCES allergen(ID)
	);

CREATE TABLE doorLog (
	ID INTEGER PRIMARY KEY,
	opendate DATETIME DEFAULT (datetime('now','localtime')),
	closedate DATETIME DEFAULT NULL
	);
