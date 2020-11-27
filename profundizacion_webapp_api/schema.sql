DROP TABLE IF EXISTS  titulo;

CREATE TABLE titulo (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [userId] INTEGER  NOT NULL,
    [title] STRING NOT NULL,
    [completed] STRING 
);