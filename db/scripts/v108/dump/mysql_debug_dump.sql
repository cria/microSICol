-- MySQL Administrator dump 1.4
--
-- ------------------------------------------------------
-- Server version	5.0.27-community-nt

USE sicol_v108; 
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

/*!40000 ALTER TABLE `contact_relations` DISABLE KEYS */;
INSERT INTO `sicol_v108`.`contact_relations` (`id_person`,`id_institution`,`contact`,`department`,`email`,`last_update`) VALUES 
 (1,1,'yes',NULL,NULL,'2006-12-19 12:34:51'),
 (3,2,'yes',NULL,NULL,'2006-12-19 12:34:52'),
 (4,2,'no',NULL,NULL,'2006-12-19 12:34:53');
/*!40000 ALTER TABLE `contact_relations` ENABLE KEYS */;

/*!40000 ALTER TABLE `doc` DISABLE KEYS */;
/*!40000 ALTER TABLE `doc` ENABLE KEYS */;

/*!40000 ALTER TABLE `doc_description` DISABLE KEYS */;
/*!40000 ALTER TABLE `doc_description` ENABLE KEYS */;

/*!40000 ALTER TABLE `doc_file` DISABLE KEYS */;
/*!40000 ALTER TABLE `doc_file` ENABLE KEYS */;

/*!40000 ALTER TABLE `doc_qualifier` DISABLE KEYS */;
/*!40000 ALTER TABLE `doc_qualifier` ENABLE KEYS */;

/*!40000 ALTER TABLE `doc_title` DISABLE KEYS */;
/*!40000 ALTER TABLE `doc_title` ENABLE KEYS */;

/*!40000 ALTER TABLE `inst_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `inst_comments` ENABLE KEYS */;

/*!40000 ALTER TABLE `institution` DISABLE KEYS */;
INSERT INTO `sicol_v108`.`institution` (`id_institution`,`code1`,`code2`,`code3`,`complement`,`nickname`,`name`,`address`,`phone`,`email`,`website`,`last_update`) VALUES 
 (1,NULL,NULL,NULL,'Instituto de Biologia','UNICAMP','Universidade Estadual de Campinas',NULL,NULL,NULL,NULL,'2006-12-19 12:34:50'),
 (2,NULL,NULL,NULL,'São Paulo','Linear','Softwares Matemáticos',NULL,NULL,NULL,NULL,'2006-12-19 12:34:51'),
 (3,NULL,NULL,NULL,'CRIA - SICol','CRIA','Cria',NULL,NULL,NULL,NULL,'2006-12-19 12:34:52');
/*!40000 ALTER TABLE `institution` ENABLE KEYS */;

/*!40000 ALTER TABLE `lang` DISABLE KEYS */;
/*!40000 ALTER TABLE `lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `loc_city` DISABLE KEYS */;
/*!40000 ALTER TABLE `loc_city` ENABLE KEYS */;

/*!40000 ALTER TABLE `loc_country` DISABLE KEYS */;
/*!40000 ALTER TABLE `loc_country` ENABLE KEYS */;

/*!40000 ALTER TABLE `loc_country_lang` DISABLE KEYS */;
/*!40000 ALTER TABLE `loc_country_lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `loc_state` DISABLE KEYS */;
/*!40000 ALTER TABLE `loc_state` ENABLE KEYS */;

/*!40000 ALTER TABLE `per_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `per_comments` ENABLE KEYS */;

/*!40000 ALTER TABLE `person` DISABLE KEYS */;
INSERT INTO `sicol_v108`.`person` (`id_person`,`name`,`nickname`,`address`,`phone`,`email`,`last_update`) VALUES 
 (1,'Fulano 1','F1',NULL,NULL,NULL,'2006-12-19 12:34:51'),
 (2,'Sicrano 2','S2',NULL,NULL,NULL,'2006-12-19 12:34:52'),
 (3,'Personne Âgée','PA',NULL,NULL,NULL,'2006-12-19 12:34:53'),
 (4,'Fulano 3','F3',NULL,NULL,NULL,'2006-12-19 12:34:54'),
 (5,'Beltrano 4','B4',NULL,NULL,NULL,'2006-12-19 12:34:54');
/*!40000 ALTER TABLE `person` ENABLE KEYS */;

/*!40000 ALTER TABLE `ref` DISABLE KEYS */;
INSERT INTO `sicol_v108`.`ref` (`id_ref`,`id_coll`,`id_subcoll`,`title`,`author`,`year`,`url`,`last_update`) VALUES
(1,1,1,'Título 1','Author #1','2001','www.linearsm.com.br',NULL),
(2,1,1,'Título 2','Unknown Author',NULL,NULL,NULL),
(3,1,1,'Título 3','Âütõr',NULL,NULL,NULL),
(4,1,1,'Título 4',NULL,'1999',NULL,NULL),
(5,1,1,'Título 5',NULL,NULL,'www.google.com.br',NULL);
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

/*!40000 ALTER TABLE `spe_subdiv` DISABLE KEYS */;
/*!40000 ALTER TABLE `spe_subdiv` ENABLE KEYS */;

/*!40000 ALTER TABLE `species` DISABLE KEYS */;
INSERT INTO `sicol_v108`.`species` (`id_species`,`id_coll`,`id_subcoll`,`id_taxon_group`,`genus`,`subgenus`,`species`,`author`,`id_subdiv`,`infra_name`,`infra_author`,`id_name_qualifier`,`taxon_ref`,`synonym`,`hazard_group`,`hazard_group_ref`,`id_alt_states`,`alt_states_type`,`comments`,`last_update`) VALUES 
 (1,1,1,1,'Leishmania','Leishmania','major',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
 (2,1,1,1,'Leishmania','Leishmania','minor',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
 (3,1,1,1,'Leishmania','Leishmania','ordinaris',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
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

/*!40000 ALTER TABLE `str_clinical_form` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_clinical_form` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_clinical_form_lang` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_clinical_form_lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_coll_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_coll_comments` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_coll_event` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_coll_event` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_cult_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_cult_comments` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_cult_way` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_cult_way` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_culture` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_culture` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_dep_reason` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_dep_reason` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_dep_reason_lang` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_dep_reason_lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_deposit` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_deposit` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_gps_datum` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_gps_datum` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_host_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_host_name` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_iso_method` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_iso_method` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_isolation` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_isolation` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_substratum` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_substratum` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_type` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_type_lang` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_type_lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `strain` DISABLE KEYS */;
INSERT INTO `sicol_v108`.`strain` (`id_strain`,`id_coll`,`id_subcoll`,`code`,`id_species`,`infra_complement`,`id_type`,`history`,`extra_codes`,`comments`,`last_update`,`status`) VALUES 
 (1,1,1,'1001',1,NULL,NULL,NULL,NULL,NULL,'2006-12-19 12:34:50','active'),
 (2,1,1,'1002',2,NULL,NULL,NULL,NULL,NULL,'2006-12-21 12:34:50','active'),
 (3,1,1,'1003',3,NULL,NULL,NULL,NULL,NULL,'2006-12-22 12:34:50','active');
/*!40000 ALTER TABLE `strain` ENABLE KEYS */;

/*!40000 ALTER TABLE `system_areas` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_areas` ENABLE KEYS */;

/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;

/*!40000 ALTER TABLE `roles_users` DISABLE KEYS */;
/*!40000 ALTER TABLE `roles_users` ENABLE KEYS */;

/*!40000 ALTER TABLE `areas_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `areas_permissions` ENABLE KEYS */;

/*!40000 ALTER TABLE `roles_permissions` DISABLE KEYS */;
-- Area[6] = 'References'
INSERT INTO roles_permissions(id_item,id_role,id_area,permission) VALUES
(1,1,6,'w'),
(2,1,6,'w'),
(3,1,6,'w'),
(4,1,6,'w'),
(5,1,6,'w');
/*!40000 ALTER TABLE `roles_permissions` ENABLE KEYS */;

/*!40000 ALTER TABLE `areas_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `areas_permissions` ENABLE KEYS */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
