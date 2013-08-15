BEGIN EXCLUSIVE TRANSACTION;

CREATE TABLE dbms (
  id_dbms INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
); 

CREATE TABLE user (
  id_user INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  login TEXT UNIQUE NOT NULL,
  pwd TEXT NOT NULL,
  name TEXT NOT NULL,
  comments TEXT
);

CREATE TABLE user_pref (
  id_user INTEGER NOT NULL PRIMARY KEY,
  label_lang TEXT NOT NULL,
  FOREIGN KEY(id_user) REFERENCES user(id_user)
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
  code TEXT UNIQUE NOT NULL,
  description TEXT
);

CREATE TABLE subcoll (
  id_subcoll INTEGER NOT NULL,
  id_coll INTEGER NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  PRIMARY KEY(id_subcoll),  
  FOREIGN KEY(id_coll) REFERENCES coll(id_coll)
);

CREATE TABLE sys_config (
  id_subcoll INTEGER NOT NULL,
  date_input_mask TEXT,
  date_output_mask TEXT,
  label_lang TEXT,
  PRIMARY KEY(id_subcoll),
  FOREIGN KEY(id_subcoll) REFERENCES subcoll(id_subcoll)
);

CREATE TABLE sys_data_lang (
  id_subcoll INTEGER NOT NULL,
  data_lang TEXT NOT NULL,
  lang_index INTEGER NOT NULL,
  PRIMARY KEY(id_subcoll, data_lang),
  FOREIGN KEY(id_subcoll) REFERENCES subcoll(id_subcoll)
);

CREATE TABLE access (
  id_user INTEGER NOT NULL,
  id_subcoll INTEGER NOT NULL,
  PRIMARY KEY(id_user, id_subcoll),  
  FOREIGN KEY(id_subcoll) REFERENCES subcoll(id_subcoll),
  FOREIGN KEY(id_user) REFERENCES user(id_user)
);

CREATE TABLE db_info (
  version INTEGER NOT NULL PRIMARY KEY
);

CREATE INDEX FK_user1 ON user_pref(id_user);
CREATE INDEX FK_user2 ON access(id_user);
CREATE INDEX FK_dbms ON dbms(id_dbms);
CREATE INDEX FK_coll ON subcoll(id_coll);
CREATE INDEX FK_coll_subcoll1 ON access(id_subcoll);
CREATE INDEX FK_coll_subcoll2 ON sys_config(id_subcoll);
CREATE INDEX FK_coll_subcoll3 ON sys_data_lang(id_subcoll);
CREATE INDEX Unique_lang_index ON sys_data_lang(id_subcoll,lang_index);

COMMIT TRANSACTION;
