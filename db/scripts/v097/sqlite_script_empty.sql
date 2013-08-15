BEGIN EXCLUSIVE TRANSACTION;

CREATE TABLE dbms (
  id_dbms INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
); 

CREATE TABLE user (
  id_user INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  login TEXT NOT NULL,
  pwd TEXT NOT NULL,
  name TEXT NOT NULL,
  comments TEXT
);

CREATE TABLE base (
  id_base INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  id_dbms INTEGER NOT NULL,
  host TEXT NOT NULL,
  port INTEGER NOT NULL,
  dbname TEXT NOT NULL,
  user TEXT,
  pwd TEXT,
  description TEXT,
  FOREIGN KEY(id_dbms) REFERENCES dbms(id_dbms)
);

CREATE TABLE coll (
  id_coll INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  id_base INTEGER NOT NULL,
  code TEXT NOT NULL,
  description TEXT
);

CREATE TABLE subcoll (
  id_subcoll INTEGER NOT NULL,
  id_coll INTEGER NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  PRIMARY KEY(id_subcoll, id_coll),  
  FOREIGN KEY(id_coll) REFERENCES coll(id_coll)
);

CREATE TABLE access (
  id_user INTEGER NOT NULL,
  id_coll INTEGER NOT NULL,
  id_subcoll INTEGER NOT NULL,
  PRIMARY KEY(id_user, id_coll, id_subcoll),  
  FOREIGN KEY(id_subcoll, id_coll) REFERENCES subcoll(id_subcoll, id_coll),
  FOREIGN KEY(id_user) REFERENCES user(id_user)
);

CREATE UNIQUE INDEX user_login ON user(login);
CREATE UNIQUE INDEX coll_code ON coll(code);
CREATE INDEX FK_dbms ON dbms(id_dbms);
CREATE INDEX FK_coll ON subcoll(id_coll);
CREATE INDEX FK_coll_subcoll ON access(id_subcoll, id_coll);
CREATE INDEX FK_user ON access(id_user);

COMMIT TRANSACTION;