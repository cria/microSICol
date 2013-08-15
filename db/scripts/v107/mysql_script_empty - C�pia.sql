DROP DATABASE IF EXISTS sicol_v108;
CREATE DATABASE IF NOT EXISTS sicol_v108 CHARACTER SET utf8;
USE sicol_v108;

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
  INDEX FK_taxon_group(id_taxon_group, id_subcoll),
  FOREIGN KEY(id_hierarchy)
    REFERENCES hierarchy_def(id_hierarchy)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_taxon_group, id_subcoll)
    REFERENCES taxon_group_subcoll(id_taxon_group, id_subcoll)
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
  comments TEXT NULL,
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

CREATE TABLE strain (
  id_strain INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_subcoll TINYINT UNSIGNED NOT NULL,
  code VARCHAR(30) NOT NULL,
  internal_code VARCHAR(30) NULL,
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
  UNIQUE INDEX code_subcoll(code,id_subcoll),
  INDEX FK_species(id_species),
  INDEX FK_str_type(id_type),
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

CREATE TABLE str_cult_way (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  way TEXT NOT NULL,
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
  num_ampoules INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(id_lot,id_strain,num_ampoules),
  FOREIGN KEY(id_lot)
    REFERENCES lot(id_lot)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_strain)
    REFERENCES strain(id_strain)
      ON DELETE CASCADE
      ON UPDATE CASCADE
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
  INDEX preservation_FKIndex1(id_lot),
  FOREIGN KEY(id_preservation_method)
    REFERENCES preservation_method(id_preservation_method)
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
  num_ampoules_used INTEGER UNSIGNED NULL COMMENT 'used if origin_type = lot',
  num_ampoules_prepared INTEGER UNSIGNED NOT NULL,
  stock_position VARCHAR(100) NULL,
  stock_minimum INTEGER UNSIGNED NOT NULL,
  id_doc INTEGER UNSIGNED NULL COMMENT 'culture way is a document qualifier',
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
  PRIMARY KEY(id_preserv_str),
  INDEX preservation_strain_FKIndex1(id_lot),
  FOREIGN KEY(id_strain)
    REFERENCES strain(id_strain)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_preservation)
    REFERENCES preservation(id_preservation)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_quality (
  id_quality INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  id_user INTEGER UNSIGNED NOT NULL,
  id_lot INTEGER UNSIGNED NOT NULL,
  id_strain INTEGER UNSIGNED NOT NULL,
  date DATE NOT NULL,
  num_ampoules INTEGER UNSIGNED NOT NULL,
  last_update DATETIME NULL,
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
      ON DELETE CASCADE
      ON UPDATE CASCADE,
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
  quantity INTEGER UNSIGNED NOT NULL,
  date DATE NOT NULL,
  id_person INTEGER UNSIGNED NULL,
  reason TEXT NULL,
  last_update DATETIME NULL,
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
