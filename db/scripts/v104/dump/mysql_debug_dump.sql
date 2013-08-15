-- MySQL Administrator dump 1.4
--
-- ------------------------------------------------------
-- Server version	5.0.27-community-nt

USE sicol_v104; 
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
/*!40000 ALTER TABLE `doc_qualifier` ENABLE KEYS */;

/*!40000 ALTER TABLE `doc_title` DISABLE KEYS */;
/*!40000 ALTER TABLE `doc_title` ENABLE KEYS */;

/*!40000 ALTER TABLE `inst_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `inst_comments` ENABLE KEYS */;

/*!40000 ALTER TABLE `institution` DISABLE KEYS */;
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
/*!40000 ALTER TABLE `person` ENABLE KEYS */;

/*!40000 ALTER TABLE `ref` DISABLE KEYS */;
INSERT INTO `sicol_v104`.`ref` (`id_ref`,`id_coll`,`id_subcoll`,`author`,`year`,`url`,`last_update`) VALUES
(1,1,1,'Author #1','2001','www.linearsm.com.br',NULL),
(2,1,1,'Unknown Author',NULL,NULL,NULL),
(3,1,1,'Âütõr',NULL,NULL,NULL),
(4,1,1,NULL,'1999',NULL,NULL),
(5,1,1,NULL,NULL,'www.google.com.br',NULL);
/*!40000 ALTER TABLE `ref` ENABLE KEYS */;

/*!40000 ALTER TABLE `ref_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `ref_comments` ENABLE KEYS */;

/*!40000 ALTER TABLE `ref_title` DISABLE KEYS */;
INSERT INTO `sicol_v104`.`ref_title` (`id_lang`,`id_coll`,`id_ref`,`title`) VALUES
(2,1,1,'Título Um'),
(1,1,1,'Title One'),
(2,1,2,'...'),
(1,1,2,'...'),
(2,1,3,'Teste'),
(1,1,3,'Teste'),
(2,1,4,'ASDF'),
(1,1,4,'FDSA'),
(2,1,5,'QWERTY'),
(1,1,5,'QWERTY');
/*!40000 ALTER TABLE `ref_title` ENABLE KEYS */;

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

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
