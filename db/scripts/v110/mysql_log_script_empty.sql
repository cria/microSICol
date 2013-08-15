DROP DATABASE IF EXISTS sicol_v110_log;
CREATE DATABASE IF NOT EXISTS sicol_v110_log CHARACTER SET utf8;
USE sicol_v110_log;

CREATE TABLE log_operations (
  id_log_operation INTEGER UNSIGNED NOT NULL,
  label VARCHAR(100) NOT NULL,
  PRIMARY KEY(id_log_operation)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE log_entities (
  id_log_entity INTEGER UNSIGNED NOT NULL,
  label VARCHAR(100) NOT NULL,
  PRIMARY KEY(id_log_entity)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE log_fields (
  id_log_field INTEGER UNSIGNED NOT NULL,
  label VARCHAR(100) NOT NULL,
  mlang_value TINYINT(1) NOT NULL DEFAULT 0 COMMENT '0 = false, 1 = true',
  mlang_table VARCHAR(100) NULL,
  mlang_key VARCHAR(100) NULL,
  mlang_field VARCHAR(100) NULL,
  label_value_lookup VARCHAR(100) NULL,
  PRIMARY KEY(id_log_field)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE log (
  id_log BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  date_time DATETIME NOT NULL,
  user VARCHAR(255) NOT NULL,
  id_log_operation INTEGER UNSIGNED NOT NULL,
  id_subcoll TINYINT UNSIGNED NOT NULL,
  id_log_entity INTEGER UNSIGNED NOT NULL,
  id_entity INTEGER UNSIGNED NOT NULL,
  code_entity VARCHAR(255) NOT NULL,
  lot VARCHAR(255) NULL,
  id_log_field INTEGER UNSIGNED NULL,
  lang VARCHAR(10) NULL,
  value TEXT NULL,
  PRIMARY KEY(id_log),
  INDEX FK_log_operation(id_log_operation),
  INDEX FK_log_entity(id_log_entity),
  INDEX FK_log_field(id_log_field),
  FOREIGN KEY(id_log_operation)
    REFERENCES log_operations(id_log_operation)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_log_entity)
    REFERENCES log_entities(id_log_entity)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_log_field)
    REFERENCES log_fields(id_log_field)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;