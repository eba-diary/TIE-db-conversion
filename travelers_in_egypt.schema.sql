CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE IF NOT EXISTS "travelers" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"name"	TEXT,
	"nationality"	TEXT
);
CREATE TABLE IF NOT EXISTS "publications" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"title"	TEXT,
	"travel_dates"	TEXT,
	"traveler_id"	INTEGER,
	"publisher"	TEXT,
	"publication_place"	TEXT,
	"publication_date"	TEXT,
	"summary"	TEXT,
	"url"	TEXT,
	"iiif"	TEXT,
	FOREIGN KEY("traveler_id") REFERENCES "travelers"("id")
);
