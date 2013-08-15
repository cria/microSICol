-- MySQL Administrator dump 1.4
--
-- ------------------------------------------------------
-- Server version	5.0.27-community-nt

USE sicol_v103; 
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
INSERT INTO `sicol_v103`.`doc_qualifier` (`id_qualifier`,`qualifier`) VALUES 
 (1,'Foto'),
 (2,'Seq'),
 (3,'Doc'),
 (4,'Meio');
/*!40000 ALTER TABLE `doc_qualifier` ENABLE KEYS */;

/*!40000 ALTER TABLE `doc_title` DISABLE KEYS */;
/*!40000 ALTER TABLE `doc_title` ENABLE KEYS */;

/*!40000 ALTER TABLE `inst_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `inst_comments` ENABLE KEYS */;

/*!40000 ALTER TABLE `institution` DISABLE KEYS */;
/*!40000 ALTER TABLE `institution` ENABLE KEYS */;

/*!40000 ALTER TABLE `lang` DISABLE KEYS */;
INSERT INTO `sicol_v103`.`lang` (`id_lang`,`code`,`lang`,`lang_en`) VALUES 
 (1,'en','English','English'),
 (2,'ptbr','Brazil Portuguese','Português Brasileiro');
/*!40000 ALTER TABLE `lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `loc_city` DISABLE KEYS */;
/*!40000 ALTER TABLE `loc_city` ENABLE KEYS */;

/*!40000 ALTER TABLE `loc_country` DISABLE KEYS */;
INSERT INTO `sicol_v103`.`loc_country` (`id_country`,`code`) VALUES 
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
INSERT INTO `sicol_v103`.`loc_country_lang` (`id_country`,`id_lang`,`country`) VALUES 
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
INSERT INTO `sicol_v103`.`loc_country_lang` (`id_country`,`id_lang`,`country`) VALUES 
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
INSERT INTO `sicol_v103`.`loc_state` (`id_state`,`id_country`,`code`,`state`) VALUES 
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

/*!40000 ALTER TABLE `ref_title` DISABLE KEYS */;
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
INSERT INTO `sicol_v103`.`spe_subdiv` (`id_subdiv`,`subdiv`) VALUES 
 (0,''),
 (1,'var.'),
 (2,'subsp.'),
 (3,'pv'),
 (4,'f.'),
 (5,'genomovar');
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

/*!40000 ALTER TABLE `str_cha_properties` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_cha_properties` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_cha_restrictions` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_cha_restrictions` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_cha_urls` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_cha_urls` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_characs` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_characs` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_clinical_form` DISABLE KEYS */;
INSERT INTO `sicol_v103`.`str_clinical_form` (`id_clinical_form`) VALUES 
 (1),
 (2),
 (3),
 (4),
 (5),
 (6),
 (7);
/*!40000 ALTER TABLE `str_clinical_form` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_clinical_form_lang` DISABLE KEYS */;
INSERT INTO `sicol_v103`.`str_clinical_form_lang` (`id_clinical_form`,`id_lang`,`code`,`clinical_form`) VALUES 
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

/*!40000 ALTER TABLE `str_cult_way` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_cult_way` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_culture` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_culture` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_dep_reason` DISABLE KEYS */;
INSERT INTO `sicol_v103`.`str_dep_reason` (`id_dep_reason`) VALUES 
 (1),
 (2),
 (3);
/*!40000 ALTER TABLE `str_dep_reason` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_dep_reason_lang` DISABLE KEYS */;
INSERT INTO `sicol_v103`.`str_dep_reason_lang` (`id_dep_reason`,`id_lang`,`dep_reason`) VALUES 
 (1,1,'Open'),
 (1,2,'Aberto'),
 (2,1,'Closed'),
 (2,2,'Fechado'),
 (3,1,'Restrict'),
 (3,2,'Restrito');
/*!40000 ALTER TABLE `str_dep_reason_lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_deposit` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_deposit` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_gps_datum` DISABLE KEYS */;
INSERT INTO `sicol_v103`.`str_gps_datum` (`id_gps_datum`,`gps_datum`) VALUES 
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

/*!40000 ALTER TABLE `str_type` DISABLE KEYS */;
INSERT INTO `sicol_v103`.`str_type` (`id_type`) VALUES 
 (1),
 (2),
 (3);
/*!40000 ALTER TABLE `str_type` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_type_lang` DISABLE KEYS */;
INSERT INTO `sicol_v103`.`str_type_lang` (`id_type`,`id_lang`,`type`) VALUES 
 (1,1,'Reference'),
 (1,2,'Referência'),
 (2,1,'Type'),
 (2,2,'Tipo'),
 (3,1,'Genotype'),
 (3,2,'Genotipo');
/*!40000 ALTER TABLE `str_type_lang` ENABLE KEYS */;

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
(6,'ref','References Tab');
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
INSERT INTO areas_permissions(id_role,id_area,allow_delete,allow_create) VALUES (2,1,'y','y'),(2,2,'y','y'),(2,3,'y','y'),(2,4,'y','y'),(2,5,'y','y'),(2,6,'y','y');
/*!40000 ALTER TABLE `areas_permissions` ENABLE KEYS */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
