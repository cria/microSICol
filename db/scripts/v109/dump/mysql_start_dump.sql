USE sicol_v109; 
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

/*!40000 ALTER TABLE `contact_relations` DISABLE KEYS */;
/*!40000 ALTER TABLE `contact_relations` ENABLE KEYS */;

/*!40000 ALTER TABLE `doc` DISABLE KEYS */;
/*!40000 ALTER TABLE `doc` ENABLE KEYS */;

/*!40000 ALTER TABLE `doc_description` DISABLE KEYS */;
/*!40000 ALTER TABLE `doc_description` ENABLE KEYS */;

/*!40000 ALTER TABLE `doc_file` DISABLE KEYS */;
/*!40000 ALTER TABLE `doc_file` ENABLE KEYS */;

/*!40000 ALTER TABLE `doc_qualifier` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`doc_qualifier` (`id_qualifier`,`qualifier`) VALUES
 (1,'Foto'),
 (2,'Seq'),
 (3,'Doc'),
 (4,'Meio'),
 (5,'Teste');
/*!40000 ALTER TABLE `doc_qualifier` ENABLE KEYS */;

/*!40000 ALTER TABLE `doc_title` DISABLE KEYS */;
/*!40000 ALTER TABLE `doc_title` ENABLE KEYS */;

/*!40000 ALTER TABLE `inst_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `inst_comments` ENABLE KEYS */;

/*!40000 ALTER TABLE `institution` DISABLE KEYS */;
/*!40000 ALTER TABLE `institution` ENABLE KEYS */;

/*!40000 ALTER TABLE `lang` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`lang` (`id_lang`,`code`,`lang`,`lang_en`) VALUES
 (1,'en','English','English'),
 (2,'ptbr','Brazilian Portuguese','Português Brasileiro');
/*!40000 ALTER TABLE `lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `loc_city` DISABLE KEYS */;
/*!40000 ALTER TABLE `loc_city` ENABLE KEYS */;

/*!40000 ALTER TABLE `loc_country` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`loc_country` (`id_country`,`code`) VALUES
 (1,'AR'),
 (2,'AZ'),
 (3,'BO'),
 (4,'BR'),
 (5,'BZ'),
 (6,'CN'),
 (7,'CO'),
 (8,'CR'),
 (9,'DO'),
 (10,'DZ'),
 (11,'EC'),
 (12,'ET'),
 (13,'HN'),
 (14,'IL'),
 (15,'JO'),
 (16,'KE'),
 (17,'MX'),
 (18,'NI'),
 (19,'PA'),
 (20,'PE'),
 (21,'PY'),
 (22,'SD'),
 (23,'SE'),
 (24,'TM'),
 (25,'TN'),
 (28,'US'),
 (26,'UZ'),
 (27,'VE');
/*!40000 ALTER TABLE `loc_country` ENABLE KEYS */;


/*!40000 ALTER TABLE `loc_country_lang` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`loc_country_lang` (`id_country`,`id_lang`,`country`) VALUES
 (1,1,'Argentina'),
 (1,2,'Argentina'),
 (2,1,'Azerbaijian'),
 (2,2,'Azerbaijão'),
 (3,1,'Bolivia'),
 (3,2,'Bolívia'),
 (4,1,'Brazil'),
 (4,2,'Brasil'),
 (5,1,'Belize'),
 (5,2,'Belize'),
 (6,1,'China'),
 (6,2,'China'),
 (7,1,'Colombia'),
 (7,2,'Colombia'),
 (8,1,'Costa Rica'),
 (8,2,'Costa Rica'),
 (9,1,'Dominican Republic'),
 (9,2,'República Dominicana'),
 (10,1,'Algeria'),
 (10,2,'Argélia'),
 (11,1,'Ecuador'),
 (11,2,'Equador'),
 (12,1,'Ethiopia'),
 (12,2,'Etiópia'),
 (13,1,'Honduras'),
 (13,2,'Honduras'),
 (14,1,'Israel'),
 (14,2,'Israel'),
 (15,1,'Jordan'),
 (15,2,'Jordânia'),
 (16,1,'Kenia'),
 (16,2,'Quênia'),
 (17,1,'Mexico'),
 (17,2,'México'),
 (18,1,'Nicaragua'),
 (18,2,'Nicaragua'),
 (19,1,'Panama'),
 (19,2,'Panamá'),
 (20,1,'Peru'),
 (20,2,'Peru'),
 (21,1,'Paraguay'),
 (21,2,'Paraguai'),
 (22,1,'Sudan'),
 (22,2,'Sudão'),
 (23,1,'Sweden'),
 (23,2,'Suécia'),
 (24,1,'Turkmenistan'),
 (24,2,'Turcomenistão');
INSERT INTO `sicol_v109`.`loc_country_lang` (`id_country`,`id_lang`,`country`) VALUES
 (25,1,'Tunisia'),
 (25,2,'Tunísia'),
 (26,1,'Uzbekistan'),
 (26,2,'Uzbequistão'),
 (27,1,'Venezuela'),
 (27,2,'Venezuela'),
 (28,1,'United States of America'),
 (28,2,'Estados Unidos da América');
/*!40000 ALTER TABLE `loc_country_lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `loc_state` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`loc_state` (`id_state`,`id_country`,`code`,`state`) VALUES
 (1,4,'AC','Acre'),
 (2,4,'AL','Alagoas'),
 (3,4,'AP','Amapá'),
 (4,4,'AM','Amazonas'),
 (5,4,'BA','Bahia'),
 (6,4,'CE','Ceará'),
 (7,4,'DF','Distrito Federal'),
 (8,4,'ES','Espírito Santo'),
 (9,4,'GO','Goiás'),
 (10,4,'MA','Maranhão'),
 (11,4,'MT','Mato Grosso'),
 (12,4,'MS','Mato Grosso do Sul'),
 (13,4,'MG','Minas Gerais'),
 (14,4,'PA','Pará'),
 (15,4,'PB','Paraíba'),
 (16,4,'PR','Paraná'),
 (17,4,'PE','Pernambuco'),
 (18,4,'PI','Piauí'),
 (19,4,'RJ','Rio de Janeiro'),
 (20,4,'RN','Rio Grande do Norte'),
 (21,4,'RS','Rio Grande do Sul'),
 (22,4,'RO','Rondônia'),
 (23,4,'RR','Roraima'),
 (24,4,'SC','Santa Catarina'),
 (25,4,'SP','São Paulo'),
 (26,4,'SE','Sergipe'),
 (27,4,'TO','Tocantins');
/*!40000 ALTER TABLE `loc_state` ENABLE KEYS */;

/*!40000 ALTER TABLE `per_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `per_comments` ENABLE KEYS */;

/*!40000 ALTER TABLE `person` DISABLE KEYS */;
/*!40000 ALTER TABLE `person` ENABLE KEYS */;

/*!40000 ALTER TABLE `ref` DISABLE KEYS */;
/*!40000 ALTER TABLE `ref` ENABLE KEYS */;

/*!40000 ALTER TABLE `ref_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `ref_comments` ENABLE KEYS */;

/*!40000 ALTER TABLE `spe_ambient_risk` DISABLE KEYS */;
/*!40000 ALTER TABLE `spe_ambient_risk` ENABLE KEYS */;

/*!40000 ALTER TABLE `spe_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `spe_comments` ENABLE KEYS */;

/*!40000 ALTER TABLE `spe_name_qualifier` DISABLE KEYS */;
/*!40000 ALTER TABLE `spe_name_qualifier` ENABLE KEYS */;

/*!40000 ALTER TABLE `spe_name_qualifier_lang` DISABLE KEYS */;
/*!40000 ALTER TABLE `spe_name_qualifier_lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `taxon_group` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`taxon_group` (`id_taxon_group`) VALUES
 (1),
 (2),
 (3),
 (4),
 (5);
/*!40000 ALTER TABLE `taxon_group` ENABLE KEYS */;

/*!40000 ALTER TABLE `taxon_group_subcoll` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`taxon_group_subcoll` (`id_taxon_group`,`id_subcoll`) VALUES
 (1,1),
 (2,1),
 (3,1),
 (4,1),
 (5,1);
/*!40000 ALTER TABLE `taxon_group_subcoll` ENABLE KEYS */;

/*!40000 ALTER TABLE `taxon_group_lang` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`taxon_group_lang` (`id_taxon_group`,`id_lang`,`taxon_group`) VALUES
 (1,1,'Bacteria'),
 (1,2,'Bactéria'),
 (2,1,'Fungi'),
 (2,2,'Fungo'),
 (3,1,'Yeast'),
 (3,2,'Levedura'),
 (4,1,'Archaea'),
 (4,2,'Arquéia'),
 (5,1,'Protozoa'),
 (5,2,'Protozoário');
/*!40000 ALTER TABLE `taxon_group_lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `hierarchy_def` DISABLE KEYS */;
INSERT INTO sicol_v109.hierarchy_def (id_hierarchy, seq, hi_tax, has_author, use_author, in_sciname, required, important, string_format, string_case, prefix, suffix) VALUES
	(1, 10, true, false, false, false, false, true, 'italic', 'ucfirst', NULL, NULL),
	(2, 20, true, false, false, false, false, true, 'italic', 'ucfirst', NULL, NULL),
	(3, 30, true, false, false, false, false, false, 'italic', 'ucfirst', NULL, NULL),
	(4, 40, true, false, false, false, false, true, 'italic', 'ucfirst', NULL, NULL),
	(5, 50,	true, false, false, false, false, false, 'italic', 'ucfirst', NULL, NULL),
	(6, 60, true, false, false, false, false, true, 'italic', 'ucfirst', NULL, NULL),
	(7, 70, true, false, false, false, false, false, 'italic', 'ucfirst', NULL, NULL),
	(8, 80, true, false, false, false, false, false, 'italic', 'ucfirst', NULL, NULL),
	(9, 90,	true, false, false, false, false, true, 'italic', 'ucfirst', NULL, NULL),
	(10, 100, true, false, false, false, false, false, 'italic', 'ucfirst', NULL, NULL),
	(11, 110, true, false, false, false, false, true, 'italic', 'ucfirst', NULL, NULL),
	(12, 120, true, false, false, false, false, false, 'italic', 'ucfirst', NULL, NULL),
	(13, 130, true, false, false, false, false, false, 'italic', 'ucfirst', NULL, NULL),
	(14, 140, true, false, false, false, false, true, 'italic', 'ucfirst', NULL, NULL),
	(15, 150, true, false, false, false, false, false, 'italic', 'ucfirst', NULL, NULL),
	(16, 160, true, false, false, false, false, false, 'italic', 'ucfirst', NULL, NULL),
	(17, 170, true, false, false, false, false, false, 'italic', 'ucfirst', NULL, NULL),
	(18, 180, false, true, false, true, true, false, 'italic', 'ucfirst', NULL, NULL),
	(19, 190, false, false, false, false, false, false, 'italic', 'ucfirst', '(', ')'),
	(20, 200, false, false, false, false, false, false, 'italic', 'ucfirst', '(', ')'),
	(21, 210, false, true, true, true, true, false, 'italic', 'lower', NULL, NULL),
	(22, 220, false, true, true, true, false, false, 'italic', 'lower', 'subsp. ', NULL),
	(23, 230, false, true, true, true, false, false, 'italic', 'lower', 'var. ', NULL),
	(24, 240, false, true, true, true, false, false, 'italic', 'lower', 'subvar. ', NULL),
	(25, 250, false, false, false, true, false, false, 'italic', 'lower', 'f. ', NULL),
	(26, 260, false, false, false, true, false, false, 'italic', 'lower', 'subf. ', NULL),
	(27, 270, false, false, false, true, false, false, 'italic', 'none', 'ser. ', NULL),
	(28, 280, false, false, false, true, false, false, 'italic', 'none', 'bv. ', NULL),
	(29, 290, false, false, false, true, false, false, 'italic', 'none', 'pv. ', NULL),
	(30, 300, false, true, true, true, false, false, 'italic', 'lower', 'f.sp. ', NULL),
	(31, 310, false, true, true, true, false, false, 'italic', 'none', NULL, NULL);
/*!40000 ALTER TABLE `hierarchy_def` ENABLE KEYS */;

/*!40000 ALTER TABLE `hierarchy_lang` DISABLE KEYS */;
INSERT INTO sicol_v109.hierarchy_lang (id_hierarchy, id_lang, rank) VALUES
(1,		1,	'Domain'),
(2,		1,	'Kingdom'),
(3,		1,	'Subkingdom'),
(4,		1,	'Phylum'),
(5,		1,	'Subphylum'),
(6,		1,	'Division'),
(7,		1,	'Subdivision'),
(8,		1,	'Superclass'),
(9,		1, 'Class'),
(10,		1,	'Subclass'),
(11,		1,	'Order'),
(12,		1,	'Suborder'),
(13,		1,	'Superfamily'),
(14,		1, 'Family'),
(15,		1,	'Subfamily'),
(16,		1,	'Tribe'),
(17,		1,	'Subtribe'),
(18,		1,	'Genus'),
(19,		1,	'Subgenus'),
(20,		1,	'section'),
(21,		1,	'species'),
(22,		1,	'subspecies'),
(23,		1,	'variety'),
(24,		1,	'subvariety'),
(25,		1,	'form'),
(26,		1,	'subform'),
(27,		1,	'serovar'),
(28,		1,	'biovar'),
(29,		1,	'pathovar'),
(30,		1,	'forma specialis'),
(31,		1,	'race'),
(1,		2, 	'Domínio'),
(2,		2,	'Reino'),
(3,		2,	'Subreino'),
(4,		2,	'Filo'),
(5,		2,	'Subfilo'),
(6,		2,	'Divisão'),
(7,		2,	'Subdivisão'),
(8,		2,	'Superclasse'),
(9,		2,	'Classe'),
(10,		2,	'Subclasse'),
(11,		2,	'Ordem'),
(12,		2,	'Subordem'),
(13,		2,	'Superfamília'),
(14,		2,	'Família'),
(15,		2,	'Subfamília'),
(16,		2,	'Tribo'),
(17,		2,	'Subtribo'),
(18,		2,	'Gênero'),
(19,		2,	'Subgênero'),
(20,		2,	'seção'),
(21,		2,	'espécie'),
(22,		2,	'subespécie'),
(23,		2,	'variedade'),
(24,		2,	'subvariedade'),
(25,		2,	'forma'),
(26,		2,	'subforma'),
(27,		2,	'sorovar'),
(28,		2,	'biovar'),
(29,		2,	'patovar'),
(30,		2,	'forma specialis'),
(31,		2,	'raça');
/*!40000 ALTER TABLE `hierarchy_lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `hierarchy_group` DISABLE KEYS */;
INSERT INTO sicol_v109.hierarchy_group (id_hierarchy, id_taxon_group, id_subcoll, hi_tax, has_author, use_author, in_sciname, required, important, string_format, string_case, prefix, suffix, default_value) VALUES
(1, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Bacteria'),
(2, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(4, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(9, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(11, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(14, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(18, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(21, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(22, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(23, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(25, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(27, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(28, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(29, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(1, 5, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(2, 5, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(4, 5, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(9, 5, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(11, 5, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(14, 5, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(18, 5, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(19, 5, 1, NULL, NULL, NULL, TRUE, NULL, TRUE, NULL, NULL, NULL, NULL, NULL),
(21, 5, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(22, 5, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(1, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Eukarya'),
(2, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Fungi'),
(6, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(7, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(9, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(10, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(11, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(12, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(14, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(15, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(16, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(17, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(18, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(19, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(20, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(21, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(22, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(23, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(30, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(31, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
/*!40000 ALTER TABLE `hierarchy_group` ENABLE KEYS */;

/*!40000 ALTER TABLE `species` DISABLE KEYS */;
/*!40000 ALTER TABLE `species` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_cha_biorisk_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_cha_biorisk_comments` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_cha_catalogue` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_cha_catalogue` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_cha_ogm_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_cha_ogm_comments` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_cha_pictures` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_cha_pictures` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_cha_restrictions` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_cha_restrictions` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_cha_urls` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_cha_urls` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_characs` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_characs` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_pro_properties` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_pro_properties` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_pro_applications` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_pro_applications` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_pro_urls` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_pro_urls` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_properties` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_properties` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_clinical_form` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`str_clinical_form` (`id_clinical_form`) VALUES
 (1),
 (2),
 (3),
 (4),
 (5),
 (6),
 (7);
/*!40000 ALTER TABLE `str_clinical_form` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_clinical_form_lang` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`str_clinical_form_lang` (`id_clinical_form`,`id_lang`,`code`,`clinical_form`) VALUES
 (1,1,'CL','Cutaneous Leishmaniasis'),
 (1,2,'LC','Leishmaniose Cutânea'),
 (2,1,'DCL','Diffuse Cutaneous Leishmaniasis'),
 (2,2,'LCD','Leishmaniose Cutânea Difusa'),
 (3,1,'ML','Mucosal Leishmaniasis'),
 (3,2,'LCM','Leishmaniose Cutâneo_Mucosa'),
 (4,1,'DL','Disseminated Leishmaniasis'),
 (4,2,'LD','Leishmaniose Disseminada'),
 (5,1,'VL','Visceral Leishmaniasis'),
 (5,2,'LV','Leishmaniose Viceral'),
 (6,1,'PKDL','Post Kala-Azar Dermal Leishmaniasis'),
 (6,2,'PKDL','Leishmaniose Dérmica Pós-Calazar'),
 (7,1,'LRC','Leishmaniasis Recidiva Cuttis'),
 (7,2,'LR','Leishmaniose Recidiva');
/*!40000 ALTER TABLE `str_clinical_form_lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_coll_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_coll_comments` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_coll_event` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_coll_event` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_cult_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_cult_comments` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_cult_medium` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_cult_medium` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_culture` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_culture` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_dep_reason` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`str_dep_reason` (`id_dep_reason`) VALUES
 (1),
 (2),
 (3);
/*!40000 ALTER TABLE `str_dep_reason` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_dep_reason_subcoll` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`str_dep_reason_subcoll` (`id_dep_reason`,`id_subcoll`) VALUES
 (1,1),
 (2,1),
 (3,1);
/*!40000 ALTER TABLE `str_dep_reason_subcoll` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_dep_reason_lang` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`str_dep_reason_lang` (`id_dep_reason`,`id_lang`,`dep_reason`) VALUES
 (1,1,'Open'),
 (1,2,'Aberto'),
 (2,1,'Closed'),
 (2,2,'Fechado'),
 (3,1,'Restrict'),
 (3,2,'Restrito');
/*!40000 ALTER TABLE `str_dep_reason_lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_deposit` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_deposit` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_type` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`str_type` (`id_type`) VALUES
 (1),
 (2),
 (3);
/*!40000 ALTER TABLE `str_type` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_type_subcoll` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`str_type_subcoll` (`id_type`,`id_subcoll`) VALUES
 (1,1),
 (2,1),
 (3,1);
/*!40000 ALTER TABLE `str_type_subcoll` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_type_lang` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`str_type_lang` (`id_type`,`id_lang`,`type`) VALUES
 (1,1,'Reference'),
 (1,2,'Referência'),
 (2,1,'Type'),
 (2,2,'Tipo'),
 (3,1,'Genotype'),
 (3,2,'Genotipo');
/*!40000 ALTER TABLE `str_type_lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `preservation_method` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`preservation_method` (`id_preservation_method`) VALUES
 (1),
 (2),
 (3),
 (4),
 (5);
/*!40000 ALTER TABLE `preservation_method` ENABLE KEYS */;

/*!40000 ALTER TABLE `preservation_method_subcoll` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`preservation_method_subcoll` (`id_preservation_method`,`id_subcoll`) VALUES
 (1,1),
 (2,1),
 (3,1),
 (4,1),
 (5,1);
/*!40000 ALTER TABLE `preservation_method_subcoll` ENABLE KEYS */;

/*!40000 ALTER TABLE `preservation_method_lang` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`preservation_method_lang` (`id_preservation_method`,`id_lang`,`method`,`unit_measure`) VALUES
 (1,1,'Liophilization','Ampoules'),
 (1,2,'Liofilização','Ampolas'),
 (2,1,'Cryopreservation','Cryotubes'),
 (2,2,'Criopreservação','Criotubos'),
 (3,1,'Water','Tubes'),
 (3,2,'Água','Tubos'),
 (4,1,'Oil','Tubes'),
 (4,2,'Óleo','Tubos'),
 (5,1,'Paper','Stripes'),
 (5,2,'Papel','Tiras');
/*!40000 ALTER TABLE `preservation_method_lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `test_group` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`test_group` (`id_test_group`) VALUES
 (1),
 (2);
/*!40000 ALTER TABLE `test_group` ENABLE KEYS */;

/*!40000 ALTER TABLE `test_group_subcoll` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`test_group_subcoll` (`id_test_group`,`id_subcoll`) VALUES
 (1,1),
 (2,1);
/*!40000 ALTER TABLE `test_group_subcoll` ENABLE KEYS */;

/*!40000 ALTER TABLE `test_group_lang` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`test_group_lang` (`id_test_group`,`id_lang`,`category`) VALUES
 (1,1,'Morphologic Characterization'),
 (1,2,'Caracterização Morfológica'),
 (2,1,'Physiologic Characterization'),
 (2,2,'Caracterização Fisiológica');
/*!40000 ALTER TABLE `test_group_lang` ENABLE KEYS */;


/*!40000 ALTER TABLE `str_gps_datum` DISABLE KEYS */;
INSERT INTO `sicol_v109`.`str_gps_datum` (`id_gps_datum`,`gps_datum`) VALUES
 (1,'WGS84'),
 (2,'SAD69'),
 (3,'SIRGAS'),
 (4,'ITRFyy'),
 (5,'NAD83'),
 (6,'WGS72'),
 (7,'WGS99');
/*!40000 ALTER TABLE `str_gps_datum` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_host_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_host_name` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_iso_method` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_iso_method` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_isolation` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_isolation` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_substratum` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_substratum` ENABLE KEYS */;

/*!40000 ALTER TABLE `strain` DISABLE KEYS */;
/*!40000 ALTER TABLE `strain` ENABLE KEYS */;

-- Insert manually all existing system areas
/*!40000 ALTER TABLE `system_areas` DISABLE KEYS */;
INSERT INTO system_areas(id_area,name,description) VALUES
(1,'species','Taxa Tab'),
(2,'strains','Strains Tab'),
(3,'people','People Tab'),
(4,'institutions','Institutions Tab'),
(5,'doc','Documents Tab'),
(6,'ref','References Tab'),
(7,'preservation','Preservation Tab'),
(8,'distribution','Distribution Tab');
/*!40000 ALTER TABLE `system_areas` ENABLE KEYS */;

-- Insert "ALL" role, "Administrator" level and "Standard System User" in database
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO roles(id_role,name,type) VALUES
(1,'all','all'),
(2,'Administrator','level'),
(3,'Usuario Padrao do Sistema','user');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;

-- The Standard User belongs to ALL and Administrator roles (id_user = 1 => "Super Admin")
/*!40000 ALTER TABLE `roles_users` DISABLE KEYS */;
INSERT INTO roles_users(id_user,id_role) VALUES
(1,1),
(1,2),
(1,3);
/*!40000 ALTER TABLE `roles_users` ENABLE KEYS */;

-- The Administrator role has create/delete permissions to all areas
/*!40000 ALTER TABLE `areas_permissions` DISABLE KEYS */;
INSERT INTO areas_permissions(id_role,id_area,allow_delete,allow_create) VALUES 
(2,1,'y','y'),
(2,2,'y','y'),
(2,3,'y','y'),
(2,4,'y','y'),
(2,5,'y','y'),
(2,6,'y','y'),
(2,7,'y','y'),
(2,8,'y','y');
/*!40000 ALTER TABLE `areas_permissions` ENABLE KEYS */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
