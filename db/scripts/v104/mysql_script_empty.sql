DROP DATABASE IF EXISTS sicol_v104;
CREATE DATABASE IF NOT EXISTS sicol_v104 CHARACTER SET utf8;
USE sicol_v104; 

CREATE TABLE lang (
  id_lang TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  code CHAR(4) NOT NULL,
  lang VARCHAR(30) NOT NULL,
  lang_en VARCHAR(30) NOT NULL,
  PRIMARY KEY(id_lang),
  UNIQUE INDEX code(code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
  address TEXT NULL,
  phone TEXT NULL,
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
  complement VARCHAR(50) NOT NULL,
  nickname VARCHAR(50) NULL,
  name VARCHAR(80) NULL,
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

CREATE TABLE doc (
  id_doc INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_subcoll TINYINT UNSIGNED NOT NULL,
  code VARCHAR(20) NOT NULL,
  id_qualifier TINYINT UNSIGNED NULL,
  last_update DATETIME NULL,
  PRIMARY KEY(id_doc, id_coll),
  UNIQUE INDEX code_coll(code,id_coll),
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

CREATE TABLE ref_title (
  id_lang TINYINT UNSIGNED NOT NULL,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_ref INTEGER UNSIGNED NOT NULL,
  title VARCHAR(255) NOT NULL,
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

CREATE TABLE species (
  id_species INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  id_coll TINYINT UNSIGNED NOT NULL,
  id_subcoll TINYINT UNSIGNED NOT NULL,
  taxon_group ENUM('bacteria','fungi','yeast','archae','protozoa') NOT NULL,
  genus VARCHAR(50) NOT NULL,
  subgenus VARCHAR(50) NULL,
  species VARCHAR(50) NOT NULL,
  author VARCHAR(100) NULL,
  id_subdiv TINYINT UNSIGNED NULL,
  infra_name VARCHAR(50) NULL,
  infra_author VARCHAR(50) NULL,
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
  UNIQUE INDEX species_fullname_subcoll(genus, subgenus, species, id_subdiv, infra_name,id_subcoll),
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
      ON UPDATE CASCADE,
  FOREIGN KEY(id_type)
    REFERENCES str_type(id_type)
      ON DELETE RESTRICT
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
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_institution)
    REFERENCES institution(id_institution)
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
  place TEXT NULL,
  gps_latitude DECIMAL(11,8) NULL,
  gps_latitude_dms VARCHAR(10) NULL,
  gps_latitude_mode ENUM('decimal','dms') NULL,
  gps_longitude DECIMAL(11,8) NULL,
  gps_longitude_dms VARCHAR(10) NULL,
  gps_longitude_mode ENUM('decimal','dms') NULL,
  gps_precision DECIMAL(5,1) NULL,
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
  biochemical TEXT NULL,
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
