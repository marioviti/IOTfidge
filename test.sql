DROP TABLE IF EXISTS item;

CREATE TABLE item (
	ID INTEGER,
	EAN13 TEXT,
	name TEXT,
	indate DATETIME DEFAULT (datetime('now','localtime')),
	expdate DATETIME
	);


