-- MySQL Administrator dump 1.4
-- 06.10.2006
--
-- ------------------------------------------------------
-- Server version	5.0.22-community-max-nt 

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

--
-- Create schema sicol_v0971
--

USE sicol_v0971;

/*!40000 ALTER TABLE `doc_qualifier` DISABLE KEYS */;
INSERT INTO `doc_qualifier` VALUES  (1,'Picture'),
 (2,'Seq16'),
 (3,'Document'),
 (4,'Method');
/*!40000 ALTER TABLE `doc_qualifier` ENABLE KEYS */;


/*!40000 ALTER TABLE `institution` DISABLE KEYS */;
INSERT INTO `institution` VALUES  (1,'328011678','CRIA.org','CRIA.org',NULL,NULL,NULL,NULL,NULL),
 (2,'30639070817','Sestari.org','Sestari.org',NULL,NULL,NULL,NULL,NULL),
 (3,'101010','UNICAMP','UNICAMP',NULL,NULL,NULL,NULL,NULL),
 (4,NULL,'Linear  - Campinas','Linear Softwares Matemáticos',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `institution` ENABLE KEYS */;


/*!40000 ALTER TABLE `lang` DISABLE KEYS */;
INSERT INTO `lang` VALUES  (1,'en','English','English'),
 (2,'ptbr','Português','Portuguese');
/*!40000 ALTER TABLE `lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `loc_country` DISABLE KEYS */;
INSERT INTO `loc_country` VALUES  (1,'BR'),
 (2,'JP');
/*!40000 ALTER TABLE `loc_country` ENABLE KEYS */;


/*!40000 ALTER TABLE `loc_country_lang` DISABLE KEYS */;
INSERT INTO `loc_country_lang` VALUES  (1,1,'Brazil'),
 (1,2,'Brasil'),
 (2,1,'Japan'),
 (2,2,'Japão');
/*!40000 ALTER TABLE `loc_country_lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `person` DISABLE KEYS */;
INSERT INTO `person` VALUES  (1,'Flávio Henrique Sestari',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
 (2,'Sidnei Sousa',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
 (3,'Luciano Laterza Lopes',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
 (4,'Linus Torvalds',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
 (5,'Guido van Rossum',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `person` ENABLE KEYS */;

/*!40000 ALTER TABLE `spe_subdiv` DISABLE KEYS */;
INSERT INTO `spe_subdiv` VALUES  (1,'var.'),
 (2,'subsp'),
 (3,'pv'),
 (4,'f.'),
 (5,'genomovar');
/*!40000 ALTER TABLE `spe_subdiv` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_clinical_form` DISABLE KEYS */;
INSERT INTO `str_clinical_form` VALUES  (1),
 (2),
 (3),
 (4),
 (5),
 (6),
 (7);
/*!40000 ALTER TABLE `str_clinical_form` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_clinical_form_lang` DISABLE KEYS */;
INSERT INTO `str_clinical_form_lang` VALUES  (1,1,'VL','Visceral Leishmaniasis'),
 (1,2,'LV','Leishmaniose Viceral'),
 (2,1,'CL','Cutaneous Leishmaniasis'),
 (2,2,'LC','Leishmaniose Cutânea'),
 (3,1,'DCL','Diffuse Cutaneous Leishmaniasis'),
 (3,2,'LCD','Leishmaniose Cutânea Difusa'),
 (4,1,'DL','Disseminated Leishmaniasis'),
 (4,2,'LD','Leishmaniose Disseminada'),
 (5,1,'ML','Mucosal Leishmaniasis'),
 (5,2,'LCM','Leishmaniose Cutâneo-Mucosa'),
 (6,1,'LRC','Leishmaniasis Recidiva Cuttis'),
 (6,2,'LR','Leishmaniose Recidiva'),
 (7,1,'PKDL','Post Kala-Azar Dermal Leishmaniasis'),
 (7,2,'PKDL','Leishmaniose Dérmica Pós-Calazar');
/*!40000 ALTER TABLE `str_clinical_form_lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_dep_reason` DISABLE KEYS */;
INSERT INTO `str_dep_reason` VALUES  (1),
 (2),
 (3),
 (4),
 (5);
/*!40000 ALTER TABLE `str_dep_reason` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_dep_reason_lang` DISABLE KEYS */;
INSERT INTO `str_dep_reason_lang` VALUES  (1,1,'Research'),
 (1,2,'Pesquisa'),
 (2,1,'Acquisition'),
 (2,2,'Aquisição'),
 (3,1,'Patent'),
 (3,2,'Patente'),
 (4,1,'Confident'),
 (4,2,'Confidencial'),
 (5,1,'Other'),
 (5,2,'Outro');
/*!40000 ALTER TABLE `str_dep_reason_lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_gps_datum` DISABLE KEYS */;
INSERT INTO `str_gps_datum` VALUES  (1,'WGS84'),
 (2,'SAD69');
/*!40000 ALTER TABLE `str_gps_datum` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_iso_method` DISABLE KEYS */;
INSERT INTO `str_iso_method` VALUES  (1,'Garden'),
 (2,'Incubus'),
 (3,'War');
/*!40000 ALTER TABLE `str_iso_method` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_type` DISABLE KEYS */;
INSERT INTO `str_type` VALUES  (1),
 (2),
 (3),
 (4);
/*!40000 ALTER TABLE `str_type` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_type_lang` DISABLE KEYS */;
INSERT INTO `str_type_lang` VALUES  (1,1,'Type'),
 (2,1,'Neo'),
 (3,1,'Genotype'),
 (4,1,'Reference'),
 (1,2,'Tipo'),
 (2,2,'Novo'),
 (3,2,'Genotipo'),
 (4,2,'Referência');
/*!40000 ALTER TABLE `str_type_lang` ENABLE KEYS */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;