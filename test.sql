DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS profile;
DROP TABLE IF EXISTS allergen;

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
	profileID INTEGER,
	name TEXT,
	FOREIGN KEY(profileID) REFERENCES profile(ID)
	);


