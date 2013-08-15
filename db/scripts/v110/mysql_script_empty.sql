DROP DATABASE IF EXISTS sicol_v110;
CREATE DATABASE IF NOT EXISTS sicol_v110 CHARACTER SET utf8;
USE sicol_v110;

CREATE TABLE lang (
  id_lang TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  code CHAR(4) NOT NULL,
  lang VARCHAR(30) NOT NULL,
  lang_en VARCHAR(30) NOT NULL,
  PRIMARY KEY(id_lang),
  UNIQUE INDEX code(code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE loc_country (
  id_country INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  code CHAR(2) NOT NULL,
  PRIMARY KEY(id_country),
  UNIQUE INDEX code(code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_clinical_form (
  id_clinical_form SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  PRIMARY KEY(id_clinical_form)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE person (
  id_person INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  nickname VARCHAR(50) NULL,
  address TEXT NULL,
  phone TEXT NULL,
  email VARCHAR(100) NULL,
  last_update DATETIME NULL,
  go_catalog TINYINT(1) NOT NULL DEFAULT 0 COMMENT '0 = false, 1 = true',
  PRIMARY KEY(id_person),
  UNIQUE INDEX person_key(name, nickname)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE spe_name_qualifier (
  id_name_qualifier TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  PRIMARY KEY(id_name_qualifier)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_dep_reason (
  id_dep_reason TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  PRIMARY KEY(id_dep_reason)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_dep_reason_lang (
  id_dep_reason TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  dep_reason VARCHAR(25) NOT NULL,
  PRIMARY KEY(id_dep_reason, id_lang),
  INDEX FK_lang(id_lang),
  INDEX FK_dep_reason(id_dep_reason),
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_dep_reason)
    REFERENCES str_dep_reason(id_dep_reason)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_dep_reason_subcoll (
  id_dep_reason TINYINT UNSIGNED NOT NULL,
  id_subcoll TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY(id_dep_reason,id_subcoll)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_gps_datum (
  id_gps_datum SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  gps_datum VARCHAR(20) NOT NULL,
  PRIMARY KEY(id_gps_datum)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE ref (
  id_ref INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_subcoll TINYINT UNSIGNED NOT NULL,
  title TEXT NOT NULL,
  author VARCHAR(100) NULL,
  year VARCHAR(100) NULL,
  url TEXT NULL,
  last_update DATETIME NULL,
  go_catalog TINYINT(1) NOT NULL DEFAULT 0 COMMENT '0 = false, 1 = true',
  PRIMARY KEY(id_ref, id_coll)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE institution (
  id_institution INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  code1 VARCHAR(20) NULL,
  code2 VARCHAR(20) NULL,
  code3 VARCHAR(20) NULL,
  complement VARCHAR(100) NULL,
  nickname VARCHAR(50) NULL,
  name VARCHAR(80) NOT NULL,
  address TEXT NULL,
  phone TEXT NULL,
  email VARCHAR(100) NULL,
  website VARCHAR(100) NULL,
  last_update DATETIME NULL,
  go_catalog TINYINT(1) NOT NULL DEFAULT 0 COMMENT '0 = false, 1 = true',
  PRIMARY KEY(id_institution),
  UNIQUE INDEX institution_key(complement, nickname)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_type (
  id_type TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  PRIMARY KEY(id_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_type_subcoll (
  id_type TINYINT UNSIGNED NOT NULL,
  id_subcoll TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY(id_type,id_subcoll)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_type_lang (
  id_type TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  type VARCHAR(15) NOT NULL,
  PRIMARY KEY(id_type, id_lang),
  INDEX FK_lang(id_lang),
  INDEX FK_type(id_type),
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_type)
    REFERENCES str_type(id_type)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE doc_qualifier (
  id_qualifier TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  qualifier VARCHAR(20) NOT NULL,
  PRIMARY KEY(id_qualifier)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE test_group (
  id_test_group TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  PRIMARY KEY(id_test_group)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE test_group_subcoll (
  id_test_group TINYINT UNSIGNED NOT NULL,
  id_subcoll TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY(id_test_group, id_subcoll),
  FOREIGN KEY(id_test_group)
    REFERENCES test_group(id_test_group)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE test_group_lang (
  id_test_group TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  category VARCHAR(100) NOT NULL,
  PRIMARY KEY(id_test_group, id_lang),
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_test_group)
    REFERENCES test_group(id_test_group)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE doc (
  id_doc INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_subcoll TINYINT UNSIGNED NOT NULL,
  code VARCHAR(20) NOT NULL,
  id_qualifier TINYINT UNSIGNED NULL,
  id_test_group TINYINT UNSIGNED NULL,
  last_update DATETIME NULL,
  go_catalog TINYINT(1) NOT NULL DEFAULT 0 COMMENT '0 = false, 1 = true',
  PRIMARY KEY(id_doc, id_coll),
  UNIQUE INDEX code_coll(code,id_coll),
  INDEX FK_qualifier(id_qualifier),
  INDEX FK_test_group(id_test_group),
  FOREIGN KEY(id_qualifier)
    REFERENCES doc_qualifier(id_qualifier)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_test_group)
    REFERENCES test_group(id_test_group)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE loc_state (
  id_state INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  id_country INTEGER UNSIGNED NOT NULL,
  code CHAR(4) NOT NULL,
  state VARCHAR(255) NOT NULL,
  PRIMARY KEY(id_state, id_country),
  UNIQUE INDEX code(id_state, id_country, code),
  INDEX FK_country(id_country),
  FOREIGN KEY(id_country)
    REFERENCES loc_country(id_country)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE loc_city (
  id_city INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  id_state INTEGER UNSIGNED NOT NULL,
  id_country INTEGER UNSIGNED NOT NULL,
  city VARCHAR(255) NOT NULL,
  PRIMARY KEY(id_city, id_state, id_country),
  INDEX FK_country_state(id_state, id_country),
  FOREIGN KEY(id_state, id_country)
    REFERENCES loc_state(id_state, id_country)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_clinical_form_lang (
  id_clinical_form SMALLINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  code VARCHAR(10) NOT NULL,
  clinical_form VARCHAR(100) NOT NULL,
  PRIMARY KEY(id_clinical_form, id_lang),
  INDEX FK_lang(id_lang),
  INDEX FK_clinical_form(id_clinical_form),
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_clinical_form)
    REFERENCES str_clinical_form(id_clinical_form)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE ref_comments (
  id_lang TINYINT UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_ref INTEGER UNSIGNED NOT NULL,
  comments TEXT NOT NULL,
  PRIMARY KEY(id_lang, id_coll, id_ref),
  INDEX FK_lang(id_lang),
  INDEX FK_ref_coll(id_ref, id_coll),
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_ref, id_coll)
    REFERENCES ref(id_ref, id_coll)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE taxon_group (
  id_taxon_group TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  PRIMARY KEY(id_taxon_group)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE taxon_group_subcoll (
  id_taxon_group TINYINT UNSIGNED NOT NULL,
  id_subcoll TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY(id_taxon_group, id_subcoll),
  FOREIGN KEY(id_taxon_group)
    REFERENCES taxon_group(id_taxon_group)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE taxon_group_lang (
  id_taxon_group TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  taxon_group VARCHAR(100) NOT NULL,
  PRIMARY KEY(id_taxon_group, id_lang),
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_taxon_group)
    REFERENCES taxon_group(id_taxon_group)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE hierarchy_def (
  id_hierarchy INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  seq INTEGER NOT NULL,
  hi_tax BOOLEAN NOT NULL DEFAULT TRUE,
  has_author BOOLEAN NOT NULL DEFAULT TRUE,
  use_author BOOLEAN NOT NULL DEFAULT FALSE,
  in_sciname BOOLEAN NOT NULL DEFAULT FALSE,
  required BOOLEAN NOT NULL DEFAULT FALSE,
  important BOOLEAN NOT NULL DEFAULT FALSE,
  string_format ENUM('none','italic','bold','italic-bold') NOT NULL DEFAULT 'none',
  string_case ENUM('none','lower','upper','ucfirst') NOT NULL DEFAULT 'none',
  prefix VARCHAR(200) NULL,
  suffix VARCHAR(200) NULL,
  PRIMARY KEY(id_hierarchy),
  UNIQUE INDEX seq_key(seq)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE hierarchy_lang (
  id_hierarchy INTEGER UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  rank VARCHAR(255) NOT NULL,
  PRIMARY KEY(id_hierarchy, id_lang),
  INDEX FK_hierarchy(id_hierarchy),
  INDEX FK_lang(id_lang),
  FOREIGN KEY(id_hierarchy)
    REFERENCES hierarchy_def(id_hierarchy)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE hierarchy_group (
  id_hierarchy INTEGER UNSIGNED NOT NULL,
  id_taxon_group TINYINT UNSIGNED NOT NULL,
  id_subcoll TINYINT UNSIGNED NOT NULL,
  hi_tax BOOLEAN NULL,
  has_author BOOLEAN NULL,
  use_author BOOLEAN NULL,
  in_sciname BOOLEAN NULL,
  required BOOLEAN NULL,
  important BOOLEAN NULL,
  string_format ENUM('none','italic','bold','italic-bold') NULL,
  string_case ENUM('none','lower','upper','ucfirst') NULL,
  prefix VARCHAR(200) NULL,
  suffix VARCHAR(200) NULL,
  default_value VARCHAR(255) NULL,
  PRIMARY KEY(id_hierarchy, id_taxon_group, id_subcoll),
  INDEX FK_hierarchy(id_hierarchy),
  FOREIGN KEY(id_hierarchy)
    REFERENCES hierarchy_def(id_hierarchy)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE scientific_names (
  id_sciname INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  hi_tax TEXT NULL,
  sciname TEXT NOT NULL,
  sciname_no_auth TEXT NOT NULL,
  PRIMARY KEY(id_sciname)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE scientific_names_hierarchy (
  id_sciname INTEGER UNSIGNED NOT NULL,
  id_hierarchy INTEGER UNSIGNED NOT NULL,
  value VARCHAR(255) NOT NULL,
  author VARCHAR(255) NULL,
  PRIMARY KEY(id_sciname, id_hierarchy),
  INDEX FK_sciname(id_sciname),
  INDEX FK_hierarchy(id_hierarchy),
  FOREIGN KEY(id_sciname)
    REFERENCES scientific_names(id_sciname)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_hierarchy)
    REFERENCES hierarchy_def(id_hierarchy)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE species (
  id_species INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_subcoll TINYINT UNSIGNED NOT NULL,
  id_taxon_group TINYINT UNSIGNED NOT NULL,
  id_sciname INTEGER UNSIGNED NOT NULL,
  id_name_qualifier TINYINT UNSIGNED NULL,
  taxon_ref TEXT NULL,
  synonym  TEXT NULL,
  hazard_group ENUM('1','2','3','4') NULL,
  hazard_group_ref TEXT NULL,
  id_alt_states INTEGER UNSIGNED NULL,
  alt_states_type ENUM('ana','teleo') NULL,
  last_update DATETIME NULL,
  PRIMARY KEY(id_species),
  UNIQUE INDEX species_sciname(id_sciname),
  INDEX FK_taxon_group(id_taxon_group),
  INDEX FK_name_qualifier(id_name_qualifier),
  FOREIGN KEY(id_taxon_group)
    REFERENCES taxon_group(id_taxon_group)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_sciname)
    REFERENCES scientific_names(id_sciname)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_name_qualifier)
    REFERENCES spe_name_qualifier(id_name_qualifier)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE doc_description (
  id_doc INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  description TEXT NOT NULL,
  PRIMARY KEY(id_doc, id_coll, id_lang),
  INDEX FK_doc_coll(id_doc, id_coll),
  INDEX FK_lang(id_lang),
  FOREIGN KEY(id_doc, id_coll)
    REFERENCES doc(id_doc, id_coll)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE per_comments (
  id_person INTEGER UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  comments TEXT NOT NULL,
  PRIMARY KEY(id_person, id_lang),
  INDEX FK_person(id_person),
  INDEX FK_lang(id_lang),
  FOREIGN KEY(id_person)
    REFERENCES person(id_person)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE doc_file (
  id_doc INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  file_name VARCHAR(100) NOT NULL,
  PRIMARY KEY(id_doc, id_coll, id_lang),
  INDEX FK_doc_coll(id_doc, id_coll),
  INDEX FK_lang(id_lang),
  FOREIGN KEY(id_doc, id_coll)
    REFERENCES doc(id_doc, id_coll)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE doc_title (
  id_doc INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  title VARCHAR(100) NOT NULL,
  PRIMARY KEY(id_doc, id_coll, id_lang),
  INDEX FK_lang(id_lang),
  INDEX FK_doc_coll(id_doc, id_coll),
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_doc, id_coll)
    REFERENCES doc(id_doc, id_coll)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE loc_country_lang (
  id_country INTEGER UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  country VARCHAR(255) NOT NULL,
  PRIMARY KEY(id_country, id_lang),
  INDEX FK_loc_country(id_country),
  INDEX FK_lang(id_lang),
  FOREIGN KEY(id_country)
    REFERENCES loc_country(id_country)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE inst_comments (
  id_institution INTEGER UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  comments TEXT NOT NULL,
  PRIMARY KEY(id_institution, id_lang),
  INDEX FK_lang(id_lang),
  INDEX FK_institution(id_institution),
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_institution)
    REFERENCES institution(id_institution)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE division (
  id_division SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_subcoll TINYINT UNSIGNED NOT NULL,
  division VARCHAR(50) NOT NULL,
  pattern varchar(50),
  PRIMARY KEY(id_division)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE strain (
  id_strain INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_subcoll TINYINT UNSIGNED NOT NULL,
  id_division SMALLINT UNSIGNED NOT NULL,
  code VARCHAR(30) NOT NULL,
  numeric_code INT UNSIGNED NOT NULL,
  internal_code VARCHAR(256) NULL,
  status ENUM('active','inactive','pending') NOT NULL,
  id_species INTEGER UNSIGNED NULL,
  infra_complement VARCHAR(50) NULL,
  id_type TINYINT UNSIGNED NULL,
  history TEXT NULL,
  extra_codes TEXT NULL,
  comments TEXT NULL,
  last_update DATETIME NULL,
  is_ogm TINYINT(1) NOT NULL DEFAULT 0 COMMENT '0 = false, 1 = true',
  go_catalog TINYINT(1) NOT NULL DEFAULT 0 COMMENT '0 = false, 1 = true',
  PRIMARY KEY(id_strain, id_coll),
  UNIQUE INDEX numeric_code_coll(numeric_code,id_coll),
  INDEX FK_division(id_division),
  INDEX FK_species(id_species),
  INDEX FK_str_type(id_type),
  FOREIGN KEY(id_division)
	REFERENCES division(id_division) 
	   ON DELETE RESTRICT
	   ON UPDATE RESTRICT,
  FOREIGN KEY(id_species)
    REFERENCES species(id_species)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_type)
    REFERENCES str_type(id_type)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE spe_comments (
  id_species INTEGER UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  comments TEXT NOT NULL,
  PRIMARY KEY(id_species, id_lang),
  INDEX FK_species(id_species),
  INDEX FK_lang(id_lang),
  FOREIGN KEY(id_species)
    REFERENCES species(id_species)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE spe_ambient_risk (
  id_species INTEGER UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  ambient_risk TEXT NOT NULL,
  PRIMARY KEY(id_species, id_lang),
  INDEX FK_species(id_species),
  INDEX FK_lang(id_lang),
  FOREIGN KEY(id_species)
    REFERENCES species(id_species)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE spe_name_qualifier_lang (
  id_name_qualifier TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  name_qualifier VARCHAR(50) NOT NULL,
  PRIMARY KEY(id_name_qualifier, id_lang),
  INDEX FK_lang(id_lang),
  INDEX FK_name_qualifier(id_name_qualifier),
  FOREIGN KEY(id_name_qualifier)
    REFERENCES spe_name_qualifier(id_name_qualifier)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE contact_relations (
  id_person INTEGER UNSIGNED NOT NULL,
  id_institution INTEGER UNSIGNED NOT NULL,
  contact ENUM('yes') NULL,
  department VARCHAR(80) NULL,
  email VARCHAR(100) NULL,
  last_update DATETIME NULL,
  PRIMARY KEY(id_person, id_institution),
  INDEX FK_institution(id_institution),
  INDEX FK_person(id_person),
  FOREIGN KEY(id_institution)
    REFERENCES institution(id_institution)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_person)
    REFERENCES person(id_person)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_deposit (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_person INTEGER UNSIGNED NULL,
  id_institution INTEGER UNSIGNED NULL,
  genus VARCHAR(50) NULL,
  species VARCHAR(50) NULL,
  classification VARCHAR(50) NULL,
  infra_name VARCHAR(100) NULL,
  infra_complement VARCHAR(100) NULL,
  date DATE NULL,
  id_dep_reason TINYINT UNSIGNED NULL,
  preserv_method TEXT NULL,
  form VARCHAR(50) NULL,
  comments TEXT NULL,
  aut_date DATETIME NULL,
  aut_person INTEGER(10) UNSIGNED NULL,
  aut_result TEXT NULL,
  PRIMARY KEY(id_strain, id_coll),
  INDEX FK_strain_coll(id_strain, id_coll),
  INDEX FK_person(id_person),
  INDEX FK_institution(id_institution),
  INDEX FK_dep_reason(id_dep_reason),
  INDEX FK_aut_person(aut_person),
  FOREIGN KEY(id_strain, id_coll)
    REFERENCES strain(id_strain, id_coll)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_person)
    REFERENCES person(id_person)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_institution)
    REFERENCES institution(id_institution)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_dep_reason)
    REFERENCES str_dep_reason(id_dep_reason)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(aut_person)
    REFERENCES person(id_person)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_isolation (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_person INTEGER UNSIGNED NULL,
  id_institution INTEGER UNSIGNED NULL,
  date DATE NULL,
  comments TEXT NULL,
  PRIMARY KEY(id_strain, id_coll),
  INDEX FK_strain_coll(id_strain, id_coll),
  INDEX FK_person(id_person),
  INDEX FK_institution(id_institution),
  FOREIGN KEY(id_strain, id_coll)
    REFERENCES strain(id_strain, id_coll)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_person)
    REFERENCES person(id_person)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_institution)
    REFERENCES institution(id_institution)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_identification (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  date DATE NULL,
  id_person INTEGER UNSIGNED NULL,
  id_institution INTEGER UNSIGNED NULL,
  genus VARCHAR(50) NULL,
  species VARCHAR(50) NULL,
  classification VARCHAR(50) NULL,
  infra_name VARCHAR(100) NULL,
  infra_complement VARCHAR(100) NULL,
  comments TEXT NULL,
  PRIMARY KEY(id_strain, id_coll),
  INDEX FK_strain_coll(id_strain, id_coll),
  INDEX FK_person(id_person),
  INDEX FK_institution(id_institution),
  FOREIGN KEY(id_strain, id_coll)
    REFERENCES strain(id_strain, id_coll)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_person)
    REFERENCES person(id_person)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_institution)
    REFERENCES institution(id_institution)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_coll_event (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_person INTEGER UNSIGNED NULL,
  id_institution INTEGER UNSIGNED NULL,
  date DATE NULL,
  id_country INTEGER UNSIGNED NULL,
  id_state INTEGER UNSIGNED NULL,
  id_city INTEGER UNSIGNED NULL,
  place TEXT NULL,
  gps_latitude DECIMAL(11,8) NULL,
  gps_latitude_dms VARCHAR(12) NULL,
  gps_latitude_mode ENUM('decimal','dms') NULL,
  gps_longitude DECIMAL(11,8) NULL,
  gps_longitude_dms VARCHAR(12) NULL,
  gps_longitude_mode ENUM('decimal','dms') NULL,
  gps_precision INTEGER(5) UNSIGNED NULL,
  id_gps_datum SMALLINT UNSIGNED NULL,
  gps_comments TEXT NULL,
  host_genus VARCHAR(50) NULL,
  host_species VARCHAR(50) NULL,
  host_classification VARCHAR(50) NULL,
  host_infra_name VARCHAR(100) NULL,
  host_infra_complement VARCHAR(100) NULL,
  global_code VARCHAR(50) NULL,
  id_clinical_form SMALLINT UNSIGNED NULL,
  hiv ENUM('yes','no') NULL,
  PRIMARY KEY(id_strain, id_coll),
  INDEX FK_strain_coll(id_strain, id_coll),
  INDEX FK_person(id_person),
  INDEX FK_institution(id_institution),
  INDEX FK_country(id_country),
  INDEX FK_state(id_state),
  INDEX FK_city(id_city),
  INDEX FK_gps_datum(id_gps_datum),
  INDEX FK_clinical_form(id_clinical_form),
  FOREIGN KEY(id_strain, id_coll)
    REFERENCES strain(id_strain, id_coll)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_person)
    REFERENCES person(id_person)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_institution)
    REFERENCES institution(id_institution)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_country)
    REFERENCES loc_country(id_country)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_state)
    REFERENCES loc_state(id_state)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_city)
    REFERENCES loc_city(id_city)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_gps_datum)
    REFERENCES str_gps_datum(id_gps_datum)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_clinical_form)
    REFERENCES str_clinical_form(id_clinical_form)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_characs (
  id_coll TINYINT UNSIGNED NOT NULL,
  id_strain INTEGER UNSIGNED NOT NULL,
  biochemical TEXT NULL,
  molecular TEXT NULL,
  immunologic TEXT NULL,
  morphologic TEXT NULL,
  pathogenic TEXT NULL,
  genotypic TEXT NULL,
  ogm ENUM('0','1','2') NULL,
  PRIMARY KEY(id_coll, id_strain),
  INDEX FK_strain_coll(id_strain, id_coll),
  FOREIGN KEY(id_strain, id_coll)
    REFERENCES strain(id_strain, id_coll)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_culture (
  id_coll TINYINT UNSIGNED NOT NULL,
  id_strain INTEGER UNSIGNED NOT NULL,
  temp VARCHAR(50) NULL,
  ph VARCHAR(50) NULL,
  PRIMARY KEY(id_coll, id_strain),
  INDEX FK_strain_coll(id_strain, id_coll),
  FOREIGN KEY(id_strain, id_coll)
    REFERENCES strain(id_strain, id_coll)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_properties (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY(id_coll, id_strain),
  INDEX FK_strain_coll(id_strain, id_coll),
  FOREIGN KEY(id_strain, id_coll)
    REFERENCES strain(id_strain, id_coll)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_incub_time (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  incub_time VARCHAR(50) NOT NULL,
  PRIMARY KEY(id_strain, id_coll, id_lang),
  INDEX FK_lang(id_lang),
  INDEX FK_strain_coll(id_coll, id_strain),
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_coll, id_strain)
    REFERENCES str_culture(id_coll, id_strain)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_oxy_req (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  oxy_req VARCHAR(50) NOT NULL,
  PRIMARY KEY(id_strain, id_coll, id_lang),
  INDEX FK_lang(id_lang),
  INDEX FK_strain_coll(id_coll, id_strain),
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_coll, id_strain)
    REFERENCES str_culture(id_coll, id_strain)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_pro_applications (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  applications TEXT NOT NULL,
  PRIMARY KEY(id_strain, id_coll, id_lang),
  INDEX FK_strain_coll(id_coll, id_strain),
  INDEX FK_lang(id_lang),
  FOREIGN KEY(id_coll, id_strain)
    REFERENCES str_properties(id_coll, id_strain)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_pro_urls (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  urls TEXT NOT NULL,
  PRIMARY KEY(id_strain, id_coll, id_lang),
  INDEX FK_strain_coll(id_coll, id_strain),
  INDEX FK_lang(id_lang),
  FOREIGN KEY(id_coll, id_strain)
    REFERENCES str_properties(id_coll, id_strain)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_pro_properties (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  properties TEXT NOT NULL,
  PRIMARY KEY(id_strain, id_coll, id_lang),
  INDEX FK_strain_coll(id_coll, id_strain),
  INDEX FK_lang(id_lang),
  FOREIGN KEY(id_coll, id_strain)
    REFERENCES str_properties(id_coll, id_strain)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_cha_urls (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  urls TEXT NOT NULL,
  PRIMARY KEY(id_strain, id_coll, id_lang),
  INDEX FK_lang(id_lang),
  INDEX FK_strain_coll(id_coll, id_strain),
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_coll, id_strain)
    REFERENCES str_characs(id_coll, id_strain)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_cha_restrictions (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  restrictions TEXT NOT NULL,
  PRIMARY KEY(id_strain, id_coll, id_lang),
  INDEX FK_strin_coll(id_coll, id_strain),
  INDEX FK_lang(id_lang),
  FOREIGN KEY(id_coll, id_strain)
    REFERENCES str_characs(id_coll, id_strain)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_iso_method (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  iso_method TEXT NOT NULL,
  PRIMARY KEY(id_strain, id_coll, id_lang),
  INDEX FK_lang(id_lang),
  INDEX FK_strain_coll(id_coll, id_strain),
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_strain, id_coll)
    REFERENCES str_isolation(id_strain, id_coll)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_isolation_from (
  id_strain INTEGER(10) UNSIGNED NOT NULL,
  id_coll TINYINT(3) UNSIGNED NOT NULL,
  id_lang TINYINT(3) UNSIGNED NOT NULL,
  isolation_from TEXT NOT NULL,
  PRIMARY KEY  (id_strain,id_coll,id_lang),
  INDEX FK_lang (id_lang),
  INDEX FK_strain_coll(id_coll, id_strain),
  FOREIGN KEY (id_lang) 
	REFERENCES lang (id_lang) 
		ON DELETE CASCADE 
		ON UPDATE CASCADE,
  FOREIGN KEY(id_strain, id_coll)
    REFERENCES str_isolation(id_strain, id_coll)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_ident_method (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  ident_method TEXT NOT NULL,
  PRIMARY KEY(id_strain, id_coll, id_lang),
  INDEX FK_lang(id_lang),
  INDEX FK_strain_coll(id_coll, id_strain),
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_strain, id_coll)
    REFERENCES str_identification(id_strain, id_coll)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_coll_comments (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  comments TEXT NOT NULL,
  PRIMARY KEY(id_strain, id_coll, id_lang),
  INDEX FK_lang(id_lang),
  INDEX FK_strain_coll(id_coll, id_strain),
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_strain, id_coll)
    REFERENCES str_coll_event(id_strain, id_coll)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_substratum (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  substratum TEXT NOT NULL,
  PRIMARY KEY(id_strain, id_coll, id_lang),
  INDEX FK_lang(id_lang),
  INDEX FK_strain_coll(id_coll, id_strain),
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_strain, id_coll)
    REFERENCES str_coll_event(id_strain, id_coll)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_host_name (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  host_name TEXT NOT NULL,
  PRIMARY KEY(id_strain, id_coll, id_lang),
  INDEX FK_lang(id_lang),
  INDEX FK_strain_coll(id_strain, id_coll),
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_strain, id_coll)
    REFERENCES str_coll_event(id_strain, id_coll)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_cult_comments (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  comments TEXT NOT NULL,
  PRIMARY KEY(id_strain, id_coll, id_lang),
  INDEX FK_lang(id_lang),
  INDEX FK_strain_coll(id_coll, id_strain),
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_coll, id_strain)
    REFERENCES str_culture(id_coll, id_strain)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_cult_medium (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  medium TEXT NOT NULL,
  PRIMARY KEY(id_strain, id_coll, id_lang),
  INDEX FK_lang(id_lang),
  INDEX FK_strain_coll(id_coll, id_strain),
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_coll, id_strain)
    REFERENCES str_culture(id_coll, id_strain)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_cha_pictures (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  pictures TEXT NOT NULL,
  PRIMARY KEY(id_strain, id_coll, id_lang),
  INDEX FK_lang(id_lang),
  INDEX FK_strain_coll(id_coll, id_strain),
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_coll, id_strain)
    REFERENCES str_characs(id_coll, id_strain)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_cha_biorisk_comments (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  biorisk_comments TEXT NOT NULL,
  PRIMARY KEY(id_strain, id_coll, id_lang),
  INDEX FK_strain_coll(id_coll, id_strain),
  INDEX FK_lang(id_lang),
  FOREIGN KEY(id_coll, id_strain)
    REFERENCES str_characs(id_coll, id_strain)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_cha_ogm_comments (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  ogm_comments TEXT NOT NULL,
  PRIMARY KEY(id_strain, id_coll, id_lang),
  INDEX FK_strain_coll(id_coll, id_strain),
  INDEX FK_lang(id_lang),
  FOREIGN KEY(id_coll, id_strain)
    REFERENCES str_characs(id_coll, id_strain)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_cha_catalogue (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  catalogue_notes TEXT NOT NULL,
  PRIMARY KEY(id_strain, id_coll, id_lang),
  INDEX FK_lang(id_lang),
  INDEX FK_strain_coll(id_coll, id_strain),
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_coll, id_strain)
    REFERENCES str_characs(id_coll, id_strain)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE roles (
  id_role INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  description TEXT NULL,
  type ENUM('user','group','level','all') NOT NULL DEFAULT 'user',
  PRIMARY KEY(id_role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE system_areas (
  id_area SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  description TEXT NULL,
  PRIMARY KEY(id_area)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE roles_users (
  id_user INTEGER UNSIGNED NOT NULL,
  id_role INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(id_user, id_role),
  INDEX FK_role(id_role),
  FOREIGN KEY(id_role)
    REFERENCES roles(id_role)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE areas_permissions (
  id_role INTEGER UNSIGNED NOT NULL,
  id_area SMALLINT UNSIGNED NOT NULL,
  allow_delete ENUM('y','n') NOT NULL DEFAULT "n",
  allow_create ENUM('y','n') NOT NULL DEFAULT "y",
  PRIMARY KEY(id_role, id_area),
  INDEX FK_role(id_role),
  FOREIGN KEY(id_area)
    REFERENCES system_areas(id_area)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_role)
    REFERENCES roles(id_role)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE roles_permissions (
  id_item INTEGER UNSIGNED NOT NULL,
  id_role INTEGER UNSIGNED NOT NULL,
  id_area SMALLINT UNSIGNED NOT NULL,
  permission ENUM('r','w') NOT NULL DEFAULT 'w',
  PRIMARY KEY(id_item, id_role, id_area),
  INDEX FK_role(id_role),
  FOREIGN KEY(id_role)
    REFERENCES roles(id_role)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_area)
    REFERENCES system_areas(id_area)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE preservation_method (
  id_preservation_method TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  PRIMARY KEY(id_preservation_method)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE preservation_method_subcoll (
  id_preservation_method TINYINT UNSIGNED NOT NULL,
  id_subcoll TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY(id_preservation_method, id_subcoll),
  FOREIGN KEY(id_preservation_method)
    REFERENCES preservation_method(id_preservation_method)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE preservation_method_lang (
  id_preservation_method TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  method VARCHAR(100) NOT NULL,
  unit_measure VARCHAR(100) NOT NULL,
  PRIMARY KEY(id_preservation_method, id_lang),
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_preservation_method)
    REFERENCES preservation_method(id_preservation_method)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE lot (
  id_lot INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  id_subcoll TINYINT UNSIGNED NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id_lot)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE lot_strain (
  id_lot INTEGER UNSIGNED NOT NULL,
  id_strain INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY  (id_lot,id_strain),
  KEY id_strain (id_strain),
  FOREIGN KEY (id_lot)
	REFERENCES lot (id_lot)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
  FOREIGN KEY (id_strain)
	REFERENCES strain (id_strain)
	ON DELETE RESTRICT
	ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE preservation (
  id_preservation INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  id_user INTEGER UNSIGNED NOT NULL,
  id_lot INTEGER UNSIGNED NOT NULL,
  id_preservation_method TINYINT UNSIGNED NOT NULL,
  date DATE NOT NULL,
  info TEXT NULL,
  last_update DATETIME NULL,
  PRIMARY KEY(id_preservation),
  INDEX FK_user(id_user),
  INDEX FK_id_lot(id_lot),
  FOREIGN KEY(id_user)
    REFERENCES person(id_person)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_lot)
    REFERENCES lot(id_lot)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_preservation_method)
    REFERENCES preservation_method(id_preservation_method)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE container (
  id_container INTEGER UNSIGNED NOT NULL auto_increment,
  abbreviation varchar(40) NOT NULL,
  description varchar(255) default NULL,
  PRIMARY KEY  (id_container)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE container_hierarchy (
  id_container_hierarchy INTEGER UNSIGNED NOT NULL auto_increment,
  id_container INTEGER UNSIGNED NOT NULL,
  id_parent INTEGER UNSIGNED default NULL,
  abbreviation varchar(40) NOT NULL,
  description varchar(255) default NULL,
  PRIMARY KEY  (id_container_hierarchy),
  INDEX FK_container (id_container),
  INDEX FK_parent (id_parent),
  FOREIGN KEY (id_container)
	REFERENCES container (id_container)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
  FOREIGN KEY (id_parent)
	REFERENCES container_hierarchy (id_container_hierarchy)
		ON DELETE CASCADE
		ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE container_preservation_method (
  id_container INTEGER UNSIGNED NOT NULL,
  id_preservation_method tinyint(3) unsigned NOT NULL,
  PRIMARY KEY  (id_container,id_preservation_method),
  INDEX FK_container (id_container),
  INDEX FK_preservation_method (id_preservation_method),
  FOREIGN KEY (id_container)
	REFERENCES container (id_container)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
  FOREIGN KEY (id_preservation_method)
	  REFERENCES preservation_method (id_preservation_method)
		ON DELETE RESTRICT
		ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE container_subcoll (
  id_container INTEGER UNSIGNED NOT NULL,
  id_subcoll tinyint(3) unsigned NOT NULL,
  PRIMARY KEY  (id_container,id_subcoll),
  INDEX FK_container (id_container),
  FOREIGN KEY (id_container)
	REFERENCES container (id_container)
		ON DELETE CASCADE
		ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE location (
  id_location INTEGER UNSIGNED NOT NULL auto_increment,
  id_container_hierarchy INTEGER UNSIGNED NOT NULL,
  rows INTEGER UNSIGNED NOT NULL,
  cols INTEGER UNSIGNED NOT NULL,
  ini_row char(1) NOT NULL,
  ini_col char(1) NOT NULL,
  pattern varchar(40) NOT NULL,
  PRIMARY KEY  (id_location),
  INDEX FK_container_hierarchy (id_container_hierarchy),
  FOREIGN KEY (id_container_hierarchy)
	REFERENCES container_hierarchy (id_container_hierarchy)
		ON DELETE RESTRICT
		ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE lot_strain_location (
  id_lot_strain_location INTEGER UNSIGNED NOT NULL auto_increment,
  id_lot INTEGER UNSIGNED NOT NULL,
  id_strain INTEGER UNSIGNED NOT NULL,
  id_container_hierarchy INTEGER UNSIGNED NOT NULL,
  row INTEGER UNSIGNED NOT NULL,
  col INTEGER UNSIGNED NOT NULL,
  quantity INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY  (id_lot_strain_location),
  UNIQUE KEY lot_strain_location_key (id_lot,id_container_hierarchy,row,col),
  INDEX FK_lot_strain (id_lot,id_strain),
  INDEX FK_container_hierarchy (id_container_hierarchy),
  FOREIGN KEY (id_lot, id_strain)
	REFERENCES lot_strain (id_lot, id_strain)
		ON DELETE RESTRICT
		ON UPDATE RESTRICT,
  FOREIGN KEY (id_container_hierarchy)
	REFERENCES container_hierarchy (id_container_hierarchy)
		ON DELETE RESTRICT
		ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE preservation_strain (
  id_preserv_str INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  id_preservation INTEGER UNSIGNED NOT NULL,
  id_strain INTEGER UNSIGNED NOT NULL,
  origin_type ENUM('original','lot') NOT NULL,
  origin VARCHAR(100) NULL COMMENT 'used if origin_type = original',
  id_lot INTEGER UNSIGNED NULL COMMENT 'used if origin_type = lot',
  id_origin_container_hierarchy INTEGER UNSIGNED default NULL COMMENT 'used if origin_type = lot',
  origin_row INTEGER UNSIGNED default NULL COMMENT 'used if origin_type = lot',
  origin_col INTEGER UNSIGNED default NULL COMMENT 'used if origin_type = lot',
  quantity INTEGER UNSIGNED default NULL COMMENT 'used if origin_type = lot',
  stock_position text NOT NULL,
  stock_minimum INTEGER UNSIGNED NOT NULL,
  id_doc INTEGER UNSIGNED NULL COMMENT 'culture medium is a document qualifier',
  temperature VARCHAR(100) NULL,
  incub_time VARCHAR(100) NULL,
  cryoprotector VARCHAR(100) NULL,
  preservation_type ENUM('block','spore','none') NULL,
  purity ENUM('y','n') NULL,
  counting VARCHAR(100) NULL,
  counting_not_apply ENUM('y','n') NOT NULL,
  macro_charac TEXT NULL,
  micro_charac TEXT NULL,
  result TEXT NULL,
  obs TEXT NULL,
  not_identified tinyint(1) unsigned NOT NULL default '0',
  PRIMARY KEY(id_preserv_str),
  INDEX IX_id_lot(id_lot),
  INDEX FK_id_strain(id_strain),
  INDEX FK_id_preservation(id_preservation),
  INDEX FK_id_origin_container_hierarchy(id_origin_container_hierarchy),
  INDEX FK_id_doc(id_doc),
  FOREIGN KEY(id_strain)
    REFERENCES strain(id_strain)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_preservation)
    REFERENCES preservation(id_preservation)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_origin_container_hierarchy)
    REFERENCES container_hierarchy(id_container_hierarchy)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_doc)
    REFERENCES doc(id_doc)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_quality (
  id_quality INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  id_user INTEGER UNSIGNED NOT NULL,
  id_lot INTEGER UNSIGNED NOT NULL,
  id_strain INTEGER UNSIGNED NOT NULL,
  date DATE NOT NULL,
  last_update DATETIME NULL,
  not_identified tinyint(1) unsigned NOT NULL default '0',
  PRIMARY KEY(id_quality),
  INDEX str_quality_FKIndex2(id_lot),
  FOREIGN KEY(id_lot)
    REFERENCES lot(id_lot)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_strain,id_lot)
    REFERENCES lot_strain(id_strain,id_lot)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_strain)
    REFERENCES strain(id_strain)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_quality_test (
  id_test INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  id_quality INTEGER UNSIGNED NOT NULL,
  id_doc INTEGER UNSIGNED NOT NULL COMMENT 'test is a document qualifier',
  result TEXT NULL,
  comments TEXT NULL,
  purity ENUM('y','n') NOT NULL,
  counting VARCHAR(100),
  counting_not_apply ENUM('y','n') NOT NULL,
  PRIMARY KEY(id_test),
  FOREIGN KEY(id_doc)
    REFERENCES doc(id_doc)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_quality)
    REFERENCES str_quality(id_quality)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE distribution (
  id_distribution INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  id_user INTEGER UNSIGNED NOT NULL,
  id_lot INTEGER UNSIGNED NOT NULL,
  id_strain INTEGER UNSIGNED NOT NULL,
  id_institution INTEGER UNSIGNED NOT NULL,
  date DATE NOT NULL,
  id_person INTEGER UNSIGNED NULL,
  reason TEXT NULL,
  last_update DATETIME NULL,
  not_identified tinyint(1) unsigned NOT NULL default '0',
  PRIMARY KEY(id_distribution),
  INDEX supply_FKIndex1(id_lot),
  FOREIGN KEY(id_lot)
    REFERENCES lot(id_lot)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_strain)
    REFERENCES strain(id_strain)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_strain,id_lot)
    REFERENCES lot_strain(id_strain,id_lot)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_institution)
    REFERENCES institution(id_institution)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_user)
    REFERENCES person(id_person)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_person)
    REFERENCES person(id_person)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE distribution_origin_location (
  id_distribution_location INTEGER UNSIGNED NOT NULL auto_increment,
  id_distribution INTEGER UNSIGNED NOT NULL,
  id_origin_lot INTEGER UNSIGNED NOT NULL,
  id_origin_container_hierarchy INTEGER UNSIGNED NOT NULL,
  origin_row INTEGER UNSIGNED NOT NULL,
  origin_col INTEGER UNSIGNED NOT NULL,
  quantity INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY  (id_distribution_location),
  INDEX FK_id_distribution (id_distribution),
  INDEX FK_id_origin_lot (id_origin_lot),
  INDEX FK_id_origin_container_hierarchy (id_origin_container_hierarchy),
  FOREIGN KEY (id_distribution)
	REFERENCES distribution (id_distribution)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
  FOREIGN KEY (id_origin_lot)
	REFERENCES lot (id_lot)
		ON DELETE RESTRICT
		ON UPDATE RESTRICT,
  FOREIGN KEY (id_origin_container_hierarchy)
	REFERENCES container_hierarchy (id_container_hierarchy)
		ON DELETE RESTRICT
		ON UPDATE RESTRICT  
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_quality_origin_location (
  id_quality_origin_location INTEGER UNSIGNED NOT NULL auto_increment,
  id_quality INTEGER UNSIGNED NOT NULL,
  id_origin_lot INTEGER UNSIGNED NOT NULL,
  id_origin_container_hierarchy INTEGER UNSIGNED NOT NULL,
  origin_row INTEGER UNSIGNED NOT NULL,
  origin_col INTEGER UNSIGNED NOT NULL,
  quantity INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY  (id_quality_origin_location),
  INDEX FK_id_quality (id_quality),
  INDEX FK_id_origin_lot (id_origin_lot),
  INDEX FK_id_origin_container_hierarchy (id_origin_container_hierarchy),
  FOREIGN KEY (id_quality)
	REFERENCES str_quality (id_quality)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
  FOREIGN KEY (id_origin_lot)
	REFERENCES lot (id_lot)
		ON DELETE RESTRICT
		ON UPDATE RESTRICT,
  FOREIGN KEY (id_origin_container_hierarchy)
	REFERENCES container_hierarchy (id_container_hierarchy)
		ON DELETE RESTRICT
		ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_stock_minimum (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_preservation_method TINYINT UNSIGNED NOT NULL,
  quantity INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY  (id_strain, id_preservation_method),
  INDEX FK_id_strain (id_strain),
  INDEX FK_id_preservation_method (id_preservation_method),
  FOREIGN KEY (id_strain)
	REFERENCES strain (id_strain)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
  FOREIGN KEY (id_preservation_method)
	REFERENCES preservation_method (id_preservation_method)
		ON DELETE CASCADE
		ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE stock_movement (
  id_stock_movement INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  id_subcoll TINYINT(3) unsigned NOT NULL,
  description VARCHAR(256) NOT NULL,
  date DATETIME NOT NULL,
  PRIMARY KEY(id_stock_movement)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE stock_movement_location (
  id_stock_movement_location INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  id_stock_movement INTEGER UNSIGNED NOT NULL,
  id_lot_strain_location_from INTEGER UNSIGNED NOT NULL,
  id_lot_strain_location_to INTEGER UNSIGNED NULL,
  PRIMARY KEY(id_stock_movement_location),
  UNIQUE KEY id_lot_strain_location_from_key (id_lot_strain_location_from),
  UNIQUE KEY id_lot_strain_location_to_key (id_lot_strain_location_to),
  INDEX FK_stock_movement(id_stock_movement),
  INDEX FK_lot_strain_location_from(id_lot_strain_location_from),
  INDEX FK_lot_strain_location_to(id_lot_strain_location_to),
  FOREIGN KEY(id_stock_movement)
    REFERENCES stock_movement(id_stock_movement)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_lot_strain_location_from)
    REFERENCES lot_strain_location(id_lot_strain_location)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT,
  FOREIGN KEY(id_lot_strain_location_to)
    REFERENCES lot_strain_location(id_lot_strain_location)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE report_types (
  id_report_type TINYINT UNSIGNED NOT NULL,
  code VARCHAR(100) NOT NULL,
  fields_definition TEXT NOT NULL,
  PRIMARY KEY(id_report_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE report_types_lang (
  id_report_type TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  type VARCHAR(200) NOT NULL,
  PRIMARY KEY(id_report_type, id_lang),
  INDEX FK_report_type(id_report_type),
  INDEX FK_id_lang(id_lang),
  FOREIGN KEY(id_report_type)
    REFERENCES report_types(id_report_type)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_lang)
    REFERENCES lang(id_lang)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE reports (
  id_report INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  id_subcoll TINYINT UNSIGNED NOT NULL,
  id_report_type TINYINT UNSIGNED NOT NULL,
  description VARCHAR(255) NOT NULL,
  definition TEXT NOT NULL,
  PRIMARY KEY(id_report),
  INDEX FK_report_type(id_report_type),
  FOREIGN KEY(id_report_type)
    REFERENCES report_types(id_report_type)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE VIEW view_hierarchy AS
	SELECT hd.id_hierarchy,
           hg.id_taxon_group,
           hg.id_subcoll,
           hd.seq,
           hl.id_lang,
           hl.rank,
           (CASE WHEN (hg.hi_tax IS NULL) THEN hd.hi_tax ELSE hg.hi_tax END) AS hi_tax,
           (CASE WHEN (hg.has_author IS NULL) THEN hd.has_author ELSE hg.has_author	END) AS has_author,
           (CASE WHEN (hg.use_author IS NULL) THEN hd.use_author ELSE hg.use_author	END) AS use_author,
           (CASE WHEN (hg.in_sciname IS NULL) THEN hd.in_sciname ELSE hg.in_sciname	END) AS in_sciname,
           (CASE WHEN (hg.required IS NULL) THEN hd.required ELSE hg.required END) AS required,
           (CASE WHEN (hg.important	IS NULL) THEN hd.important ELSE hg.important END) AS important,
           (CASE WHEN (hg.string_format IS NULL) THEN hd.string_format ELSE hg.string_format END) AS string_format,
           (CASE WHEN (hg.string_case IS NULL) THEN hd.string_case ELSE hg.string_case END) AS string_case,
           (CASE WHEN (hg.prefix IS NULL) THEN hd.prefix ELSE hg.prefix END) AS prefix,
           (CASE WHEN (hg.suffix IS NULL) THEN hd.suffix ELSE hg.suffix END) AS suffix,
           hg.default_value
FROM hierarchy_group hg
     INNER JOIN hierarchy_def hd ON (hg.id_hierarchy = hd.id_hierarchy)
     INNER JOIN hierarchy_lang hl ON (hd.id_hierarchy = hl.id_hierarchy);
	 
CREATE VIEW lot_strain_stock_data AS 
  select 
    `lsl`.`id_lot` AS `id_lot`,
    `lsl`.`id_strain` AS `id_strain`,
    `lsl`.`id_container_hierarchy` AS `id_container_hierarchy`,
    `lsl`.`row` AS `row`,
    `lsl`.`col` AS `col`,
    `lsl`.`quantity` AS `quantity`,
    cast((
  select 
    sum(`ps`.`quantity`) AS `sum(quantity)` 
  from 
    `preservation_strain` `ps` 
  where 
    ((`ps`.`id_lot` = `lsl`.`id_lot`) and (`ps`.`id_origin_container_hierarchy` = `lsl`.`id_container_hierarchy`) and (`ps`.`origin_row` = `lsl`.`row`) and (`ps`.`origin_col` = `lsl`.`col`))) as unsigned) AS `used_qt_pres`,cast((
  select 
    sum(`dol`.`quantity`) AS `sum(quantity)` 
  from 
    `distribution_origin_location` `dol` 
  where 
    ((`dol`.`id_origin_lot` = `lsl`.`id_lot`) and (`dol`.`id_origin_container_hierarchy` = `lsl`.`id_container_hierarchy`) and (`dol`.`origin_row` = `lsl`.`row`) and (`dol`.`origin_col` = `lsl`.`col`))) as unsigned) AS `used_qt_dist`,cast((
  select 
    sum(`qol`.`quantity`) AS `sum(quantity)` 
  from 
    `str_quality_origin_location` `qol` 
  where 
    ((`qol`.`id_origin_lot` = `lsl`.`id_lot`) and (`qol`.`id_origin_container_hierarchy` = `lsl`.`id_container_hierarchy`) and (`qol`.`origin_row` = `lsl`.`row`) and (`qol`.`origin_col` = `lsl`.`col`))) as unsigned) AS `used_qt_qual` 
  from 
    `lot_strain_location` `lsl` 
  where 
    (not(`lsl`.`id_lot_strain_location` in (
  select 
    `stock_movement_location`.`id_lot_strain_location_from` AS `id_lot_strain_location_from` 
  from 
    `stock_movement_location`)));
	
CREATE VIEW lot_strain_stock AS
  select
    `lslm`.`id_lot` AS `id_lot`,
    `lslm`.`id_strain` AS `id_strain`,
    cast(sum(`lslm`.`quantity`) - sum(ifnull(`lslm`.`used_qt_pres`, 0)) - sum(ifnull(`lslm`.`used_qt_dist`, 0)) - sum(ifnull(`lslm`.`used_qt_qual`, 0)) as unsigned integer) AS `stock`
  from `lot_strain_stock_data` `lslm`
  group by `lslm`.`id_lot`,`lslm`.`id_strain`;
	
CREATE VIEW preservation_strain_locations AS 
  select
    `p`.`id_preservation` AS `id_preservation`,
    `p`.`id_lot` AS `id_lot`,
    `ps`.`id_strain` AS `id_strain`,
    `ps`.`origin_type` AS `origin_type`,
    `lsl`.`id_container_hierarchy` AS `id_container_hierarchy`,
    `lsl`.`row` AS `row`,
    `lsl`.`col` AS `col`,
    `ps`.`id_lot` AS `id_origin_lot`,
    `ps`.`id_origin_container_hierarchy` AS `id_origin_container_hierarchy`,
    `ps`.`origin_row` AS `origin_row`,
    `ps`.`origin_col` AS `origin_col`,
    `ps`.`quantity` AS `quantity`
  from
    ((`preservation` `p` join `preservation_strain` `ps` on((`p`.`id_preservation` = `ps`.`id_preservation`))) join `lot_strain_location` `lsl` on(((`lsl`.`id_lot` = `p`.`id_lot`) and (`lsl`.`id_strain` = `ps`.`id_strain`))))
  order by
    `p`.`id_preservation`,`ps`.`id_lot`,`ps`.`id_strain`,`lsl`.`id_container_hierarchy`,`lsl`.`row`,`lsl`.`col`;

CREATE VIEW used_origin_all AS 
    select
      'distribution' as origin,
      distribution_origin_location.id_origin_lot AS id_origin_lot,
      distribution_origin_location.id_origin_container_hierarchy AS id_origin_container_hierarchy,
      distribution_origin_location.origin_row AS origin_row,
      distribution_origin_location.origin_col AS origin_col,
      distribution_origin_location.quantity AS used_qt
    from
      distribution_origin_location
    union
    select
      'quality' as origin,
      str_quality_origin_location.id_origin_lot AS id_origin_lot,
      str_quality_origin_location.id_origin_container_hierarchy AS id_origin_container_hierarchy,
      str_quality_origin_location.origin_row AS origin_row,
      str_quality_origin_location.origin_col AS origin_col,
      str_quality_origin_location.quantity AS used_qt
    from
      str_quality_origin_location
    union
    select
      'preservation' as origin,
      preservation_strain_locations.id_lot AS id_origin_lot,
      preservation_strain_locations.id_origin_container_hierarchy AS id_origin_container_hierarchy,
      preservation_strain_locations.origin_row AS origin_row,
      preservation_strain_locations.origin_col AS origin_col,
      preservation_strain_locations.quantity AS used_qt
    from
      preservation_strain_locations
      INNER JOIN preservation_strain ps ON (
        ps.id_preservation = preservation_strain_locations.id_preservation
        AND ps.id_strain = preservation_strain_locations.id_strain)
    where
      ps.origin_type = 'lot';
  
CREATE VIEW used_origin AS 
  select
    distribution_origin_location.id_origin_lot AS id_origin_lot,
    distribution_origin_location.id_origin_container_hierarchy AS id_origin_container_hierarchy,
    distribution_origin_location.origin_row AS origin_row,
    distribution_origin_location.origin_col AS origin_col,
    distribution_origin_location.quantity AS used_qt
  from
    distribution_origin_location
 union
  select
    str_quality_origin_location.id_origin_lot AS id_origin_lot,
    str_quality_origin_location.id_origin_container_hierarchy AS id_origin_container_hierarchy,
    str_quality_origin_location.origin_row AS origin_row,
    str_quality_origin_location.origin_col AS origin_col,
    str_quality_origin_location.quantity AS used_qt
  from
    str_quality_origin_location
 union
  select
    preservation_strain_locations.id_lot AS id_origin_lot,
    preservation_strain_locations.id_origin_container_hierarchy AS id_origin_container_hierarchy,
    preservation_strain_locations.origin_row AS origin_row,
    preservation_strain_locations.origin_col AS origin_col,
    preservation_strain_locations.quantity AS used_qt
  from
    preservation_strain_locations
  where
    (preservation_strain_locations.`origin_type` = 'lot');

CREATE VIEW lot_strain_available_locations AS 
  select
    `lslm`.`id_lot` AS `id_lot`,
    `lslm`.`id_strain` AS `id_strain`,
    `lslm`.`id_container_hierarchy`,
    `lslm`.`row`,
    `lslm`.`col`,
    cast((`lslm`.`quantity` - ifnull(`lslm`.`used_qt_pres`,0) - ifnull(`lslm`.`used_qt_dist`,0) - ifnull(`lslm`.`used_qt_qual`,0)) as unsigned integer) AS `available_qt`
  from `lot_strain_stock_data` `lslm`
  where (`lslm`.`quantity` - ifnull(`lslm`.`used_qt_pres`,0) - ifnull(`lslm`.`used_qt_dist`,0) - ifnull(`lslm`.`used_qt_qual`,0)) > 0
  order by
    `lslm`.`id_strain`,`lslm`.id_lot,`lslm`.id_container_hierarchy,`lslm`.row,`lslm`.col;

CREATE FUNCTION get_report_lang() returns INTEGER DETERMINISTIC NO SQL return @report_lang;

CREATE OR REPLACE VIEW strain_report AS
SELECT
	st.id_strain AS id_strain,
	st.id_subcoll AS id_subcoll,
	dv.division AS division,
    st.code AS code,
    st.numeric_code AS numeric_code,
    st.internal_code AS origin_code,
    st.status AS status,
    tgl.taxon_group,
    sn.sciname AS taxon,
    stl.type AS type,
    st.is_ogm AS is_ogm,
    st.infra_complement AS taxonomic_complement,
    st.history AS history,
    st.extra_codes AS other_codes,
    st.comments AS general_comments,
    sce.date AS coll_date,
    YEAR(sce.date) AS coll_year,
    MONTH(sce.date) AS coll_month,
    p1.name AS coll_person,
    i1.name AS coll_institution,
    lcl.country AS country,
    ls.code AS state_code,
    ls.state AS state_name,
    lc.city AS city,
    sce.place AS place,
    sce.gps_latitude AS gps_latitude,
    sce.gps_latitude_dms AS gps_latitude_dms,
    sce.gps_latitude_mode AS gps_latitude_mode,
    sce.gps_longitude AS gps_longitude,
    sce.gps_longitude_dms AS gps_longitude_dms,
    sce.gps_longitude_mode AS gps_longitude_mode,
    sgd.gps_datum AS gps_datum,
    sce.gps_precision AS gps_precision,
    sce.gps_comments AS gps_comments,
    ss.substratum AS substratum,
    shn.host_name AS host_name,
    sce.host_genus AS host_genus,
    sce.host_species AS host_species,
    sce.host_classification AS host_level,
    sce.host_infra_name AS host_subspecies,
    sce.host_infra_complement AS host_taxonomic_complement,
    sce.global_code AS international_code,
    scfl.code AS clinical_form_code,
    scfl.clinical_form AS clinical_form_name,
    sce.hiv AS hiv,
    scc.comments AS coll_comments,
    si.date AS iso_date,
    YEAR(si.date) AS iso_year,
    MONTH(si.date) AS iso_month,
    p2.name AS iso_person,
    i2.name AS iso_institution,
    sif.isolation_from AS isolation_from,
    sim.iso_method AS iso_method,
    si.comments AS iso_comments,
    sid.date AS ident_date,
    YEAR(sid.date) AS ident_year,
    MONTH(sid.date) AS ident_month,
    p3.name AS ident_person,
    i3.name AS ident_institution,
    sid.genus AS ident_genus,
    sid.species AS ident_species,
    sid.classification AS ident_level,
    sid.infra_name AS ident_subspecies,
    sid.infra_complement AS ident_taxonomic_complement,
    sidm.ident_method AS ident_method,
    sid.comments AS ident_comments,
    sd.date AS dep_date,
    YEAR(sd.date) AS dep_year,
    MONTH(sd.date) AS dep_month,
    p4.name AS dep_person,
    i4.name AS dep_institution,
    sd.genus AS dep_genus,
    sd.species AS dep_species,
    sd.classification AS dep_level,
    sd.infra_name AS dep_subspecies,
    sd.infra_complement AS dep_taxonomic_complement,
    sdrl.dep_reason AS dep_reason,
    sd.form AS dep_form,
    sd.preserv_method AS recom_preserv_method,
    sd.aut_date AS aut_date,
    YEAR(sd.aut_date) AS aut_year,
    MONTH(sd.aut_date) AS aut_month,
    p5.name AS aut_person,
    sd.aut_result AS aut_result,
    sd.comments AS dep_comments,
    scm.medium AS recom_growth_medium,
    sc.temp AS recom_temp,
    sit.incub_time AS incubation_time,
    sc.ph AS ph,
    sor.oxy_req AS oxygen_requirements,
    scuc.comments AS grow_comments,
    sch.morphologic AS morphological_characteristics,
    sch.molecular AS molecular_characteristics,
    sch.biochemical AS biochemical_characteristics,
    sch.immunologic AS immunologic_characteristics,
    sch.pathogenic AS pathogenic_characteristics,
    sch.genotypic AS genotypic_characteristics,
    sch.ogm AS ogm,
    scoc.ogm_comments AS ogm_comments,
    scbc.biorisk_comments AS biorisk_comments,
    scr.restrictions AS restrictions,
    scp.pictures AS pictures,
    scu.urls AS charac_references,
    scca.catalogue_notes AS catalogue_notes,
    spp.properties AS properties,
    spa.applications AS applications,
    spu.urls AS prop_references,
    st.go_catalog AS go_catalog
    /*(SELECT SUM(stock) FROM lot_strain_stock lss WHERE lss.id_strain = st.id_strain GROUP BY lss.id_strain) AS stock_quantity,*/
FROM strain st
INNER JOIN division dv ON (st.id_division = dv.id_division)
INNER JOIN species sp ON (st.id_species = sp.id_species)
INNER JOIN taxon_group_lang tgl ON (sp.id_taxon_group = tgl.id_taxon_group AND tgl.id_lang = get_report_lang())
INNER JOIN scientific_names sn ON (sp.id_sciname = sn.id_sciname)
LEFT JOIN str_type_lang stl ON (st.id_type = stl.id_type AND stl.id_lang = get_report_lang())
LEFT JOIN str_coll_event sce ON (st.id_strain = sce.id_strain)
LEFT JOIN person p1 ON (sce.id_person = p1.id_person)
LEFT JOIN institution i1 ON (sce.id_institution = i1.id_institution)
LEFT JOIN loc_country_lang lcl ON (sce.id_country = lcl.id_country AND lcl.id_lang = get_report_lang())
LEFT JOIN loc_state ls ON (sce.id_state = ls.id_state)
LEFT JOIN loc_city lc ON (sce.id_city = lc.id_city)
LEFT JOIN str_gps_datum sgd ON (sce.id_gps_datum = sgd.id_gps_datum)
LEFT JOIN str_substratum ss ON (st.id_strain = ss.id_strain AND ss.id_lang = get_report_lang())
LEFT JOIN str_host_name shn ON (st.id_strain = shn.id_strain AND shn.id_lang = get_report_lang())
LEFT JOIN str_clinical_form_lang scfl ON (sce.id_clinical_form = scfl.id_clinical_form AND scfl.id_lang = get_report_lang())
LEFT JOIN str_coll_comments scc ON (st.id_strain = scc.id_strain AND scc.id_lang = get_report_lang())
LEFT JOIN str_isolation si ON (st.id_strain = si.id_strain)
LEFT JOIN person p2 ON (si.id_person = p2.id_person)
LEFT JOIN institution i2 ON (si.id_institution = i2.id_institution)
LEFT JOIN str_isolation_from sif ON (st.id_strain = sif.id_strain AND sif.id_lang = get_report_lang())
LEFT JOIN str_iso_method sim ON (si.id_strain = sim.id_strain AND sim.id_lang = get_report_lang())
LEFT JOIN str_identification sid ON (st.id_strain = sid.id_strain)
LEFT JOIN person p3 ON (sid.id_person = p3.id_person)
LEFT JOIN institution i3 ON (sid.id_institution = i3.id_institution)
LEFT JOIN str_ident_method sidm ON (st.id_strain = sidm.id_strain AND sidm.id_lang = get_report_lang())
LEFT JOIN str_deposit sd ON (st.id_strain = sd.id_strain)
LEFT JOIN person p4 ON (sd.id_person = p4.id_person)
LEFT JOIN institution i4 ON (sd.id_institution = i4.id_institution)
LEFT JOIN str_dep_reason_lang sdrl ON (sd.id_dep_reason = sdrl.id_dep_reason AND sdrl.id_lang = get_report_lang())
LEFT JOIN person p5 ON (sd.aut_person = p5.id_person)
LEFT JOIN str_culture sc ON (st.id_strain = sc.id_strain)
LEFT JOIN str_cult_medium scm ON (st.id_strain = scm.id_strain AND scm.id_lang = get_report_lang())
LEFT JOIN str_incub_time sit ON (st.id_strain = sit.id_strain AND sit.id_lang = get_report_lang())
LEFT JOIN str_oxy_req sor ON (st.id_strain = sor.id_strain AND sor.id_lang = get_report_lang())
LEFT JOIN str_cult_comments scuc ON (st.id_strain = scuc.id_strain AND scuc.id_lang = get_report_lang())
LEFT JOIN str_characs sch ON (st.id_strain = sch.id_strain)
LEFT JOIN str_cha_ogm_comments scoc ON (st.id_strain = scoc.id_strain AND scoc.id_lang = get_report_lang())
LEFT JOIN str_cha_biorisk_comments scbc ON (st.id_strain = scbc.id_strain AND scbc.id_lang = get_report_lang())
LEFT JOIN str_cha_restrictions scr ON (st.id_strain = scr.id_strain AND scr.id_lang = get_report_lang())
LEFT JOIN str_cha_pictures scp ON (st.id_strain = scp.id_strain AND scp.id_lang = get_report_lang())
LEFT JOIN str_cha_urls scu ON (st.id_strain = scu.id_strain AND scu.id_lang = get_report_lang())
LEFT JOIN str_cha_catalogue scca ON (st.id_strain = scca.id_strain AND scca.id_lang = get_report_lang())
LEFT JOIN str_properties spr ON (st.id_strain = spr.id_strain)
LEFT JOIN str_pro_properties spp ON (st.id_strain = spp.id_strain AND spp.id_lang = get_report_lang())
LEFT JOIN str_pro_applications spa ON (st.id_strain = spa.id_strain AND spa.id_lang = get_report_lang())
LEFT JOIN str_pro_urls spu ON (st.id_strain = spu.id_strain AND spu.id_lang = get_report_lang());
