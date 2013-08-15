CREATE DATABASE IF NOT EXISTS sicol_v099 CHARACTER SET utf8;
USE sicol_v099; 

CREATE TABLE loc_country (
  id_country TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
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
  address VARCHAR(255) NULL,
  complement VARCHAR(50) NULL,
  postal_code VARCHAR(15) NULL,
  phone VARCHAR(255) NULL,
  email VARCHAR(100) NULL,
  last_update DATETIME NULL,
  PRIMARY KEY(id_person),
  UNIQUE INDEX person_key(name, nickname)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE spe_subdiv (
  id_subdiv TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  subdiv VARCHAR(20) NOT NULL,
  PRIMARY KEY(id_subdiv)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE spe_name_qualifier (
  id_name_qualifier TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  PRIMARY KEY(id_name_qualifier)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_dep_reason (
  id_dep_reason TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  PRIMARY KEY(id_dep_reason)
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
  author VARCHAR(100) NULL,
  year YEAR NULL,
  url VARCHAR(255) NULL,
  last_update DATETIME NULL,
  PRIMARY KEY(id_ref, id_coll)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_iso_method (
  id_iso_method INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  iso_method VARCHAR(100) NOT NULL,
  PRIMARY KEY(id_iso_method)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE institution (
  id_institution INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  code1 VARCHAR(20) NULL,
  code2 VARCHAR(20) NULL,
  code3 VARCHAR(20) NULL,
  dbafbn VARCHAR(50) NOT NULL,
  nickname VARCHAR(50) NULL,
  name VARCHAR(80) NULL,
  address VARCHAR(255) NULL,
  phone VARCHAR(255) NULL,
  email VARCHAR(100) NULL,
  website VARCHAR(100) NULL,
  last_update DATETIME NULL,
  PRIMARY KEY(id_institution),
  UNIQUE INDEX institution_key(dbafbn, nickname)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_type (
  id_type TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  PRIMARY KEY(id_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE doc_qualifier (
  id_qualifier TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  qualifier VARCHAR(20) NOT NULL,
  PRIMARY KEY(id_qualifier)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE lang (
  id_lang TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  code CHAR(4) NOT NULL,
  lang VARCHAR(30) NOT NULL,
  lang_en VARCHAR(30) NOT NULL,
  PRIMARY KEY(id_lang),
  UNIQUE INDEX code(code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE doc (
  id_doc INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_subcoll TINYINT UNSIGNED NOT NULL,
  code VARCHAR(20) NOT NULL,
  id_qualifier TINYINT UNSIGNED NULL,
  last_update DATETIME NULL,
  PRIMARY KEY(id_doc, id_coll),
  UNIQUE INDEX code(code),
  INDEX FK_qualifier(id_qualifier),
  FOREIGN KEY(id_qualifier)
    REFERENCES doc_qualifier(id_qualifier)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE loc_state (
  id_state TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_country TINYINT UNSIGNED NOT NULL,
  code CHAR(4) NOT NULL,
  state VARCHAR(50) NOT NULL,
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
  id_state TINYINT UNSIGNED NOT NULL,
  id_country TINYINT UNSIGNED NOT NULL,
  city VARCHAR(50) NOT NULL,
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

CREATE TABLE ref_title (
  id_lang TINYINT UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_ref INTEGER UNSIGNED NOT NULL,
  title VARCHAR(50) NOT NULL,
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

CREATE TABLE ref_comments (
  id_lang TINYINT UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_ref INTEGER UNSIGNED NOT NULL,
  comments VARCHAR(255) NOT NULL,
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

CREATE TABLE species (
  id_species INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  taxon_group ENUM('bacteria','fungi','yeast','archae','protozoa') NOT NULL,
  genus VARCHAR(50) NOT NULL,
  subgenus VARCHAR(50) NULL,
  species VARCHAR(50) NOT NULL,
  author VARCHAR(100) NULL,
  id_subdiv TINYINT UNSIGNED NULL,
  infra_name VARCHAR(50) NULL,
  infra_author VARCHAR(50) NULL,
  id_name_qualifier TINYINT UNSIGNED NULL,
  taxon_ref VARCHAR(255) NULL,
  synonym  VARCHAR(100) NULL,
  hazard_group ENUM('1','2','3','4') NULL,
  hazard_group_ref VARCHAR(255) NULL,
  id_alt_states INTEGER UNSIGNED NULL,
  alt_states_type ENUM('ana','teleo') NULL,
  comments TEXT NULL,
  last_update DATETIME NULL,
  PRIMARY KEY(id_species),
  UNIQUE INDEX species_fullname(genus, subgenus, species, id_subdiv, infra_name),
  INDEX FK_subdiv(id_subdiv),
  INDEX FK_name_qualifier(id_name_qualifier),
  FOREIGN KEY(id_subdiv)
    REFERENCES spe_subdiv(id_subdiv)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_name_qualifier)
    REFERENCES spe_name_qualifier(id_name_qualifier)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE doc_description (
  id_doc INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  description VARCHAR(255) NOT NULL,
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
  id_country TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  country VARCHAR(30) NOT NULL,
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
  id_species INTEGER UNSIGNED NULL,
  infra_complement VARCHAR(50) NULL,
  id_type TINYINT UNSIGNED NULL,
  history VARCHAR(255) NULL,
  extra_codes VARCHAR(255) NULL,
  comments TEXT NULL,
  last_update DATETIME NULL,
  PRIMARY KEY(id_strain, id_coll),
  UNIQUE INDEX code(code),
  INDEX FK_species(id_species),
  INDEX FK_str_type(id_type),
  FOREIGN KEY(id_species)
    REFERENCES species(id_species)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_type)
    REFERENCES str_type(id_type)
      ON DELETE CASCADE
      ON UPDATE CASCADE
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
  ambient_risk VARCHAR(255) NOT NULL,
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
  species VARCHAR(100) NULL,
  date DATE NULL,
  id_dep_reason TINYINT UNSIGNED NULL,
  risk VARCHAR(255) NULL,
  preserv_method VARCHAR(255) NULL,
  form VARCHAR(50) NULL,
  comments TEXT NULL,
  PRIMARY KEY(id_strain, id_coll),
  INDEX FK_strain_coll(id_strain, id_coll),
  INDEX FK_person(id_person),
  INDEX FK_institution(id_institution),
  INDEX FK_dep_reason(id_dep_reason),
  FOREIGN KEY(id_strain, id_coll)
    REFERENCES strain(id_strain, id_coll)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_person)
    REFERENCES person(id_person)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_institution)
    REFERENCES institution(id_institution)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_dep_reason)
    REFERENCES str_dep_reason(id_dep_reason)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_isolation (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_person INTEGER UNSIGNED NULL,
  id_institution INTEGER UNSIGNED NULL,
  date DATE NULL,
  id_iso_method INTEGER UNSIGNED NULL,
  way VARCHAR(255) NULL,
  temp VARCHAR(50) NULL,
  incub_time VARCHAR(50) NULL,
  comments TEXT NULL,
  PRIMARY KEY(id_strain, id_coll),
  INDEX FK_strain_coll(id_strain, id_coll),
  INDEX FK_person(id_person),
  INDEX FK_institution(id_institution),
  INDEX FK_iso_method(id_iso_method),
  FOREIGN KEY(id_strain, id_coll)
    REFERENCES strain(id_strain, id_coll)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_person)
    REFERENCES person(id_person)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_institution)
    REFERENCES institution(id_institution)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_iso_method)
    REFERENCES str_iso_method(id_iso_method)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_coll_event (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_person INTEGER UNSIGNED NULL,
  id_institution INTEGER UNSIGNED NULL,
  date DATE NULL,
  id_country TINYINT UNSIGNED NULL,
  id_state TINYINT UNSIGNED NULL,
  id_city INTEGER UNSIGNED NULL,
  place VARCHAR(255) NULL,
  gps_latitude DECIMAL(9,6) NULL,
  gps_longitude DECIMAL(9,6) NULL,
  gps_precision DECIMAL(5,1) NULL,
  id_gps_datum SMALLINT UNSIGNED NULL,
  gps_comments VARCHAR(255) NULL,
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
  INDEX FK_gps_datum(id_gps_datum),
  INDEX FK_clinical_form(id_clinical_form),
  FOREIGN KEY(id_strain, id_coll)
    REFERENCES strain(id_strain, id_coll)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_person)
    REFERENCES person(id_person)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_institution)
    REFERENCES institution(id_institution)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_gps_datum)
    REFERENCES str_gps_datum(id_gps_datum)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_clinical_form)
    REFERENCES str_clinical_form(id_clinical_form)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_characs (
  id_coll TINYINT UNSIGNED NOT NULL,
  id_strain INTEGER UNSIGNED NOT NULL,
  zymodeme TINYINT UNSIGNED NULL,
  serodeme VARCHAR(20) NULL,
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
  PRIMARY KEY(id_coll, id_strain),
  INDEX FK_strain_coll(id_strain, id_coll),
  FOREIGN KEY(id_strain, id_coll)
    REFERENCES strain(id_strain, id_coll)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE str_cha_properties (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  properties VARCHAR(255) NOT NULL,
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
  restrictions VARCHAR(255) NOT NULL,
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

CREATE TABLE str_substratum (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  substratum VARCHAR(255) NOT NULL,
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
  host_name VARCHAR(100) NOT NULL,
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
  way VARCHAR(255) NOT NULL,
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
  pictures VARCHAR(255) NOT NULL,
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

CREATE TABLE str_cha_applications (
  id_strain INTEGER UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_lang TINYINT UNSIGNED NOT NULL,
  applications VARCHAR(255) NOT NULL,
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
  catalogue_notes VARCHAR(255) NOT NULL,
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
  description VARCHAR(255) NULL,
  type ENUM('user','group','level','all') NOT NULL DEFAULT 'user',
  PRIMARY KEY(id_role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE system_areas (
  id_area SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  description VARCHAR(255) NULL,
  PRIMARY KEY(id_area)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE roles_users (
  id_user INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
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
  permission ENUM('r','w') NOT NULL DEFAULT 'w',
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
  id_item INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
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

CREATE VIEW view_cria AS
  SELECT S.id_coll AS institution,
  CASE id_subcoll WHEN 1 THEN 'IOC-L' ELSE ''
  END AS collection, S.id_strain as skey, now() AS datecreated,
  null AS basisofrecord, null AS kingdom, null AS phylum, null AS class, null AS 'order', null AS family,
  SP.genus, SP.species, SP.infra_name AS subspecies,
  TRIM(CONCAT_WS(' ', SP.genus, SP.species, SP.infra_name)) AS scientificname,
  IF(ISNULL(SP.infra_name), SP.author, SP.infra_author) AS author,
  null AS identifiedby, null AS yearidentified, null AS monthidentified, null AS dayidentified,
  S.id_strain as catalognumber,
  STL.type AS typestatus,
  null AS collectornumber, null AS fieldnumber,
  SD.preserv_method AS preparationtype,
  Date_Format(SCE.date, '%d') AS daycollected,
  Date_Format(SCE.date, '%m') AS monthcollected,
  Date_Format(SCE.date, '%Y') AS yearcollected,
  null AS timeofday, null AS continentocean,
  P.name AS collectorname,
  LC.city As county, LS.state AS state, LCL.country AS country, SCE.place AS locality,
  SCE.gps_latitude AS latitude, SCE.gps_longitude AS longitude, SCE.gps_precision AS coordinateprecision,
  null AS minimumelevation, null AS maximumelevation, null AS minimumdepth, null AS maximumdepth, null AS sex,
  null AS individualcount, null AS previouscatalognumber, null AS relationshiptype, null AS relatedcatalogitem,
  S.comments AS strainnotes, SCE.gps_comments AS localnotes, SCC.comments AS collnotes, SPC.comments AS speciesnotes,
  SCN.catalogue_notes AS catalognotes
  FROM (((((((((((strain S INNER JOIN str_coll_event SCE ON S.id_strain = SCE.id_strain AND S.id_coll = SCE.id_coll)
  LEFT OUTER JOIN str_type_lang STL ON S.id_type = STL.id_type AND STL.id_lang = 2)
  LEFT OUTER JOIN loc_city LC ON SCE.id_city = LC.id_city)
  LEFT OUTER JOIN loc_state LS ON LC.id_state = LS.id_state)
  LEFT OUTER JOIN loc_country_lang LCL ON LC.id_country = LCL.id_country)
  LEFT OUTER JOIN str_coll_comments SCC ON S.id_coll = SCC.id_coll AND SCE.id_strain = SCC.id_strain AND SCC.id_lang = 2)
  LEFT OUTER JOIN person P ON SCE.id_person = P.id_person)
  LEFT OUTER JOIN str_deposit SD ON S.id_strain = SD.id_strain AND S.id_coll = SD.id_coll)
  LEFT OUTER JOIN species SP ON S.id_species = SP.id_species)
  LEFT OUTER JOIN spe_comments SPC ON SP.id_species = SPC.id_species AND SPC.id_lang = 2)
  LEFT OUTER JOIN str_cha_catalogue SCN ON S.id_strain = SCN.id_strain AND S.id_coll = SCN.id_coll AND SCN.id_lang = 2);