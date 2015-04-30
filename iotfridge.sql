DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS profile;
DROP TABLE IF EXISTS allergen;
DROP TABLE IF EXISTS allergenListItem;
DROP TABLE IF EXISTS allergenListProfile;
DROP TABLE IF EXISTS persist_item;
DROP TABLE IF EXISTS persist_allergenListItem;
DROP TABLE IF EXISTS itemdate;
DROP TABLE IF EXISTS doorLog;
DROP TABLE IF EXISTS users_data;
DROP TABLE IF EXISTS itemToAllergen;
DROP TABLE IF EXISTS itemToProfile;
DROP TABLE IF EXISTS allergenToProfile;

CREATE TABLE users_data (
	ID INTEGER PRIMARY KEY,
	usr TEXT,
	passwd TEXT,
	salt TEXT
	);

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

CREATE TABLE itemToAllergen (
	item TEXT,
	allerg TEXT
	);

CREATE TABLE itemToProfile (
	item TEXT,
	name TEXT,
	last_name TEXT
	);

CREATE TABLE allergenToProfile (
	name TEXT,
	last_name TEXT,
	allerg TEXT
	);

CREATE TRIGGER persist_item_log AFTER INSERT ON persist_allergenListItem
BEGIN
   	INSERT INTO itemToAllergen (item,allerg)
   	SELECT DISTINCT persist_item.item_name, allergen.allergen_name 
   	FROM persist_item JOIN persist_allergenListItem ON persist_item.ID = persist_allergenListItem.item_ID 
   	JOIN allergen ON allergen.ID = persist_allergenListItem.allergen_ID 
   	WHERE persist_item.ID = (SELECT MAX(ID) FROM persist_item);
END;

CREATE TRIGGER persist_item_allergen_log AFTER INSERT ON persist_allergenListItem
BEGIN
   	INSERT INTO itemToProfile (item,name,last_name)
   	SELECT DISTINCT persist_item.item_name, profile.profile_name, profile.profile_last_name 
   	FROM persist_item JOIN persist_allergenListItem ON persist_item.ID = persist_allergenListItem.item_ID 
   	JOIN allergenListProfile ON persist_allergenListItem.allergen_ID = allergenListProfile.allergen_ID 
   	JOIN profile ON profile.ID = allergenListProfile.profile_ID
   	WHERE persist_item.ID = (SELECT MAX(ID) FROM persist_item);
END;

CREATE TRIGGER profile_allergen_log AFTER INSERT ON allergenListProfile
BEGIN
   	INSERT INTO itemToProfile (item,name,last_name)
   	SELECT DISTINCT persist_item.item_name, profile.profile_name, profile.profile_last_name 
   	FROM persist_item JOIN persist_allergenListItem ON persist_item.ID = persist_allergenListItem.item_ID 
   	JOIN allergenListProfile ON persist_allergenListItem.allergen_ID = allergenListProfile.allergen_ID 
   	JOIN profile ON profile.ID = allergenListProfile.profile_ID
   	WHERE profile.ID = (SELECT MAX(ID) FROM profile);
END;

CREATE TRIGGER profile_log AFTER INSERT ON allergenListProfile
BEGIN
	INSERT INTO allergenToProfile (name,last_name,allerg)
	SELECT DISTINCT profile.profile_name, profile.profile_last_name, allergen.allergen_name 
	FROM profile JOIN allergenListProfile ON profile.ID = allergenListProfile.profile_ID 
	JOIN allergen ON allergen.ID = allergenListProfile.allergen_ID 
	WHERE profile.ID = (SELECT MAX(ID) FROM profile);
END;


