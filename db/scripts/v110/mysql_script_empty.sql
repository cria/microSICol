DROP DATABASE IF EXISTS sicol_v110;
CREATE USER 'sicol'@'localhost' IDENTIFIED BY 'sicol';
CREATE DATABASE IF NOT EXISTS sicol_v110 CHARACTER SET utf8;
GRANT ALL PRIVILEGES ON sicol_v110 . * TO 'sicol'@'localhost'; flush privileges;
GRANT ALL PRIVILEGES ON sicol_v110_log . * TO 'sicol'@'localhost'; flush privileges;
USE sicol_v110;

-- MySQL dump 10.11
--
-- Host: localhost    Database: sicol_v110_clioc
-- ------------------------------------------------------
-- Server version	5.0.51a-24+lenny3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `areas_permissions`
--

DROP TABLE IF EXISTS `areas_permissions`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `areas_permissions` (
  `id_role` int(10) unsigned NOT NULL,
  `id_area` smallint(5) unsigned NOT NULL,
  `allow_delete` enum('y','n') NOT NULL default 'n',
  `allow_create` enum('y','n') NOT NULL default 'y',
  PRIMARY KEY  (`id_role`,`id_area`),
  KEY `FK_role` (`id_role`),
  KEY `id_area` (`id_area`),
  CONSTRAINT `areas_permissions_ibfk_1` FOREIGN KEY (`id_area`) REFERENCES `system_areas` (`id_area`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `areas_permissions_ibfk_2` FOREIGN KEY (`id_role`) REFERENCES `roles` (`id_role`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `contact_relations`
--

DROP TABLE IF EXISTS `contact_relations`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `contact_relations` (
  `id_person` int(10) unsigned NOT NULL,
  `id_institution` int(10) unsigned NOT NULL,
  `contact` enum('yes') default NULL,
  `department` varchar(80) default NULL,
  `email` varchar(100) default NULL,
  `last_update` datetime default NULL,
  PRIMARY KEY  (`id_person`,`id_institution`),
  KEY `FK_institution` (`id_institution`),
  KEY `FK_person` (`id_person`),
  CONSTRAINT `contact_relations_ibfk_1` FOREIGN KEY (`id_institution`) REFERENCES `institution` (`id_institution`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `contact_relations_ibfk_2` FOREIGN KEY (`id_person`) REFERENCES `person` (`id_person`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `container`
--

DROP TABLE IF EXISTS `container`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `container` (
  `id_container` int(10) unsigned NOT NULL auto_increment,
  `abbreviation` varchar(40) NOT NULL,
  `description` varchar(255) default NULL,
  PRIMARY KEY  (`id_container`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `container_hierarchy`
--

DROP TABLE IF EXISTS `container_hierarchy`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `container_hierarchy` (
  `id_container_hierarchy` int(10) unsigned NOT NULL auto_increment,
  `id_container` int(10) unsigned NOT NULL,
  `id_parent` int(10) unsigned default NULL,
  `abbreviation` varchar(40) NOT NULL,
  `description` varchar(255) default NULL,
  PRIMARY KEY  (`id_container_hierarchy`),
  KEY `FK_container` (`id_container`),
  KEY `FK_parent` (`id_parent`),
  CONSTRAINT `container_hierarchy_ibfk_1` FOREIGN KEY (`id_container`) REFERENCES `container` (`id_container`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `container_hierarchy_ibfk_2` FOREIGN KEY (`id_parent`) REFERENCES `container_hierarchy` (`id_container_hierarchy`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=241 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `container_preservation_method`
--

DROP TABLE IF EXISTS `container_preservation_method`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `container_preservation_method` (
  `id_container` int(10) unsigned NOT NULL,
  `id_preservation_method` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY  (`id_container`,`id_preservation_method`),
  KEY `FK_container` (`id_container`),
  KEY `FK_preservation_method` (`id_preservation_method`),
  CONSTRAINT `container_preservation_method_ibfk_1` FOREIGN KEY (`id_container`) REFERENCES `container` (`id_container`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `container_preservation_method_ibfk_2` FOREIGN KEY (`id_preservation_method`) REFERENCES `preservation_method` (`id_preservation_method`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `container_subcoll`
--

DROP TABLE IF EXISTS `container_subcoll`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `container_subcoll` (
  `id_container` int(10) unsigned NOT NULL,
  `id_subcoll` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY  (`id_container`,`id_subcoll`),
  KEY `FK_container` (`id_container`),
  CONSTRAINT `container_subcoll_ibfk_1` FOREIGN KEY (`id_container`) REFERENCES `container` (`id_container`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `distribution`
--

DROP TABLE IF EXISTS `distribution`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `distribution` (
  `id_distribution` int(10) unsigned NOT NULL auto_increment,
  `id_user` int(10) unsigned NOT NULL,
  `id_lot` int(10) unsigned NOT NULL,
  `id_strain` int(10) unsigned NOT NULL,
  `id_institution` int(10) unsigned NOT NULL,
  `date` date NOT NULL,
  `id_person` int(10) unsigned default NULL,
  `reason` text,
  `last_update` datetime default NULL,
  `not_identified` tinyint(1) unsigned NOT NULL default '0',
  PRIMARY KEY  (`id_distribution`),
  KEY `supply_FKIndex1` (`id_lot`),
  KEY `id_strain` (`id_strain`,`id_lot`),
  KEY `id_institution` (`id_institution`),
  KEY `id_user` (`id_user`),
  KEY `id_person` (`id_person`),
  CONSTRAINT `distribution_ibfk_1` FOREIGN KEY (`id_lot`) REFERENCES `lot` (`id_lot`),
  CONSTRAINT `distribution_ibfk_2` FOREIGN KEY (`id_strain`) REFERENCES `strain` (`id_strain`),
  CONSTRAINT `distribution_ibfk_4` FOREIGN KEY (`id_institution`) REFERENCES `institution` (`id_institution`),
  CONSTRAINT `distribution_ibfk_5` FOREIGN KEY (`id_user`) REFERENCES `person` (`id_person`),
  CONSTRAINT `distribution_ibfk_6` FOREIGN KEY (`id_person`) REFERENCES `person` (`id_person`),
  CONSTRAINT `distribution_ibfk_7` FOREIGN KEY (`id_strain`, `id_lot`) REFERENCES `lot_strain` (`id_strain`, `id_lot`)
) ENGINE=InnoDB AUTO_INCREMENT=505 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `distribution_origin_location`
--

DROP TABLE IF EXISTS `distribution_origin_location`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `distribution_origin_location` (
  `id_distribution_location` int(10) unsigned NOT NULL auto_increment,
  `id_distribution` int(10) unsigned NOT NULL,
  `id_origin_lot` int(10) unsigned NOT NULL,
  `id_origin_container_hierarchy` int(10) unsigned NOT NULL,
  `origin_row` int(10) unsigned NOT NULL,
  `origin_col` int(10) unsigned NOT NULL,
  `quantity` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id_distribution_location`),
  KEY `FK_id_distribution` (`id_distribution`),
  KEY `FK_id_origin_lot` (`id_origin_lot`),
  KEY `FK_id_origin_container_hierarchy` (`id_origin_container_hierarchy`),
  CONSTRAINT `distribution_origin_location_ibfk_1` FOREIGN KEY (`id_distribution`) REFERENCES `distribution` (`id_distribution`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `distribution_origin_location_ibfk_2` FOREIGN KEY (`id_origin_lot`) REFERENCES `lot` (`id_lot`),
  CONSTRAINT `distribution_origin_location_ibfk_3` FOREIGN KEY (`id_origin_container_hierarchy`) REFERENCES `container_hierarchy` (`id_container_hierarchy`)
) ENGINE=InnoDB AUTO_INCREMENT=532 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `division`
--

DROP TABLE IF EXISTS `division`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `division` (
  `id_division` smallint(5) unsigned NOT NULL auto_increment,
  `id_subcoll` tinyint(3) unsigned NOT NULL,
  `division` varchar(50) NOT NULL,
  `pattern` varchar(50) default NULL,
  PRIMARY KEY  (`id_division`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `doc`
--

DROP TABLE IF EXISTS `doc`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `doc` (
  `id_doc` int(10) unsigned NOT NULL auto_increment,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_subcoll` tinyint(3) unsigned NOT NULL,
  `code` varchar(20) NOT NULL,
  `id_qualifier` tinyint(3) unsigned default NULL,
  `id_test_group` tinyint(3) unsigned default NULL,
  `last_update` datetime default NULL,
  `go_catalog` tinyint(1) NOT NULL default '0' COMMENT '0 = false, 1 = true',
  PRIMARY KEY  (`id_doc`,`id_coll`),
  UNIQUE KEY `code_coll` (`code`,`id_coll`),
  KEY `FK_qualifier` (`id_qualifier`),
  KEY `FK_test_group` (`id_test_group`),
  CONSTRAINT `doc_ibfk_1` FOREIGN KEY (`id_qualifier`) REFERENCES `doc_qualifier` (`id_qualifier`),
  CONSTRAINT `doc_ibfk_2` FOREIGN KEY (`id_test_group`) REFERENCES `test_group` (`id_test_group`)
) ENGINE=InnoDB AUTO_INCREMENT=323 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `doc_description`
--

DROP TABLE IF EXISTS `doc_description`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `doc_description` (
  `id_doc` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY  (`id_doc`,`id_coll`,`id_lang`),
  KEY `FK_doc_coll` (`id_doc`,`id_coll`),
  KEY `FK_lang` (`id_lang`),
  CONSTRAINT `doc_description_ibfk_1` FOREIGN KEY (`id_doc`, `id_coll`) REFERENCES `doc` (`id_doc`, `id_coll`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `doc_description_ibfk_2` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `doc_file`
--

DROP TABLE IF EXISTS `doc_file`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `doc_file` (
  `id_doc` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `file_name` varchar(100) NOT NULL,
  PRIMARY KEY  (`id_doc`,`id_coll`,`id_lang`),
  KEY `FK_doc_coll` (`id_doc`,`id_coll`),
  KEY `FK_lang` (`id_lang`),
  CONSTRAINT `doc_file_ibfk_1` FOREIGN KEY (`id_doc`, `id_coll`) REFERENCES `doc` (`id_doc`, `id_coll`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `doc_file_ibfk_2` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `doc_qualifier`
--

DROP TABLE IF EXISTS `doc_qualifier`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `doc_qualifier` (
  `id_qualifier` tinyint(3) unsigned NOT NULL auto_increment,
  `qualifier` varchar(20) NOT NULL,
  PRIMARY KEY  (`id_qualifier`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `doc_report`
--

DROP TABLE IF EXISTS `doc_report`;
/*!50001 DROP VIEW IF EXISTS `doc_report`*/;
/*!50001 CREATE TABLE `doc_report` (
  `id_doc` int(10) unsigned,
  `id_coll` tinyint(3) unsigned,
  `id_subcoll` tinyint(3) unsigned,
  `code` varchar(20),
  `qualifier` varchar(20),
  `title` varchar(100),
  `description` text,
  `file_name` varchar(100),
  `category` varchar(100),
  `go_catalog` tinyint(1)
) */;

--
-- Table structure for table `doc_title`
--

DROP TABLE IF EXISTS `doc_title`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `doc_title` (
  `id_doc` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `title` varchar(100) NOT NULL,
  PRIMARY KEY  (`id_doc`,`id_coll`,`id_lang`),
  KEY `FK_lang` (`id_lang`),
  KEY `FK_doc_coll` (`id_doc`,`id_coll`),
  CONSTRAINT `doc_title_ibfk_1` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `doc_title_ibfk_2` FOREIGN KEY (`id_doc`, `id_coll`) REFERENCES `doc` (`id_doc`, `id_coll`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `hierarchy_def`
--

DROP TABLE IF EXISTS `hierarchy_def`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `hierarchy_def` (
  `id_hierarchy` int(10) unsigned NOT NULL auto_increment,
  `seq` int(11) NOT NULL,
  `hi_tax` tinyint(1) NOT NULL default '1',
  `has_author` tinyint(1) NOT NULL default '1',
  `use_author` tinyint(1) NOT NULL default '0',
  `in_sciname` tinyint(1) NOT NULL default '0',
  `required` tinyint(1) NOT NULL default '0',
  `important` tinyint(1) NOT NULL default '0',
  `string_format` enum('none','italic','bold','italic-bold') NOT NULL default 'none',
  `string_case` enum('none','lower','upper','ucfirst') NOT NULL default 'none',
  `prefix` varchar(200) default NULL,
  `suffix` varchar(200) default NULL,
  PRIMARY KEY  (`id_hierarchy`),
  UNIQUE KEY `seq_key` (`seq`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `hierarchy_group`
--

DROP TABLE IF EXISTS `hierarchy_group`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `hierarchy_group` (
  `id_hierarchy` int(10) unsigned NOT NULL,
  `id_taxon_group` tinyint(3) unsigned NOT NULL,
  `id_subcoll` tinyint(3) unsigned NOT NULL,
  `hi_tax` tinyint(1) default NULL,
  `has_author` tinyint(1) default NULL,
  `use_author` tinyint(1) default NULL,
  `in_sciname` tinyint(1) default NULL,
  `required` tinyint(1) default NULL,
  `important` tinyint(1) default NULL,
  `string_format` enum('none','italic','bold','italic-bold') default NULL,
  `string_case` enum('none','lower','upper','ucfirst') default NULL,
  `prefix` varchar(200) default NULL,
  `suffix` varchar(200) default NULL,
  `default_value` varchar(255) default NULL,
  PRIMARY KEY  (`id_hierarchy`,`id_taxon_group`,`id_subcoll`),
  KEY `FK_hierarchy` (`id_hierarchy`),
  CONSTRAINT `hierarchy_group_ibfk_1` FOREIGN KEY (`id_hierarchy`) REFERENCES `hierarchy_def` (`id_hierarchy`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `hierarchy_lang`
--

DROP TABLE IF EXISTS `hierarchy_lang`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `hierarchy_lang` (
  `id_hierarchy` int(10) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `rank` varchar(255) NOT NULL,
  PRIMARY KEY  (`id_hierarchy`,`id_lang`),
  KEY `FK_hierarchy` (`id_hierarchy`),
  KEY `FK_lang` (`id_lang`),
  CONSTRAINT `hierarchy_lang_ibfk_1` FOREIGN KEY (`id_hierarchy`) REFERENCES `hierarchy_def` (`id_hierarchy`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `hierarchy_lang_ibfk_2` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `inst_comments`
--

DROP TABLE IF EXISTS `inst_comments`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `inst_comments` (
  `id_institution` int(10) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `comments` text NOT NULL,
  PRIMARY KEY  (`id_institution`,`id_lang`),
  KEY `FK_lang` (`id_lang`),
  KEY `FK_institution` (`id_institution`),
  CONSTRAINT `inst_comments_ibfk_1` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `inst_comments_ibfk_2` FOREIGN KEY (`id_institution`) REFERENCES `institution` (`id_institution`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `institution`
--

DROP TABLE IF EXISTS `institution`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `institution` (
  `id_institution` int(10) unsigned NOT NULL auto_increment,
  `code1` varchar(20) default NULL,
  `code2` varchar(20) default NULL,
  `code3` varchar(20) default NULL,
  `complement` varchar(100) default NULL,
  `nickname` varchar(50) default NULL,
  `name` varchar(80) NOT NULL,
  `address` text,
  `phone` text,
  `email` varchar(100) default NULL,
  `website` varchar(100) default NULL,
  `last_update` datetime default NULL,
  `go_catalog` tinyint(1) NOT NULL default '0' COMMENT '0 = false, 1 = true',
  PRIMARY KEY  (`id_institution`),
  UNIQUE KEY `institution_key` (`complement`,`nickname`)
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `institution_report`
--

DROP TABLE IF EXISTS `institution_report`;
/*!50001 DROP VIEW IF EXISTS `institution_report`*/;
/*!50001 CREATE TABLE `institution_report` (
  `id_institution` int(10) unsigned,
  `code1` varchar(20),
  `code2` varchar(20),
  `code3` varchar(20),
  `complement` varchar(100),
  `nickname` varchar(50),
  `name` varchar(80),
  `address` text,
  `phone` text,
  `email` varchar(100),
  `website` varchar(100),
  `go_catalog` tinyint(1),
  `comments` text
) */;

--
-- Table structure for table `lang`
--

DROP TABLE IF EXISTS `lang`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `lang` (
  `id_lang` tinyint(3) unsigned NOT NULL auto_increment,
  `code` char(4) NOT NULL,
  `lang` varchar(30) NOT NULL,
  `lang_en` varchar(30) NOT NULL,
  PRIMARY KEY  (`id_lang`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `loc_city`
--

DROP TABLE IF EXISTS `loc_city`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `loc_city` (
  `id_city` int(10) unsigned NOT NULL auto_increment,
  `id_state` int(10) unsigned NOT NULL,
  `id_country` int(10) unsigned NOT NULL,
  `city` varchar(255) NOT NULL,
  PRIMARY KEY  (`id_city`,`id_state`,`id_country`),
  KEY `FK_country_state` (`id_state`,`id_country`),
  CONSTRAINT `loc_city_ibfk_1` FOREIGN KEY (`id_state`, `id_country`) REFERENCES `loc_state` (`id_state`, `id_country`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5721 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `loc_country`
--

DROP TABLE IF EXISTS `loc_country`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `loc_country` (
  `id_country` int(10) unsigned NOT NULL auto_increment,
  `code` char(2) NOT NULL,
  PRIMARY KEY  (`id_country`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=248 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `loc_country_lang`
--

DROP TABLE IF EXISTS `loc_country_lang`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `loc_country_lang` (
  `id_country` int(10) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `country` varchar(255) NOT NULL,
  PRIMARY KEY  (`id_country`,`id_lang`),
  KEY `FK_loc_country` (`id_country`),
  KEY `FK_lang` (`id_lang`),
  CONSTRAINT `loc_country_lang_ibfk_1` FOREIGN KEY (`id_country`) REFERENCES `loc_country` (`id_country`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `loc_country_lang_ibfk_2` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `loc_state`
--

DROP TABLE IF EXISTS `loc_state`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `loc_state` (
  `id_state` int(10) unsigned NOT NULL auto_increment,
  `id_country` int(10) unsigned NOT NULL,
  `code` char(4) NOT NULL,
  `state` varchar(255) NOT NULL,
  PRIMARY KEY  (`id_state`,`id_country`),
  UNIQUE KEY `code` (`id_state`,`id_country`,`code`),
  KEY `FK_country` (`id_country`),
  CONSTRAINT `loc_state_ibfk_1` FOREIGN KEY (`id_country`) REFERENCES `loc_country` (`id_country`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1674 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `location` (
  `id_location` int(10) unsigned NOT NULL auto_increment,
  `id_container_hierarchy` int(10) unsigned NOT NULL,
  `rows` int(10) unsigned NOT NULL,
  `cols` int(10) unsigned NOT NULL,
  `ini_row` char(1) NOT NULL,
  `ini_col` char(1) NOT NULL,
  `pattern` varchar(40) NOT NULL,
  PRIMARY KEY  (`id_location`),
  KEY `FK_container_hierarchy` (`id_container_hierarchy`),
  CONSTRAINT `location_ibfk_1` FOREIGN KEY (`id_container_hierarchy`) REFERENCES `container_hierarchy` (`id_container_hierarchy`)
) ENGINE=InnoDB AUTO_INCREMENT=213 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `lot`
--

DROP TABLE IF EXISTS `lot`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `lot` (
  `id_lot` int(10) unsigned NOT NULL auto_increment,
  `id_subcoll` tinyint(3) unsigned NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY  (`id_lot`)
) ENGINE=InnoDB AUTO_INCREMENT=792 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `lot_strain`
--

DROP TABLE IF EXISTS `lot_strain`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `lot_strain` (
  `id_lot` int(10) unsigned NOT NULL,
  `id_strain` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id_lot`,`id_strain`),
  KEY `id_strain` (`id_strain`),
  CONSTRAINT `lot_strain_ibfk_1` FOREIGN KEY (`id_lot`) REFERENCES `lot` (`id_lot`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `lot_strain_ibfk_2` FOREIGN KEY (`id_strain`) REFERENCES `strain` (`id_strain`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `lot_strain_available_locations`
--

DROP TABLE IF EXISTS `lot_strain_available_locations`;
/*!50001 DROP VIEW IF EXISTS `lot_strain_available_locations`*/;
/*!50001 CREATE TABLE `lot_strain_available_locations` (
  `id_lot` int(10) unsigned,
  `id_strain` int(10) unsigned,
  `id_container_hierarchy` int(10) unsigned,
  `row` int(10) unsigned,
  `col` int(10) unsigned,
  `available_qt` bigint(24) unsigned
) */;

--
-- Table structure for table `lot_strain_location`
--

DROP TABLE IF EXISTS `lot_strain_location`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `lot_strain_location` (
  `id_lot_strain_location` int(10) unsigned NOT NULL auto_increment,
  `id_lot` int(10) unsigned NOT NULL,
  `id_strain` int(10) unsigned NOT NULL,
  `id_container_hierarchy` int(10) unsigned NOT NULL,
  `row` int(10) unsigned NOT NULL,
  `col` int(10) unsigned NOT NULL,
  `quantity` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id_lot_strain_location`),
  KEY `FK_lot_strain` (`id_lot`,`id_strain`),
  KEY `FK_container_hierarchy` (`id_container_hierarchy`),
  CONSTRAINT `lot_strain_location_ibfk_1` FOREIGN KEY (`id_lot`, `id_strain`) REFERENCES `lot_strain` (`id_lot`, `id_strain`),
  CONSTRAINT `lot_strain_location_ibfk_2` FOREIGN KEY (`id_container_hierarchy`) REFERENCES `container_hierarchy` (`id_container_hierarchy`)
) ENGINE=InnoDB AUTO_INCREMENT=26628 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

/*!50003 SET @SAVE_SQL_MODE=@@SQL_MODE*/;

DELIMITER ;;
/*!50003 SET SESSION SQL_MODE="" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`localhost` */ /*!50003 TRIGGER `check_stock` BEFORE INSERT ON `lot_strain_location` FOR EACH ROW BEGIN
    DECLARE check_count int;
    select COUNT(*) INTO check_count from
    (
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
        not(`lsl`.`id_lot_strain_location` in (
      select 
        `stock_movement_location`.`id_lot_strain_location_from` AS `id_lot_strain_location_from` 
      from 
        `stock_movement_location`))
    ) lslm
    WHERE ((((`lslm`.`quantity` - ifnull(`lslm`.`used_qt_pres`,0)) - ifnull(`lslm`.`used_qt_dist`,0)) - ifnull(`lslm`.`used_qt_qual`,0)) > 0) 
        AND lslm.id_container_hierarchy = NEW.id_container_hierarchy AND lslm.row = NEW.row AND lslm.col = NEW.col;
    IF (check_count > 0) THEN
        SET NEW.id_container_hierarchy = NULL;
    END IF;
END */;;

DELIMITER ;
/*!50003 SET SESSION SQL_MODE=@SAVE_SQL_MODE*/;

--
-- Temporary table structure for view `lot_strain_stock`
--

DROP TABLE IF EXISTS `lot_strain_stock`;
/*!50001 DROP VIEW IF EXISTS `lot_strain_stock`*/;
/*!50001 CREATE TABLE `lot_strain_stock` (
  `id_lot` int(10) unsigned,
  `id_strain` int(10) unsigned,
  `stock` bigint(46) unsigned
) */;

--
-- Temporary table structure for view `lot_strain_stock_data`
--

DROP TABLE IF EXISTS `lot_strain_stock_data`;
/*!50001 DROP VIEW IF EXISTS `lot_strain_stock_data`*/;
/*!50001 CREATE TABLE `lot_strain_stock_data` (
  `id_lot` int(10) unsigned,
  `id_strain` int(10) unsigned,
  `id_container_hierarchy` int(10) unsigned,
  `row` int(10) unsigned,
  `col` int(10) unsigned,
  `quantity` int(10) unsigned,
  `used_qt_pres` bigint(34) unsigned,
  `used_qt_dist` bigint(34) unsigned,
  `used_qt_qual` bigint(34) unsigned
) */;

--
-- Table structure for table `per_comments`
--

DROP TABLE IF EXISTS `per_comments`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `per_comments` (
  `id_person` int(10) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `comments` text NOT NULL,
  PRIMARY KEY  (`id_person`,`id_lang`),
  KEY `FK_person` (`id_person`),
  KEY `FK_lang` (`id_lang`),
  CONSTRAINT `per_comments_ibfk_1` FOREIGN KEY (`id_person`) REFERENCES `person` (`id_person`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `per_comments_ibfk_2` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `person`
--

DROP TABLE IF EXISTS `person`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `person` (
  `id_person` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(50) NOT NULL,
  `nickname` varchar(50) default NULL,
  `address` text,
  `phone` text,
  `email` varchar(100) default NULL,
  `last_update` datetime default NULL,
  `go_catalog` tinyint(1) NOT NULL default '0' COMMENT '0 = false, 1 = true',
  PRIMARY KEY  (`id_person`),
  UNIQUE KEY `person_key` (`name`,`nickname`)
) ENGINE=InnoDB AUTO_INCREMENT=153 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `person_report`
--

DROP TABLE IF EXISTS `person_report`;
/*!50001 DROP VIEW IF EXISTS `person_report`*/;
/*!50001 CREATE TABLE `person_report` (
  `id_person` int(10) unsigned,
  `name` varchar(50),
  `nickname` varchar(50),
  `address` text,
  `phone` text,
  `email` varchar(100),
  `go_catalog` tinyint(1),
  `comments` text
) */;

--
-- Table structure for table `preservation`
--

DROP TABLE IF EXISTS `preservation`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `preservation` (
  `id_preservation` int(10) unsigned NOT NULL auto_increment,
  `id_user` int(10) unsigned NOT NULL,
  `id_lot` int(10) unsigned NOT NULL,
  `id_preservation_method` tinyint(3) unsigned NOT NULL,
  `date` date NOT NULL,
  `info` text,
  `last_update` datetime default NULL,
  PRIMARY KEY  (`id_preservation`),
  KEY `id_preservation_method` (`id_preservation_method`),
  KEY `FK_user` (`id_user`),
  KEY `FK_id_lot` (`id_lot`),
  CONSTRAINT `preservation_ibfk_1` FOREIGN KEY (`id_preservation_method`) REFERENCES `preservation_method` (`id_preservation_method`),
  CONSTRAINT `preservation_ibfk_2` FOREIGN KEY (`id_user`) REFERENCES `person` (`id_person`),
  CONSTRAINT `preservation_ibfk_3` FOREIGN KEY (`id_lot`) REFERENCES `lot` (`id_lot`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=792 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `preservation_method`
--

DROP TABLE IF EXISTS `preservation_method`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `preservation_method` (
  `id_preservation_method` tinyint(3) unsigned NOT NULL auto_increment,
  PRIMARY KEY  (`id_preservation_method`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `preservation_method_lang`
--

DROP TABLE IF EXISTS `preservation_method_lang`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `preservation_method_lang` (
  `id_preservation_method` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `method` varchar(100) NOT NULL,
  `unit_measure` varchar(100) NOT NULL,
  PRIMARY KEY  (`id_preservation_method`,`id_lang`),
  KEY `id_lang` (`id_lang`),
  CONSTRAINT `preservation_method_lang_ibfk_1` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `preservation_method_lang_ibfk_2` FOREIGN KEY (`id_preservation_method`) REFERENCES `preservation_method` (`id_preservation_method`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `preservation_method_subcoll`
--

DROP TABLE IF EXISTS `preservation_method_subcoll`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `preservation_method_subcoll` (
  `id_preservation_method` tinyint(3) unsigned NOT NULL,
  `id_subcoll` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY  (`id_preservation_method`,`id_subcoll`),
  CONSTRAINT `preservation_method_subcoll_ibfk_1` FOREIGN KEY (`id_preservation_method`) REFERENCES `preservation_method` (`id_preservation_method`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `preservation_strain`
--

DROP TABLE IF EXISTS `preservation_strain`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `preservation_strain` (
  `id_preserv_str` int(10) unsigned NOT NULL auto_increment,
  `id_preservation` int(10) unsigned NOT NULL,
  `id_strain` int(10) unsigned NOT NULL,
  `origin_type` enum('original','lot') NOT NULL,
  `origin` varchar(100) default NULL COMMENT 'used if origin_type = original',
  `id_lot` int(10) unsigned default NULL COMMENT 'used if origin_type = lot',
  `id_origin_container_hierarchy` int(10) unsigned default NULL COMMENT 'used if origin_type = lot',
  `origin_row` int(10) unsigned default NULL COMMENT 'used if origin_type = lot',
  `origin_col` int(10) unsigned default NULL COMMENT 'used if origin_type = lot',
  `quantity` int(10) unsigned default NULL COMMENT 'used if origin_type = lot',
  `stock_position` text NOT NULL,
  `stock_minimum` int(10) unsigned NOT NULL,
  `id_doc` int(10) unsigned default NULL COMMENT 'culture medium is a document qualifier',
  `temperature` varchar(100) default NULL,
  `incub_time` varchar(100) default NULL,
  `cryoprotector` varchar(100) default NULL,
  `preservation_type` enum('block','spore','none') default NULL,
  `purity` enum('y','n') default NULL,
  `counting` varchar(100) default NULL,
  `counting_not_apply` enum('y','n') NOT NULL,
  `macro_charac` text,
  `micro_charac` text,
  `result` text,
  `obs` text,
  `not_identified` tinyint(1) unsigned NOT NULL default '0',
  PRIMARY KEY  (`id_preserv_str`),
  KEY `id_strain` (`id_strain`),
  KEY `id_preservation` (`id_preservation`),
  KEY `IX_id_lot` (`id_lot`),
  KEY `FK_id_strain` (`id_strain`),
  KEY `FK_id_preservation` (`id_preservation`),
  KEY `FK_id_origin_container_hierarchy` (`id_origin_container_hierarchy`),
  KEY `FK_id_doc` (`id_doc`),
  CONSTRAINT `preservation_strain_ibfk_2` FOREIGN KEY (`id_preservation`) REFERENCES `preservation` (`id_preservation`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `preservation_strain_ibfk_3` FOREIGN KEY (`id_strain`) REFERENCES `strain` (`id_strain`),
  CONSTRAINT `preservation_strain_ibfk_4` FOREIGN KEY (`id_origin_container_hierarchy`) REFERENCES `container_hierarchy` (`id_container_hierarchy`),
  CONSTRAINT `preservation_strain_ibfk_5` FOREIGN KEY (`id_doc`) REFERENCES `doc` (`id_doc`)
) ENGINE=InnoDB AUTO_INCREMENT=14018 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `preservation_strain_locations`
--

DROP TABLE IF EXISTS `preservation_strain_locations`;
/*!50001 DROP VIEW IF EXISTS `preservation_strain_locations`*/;
/*!50001 CREATE TABLE `preservation_strain_locations` (
  `id_preservation` int(10) unsigned,
  `id_lot` int(10) unsigned,
  `id_strain` int(10) unsigned,
  `origin_type` enum('original','lot'),
  `id_container_hierarchy` int(10) unsigned,
  `row` int(10) unsigned,
  `col` int(10) unsigned,
  `id_origin_lot` int(10) unsigned,
  `id_origin_container_hierarchy` int(10) unsigned,
  `origin_row` int(10) unsigned,
  `origin_col` int(10) unsigned,
  `quantity` int(10) unsigned
) */;

--
-- Table structure for table `ref`
--

DROP TABLE IF EXISTS `ref`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `ref` (
  `id_ref` int(10) unsigned NOT NULL auto_increment,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_subcoll` tinyint(3) unsigned NOT NULL,
  `title` text NOT NULL,
  `author` varchar(100) default NULL,
  `year` varchar(100) default NULL,
  `url` text,
  `last_update` datetime default NULL,
  `go_catalog` tinyint(1) NOT NULL default '0' COMMENT '0 = false, 1 = true',
  PRIMARY KEY  (`id_ref`,`id_coll`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `ref_comments`
--

DROP TABLE IF EXISTS `ref_comments`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `ref_comments` (
  `id_lang` tinyint(3) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_ref` int(10) unsigned NOT NULL,
  `comments` text NOT NULL,
  PRIMARY KEY  (`id_lang`,`id_coll`,`id_ref`),
  KEY `FK_lang` (`id_lang`),
  KEY `FK_ref_coll` (`id_ref`,`id_coll`),
  CONSTRAINT `ref_comments_ibfk_1` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ref_comments_ibfk_2` FOREIGN KEY (`id_ref`, `id_coll`) REFERENCES `ref` (`id_ref`, `id_coll`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `ref_report`
--

DROP TABLE IF EXISTS `ref_report`;
/*!50001 DROP VIEW IF EXISTS `ref_report`*/;
/*!50001 CREATE TABLE `ref_report` (
  `id_ref` int(10) unsigned,
  `id_coll` tinyint(3) unsigned,
  `id_subcoll` tinyint(3) unsigned,
  `title` text,
  `author` varchar(100),
  `year` varchar(100),
  `url` text,
  `comments` text,
  `go_catalog` tinyint(1)
) */;

--
-- Table structure for table `report_types`
--

DROP TABLE IF EXISTS `report_types`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `report_types` (
  `id_report_type` tinyint(3) unsigned NOT NULL,
  `code` varchar(100) NOT NULL,
  `fields_definition` text NOT NULL,
  PRIMARY KEY  (`id_report_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `report_types_lang`
--

DROP TABLE IF EXISTS `report_types_lang`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `report_types_lang` (
  `id_report_type` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `type` varchar(200) NOT NULL,
  PRIMARY KEY  (`id_report_type`,`id_lang`),
  KEY `FK_report_type` (`id_report_type`),
  KEY `FK_id_lang` (`id_lang`),
  CONSTRAINT `report_types_lang_ibfk_1` FOREIGN KEY (`id_report_type`) REFERENCES `report_types` (`id_report_type`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `report_types_lang_ibfk_2` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `reports`
--

DROP TABLE IF EXISTS `reports`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `reports` (
  `id_report` int(10) unsigned NOT NULL auto_increment,
  `id_subcoll` tinyint(3) unsigned NOT NULL,
  `id_report_type` tinyint(3) unsigned NOT NULL,
  `description` varchar(255) NOT NULL,
  `definition` text NOT NULL,
  PRIMARY KEY  (`id_report`),
  KEY `FK_report_type` (`id_report_type`),
  CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`id_report_type`) REFERENCES `report_types` (`id_report_type`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `roles` (
  `id_role` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(100) NOT NULL,
  `description` text,
  `type` enum('user','group','level','all') NOT NULL default 'user',
  PRIMARY KEY  (`id_role`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `roles_permissions`
--

DROP TABLE IF EXISTS `roles_permissions`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `roles_permissions` (
  `id_item` int(10) unsigned NOT NULL,
  `id_role` int(10) unsigned NOT NULL,
  `id_area` smallint(5) unsigned NOT NULL,
  `permission` enum('r','w') NOT NULL default 'w',
  PRIMARY KEY  (`id_item`,`id_role`,`id_area`),
  KEY `FK_role` (`id_role`),
  KEY `id_area` (`id_area`),
  CONSTRAINT `roles_permissions_ibfk_1` FOREIGN KEY (`id_role`) REFERENCES `roles` (`id_role`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `roles_permissions_ibfk_2` FOREIGN KEY (`id_area`) REFERENCES `system_areas` (`id_area`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `roles_users`
--

DROP TABLE IF EXISTS `roles_users`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `roles_users` (
  `id_user` int(10) unsigned NOT NULL,
  `id_role` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id_user`,`id_role`),
  KEY `FK_role` (`id_role`),
  CONSTRAINT `roles_users_ibfk_1` FOREIGN KEY (`id_role`) REFERENCES `roles` (`id_role`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `scientific_names`
--

DROP TABLE IF EXISTS `scientific_names`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `scientific_names` (
  `id_sciname` int(10) unsigned NOT NULL auto_increment,
  `hi_tax` text,
  `sciname` text NOT NULL,
  `sciname_no_auth` text NOT NULL,
  PRIMARY KEY  (`id_sciname`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `scientific_names_hierarchy`
--

DROP TABLE IF EXISTS `scientific_names_hierarchy`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `scientific_names_hierarchy` (
  `id_sciname` int(10) unsigned NOT NULL,
  `id_hierarchy` int(10) unsigned NOT NULL,
  `value` varchar(255) NOT NULL,
  `author` varchar(255) default NULL,
  PRIMARY KEY  (`id_sciname`,`id_hierarchy`),
  KEY `FK_sciname` (`id_sciname`),
  KEY `FK_hierarchy` (`id_hierarchy`),
  CONSTRAINT `scientific_names_hierarchy_ibfk_1` FOREIGN KEY (`id_sciname`) REFERENCES `scientific_names` (`id_sciname`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `scientific_names_hierarchy_ibfk_2` FOREIGN KEY (`id_hierarchy`) REFERENCES `hierarchy_def` (`id_hierarchy`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `sidneiView`
--

DROP TABLE IF EXISTS `sidneiView`;
/*!50001 DROP VIEW IF EXISTS `sidneiView`*/;
/*!50001 CREATE TABLE `sidneiView` (
  `record_uid` int(10) unsigned,
  `datelastmodified` datetime,
  `institutioncode` varchar(7),
  `collectioncode` varchar(7),
  `subcollectioncode` tinyint(3) unsigned,
  `catalognumber` varchar(30),
  `scientificname` longtext,
  `basisofrecord` varchar(1),
  `kingdom` varchar(100),
  `phylum` varchar(255),
  `class` varchar(255),
  `order` varchar(255),
  `family` varchar(255),
  `genus` varchar(255),
  `species` varchar(255),
  `subspecies` varchar(255),
  `scientificnameauthor` varchar(255),
  `identifiedby` varchar(50),
  `yearidentified` varchar(4),
  `monthidentified` varchar(2),
  `dayidentified` varchar(2),
  `typestatus` varchar(15),
  `collectornumber` binary(0),
  `fieldnumber` binary(0),
  `collector` varchar(50),
  `yearcollected` varchar(4),
  `monthcollected` varchar(2),
  `daycollected` varchar(2),
  `julianday` binary(0),
  `timeOfday` binary(0),
  `continentocean` binary(0),
  `country` varchar(255),
  `stateprovince` varchar(255),
  `county` varchar(255),
  `locality` longtext,
  `longitude` decimal(11,8),
  `latitude` decimal(11,8),
  `coordinateprecision` int(5) unsigned,
  `boundingbox` binary(0),
  `minimumelevation` binary(0),
  `maximumelevation` binary(0),
  `minimumdepth` binary(0),
  `maximumdepth` binary(0),
  `sex` binary(0),
  `preparationtype` binary(0),
  `individualcount` binary(0),
  `previouscatalognumber` binary(0),
  `relationshiptype` text,
  `relatedcatalogitem` binary(0),
  `notes` longtext,
  `historyofdeposit` longtext,
  `depositor` varchar(50),
  `yeardeposited` varchar(4),
  `monthdeposited` varchar(2),
  `daydeposited` varchar(2),
  `isolatedfrom` text,
  `isolator` varchar(50),
  `isolationmethod` text,
  `conditionsforgrowth` varchar(111),
  `geneticallymodified` tinyint(1),
  `genotype` text,
  `mutant` binary(0),
  `race` binary(0),
  `alternatestate` longtext,
  `strainproperties` text,
  `strainapplications` text,
  `formofsupply` binary(0),
  `restrictions` text,
  `biologicalrisks` text,
  `pathogenicity` text
) */;

--
-- Table structure for table `spe_ambient_risk`
--

DROP TABLE IF EXISTS `spe_ambient_risk`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `spe_ambient_risk` (
  `id_species` int(10) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `ambient_risk` text NOT NULL,
  PRIMARY KEY  (`id_species`,`id_lang`),
  KEY `FK_species` (`id_species`),
  KEY `FK_lang` (`id_lang`),
  CONSTRAINT `spe_ambient_risk_ibfk_1` FOREIGN KEY (`id_species`) REFERENCES `species` (`id_species`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `spe_ambient_risk_ibfk_2` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `spe_comments`
--

DROP TABLE IF EXISTS `spe_comments`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `spe_comments` (
  `id_species` int(10) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `comments` text NOT NULL,
  PRIMARY KEY  (`id_species`,`id_lang`),
  KEY `FK_species` (`id_species`),
  KEY `FK_lang` (`id_lang`),
  CONSTRAINT `spe_comments_ibfk_1` FOREIGN KEY (`id_species`) REFERENCES `species` (`id_species`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `spe_comments_ibfk_2` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `spe_name_qualifier`
--

DROP TABLE IF EXISTS `spe_name_qualifier`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `spe_name_qualifier` (
  `id_name_qualifier` tinyint(3) unsigned NOT NULL auto_increment,
  PRIMARY KEY  (`id_name_qualifier`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `spe_name_qualifier_lang`
--

DROP TABLE IF EXISTS `spe_name_qualifier_lang`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `spe_name_qualifier_lang` (
  `id_name_qualifier` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `name_qualifier` varchar(50) NOT NULL,
  PRIMARY KEY  (`id_name_qualifier`,`id_lang`),
  KEY `FK_lang` (`id_lang`),
  KEY `FK_name_qualifier` (`id_name_qualifier`),
  CONSTRAINT `spe_name_qualifier_lang_ibfk_1` FOREIGN KEY (`id_name_qualifier`) REFERENCES `spe_name_qualifier` (`id_name_qualifier`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `spe_name_qualifier_lang_ibfk_2` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `species`
--

DROP TABLE IF EXISTS `species`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `species` (
  `id_species` int(10) unsigned NOT NULL auto_increment,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_subcoll` tinyint(3) unsigned NOT NULL,
  `id_taxon_group` tinyint(3) unsigned NOT NULL,
  `id_sciname` int(10) unsigned NOT NULL,
  `id_name_qualifier` tinyint(3) unsigned default NULL,
  `taxon_ref` text,
  `synonym` text,
  `hazard_group` enum('1','2','3','4') default NULL,
  `hazard_group_ref` text,
  `id_alt_states` int(10) unsigned default NULL,
  `alt_states_type` enum('ana','teleo') default NULL,
  `last_update` datetime default NULL,
  PRIMARY KEY  (`id_species`),
  UNIQUE KEY `species_sciname` (`id_sciname`),
  KEY `FK_taxon_group` (`id_taxon_group`),
  KEY `FK_name_qualifier` (`id_name_qualifier`),
  CONSTRAINT `species_ibfk_1` FOREIGN KEY (`id_taxon_group`) REFERENCES `taxon_group` (`id_taxon_group`),
  CONSTRAINT `species_ibfk_2` FOREIGN KEY (`id_sciname`) REFERENCES `scientific_names` (`id_sciname`),
  CONSTRAINT `species_ibfk_3` FOREIGN KEY (`id_name_qualifier`) REFERENCES `spe_name_qualifier` (`id_name_qualifier`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `species_report`
--

DROP TABLE IF EXISTS `species_report`;
/*!50001 DROP VIEW IF EXISTS `species_report`*/;
/*!50001 CREATE TABLE `species_report` (
  `id_species` int(10) unsigned,
  `id_coll` tinyint(3) unsigned,
  `id_subcoll` tinyint(3) unsigned,
  `taxon_group` varchar(100),
  `hi_tax` text,
  `sciname` text,
  `sciname_no_auth` text,
  `taxon_ref` text,
  `synonym` text,
  `hazard_group` enum('1','2','3','4'),
  `hazard_group_ref` text,
  `ambient_risk` text,
  `sciname_alt_state` text,
  `alt_states_type` enum('ana','teleo'),
  `comments` text
) */;

--
-- Temporary table structure for view `specieslinkdwc`
--

DROP TABLE IF EXISTS `specieslinkdwc`;
/*!50001 DROP VIEW IF EXISTS `specieslinkdwc`*/;
/*!50001 CREATE TABLE `specieslinkdwc` (
  `record_uid` int(10) unsigned,
  `datelastmodified` datetime,
  `institutioncode` varchar(7),
  `collectioncode` varchar(7),
  `subcollectioncode` tinyint(3) unsigned,
  `catalognumber` varchar(30),
  `scientificname` longtext,
  `basisofrecord` varchar(1),
  `kingdom` varchar(255),
  `phylum` varchar(255),
  `class` varchar(255),
  `order` varchar(255),
  `family` varchar(255),
  `genus` varchar(255),
  `species` varchar(255),
  `subspecies` varchar(255),
  `scientificnameauthor` varchar(255),
  `identifiedby` varchar(50),
  `yearidentified` varchar(4),
  `monthidentified` varchar(2),
  `dayidentified` varchar(2),
  `typestatus` varchar(15),
  `collectornumber` binary(0),
  `fieldnumber` binary(0),
  `collector` varchar(50),
  `yearcollected` varchar(4),
  `monthcollected` varchar(2),
  `daycollected` varchar(2),
  `julianday` binary(0),
  `timeOfday` binary(0),
  `continentocean` binary(0),
  `country` varchar(255),
  `stateprovince` varchar(255),
  `county` varchar(255),
  `locality` longtext,
  `longitude` decimal(11,8),
  `latitude` decimal(11,8),
  `coordinateprecision` int(5) unsigned,
  `boundingbox` binary(0),
  `minimumelevation` binary(0),
  `maximumelevation` binary(0),
  `minimumdepth` binary(0),
  `maximumdepth` binary(0),
  `sex` binary(0),
  `preparationtype` binary(0),
  `individualcount` binary(0),
  `previouscatalognumber` text,
  `relationshiptype` text,
  `relatedcatalogitem` binary(0),
  `notes` longtext,
  `historyofdeposit` longtext,
  `depositor` varchar(50),
  `yeardeposited` varchar(4),
  `monthdeposited` varchar(2),
  `daydeposited` varchar(2),
  `isolatedfrom` text,
  `isolator` varchar(50),
  `isolationmethod` text,
  `conditionsforgrowth` varchar(111),
  `geneticallymodified` tinyint(1),
  `genotype` text,
  `mutant` binary(0),
  `race` binary(0),
  `alternatestate` longtext,
  `strainproperties` text,
  `strainapplications` text,
  `formofsupply` binary(0),
  `restrictions` text,
  `biologicalrisks` text,
  `pathogenicity` text
) */;

--
-- Table structure for table `stock_movement`
--

DROP TABLE IF EXISTS `stock_movement`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `stock_movement` (
  `id_stock_movement` int(10) unsigned NOT NULL auto_increment,
  `id_subcoll` tinyint(3) unsigned NOT NULL,
  `id_preservation_method` tinyint(3) unsigned NOT NULL,
  `description` varchar(256) NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY  (`id_stock_movement`),
  KEY `FK_id_preservation_method` (`id_preservation_method`),
  CONSTRAINT `stock_movement_ibfk_1` FOREIGN KEY (`id_preservation_method`) REFERENCES `preservation_method` (`id_preservation_method`)
) ENGINE=InnoDB AUTO_INCREMENT=130 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `stock_movement_location`
--

DROP TABLE IF EXISTS `stock_movement_location`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `stock_movement_location` (
  `id_stock_movement_location` int(10) unsigned NOT NULL auto_increment,
  `id_stock_movement` int(10) unsigned NOT NULL,
  `id_lot_strain_location_from` int(10) unsigned NOT NULL,
  `id_lot_strain_location_to` int(10) unsigned default NULL,
  PRIMARY KEY  (`id_stock_movement_location`),
  UNIQUE KEY `id_lot_strain_location_from_key` (`id_lot_strain_location_from`),
  UNIQUE KEY `id_lot_strain_location_to_key` (`id_lot_strain_location_to`),
  KEY `FK_stock_movement` (`id_stock_movement`),
  KEY `FK_lot_strain_location_from` (`id_lot_strain_location_from`),
  KEY `FK_lot_strain_location_to` (`id_lot_strain_location_to`),
  CONSTRAINT `stock_movement_location_ibfk_1` FOREIGN KEY (`id_stock_movement`) REFERENCES `stock_movement` (`id_stock_movement`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `stock_movement_location_ibfk_2` FOREIGN KEY (`id_lot_strain_location_from`) REFERENCES `lot_strain_location` (`id_lot_strain_location`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `stock_movement_location_ibfk_3` FOREIGN KEY (`id_lot_strain_location_to`) REFERENCES `lot_strain_location` (`id_lot_strain_location`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2238 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `stock_report`
--

DROP TABLE IF EXISTS `stock_report`;
/*!50001 DROP VIEW IF EXISTS `stock_report`*/;
/*!50001 CREATE TABLE `stock_report` (
  `id_subcoll` tinyint(3) unsigned,
  `id_strain` int(10) unsigned,
  `strain_code` varchar(30),
  `strain_numeric_code` int(10) unsigned,
  `taxon` text,
  `preservation_method` varchar(100),
  `lot` varchar(50),
  `position` varbinary(47),
  `available_qt` bigint(24) unsigned
) */;

--
-- Table structure for table `str_cha_biorisk_comments`
--

DROP TABLE IF EXISTS `str_cha_biorisk_comments`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_cha_biorisk_comments` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `biorisk_comments` text NOT NULL,
  PRIMARY KEY  (`id_strain`,`id_coll`,`id_lang`),
  KEY `FK_strain_coll` (`id_coll`,`id_strain`),
  KEY `FK_lang` (`id_lang`),
  CONSTRAINT `str_cha_biorisk_comments_ibfk_1` FOREIGN KEY (`id_coll`, `id_strain`) REFERENCES `str_characs` (`id_coll`, `id_strain`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_cha_biorisk_comments_ibfk_2` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_cha_catalogue`
--

DROP TABLE IF EXISTS `str_cha_catalogue`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_cha_catalogue` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `catalogue_notes` text NOT NULL,
  PRIMARY KEY  (`id_strain`,`id_coll`,`id_lang`),
  KEY `FK_lang` (`id_lang`),
  KEY `FK_strain_coll` (`id_coll`,`id_strain`),
  CONSTRAINT `str_cha_catalogue_ibfk_1` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_cha_catalogue_ibfk_2` FOREIGN KEY (`id_coll`, `id_strain`) REFERENCES `str_characs` (`id_coll`, `id_strain`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_cha_ogm_comments`
--

DROP TABLE IF EXISTS `str_cha_ogm_comments`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_cha_ogm_comments` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `ogm_comments` text NOT NULL,
  PRIMARY KEY  (`id_strain`,`id_coll`,`id_lang`),
  KEY `FK_strain_coll` (`id_coll`,`id_strain`),
  KEY `FK_lang` (`id_lang`),
  CONSTRAINT `str_cha_ogm_comments_ibfk_1` FOREIGN KEY (`id_coll`, `id_strain`) REFERENCES `str_characs` (`id_coll`, `id_strain`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_cha_ogm_comments_ibfk_2` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_cha_pictures`
--

DROP TABLE IF EXISTS `str_cha_pictures`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_cha_pictures` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `pictures` text NOT NULL,
  PRIMARY KEY  (`id_strain`,`id_coll`,`id_lang`),
  KEY `FK_lang` (`id_lang`),
  KEY `FK_strain_coll` (`id_coll`,`id_strain`),
  CONSTRAINT `str_cha_pictures_ibfk_1` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_cha_pictures_ibfk_2` FOREIGN KEY (`id_coll`, `id_strain`) REFERENCES `str_characs` (`id_coll`, `id_strain`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_cha_restrictions`
--

DROP TABLE IF EXISTS `str_cha_restrictions`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_cha_restrictions` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `restrictions` text NOT NULL,
  PRIMARY KEY  (`id_strain`,`id_coll`,`id_lang`),
  KEY `FK_strin_coll` (`id_coll`,`id_strain`),
  KEY `FK_lang` (`id_lang`),
  CONSTRAINT `str_cha_restrictions_ibfk_1` FOREIGN KEY (`id_coll`, `id_strain`) REFERENCES `str_characs` (`id_coll`, `id_strain`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_cha_restrictions_ibfk_2` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_cha_urls`
--

DROP TABLE IF EXISTS `str_cha_urls`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_cha_urls` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `urls` text NOT NULL,
  PRIMARY KEY  (`id_strain`,`id_coll`,`id_lang`),
  KEY `FK_lang` (`id_lang`),
  KEY `FK_strain_coll` (`id_coll`,`id_strain`),
  CONSTRAINT `str_cha_urls_ibfk_1` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_cha_urls_ibfk_2` FOREIGN KEY (`id_coll`, `id_strain`) REFERENCES `str_characs` (`id_coll`, `id_strain`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_characs`
--

DROP TABLE IF EXISTS `str_characs`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_characs` (
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_strain` int(10) unsigned NOT NULL,
  `biochemical` text,
  `molecular` text,
  `immunologic` text,
  `morphologic` text,
  `pathogenic` text,
  `genotypic` text,
  `ogm` enum('0','1','2') default NULL,
  PRIMARY KEY  (`id_coll`,`id_strain`),
  KEY `FK_strain_coll` (`id_strain`,`id_coll`),
  CONSTRAINT `str_characs_ibfk_1` FOREIGN KEY (`id_strain`, `id_coll`) REFERENCES `strain` (`id_strain`, `id_coll`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_clinical_form`
--

DROP TABLE IF EXISTS `str_clinical_form`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_clinical_form` (
  `id_clinical_form` smallint(5) unsigned NOT NULL auto_increment,
  PRIMARY KEY  (`id_clinical_form`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_clinical_form_lang`
--

DROP TABLE IF EXISTS `str_clinical_form_lang`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_clinical_form_lang` (
  `id_clinical_form` smallint(5) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `code` varchar(10) NOT NULL,
  `clinical_form` varchar(100) NOT NULL,
  PRIMARY KEY  (`id_clinical_form`,`id_lang`),
  KEY `FK_lang` (`id_lang`),
  KEY `FK_clinical_form` (`id_clinical_form`),
  CONSTRAINT `str_clinical_form_lang_ibfk_1` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_clinical_form_lang_ibfk_2` FOREIGN KEY (`id_clinical_form`) REFERENCES `str_clinical_form` (`id_clinical_form`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_coll_comments`
--

DROP TABLE IF EXISTS `str_coll_comments`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_coll_comments` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `comments` text NOT NULL,
  PRIMARY KEY  (`id_strain`,`id_coll`,`id_lang`),
  KEY `FK_lang` (`id_lang`),
  KEY `FK_strain_coll` (`id_coll`,`id_strain`),
  CONSTRAINT `str_coll_comments_ibfk_1` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_coll_comments_ibfk_2` FOREIGN KEY (`id_strain`, `id_coll`) REFERENCES `str_coll_event` (`id_strain`, `id_coll`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_coll_event`
--

DROP TABLE IF EXISTS `str_coll_event`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_coll_event` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_person` int(10) unsigned default NULL,
  `id_institution` int(10) unsigned default NULL,
  `date` date default NULL,
  `id_country` int(10) unsigned default NULL,
  `id_state` int(10) unsigned default NULL,
  `id_city` int(10) unsigned default NULL,
  `place` text,
  `gps_latitude` decimal(11,8) default NULL,
  `gps_latitude_dms` varchar(12) default NULL,
  `gps_latitude_mode` enum('decimal','dms') default NULL,
  `gps_longitude` decimal(11,8) default NULL,
  `gps_longitude_dms` varchar(12) default NULL,
  `gps_longitude_mode` enum('decimal','dms') default NULL,
  `gps_precision` int(5) unsigned default NULL,
  `id_gps_datum` smallint(5) unsigned default NULL,
  `gps_comments` text,
  `host_genus` varchar(50) default NULL,
  `host_species` varchar(50) default NULL,
  `host_classification` varchar(50) default NULL,
  `host_infra_name` varchar(100) default NULL,
  `host_infra_complement` varchar(100) default NULL,
  `global_code` varchar(50) default NULL,
  `id_clinical_form` smallint(5) unsigned default NULL,
  `hiv` enum('yes','no') default NULL,
  PRIMARY KEY  (`id_strain`,`id_coll`),
  KEY `FK_strain_coll` (`id_strain`,`id_coll`),
  KEY `FK_person` (`id_person`),
  KEY `FK_institution` (`id_institution`),
  KEY `FK_country` (`id_country`),
  KEY `FK_state` (`id_state`),
  KEY `FK_city` (`id_city`),
  KEY `FK_gps_datum` (`id_gps_datum`),
  KEY `FK_clinical_form` (`id_clinical_form`),
  CONSTRAINT `str_coll_event_ibfk_1` FOREIGN KEY (`id_strain`, `id_coll`) REFERENCES `strain` (`id_strain`, `id_coll`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_coll_event_ibfk_2` FOREIGN KEY (`id_person`) REFERENCES `person` (`id_person`),
  CONSTRAINT `str_coll_event_ibfk_3` FOREIGN KEY (`id_institution`) REFERENCES `institution` (`id_institution`),
  CONSTRAINT `str_coll_event_ibfk_4` FOREIGN KEY (`id_country`) REFERENCES `loc_country` (`id_country`),
  CONSTRAINT `str_coll_event_ibfk_5` FOREIGN KEY (`id_state`) REFERENCES `loc_state` (`id_state`),
  CONSTRAINT `str_coll_event_ibfk_6` FOREIGN KEY (`id_city`) REFERENCES `loc_city` (`id_city`),
  CONSTRAINT `str_coll_event_ibfk_7` FOREIGN KEY (`id_gps_datum`) REFERENCES `str_gps_datum` (`id_gps_datum`),
  CONSTRAINT `str_coll_event_ibfk_8` FOREIGN KEY (`id_clinical_form`) REFERENCES `str_clinical_form` (`id_clinical_form`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_cult_comments`
--

DROP TABLE IF EXISTS `str_cult_comments`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_cult_comments` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `comments` text NOT NULL,
  PRIMARY KEY  (`id_strain`,`id_coll`,`id_lang`),
  KEY `FK_lang` (`id_lang`),
  KEY `FK_strain_coll` (`id_coll`,`id_strain`),
  CONSTRAINT `str_cult_comments_ibfk_1` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_cult_comments_ibfk_2` FOREIGN KEY (`id_coll`, `id_strain`) REFERENCES `str_culture` (`id_coll`, `id_strain`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_cult_medium`
--

DROP TABLE IF EXISTS `str_cult_medium`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_cult_medium` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `medium` text NOT NULL,
  PRIMARY KEY  (`id_strain`,`id_coll`,`id_lang`),
  KEY `FK_lang` (`id_lang`),
  KEY `FK_strain_coll` (`id_coll`,`id_strain`),
  CONSTRAINT `str_cult_medium_ibfk_1` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_cult_medium_ibfk_2` FOREIGN KEY (`id_coll`, `id_strain`) REFERENCES `str_culture` (`id_coll`, `id_strain`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_culture`
--

DROP TABLE IF EXISTS `str_culture`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_culture` (
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_strain` int(10) unsigned NOT NULL,
  `temp` varchar(50) default NULL,
  `ph` varchar(50) default NULL,
  PRIMARY KEY  (`id_coll`,`id_strain`),
  KEY `FK_strain_coll` (`id_strain`,`id_coll`),
  CONSTRAINT `str_culture_ibfk_1` FOREIGN KEY (`id_strain`, `id_coll`) REFERENCES `strain` (`id_strain`, `id_coll`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_dep_reason`
--

DROP TABLE IF EXISTS `str_dep_reason`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_dep_reason` (
  `id_dep_reason` tinyint(3) unsigned NOT NULL auto_increment,
  PRIMARY KEY  (`id_dep_reason`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_dep_reason_lang`
--

DROP TABLE IF EXISTS `str_dep_reason_lang`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_dep_reason_lang` (
  `id_dep_reason` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `dep_reason` varchar(25) NOT NULL,
  PRIMARY KEY  (`id_dep_reason`,`id_lang`),
  KEY `FK_lang` (`id_lang`),
  KEY `FK_dep_reason` (`id_dep_reason`),
  CONSTRAINT `str_dep_reason_lang_ibfk_1` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_dep_reason_lang_ibfk_2` FOREIGN KEY (`id_dep_reason`) REFERENCES `str_dep_reason` (`id_dep_reason`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_dep_reason_subcoll`
--

DROP TABLE IF EXISTS `str_dep_reason_subcoll`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_dep_reason_subcoll` (
  `id_dep_reason` tinyint(3) unsigned NOT NULL,
  `id_subcoll` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY  (`id_dep_reason`,`id_subcoll`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_deposit`
--

DROP TABLE IF EXISTS `str_deposit`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_deposit` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_person` int(10) unsigned default NULL,
  `id_institution` int(10) unsigned default NULL,
  `genus` varchar(50) default NULL,
  `species` varchar(50) default NULL,
  `classification` varchar(50) default NULL,
  `infra_name` varchar(100) default NULL,
  `infra_complement` varchar(100) default NULL,
  `date` date default NULL,
  `id_dep_reason` tinyint(3) unsigned default NULL,
  `preserv_method` text,
  `form` varchar(50) default NULL,
  `comments` text,
  `aut_date` datetime default NULL,
  `aut_person` int(10) unsigned default NULL,
  `aut_result` text,
  PRIMARY KEY  (`id_strain`,`id_coll`),
  KEY `FK_strain_coll` (`id_strain`,`id_coll`),
  KEY `FK_person` (`id_person`),
  KEY `FK_institution` (`id_institution`),
  KEY `FK_dep_reason` (`id_dep_reason`),
  KEY `FK_aut_person` (`aut_person`),
  CONSTRAINT `str_deposit_ibfk_1` FOREIGN KEY (`id_strain`, `id_coll`) REFERENCES `strain` (`id_strain`, `id_coll`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_deposit_ibfk_2` FOREIGN KEY (`id_person`) REFERENCES `person` (`id_person`),
  CONSTRAINT `str_deposit_ibfk_3` FOREIGN KEY (`id_institution`) REFERENCES `institution` (`id_institution`),
  CONSTRAINT `str_deposit_ibfk_4` FOREIGN KEY (`id_dep_reason`) REFERENCES `str_dep_reason` (`id_dep_reason`),
  CONSTRAINT `str_deposit_ibfk_5` FOREIGN KEY (`aut_person`) REFERENCES `person` (`id_person`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_gps_datum`
--

DROP TABLE IF EXISTS `str_gps_datum`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_gps_datum` (
  `id_gps_datum` smallint(5) unsigned NOT NULL auto_increment,
  `gps_datum` varchar(20) NOT NULL,
  PRIMARY KEY  (`id_gps_datum`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_host_name`
--

DROP TABLE IF EXISTS `str_host_name`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_host_name` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `host_name` text NOT NULL,
  PRIMARY KEY  (`id_strain`,`id_coll`,`id_lang`),
  KEY `FK_lang` (`id_lang`),
  KEY `FK_strain_coll` (`id_strain`,`id_coll`),
  CONSTRAINT `str_host_name_ibfk_1` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_host_name_ibfk_2` FOREIGN KEY (`id_strain`, `id_coll`) REFERENCES `str_coll_event` (`id_strain`, `id_coll`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_ident_method`
--

DROP TABLE IF EXISTS `str_ident_method`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_ident_method` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `ident_method` text NOT NULL,
  PRIMARY KEY  (`id_strain`,`id_coll`,`id_lang`),
  KEY `FK_lang` (`id_lang`),
  KEY `FK_strain_coll` (`id_coll`,`id_strain`),
  CONSTRAINT `str_ident_method_ibfk_1` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_ident_method_ibfk_2` FOREIGN KEY (`id_strain`, `id_coll`) REFERENCES `str_identification` (`id_strain`, `id_coll`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_identification`
--

DROP TABLE IF EXISTS `str_identification`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_identification` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `date` date default NULL,
  `id_person` int(10) unsigned default NULL,
  `id_institution` int(10) unsigned default NULL,
  `genus` varchar(50) default NULL,
  `species` varchar(50) default NULL,
  `classification` varchar(50) default NULL,
  `infra_name` varchar(100) default NULL,
  `infra_complement` varchar(100) default NULL,
  `comments` text,
  PRIMARY KEY  (`id_strain`,`id_coll`),
  KEY `FK_strain_coll` (`id_strain`,`id_coll`),
  KEY `FK_person` (`id_person`),
  KEY `FK_institution` (`id_institution`),
  CONSTRAINT `str_identification_ibfk_1` FOREIGN KEY (`id_strain`, `id_coll`) REFERENCES `strain` (`id_strain`, `id_coll`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_identification_ibfk_2` FOREIGN KEY (`id_person`) REFERENCES `person` (`id_person`),
  CONSTRAINT `str_identification_ibfk_3` FOREIGN KEY (`id_institution`) REFERENCES `institution` (`id_institution`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_incub_time`
--

DROP TABLE IF EXISTS `str_incub_time`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_incub_time` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `incub_time` varchar(50) NOT NULL,
  PRIMARY KEY  (`id_strain`,`id_coll`,`id_lang`),
  KEY `FK_lang` (`id_lang`),
  KEY `FK_strain_coll` (`id_coll`,`id_strain`),
  CONSTRAINT `str_incub_time_ibfk_1` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_incub_time_ibfk_2` FOREIGN KEY (`id_coll`, `id_strain`) REFERENCES `str_culture` (`id_coll`, `id_strain`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_iso_method`
--

DROP TABLE IF EXISTS `str_iso_method`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_iso_method` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `iso_method` text NOT NULL,
  PRIMARY KEY  (`id_strain`,`id_coll`,`id_lang`),
  KEY `FK_lang` (`id_lang`),
  KEY `FK_strain_coll` (`id_coll`,`id_strain`),
  CONSTRAINT `str_iso_method_ibfk_1` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_iso_method_ibfk_2` FOREIGN KEY (`id_strain`, `id_coll`) REFERENCES `str_isolation` (`id_strain`, `id_coll`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_isolation`
--

DROP TABLE IF EXISTS `str_isolation`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_isolation` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_person` int(10) unsigned default NULL,
  `id_institution` int(10) unsigned default NULL,
  `date` date default NULL,
  `comments` text,
  PRIMARY KEY  (`id_strain`,`id_coll`),
  KEY `FK_strain_coll` (`id_strain`,`id_coll`),
  KEY `FK_person` (`id_person`),
  KEY `FK_institution` (`id_institution`),
  CONSTRAINT `str_isolation_ibfk_1` FOREIGN KEY (`id_strain`, `id_coll`) REFERENCES `strain` (`id_strain`, `id_coll`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_isolation_ibfk_2` FOREIGN KEY (`id_person`) REFERENCES `person` (`id_person`),
  CONSTRAINT `str_isolation_ibfk_3` FOREIGN KEY (`id_institution`) REFERENCES `institution` (`id_institution`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_isolation_from`
--

DROP TABLE IF EXISTS `str_isolation_from`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_isolation_from` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `isolation_from` text NOT NULL,
  PRIMARY KEY  (`id_strain`,`id_coll`,`id_lang`),
  KEY `FK_lang` (`id_lang`),
  KEY `FK_strain_coll` (`id_coll`,`id_strain`),
  CONSTRAINT `str_isolation_from_ibfk_1` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_isolation_from_ibfk_2` FOREIGN KEY (`id_strain`, `id_coll`) REFERENCES `str_isolation` (`id_strain`, `id_coll`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_oxy_req`
--

DROP TABLE IF EXISTS `str_oxy_req`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_oxy_req` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `oxy_req` varchar(50) NOT NULL,
  PRIMARY KEY  (`id_strain`,`id_coll`,`id_lang`),
  KEY `FK_lang` (`id_lang`),
  KEY `FK_strain_coll` (`id_coll`,`id_strain`),
  CONSTRAINT `str_oxy_req_ibfk_1` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_oxy_req_ibfk_2` FOREIGN KEY (`id_coll`, `id_strain`) REFERENCES `str_culture` (`id_coll`, `id_strain`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_pro_applications`
--

DROP TABLE IF EXISTS `str_pro_applications`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_pro_applications` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `applications` text NOT NULL,
  PRIMARY KEY  (`id_strain`,`id_coll`,`id_lang`),
  KEY `FK_strain_coll` (`id_coll`,`id_strain`),
  KEY `FK_lang` (`id_lang`),
  CONSTRAINT `str_pro_applications_ibfk_1` FOREIGN KEY (`id_coll`, `id_strain`) REFERENCES `str_properties` (`id_coll`, `id_strain`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_pro_applications_ibfk_2` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_pro_properties`
--

DROP TABLE IF EXISTS `str_pro_properties`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_pro_properties` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `properties` text NOT NULL,
  PRIMARY KEY  (`id_strain`,`id_coll`,`id_lang`),
  KEY `FK_strain_coll` (`id_coll`,`id_strain`),
  KEY `FK_lang` (`id_lang`),
  CONSTRAINT `str_pro_properties_ibfk_1` FOREIGN KEY (`id_coll`, `id_strain`) REFERENCES `str_properties` (`id_coll`, `id_strain`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_pro_properties_ibfk_2` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_pro_urls`
--

DROP TABLE IF EXISTS `str_pro_urls`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_pro_urls` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `urls` text NOT NULL,
  PRIMARY KEY  (`id_strain`,`id_coll`,`id_lang`),
  KEY `FK_strain_coll` (`id_coll`,`id_strain`),
  KEY `FK_lang` (`id_lang`),
  CONSTRAINT `str_pro_urls_ibfk_1` FOREIGN KEY (`id_coll`, `id_strain`) REFERENCES `str_properties` (`id_coll`, `id_strain`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_pro_urls_ibfk_2` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_properties`
--

DROP TABLE IF EXISTS `str_properties`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_properties` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY  (`id_coll`,`id_strain`),
  KEY `FK_strain_coll` (`id_strain`,`id_coll`),
  CONSTRAINT `str_properties_ibfk_1` FOREIGN KEY (`id_strain`, `id_coll`) REFERENCES `strain` (`id_strain`, `id_coll`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_quality`
--

DROP TABLE IF EXISTS `str_quality`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_quality` (
  `id_quality` int(10) unsigned NOT NULL auto_increment,
  `id_user` int(10) unsigned NOT NULL,
  `id_lot` int(10) unsigned NOT NULL,
  `id_strain` int(10) unsigned NOT NULL,
  `date` date NOT NULL,
  `last_update` datetime default NULL,
  `not_identified` tinyint(1) unsigned NOT NULL default '0',
  PRIMARY KEY  (`id_quality`),
  KEY `str_quality_FKIndex2` (`id_lot`),
  KEY `id_strain` (`id_strain`,`id_lot`),
  CONSTRAINT `str_quality_ibfk_1` FOREIGN KEY (`id_lot`) REFERENCES `lot` (`id_lot`),
  CONSTRAINT `str_quality_ibfk_3` FOREIGN KEY (`id_strain`) REFERENCES `strain` (`id_strain`),
  CONSTRAINT `str_quality_ibfk_4` FOREIGN KEY (`id_strain`, `id_lot`) REFERENCES `lot_strain` (`id_strain`, `id_lot`)
) ENGINE=InnoDB AUTO_INCREMENT=389 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_quality_origin_location`
--

DROP TABLE IF EXISTS `str_quality_origin_location`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_quality_origin_location` (
  `id_quality_origin_location` int(10) unsigned NOT NULL auto_increment,
  `id_quality` int(10) unsigned NOT NULL,
  `id_origin_lot` int(10) unsigned NOT NULL,
  `id_origin_container_hierarchy` int(10) unsigned NOT NULL,
  `origin_row` int(10) unsigned NOT NULL,
  `origin_col` int(10) unsigned NOT NULL,
  `quantity` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id_quality_origin_location`),
  KEY `FK_id_quality` (`id_quality`),
  KEY `FK_id_origin_lot` (`id_origin_lot`),
  KEY `FK_id_origin_container_hierarchy` (`id_origin_container_hierarchy`),
  CONSTRAINT `str_quality_origin_location_ibfk_1` FOREIGN KEY (`id_quality`) REFERENCES `str_quality` (`id_quality`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_quality_origin_location_ibfk_2` FOREIGN KEY (`id_origin_lot`) REFERENCES `lot` (`id_lot`),
  CONSTRAINT `str_quality_origin_location_ibfk_3` FOREIGN KEY (`id_origin_container_hierarchy`) REFERENCES `container_hierarchy` (`id_container_hierarchy`)
) ENGINE=InnoDB AUTO_INCREMENT=389 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_quality_test`
--

DROP TABLE IF EXISTS `str_quality_test`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_quality_test` (
  `id_test` int(10) unsigned NOT NULL auto_increment,
  `id_quality` int(10) unsigned NOT NULL,
  `id_doc` int(10) unsigned NOT NULL COMMENT 'test is a document qualifier',
  `result` text,
  `comments` text,
  `purity` enum('y','n') NOT NULL,
  `counting` varchar(100) default NULL,
  `counting_not_apply` enum('y','n') NOT NULL,
  PRIMARY KEY  (`id_test`),
  KEY `id_doc` (`id_doc`),
  KEY `id_quality` (`id_quality`),
  CONSTRAINT `str_quality_test_ibfk_2` FOREIGN KEY (`id_quality`) REFERENCES `str_quality` (`id_quality`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_quality_test_ibfk_3` FOREIGN KEY (`id_doc`) REFERENCES `doc` (`id_doc`)
) ENGINE=InnoDB AUTO_INCREMENT=403 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_stock_minimum`
--

DROP TABLE IF EXISTS `str_stock_minimum`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_stock_minimum` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_preservation_method` tinyint(3) unsigned NOT NULL,
  `quantity` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id_strain`,`id_preservation_method`),
  KEY `FK_id_strain` (`id_strain`),
  KEY `FK_id_preservation_method` (`id_preservation_method`),
  CONSTRAINT `str_stock_minimum_ibfk_1` FOREIGN KEY (`id_strain`) REFERENCES `strain` (`id_strain`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_stock_minimum_ibfk_2` FOREIGN KEY (`id_preservation_method`) REFERENCES `preservation_method` (`id_preservation_method`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_substratum`
--

DROP TABLE IF EXISTS `str_substratum`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_substratum` (
  `id_strain` int(10) unsigned NOT NULL,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `substratum` text NOT NULL,
  PRIMARY KEY  (`id_strain`,`id_coll`,`id_lang`),
  KEY `FK_lang` (`id_lang`),
  KEY `FK_strain_coll` (`id_coll`,`id_strain`),
  CONSTRAINT `str_substratum_ibfk_1` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_substratum_ibfk_2` FOREIGN KEY (`id_strain`, `id_coll`) REFERENCES `str_coll_event` (`id_strain`, `id_coll`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_type`
--

DROP TABLE IF EXISTS `str_type`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_type` (
  `id_type` tinyint(3) unsigned NOT NULL auto_increment,
  PRIMARY KEY  (`id_type`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_type_lang`
--

DROP TABLE IF EXISTS `str_type_lang`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_type_lang` (
  `id_type` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `type` varchar(15) NOT NULL,
  PRIMARY KEY  (`id_type`,`id_lang`),
  KEY `FK_lang` (`id_lang`),
  KEY `FK_type` (`id_type`),
  CONSTRAINT `str_type_lang_ibfk_1` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `str_type_lang_ibfk_2` FOREIGN KEY (`id_type`) REFERENCES `str_type` (`id_type`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `str_type_subcoll`
--

DROP TABLE IF EXISTS `str_type_subcoll`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `str_type_subcoll` (
  `id_type` tinyint(3) unsigned NOT NULL,
  `id_subcoll` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY  (`id_type`,`id_subcoll`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `strain`
--

DROP TABLE IF EXISTS `strain`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `strain` (
  `id_strain` int(10) unsigned NOT NULL auto_increment,
  `id_coll` tinyint(3) unsigned NOT NULL,
  `id_subcoll` tinyint(3) unsigned NOT NULL,
  `id_division` smallint(5) unsigned NOT NULL,
  `code` varchar(30) NOT NULL,
  `numeric_code` int(10) unsigned NOT NULL,
  `internal_code` varchar(30) default NULL,
  `status` enum('active','inactive','pending') NOT NULL,
  `id_species` int(10) unsigned default NULL,
  `infra_complement` varchar(50) default NULL,
  `id_type` tinyint(3) unsigned default NULL,
  `history` text,
  `extra_codes` text,
  `comments` text,
  `last_update` datetime default NULL,
  `is_ogm` tinyint(1) NOT NULL default '0' COMMENT '0 = false, 1 = true',
  `go_catalog` tinyint(1) NOT NULL default '0' COMMENT '0 = false, 1 = true',
  PRIMARY KEY  (`id_strain`,`id_coll`),
  UNIQUE KEY `numeric_code_coll` (`numeric_code`,`id_coll`),
  KEY `FK_species` (`id_species`),
  KEY `FK_str_type` (`id_type`),
  KEY `FK_division` (`id_division`),
  CONSTRAINT `strain_ibfk_1` FOREIGN KEY (`id_species`) REFERENCES `species` (`id_species`),
  CONSTRAINT `strain_ibfk_2` FOREIGN KEY (`id_type`) REFERENCES `str_type` (`id_type`),
  CONSTRAINT `strain_ibfk_3` FOREIGN KEY (`id_division`) REFERENCES `division` (`id_division`)
) ENGINE=InnoDB AUTO_INCREMENT=3824 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `strain_report`
--

DROP TABLE IF EXISTS `strain_report`;
/*!50001 DROP VIEW IF EXISTS `strain_report`*/;
/*!50001 CREATE TABLE `strain_report` (
  `id_strain` int(10) unsigned,
  `id_subcoll` tinyint(3) unsigned,
  `division` varchar(50),
  `code` varchar(30),
  `numeric_code` int(10) unsigned,
  `origin_code` varchar(30),
  `status` enum('active','inactive','pending'),
  `taxon_group` varchar(100),
  `taxon` text,
  `type` varchar(15),
  `is_ogm` tinyint(1),
  `taxonomic_complement` varchar(50),
  `history` text,
  `other_codes` text,
  `general_comments` text,
  `coll_date` date,
  `coll_year` int(4),
  `coll_month` int(2),
  `coll_person` varchar(50),
  `coll_institution` varchar(80),
  `country` varchar(255),
  `state_code` char(4),
  `state_name` varchar(255),
  `city` varchar(255),
  `place` text,
  `gps_latitude` decimal(11,8),
  `gps_latitude_dms` varchar(12),
  `gps_latitude_mode` enum('decimal','dms'),
  `gps_longitude` decimal(11,8),
  `gps_longitude_dms` varchar(12),
  `gps_longitude_mode` enum('decimal','dms'),
  `gps_datum` varchar(20),
  `gps_precision` int(5) unsigned,
  `gps_comments` text,
  `substratum` text,
  `host_name` text,
  `host_genus` varchar(50),
  `host_species` varchar(50),
  `host_level` varchar(50),
  `host_subspecies` varchar(100),
  `host_taxonomic_complement` varchar(100),
  `international_code` varchar(50),
  `clinical_form_code` varchar(10),
  `clinical_form_name` varchar(100),
  `hiv` enum('yes','no'),
  `coll_comments` text,
  `iso_date` date,
  `iso_year` int(4),
  `iso_month` int(2),
  `iso_person` varchar(50),
  `iso_institution` varchar(80),
  `isolation_from` text,
  `iso_method` text,
  `iso_comments` text,
  `ident_date` date,
  `ident_year` int(4),
  `ident_month` int(2),
  `ident_person` varchar(50),
  `ident_institution` varchar(80),
  `ident_genus` varchar(50),
  `ident_species` varchar(50),
  `ident_level` varchar(50),
  `ident_subspecies` varchar(100),
  `ident_taxonomic_complement` varchar(100),
  `ident_method` text,
  `ident_comments` text,
  `dep_date` date,
  `dep_year` int(4),
  `dep_month` int(2),
  `dep_person` varchar(50),
  `dep_institution` varchar(80),
  `dep_genus` varchar(50),
  `dep_species` varchar(50),
  `dep_level` varchar(50),
  `dep_subspecies` varchar(100),
  `dep_taxonomic_complement` varchar(100),
  `dep_reason` varchar(25),
  `dep_form` varchar(50),
  `recom_preserv_method` text,
  `aut_date` datetime,
  `aut_year` int(4),
  `aut_month` int(2),
  `aut_person` varchar(50),
  `aut_result` text,
  `dep_comments` text,
  `recom_growth_medium` text,
  `recom_temp` varchar(50),
  `incubation_time` varchar(50),
  `ph` varchar(50),
  `oxygen_requirements` varchar(50),
  `grow_comments` text,
  `morphological_characteristics` text,
  `molecular_characteristics` text,
  `biochemical_characteristics` text,
  `immunologic_characteristics` text,
  `pathogenic_characteristics` text,
  `genotypic_characteristics` text,
  `ogm` enum('0','1','2'),
  `ogm_comments` text,
  `biorisk_comments` text,
  `restrictions` text,
  `pictures` text,
  `charac_references` text,
  `catalogue_notes` text,
  `properties` text,
  `applications` text,
  `prop_references` text,
  `go_catalog` tinyint(1)
) */;

--
-- Table structure for table `system_areas`
--

DROP TABLE IF EXISTS `system_areas`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `system_areas` (
  `id_area` smallint(5) unsigned NOT NULL auto_increment,
  `name` varchar(100) NOT NULL,
  `description` text,
  PRIMARY KEY  (`id_area`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `taxon_group`
--

DROP TABLE IF EXISTS `taxon_group`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `taxon_group` (
  `id_taxon_group` tinyint(3) unsigned NOT NULL auto_increment,
  PRIMARY KEY  (`id_taxon_group`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `taxon_group_lang`
--

DROP TABLE IF EXISTS `taxon_group_lang`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `taxon_group_lang` (
  `id_taxon_group` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `taxon_group` varchar(100) NOT NULL,
  PRIMARY KEY  (`id_taxon_group`,`id_lang`),
  KEY `id_lang` (`id_lang`),
  CONSTRAINT `taxon_group_lang_ibfk_1` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `taxon_group_lang_ibfk_2` FOREIGN KEY (`id_taxon_group`) REFERENCES `taxon_group` (`id_taxon_group`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `taxon_group_subcoll`
--

DROP TABLE IF EXISTS `taxon_group_subcoll`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `taxon_group_subcoll` (
  `id_taxon_group` tinyint(3) unsigned NOT NULL,
  `id_subcoll` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY  (`id_taxon_group`,`id_subcoll`),
  CONSTRAINT `taxon_group_subcoll_ibfk_1` FOREIGN KEY (`id_taxon_group`) REFERENCES `taxon_group` (`id_taxon_group`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `test_group`
--

DROP TABLE IF EXISTS `test_group`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `test_group` (
  `id_test_group` tinyint(3) unsigned NOT NULL auto_increment,
  PRIMARY KEY  (`id_test_group`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `test_group_lang`
--

DROP TABLE IF EXISTS `test_group_lang`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `test_group_lang` (
  `id_test_group` tinyint(3) unsigned NOT NULL,
  `id_lang` tinyint(3) unsigned NOT NULL,
  `category` varchar(100) NOT NULL,
  PRIMARY KEY  (`id_test_group`,`id_lang`),
  KEY `id_lang` (`id_lang`),
  CONSTRAINT `test_group_lang_ibfk_1` FOREIGN KEY (`id_lang`) REFERENCES `lang` (`id_lang`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `test_group_lang_ibfk_2` FOREIGN KEY (`id_test_group`) REFERENCES `test_group` (`id_test_group`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `test_group_subcoll`
--

DROP TABLE IF EXISTS `test_group_subcoll`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `test_group_subcoll` (
  `id_test_group` tinyint(3) unsigned NOT NULL,
  `id_subcoll` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY  (`id_test_group`,`id_subcoll`),
  CONSTRAINT `test_group_subcoll_ibfk_1` FOREIGN KEY (`id_test_group`) REFERENCES `test_group` (`id_test_group`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `used_origin`
--

DROP TABLE IF EXISTS `used_origin`;
/*!50001 DROP VIEW IF EXISTS `used_origin`*/;
/*!50001 CREATE TABLE `used_origin` (
  `id_origin_lot` int(11) unsigned,
  `id_origin_container_hierarchy` int(11) unsigned,
  `origin_row` int(11) unsigned,
  `origin_col` int(11) unsigned,
  `used_qt` int(11) unsigned
) */;

--
-- Temporary table structure for view `used_origin_all`
--

DROP TABLE IF EXISTS `used_origin_all`;
/*!50001 DROP VIEW IF EXISTS `used_origin_all`*/;
/*!50001 CREATE TABLE `used_origin_all` (
  `origin` varchar(12),
  `id_origin_lot` int(11) unsigned,
  `id_origin_container_hierarchy` int(11) unsigned,
  `origin_row` int(11) unsigned,
  `origin_col` int(11) unsigned,
  `used_qt` int(11) unsigned
) */;

--
-- Temporary table structure for view `view_hierarchy`
--

DROP TABLE IF EXISTS `view_hierarchy`;
/*!50001 DROP VIEW IF EXISTS `view_hierarchy`*/;
/*!50001 CREATE TABLE `view_hierarchy` (
  `id_hierarchy` int(10) unsigned,
  `id_taxon_group` tinyint(3) unsigned,
  `id_subcoll` tinyint(3) unsigned,
  `seq` int(11),
  `id_lang` tinyint(3) unsigned,
  `rank` varchar(255),
  `hi_tax` int(4),
  `has_author` int(4),
  `use_author` int(4),
  `in_sciname` int(4),
  `required` int(4),
  `important` int(4),
  `string_format` varchar(11),
  `string_case` varchar(7),
  `prefix` varchar(200),
  `suffix` varchar(200),
  `default_value` varchar(255)
) */;

--
-- Dumping routines for database 'sicol_v110_clioc'
--
DELIMITER ;;
/*!50003 DROP FUNCTION IF EXISTS `get_report_lang` */;;
/*!50003 SET SESSION SQL_MODE=""*/;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 FUNCTION `get_report_lang`() RETURNS int(11)
    NO SQL
    DETERMINISTIC
return @report_lang */;;
/*!50003 SET SESSION SQL_MODE=@OLD_SQL_MODE*/;;
DELIMITER ;

--
-- Final view structure for view `doc_report`
--

/*!50001 DROP TABLE `doc_report`*/;
/*!50001 DROP VIEW IF EXISTS `doc_report`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `doc_report` AS select `d`.`id_doc` AS `id_doc`,`d`.`id_coll` AS `id_coll`,`d`.`id_subcoll` AS `id_subcoll`,`d`.`code` AS `code`,`dq`.`qualifier` AS `qualifier`,`dt`.`title` AS `title`,`dd`.`description` AS `description`,`df`.`file_name` AS `file_name`,`tgl`.`category` AS `category`,`d`.`go_catalog` AS `go_catalog` from (((((`doc` `d` join `doc_qualifier` `dq` on((`d`.`id_qualifier` = `dq`.`id_qualifier`))) left join `doc_title` `dt` on(((`d`.`id_doc` = `dt`.`id_doc`) and (`dt`.`id_lang` = `get_report_lang`())))) left join `doc_description` `dd` on(((`d`.`id_doc` = `dd`.`id_doc`) and (`dd`.`id_lang` = `get_report_lang`())))) left join `doc_file` `df` on(((`d`.`id_doc` = `df`.`id_doc`) and (`df`.`id_lang` = `get_report_lang`())))) left join `test_group_lang` `tgl` on(((`d`.`id_test_group` = `tgl`.`id_test_group`) and (`tgl`.`id_lang` = `get_report_lang`())))) */;

--
-- Final view structure for view `institution_report`
--

/*!50001 DROP TABLE `institution_report`*/;
/*!50001 DROP VIEW IF EXISTS `institution_report`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `institution_report` AS select `i`.`id_institution` AS `id_institution`,`i`.`code1` AS `code1`,`i`.`code2` AS `code2`,`i`.`code3` AS `code3`,`i`.`complement` AS `complement`,`i`.`nickname` AS `nickname`,`i`.`name` AS `name`,`i`.`address` AS `address`,`i`.`phone` AS `phone`,`i`.`email` AS `email`,`i`.`website` AS `website`,`i`.`go_catalog` AS `go_catalog`,`ic`.`comments` AS `comments` from (`institution` `i` left join `inst_comments` `ic` on(((`ic`.`id_institution` = `i`.`id_institution`) and (`ic`.`id_lang` = `get_report_lang`())))) */;

--
-- Final view structure for view `lot_strain_available_locations`
--

/*!50001 DROP TABLE `lot_strain_available_locations`*/;
/*!50001 DROP VIEW IF EXISTS `lot_strain_available_locations`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `lot_strain_available_locations` AS select `lslm`.`id_lot` AS `id_lot`,`lslm`.`id_strain` AS `id_strain`,`lslm`.`id_container_hierarchy` AS `id_container_hierarchy`,`lslm`.`row` AS `row`,`lslm`.`col` AS `col`,cast((((`lslm`.`quantity` - ifnull(`lslm`.`used_qt_pres`,0)) - ifnull(`lslm`.`used_qt_dist`,0)) - ifnull(`lslm`.`used_qt_qual`,0)) as unsigned) AS `available_qt` from `lot_strain_stock_data` `lslm` where ((((`lslm`.`quantity` - ifnull(`lslm`.`used_qt_pres`,0)) - ifnull(`lslm`.`used_qt_dist`,0)) - ifnull(`lslm`.`used_qt_qual`,0)) > 0) order by `lslm`.`id_strain`,`lslm`.`id_lot`,`lslm`.`id_container_hierarchy`,`lslm`.`row`,`lslm`.`col` */;

--
-- Final view structure for view `lot_strain_stock`
--

/*!50001 DROP TABLE `lot_strain_stock`*/;
/*!50001 DROP VIEW IF EXISTS `lot_strain_stock`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `lot_strain_stock` AS select `lslm`.`id_lot` AS `id_lot`,`lslm`.`id_strain` AS `id_strain`,cast((((sum(`lslm`.`quantity`) - sum(ifnull(`lslm`.`used_qt_pres`,0))) - sum(ifnull(`lslm`.`used_qt_dist`,0))) - sum(ifnull(`lslm`.`used_qt_qual`,0))) as unsigned) AS `stock` from `lot_strain_stock_data` `lslm` group by `lslm`.`id_lot`,`lslm`.`id_strain` */;

--
-- Final view structure for view `lot_strain_stock_data`
--

/*!50001 DROP TABLE `lot_strain_stock_data`*/;
/*!50001 DROP VIEW IF EXISTS `lot_strain_stock_data`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`sicol`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `lot_strain_stock_data` AS select `lsl`.`id_lot` AS `id_lot`,`lsl`.`id_strain` AS `id_strain`,`lsl`.`id_container_hierarchy` AS `id_container_hierarchy`,`lsl`.`row` AS `row`,`lsl`.`col` AS `col`,`lsl`.`quantity` AS `quantity`,cast((select sum(`ps`.`quantity`) AS `sum(quantity)` from `preservation_strain` `ps` where ((`ps`.`id_lot` = `lsl`.`id_lot`) and (`ps`.`id_origin_container_hierarchy` = `lsl`.`id_container_hierarchy`) and (`ps`.`origin_row` = `lsl`.`row`) and (`ps`.`origin_col` = `lsl`.`col`))) as unsigned) AS `used_qt_pres`,cast((select sum(`dol`.`quantity`) AS `sum(quantity)` from `distribution_origin_location` `dol` where ((`dol`.`id_origin_lot` = `lsl`.`id_lot`) and (`dol`.`id_origin_container_hierarchy` = `lsl`.`id_container_hierarchy`) and (`dol`.`origin_row` = `lsl`.`row`) and (`dol`.`origin_col` = `lsl`.`col`))) as unsigned) AS `used_qt_dist`,cast((select sum(`qol`.`quantity`) AS `sum(quantity)` from `str_quality_origin_location` `qol` where ((`qol`.`id_origin_lot` = `lsl`.`id_lot`) and (`qol`.`id_origin_container_hierarchy` = `lsl`.`id_container_hierarchy`) and (`qol`.`origin_row` = `lsl`.`row`) and (`qol`.`origin_col` = `lsl`.`col`))) as unsigned) AS `used_qt_qual` from `lot_strain_location` `lsl` where (not(`lsl`.`id_lot_strain_location` in (select `stock_movement_location`.`id_lot_strain_location_from` AS `id_lot_strain_location_from` from `stock_movement_location`))) */;

--
-- Final view structure for view `person_report`
--

/*!50001 DROP TABLE `person_report`*/;
/*!50001 DROP VIEW IF EXISTS `person_report`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `person_report` AS select `p`.`id_person` AS `id_person`,`p`.`name` AS `name`,`p`.`nickname` AS `nickname`,`p`.`address` AS `address`,`p`.`phone` AS `phone`,`p`.`email` AS `email`,`p`.`go_catalog` AS `go_catalog`,`pc`.`comments` AS `comments` from (`person` `p` left join `per_comments` `pc` on(((`pc`.`id_person` = `p`.`id_person`) and (`pc`.`id_lang` = `get_report_lang`())))) */;

--
-- Final view structure for view `preservation_strain_locations`
--

/*!50001 DROP TABLE `preservation_strain_locations`*/;
/*!50001 DROP VIEW IF EXISTS `preservation_strain_locations`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `preservation_strain_locations` AS select `p`.`id_preservation` AS `id_preservation`,`p`.`id_lot` AS `id_lot`,`ps`.`id_strain` AS `id_strain`,`ps`.`origin_type` AS `origin_type`,`lsl`.`id_container_hierarchy` AS `id_container_hierarchy`,`lsl`.`row` AS `row`,`lsl`.`col` AS `col`,`ps`.`id_lot` AS `id_origin_lot`,`ps`.`id_origin_container_hierarchy` AS `id_origin_container_hierarchy`,`ps`.`origin_row` AS `origin_row`,`ps`.`origin_col` AS `origin_col`,`ps`.`quantity` AS `quantity` from ((`preservation` `p` join `preservation_strain` `ps` on((`p`.`id_preservation` = `ps`.`id_preservation`))) join `lot_strain_location` `lsl` on(((`lsl`.`id_lot` = `p`.`id_lot`) and (`lsl`.`id_strain` = `ps`.`id_strain`)))) order by `p`.`id_preservation`,`ps`.`id_lot`,`ps`.`id_strain`,`lsl`.`id_container_hierarchy`,`lsl`.`row`,`lsl`.`col` */;

--
-- Final view structure for view `ref_report`
--

/*!50001 DROP TABLE `ref_report`*/;
/*!50001 DROP VIEW IF EXISTS `ref_report`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `ref_report` AS select `r`.`id_ref` AS `id_ref`,`r`.`id_coll` AS `id_coll`,`r`.`id_subcoll` AS `id_subcoll`,`r`.`title` AS `title`,`r`.`author` AS `author`,`r`.`year` AS `year`,`r`.`url` AS `url`,`rc`.`comments` AS `comments`,`r`.`go_catalog` AS `go_catalog` from (`ref` `r` left join `ref_comments` `rc` on(((`r`.`id_ref` = `rc`.`id_ref`) and (`rc`.`id_lang` = `get_report_lang`())))) */;

--
-- Final view structure for view `sidneiView`
--

/*!50001 DROP TABLE `sidneiView`*/;
/*!50001 DROP VIEW IF EXISTS `sidneiView`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`sicol`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `sidneiView` AS select `strain`.`id_strain` AS `record_uid`,`strain`.`last_update` AS `datelastmodified`,_utf8'Fiocruz' AS `institutioncode`,(case `strain`.`id_coll` when 1 then _utf8'CLIOC' when 2 then _utf8'CCBS' when 3 then _utf8'CCGB' when 4 then _utf8'CCFF' when 5 then _utf8'CMT' when 6 then _utf8'ColTryp' when 7 then _utf8'CFP' when 8 then _utf8'CBMA' when 9 then _utf8'INCQS' else NULL end) AS `collectioncode`,`strain`.`id_subcoll` AS `subcollectioncode`,`strain`.`code` AS `catalognumber`,replace(replace(replace(replace(`scientific_names`.`sciname_no_auth`,_utf8'<b>',_utf8''),_utf8'<i>',_utf8''),_utf8'</b>',_utf8''),_utf8'</i>',_utf8'') AS `scientificname`,_utf8'L' AS `basisofrecord`,`taxon_group_lang`.`taxon_group` AS `kingdom`,(select `scientific_names_hierarchy`.`value` AS `value` from `scientific_names_hierarchy` where ((`scientific_names_hierarchy`.`id_sciname` = `species`.`id_sciname`) and (`scientific_names_hierarchy`.`id_hierarchy` = 4))) AS `phylum`,(select `scientific_names_hierarchy`.`value` AS `value` from `scientific_names_hierarchy` where ((`scientific_names_hierarchy`.`id_sciname` = `species`.`id_sciname`) and (`scientific_names_hierarchy`.`id_hierarchy` = 9))) AS `class`,(select `scientific_names_hierarchy`.`value` AS `value` from `scientific_names_hierarchy` where ((`scientific_names_hierarchy`.`id_sciname` = `species`.`id_sciname`) and (`scientific_names_hierarchy`.`id_hierarchy` = 11))) AS `order`,(select `scientific_names_hierarchy`.`value` AS `value` from `scientific_names_hierarchy` where ((`scientific_names_hierarchy`.`id_sciname` = `species`.`id_sciname`) and (`scientific_names_hierarchy`.`id_hierarchy` = 14))) AS `family`,(select `scientific_names_hierarchy`.`value` AS `value` from `scientific_names_hierarchy` where ((`scientific_names_hierarchy`.`id_sciname` = `species`.`id_sciname`) and (`scientific_names_hierarchy`.`id_hierarchy` = 18))) AS `genus`,(select `scientific_names_hierarchy`.`value` AS `value` from `scientific_names_hierarchy` where ((`scientific_names_hierarchy`.`id_sciname` = `species`.`id_sciname`) and (`scientific_names_hierarchy`.`id_hierarchy` = 21))) AS `species`,(select `scientific_names_hierarchy`.`value` AS `value` from `scientific_names_hierarchy` where ((`scientific_names_hierarchy`.`id_sciname` = `species`.`id_sciname`) and ((`scientific_names_hierarchy`.`id_hierarchy` = 22) or (`scientific_names_hierarchy`.`id_hierarchy` = 23))) order by `scientific_names_hierarchy`.`id_hierarchy` limit 1) AS `subspecies`,(select `scientific_names_hierarchy`.`author` AS `author` from (`scientific_names_hierarchy` join `hierarchy_def` on((`scientific_names_hierarchy`.`id_hierarchy` = `hierarchy_def`.`id_hierarchy`))) where ((`scientific_names_hierarchy`.`id_sciname` = `species`.`id_sciname`) and (`scientific_names_hierarchy`.`author` is not null)) order by `hierarchy_def`.`seq` desc limit 1) AS `scientificnameauthor`,`identifiedby`.`name` AS `identifiedby`,date_format(`str_identification`.`date`,_utf8'%Y') AS `yearidentified`,date_format(`str_identification`.`date`,_utf8'%m') AS `monthidentified`,date_format(`str_identification`.`date`,_utf8'%d') AS `dayidentified`,`str_type_lang`.`type` AS `typestatus`,NULL AS `collectornumber`,NULL AS `fieldnumber`,`collector`.`name` AS `collector`,date_format(`str_coll_event`.`date`,_utf8'%Y') AS `yearcollected`,date_format(`str_coll_event`.`date`,_utf8'%m') AS `monthcollected`,date_format(`str_coll_event`.`date`,_utf8'%d') AS `daycollected`,NULL AS `julianday`,NULL AS `timeOfday`,NULL AS `continentocean`,`loc_country_lang`.`country` AS `country`,`loc_state`.`state` AS `stateprovince`,`loc_city`.`city` AS `county`,replace(`str_coll_event`.`place`,_utf8'<br />',_utf8' ') AS `locality`,`str_coll_event`.`gps_longitude` AS `longitude`,`str_coll_event`.`gps_latitude` AS `latitude`,`str_coll_event`.`gps_precision` AS `coordinateprecision`,NULL AS `boundingbox`,NULL AS `minimumelevation`,NULL AS `maximumelevation`,NULL AS `minimumdepth`,NULL AS `maximumdepth`,NULL AS `sex`,NULL AS `preparationtype`,NULL AS `individualcount`,NULL AS `previouscatalognumber`,`str_host_name`.`host_name` AS `relationshiptype`,NULL AS `relatedcatalogitem`,replace(`str_cha_catalogue`.`catalogue_notes`,_utf8'<br />',_utf8' ') AS `notes`,replace(`strain`.`history`,_utf8'<br />',_utf8' ') AS `historyofdeposit`,`depositor`.`name` AS `depositor`,date_format(`str_deposit`.`date`,_utf8'%Y') AS `yeardeposited`,date_format(`str_deposit`.`date`,_utf8'%m') AS `monthdeposited`,date_format(`str_deposit`.`date`,_utf8'%d') AS `daydeposited`,`str_substratum`.`substratum` AS `isolatedfrom`,`isolator`.`name` AS `isolator`,`str_iso_method`.`iso_method` AS `isolationmethod`,concat_ws(_utf8' ',(case when (`str_culture`.`temp` is not null) then concat_ws(_utf8' ',_utf8'Temp:',`str_culture`.`temp`) else NULL end),(case when (`str_culture`.`ph` is not null) then concat_ws(_utf8' ',_utf8'PH:',`str_culture`.`ph`) else NULL end)) AS `conditionsforgrowth`,`strain`.`is_ogm` AS `geneticallymodified`,`str_characs`.`genotypic` AS `genotype`,NULL AS `mutant`,NULL AS `race`,replace(replace(replace(replace(`alternative_names`.`sciname_no_auth`,_utf8'<b>',_utf8''),_utf8'<i>',_utf8''),_utf8'</b>',_utf8''),_utf8'</i>',_utf8'') AS `alternatestate`,`str_pro_properties`.`properties` AS `strainproperties`,`str_pro_applications`.`applications` AS `strainapplications`,NULL AS `formofsupply`,`str_cha_restrictions`.`restrictions` AS `restrictions`,`str_cha_biorisk_comments`.`biorisk_comments` AS `biologicalrisks`,`str_characs`.`pathogenic` AS `pathogenicity` from ((((((((((((((((((((((((((((`strain` left join `str_deposit` on(((`str_deposit`.`id_strain` = `strain`.`id_strain`) and (`str_deposit`.`id_coll` = `strain`.`id_coll`)))) left join `person` `depositor` on((`str_deposit`.`id_person` = `depositor`.`id_person`))) left join `species` on((`strain`.`id_species` = `species`.`id_species`))) left join `scientific_names` on((`species`.`id_sciname` = `scientific_names`.`id_sciname`))) left join `str_coll_event` on(((`str_coll_event`.`id_strain` = `strain`.`id_strain`) and (`str_coll_event`.`id_coll` = `strain`.`id_coll`)))) left join `person` `collector` on((`str_coll_event`.`id_person` = `collector`.`id_person`))) left join `str_identification` on(((`str_identification`.`id_coll` = `strain`.`id_coll`) and (`str_identification`.`id_strain` = `strain`.`id_strain`)))) left join `person` `identifiedby` on((`str_identification`.`id_person` = `identifiedby`.`id_person`))) left join `str_substratum` on(((`str_substratum`.`id_strain` = `strain`.`id_strain`) and (`str_substratum`.`id_coll` = `strain`.`id_coll`) and (`str_substratum`.`id_lang` = 2)))) left join `str_isolation` on(((`str_isolation`.`id_strain` = `strain`.`id_strain`) and (`str_isolation`.`id_coll` = `strain`.`id_coll`)))) left join `person` `isolator` on((`str_isolation`.`id_person` = `isolator`.`id_person`))) left join `str_iso_method` on(((`str_iso_method`.`id_strain` = `strain`.`id_strain`) and (`str_iso_method`.`id_coll` = `strain`.`id_coll`) and (`str_iso_method`.`id_lang` = 2)))) left join `str_culture` on(((`str_culture`.`id_strain` = `strain`.`id_strain`) and (`str_culture`.`id_coll` = `strain`.`id_coll`)))) left join `str_characs` on(((`str_characs`.`id_strain` = `strain`.`id_strain`) and (`str_characs`.`id_coll` = `strain`.`id_coll`)))) left join `str_pro_properties` on(((`str_pro_properties`.`id_strain` = `strain`.`id_strain`) and (`str_pro_properties`.`id_coll` = `strain`.`id_coll`) and (`str_pro_properties`.`id_lang` = 2)))) left join `str_pro_applications` on(((`str_pro_applications`.`id_strain` = `strain`.`id_strain`) and (`str_pro_applications`.`id_coll` = `strain`.`id_coll`) and (`str_pro_applications`.`id_lang` = 2)))) left join `str_cha_restrictions` on(((`str_cha_restrictions`.`id_strain` = `strain`.`id_strain`) and (`str_cha_restrictions`.`id_coll` = `strain`.`id_coll`) and (`str_cha_restrictions`.`id_lang` = 2)))) left join `str_cha_biorisk_comments` on(((`str_cha_biorisk_comments`.`id_strain` = `strain`.`id_strain`) and (`str_cha_biorisk_comments`.`id_coll` = `strain`.`id_coll`) and (`str_cha_biorisk_comments`.`id_lang` = 2)))) left join `str_cha_catalogue` on(((`str_cha_catalogue`.`id_strain` = `strain`.`id_strain`) and (`str_cha_catalogue`.`id_coll` = `strain`.`id_coll`) and (`str_cha_catalogue`.`id_lang` = 2)))) left join `str_host_name` on(((`str_host_name`.`id_strain` = `strain`.`id_strain`) and (`str_host_name`.`id_coll` = `strain`.`id_coll`) and (`str_host_name`.`id_lang` = 2)))) left join `taxon_group_lang` on(((`taxon_group_lang`.`id_taxon_group` = `species`.`id_taxon_group`) and (`taxon_group_lang`.`id_lang` = 2)))) left join `loc_country_lang` on(((`str_coll_event`.`id_country` = `loc_country_lang`.`id_country`) and (`loc_country_lang`.`id_lang` = 2)))) left join `loc_state` on((`str_coll_event`.`id_state` = `loc_state`.`id_state`))) left join `loc_city` on((`str_coll_event`.`id_city` = `loc_city`.`id_city`))) left join `species` `alternative` on((`species`.`id_alt_states` = `alternative`.`id_species`))) left join `scientific_names` `alternative_names` on((`alternative`.`id_sciname` = `alternative_names`.`id_sciname`))) left join `str_type_lang` on(((`strain`.`id_type` = `str_type_lang`.`id_type`) and (`str_type_lang`.`id_lang` = 2)))) join `roles_permissions` `rp` on(((`rp`.`id_item` = `strain`.`id_strain`) and (`rp`.`id_role` = 1) and (`rp`.`id_area` = 2)))) */;

--
-- Final view structure for view `species_report`
--

/*!50001 DROP TABLE `species_report`*/;
/*!50001 DROP VIEW IF EXISTS `species_report`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `species_report` AS select `s`.`id_species` AS `id_species`,`s`.`id_coll` AS `id_coll`,`s`.`id_subcoll` AS `id_subcoll`,`tgl`.`taxon_group` AS `taxon_group`,`sn`.`hi_tax` AS `hi_tax`,`sn`.`sciname` AS `sciname`,`sn`.`sciname_no_auth` AS `sciname_no_auth`,`s`.`taxon_ref` AS `taxon_ref`,`s`.`synonym` AS `synonym`,`s`.`hazard_group` AS `hazard_group`,`s`.`hazard_group_ref` AS `hazard_group_ref`,`sar`.`ambient_risk` AS `ambient_risk`,`snsas`.`sciname` AS `sciname_alt_state`,`s`.`alt_states_type` AS `alt_states_type`,`sc`.`comments` AS `comments` from (((((((`species` `s` join `taxon_group_lang` `tgl` on(((`s`.`id_taxon_group` = `tgl`.`id_taxon_group`) and (`tgl`.`id_lang` = `get_report_lang`())))) join `scientific_names` `sn` on((`s`.`id_sciname` = `sn`.`id_sciname`))) left join `spe_name_qualifier_lang` `snql` on(((`s`.`id_name_qualifier` = `snql`.`id_name_qualifier`) and (`snql`.`id_lang` = `get_report_lang`())))) left join `species` `sas` on((`s`.`id_alt_states` = `sas`.`id_species`))) left join `scientific_names` `snsas` on((`sas`.`id_sciname` = `snsas`.`id_sciname`))) left join `spe_ambient_risk` `sar` on(((`s`.`id_species` = `sar`.`id_species`) and (`sar`.`id_lang` = `get_report_lang`())))) left join `spe_comments` `sc` on(((`s`.`id_species` = `sc`.`id_species`) and (`sc`.`id_lang` = `get_report_lang`())))) */;

--
-- Final view structure for view `specieslinkdwc`
--

/*!50001 DROP TABLE `specieslinkdwc`*/;
/*!50001 DROP VIEW IF EXISTS `specieslinkdwc`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`sicol`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `specieslinkdwc` AS select `strain`.`id_strain` AS `record_uid`,`strain`.`last_update` AS `datelastmodified`,_latin1'Fiocruz' AS `institutioncode`,(case `strain`.`id_coll` when 1 then _latin1'CLIOC' when 2 then _latin1'CCBH' when 3 then _latin1'CCGB' when 4 then _latin1'CCFF' when 5 then _latin1'CMT' when 6 then _latin1'COLTRYP' when 7 then _latin1'CFP' when 8 then _latin1'CBMA' when 9 then _latin1'INCQS' when 10 then _latin1'CLIST' when 11 then _latin1'CCAMP' when 12 then _latin1'CENT' when 13 then _latin1'CLEP' when 14 then _latin1'COLPROT' when 15 then _latin1'CYP' when 16 then _latin1'CBAM' when 17 then _latin1'CFAM' else NULL end) AS `collectioncode`,`strain`.`id_subcoll` AS `subcollectioncode`,`strain`.`code` AS `catalognumber`,replace(replace(replace(replace(`scientific_names`.`sciname_no_auth`,_utf8'<b>',_utf8''),_utf8'<i>',_utf8''),_utf8'</b>',_utf8''),_utf8'</i>',_utf8'') AS `scientificname`,_latin1'L' AS `basisofrecord`,(select `scientific_names_hierarchy`.`value` AS `value` from `scientific_names_hierarchy` where ((`scientific_names_hierarchy`.`id_sciname` = `species`.`id_sciname`) and (`scientific_names_hierarchy`.`id_hierarchy` = 2))) AS `kingdom`,(select `scientific_names_hierarchy`.`value` AS `value` from `scientific_names_hierarchy` where ((`scientific_names_hierarchy`.`id_sciname` = `species`.`id_sciname`) and (`scientific_names_hierarchy`.`id_hierarchy` = 4))) AS `phylum`,(select `scientific_names_hierarchy`.`value` AS `value` from `scientific_names_hierarchy` where ((`scientific_names_hierarchy`.`id_sciname` = `species`.`id_sciname`) and (`scientific_names_hierarchy`.`id_hierarchy` = 9))) AS `class`,(select `scientific_names_hierarchy`.`value` AS `value` from `scientific_names_hierarchy` where ((`scientific_names_hierarchy`.`id_sciname` = `species`.`id_sciname`) and (`scientific_names_hierarchy`.`id_hierarchy` = 11))) AS `order`,(select `scientific_names_hierarchy`.`value` AS `value` from `scientific_names_hierarchy` where ((`scientific_names_hierarchy`.`id_sciname` = `species`.`id_sciname`) and (`scientific_names_hierarchy`.`id_hierarchy` = 14))) AS `family`,(select `scientific_names_hierarchy`.`value` AS `value` from `scientific_names_hierarchy` where ((`scientific_names_hierarchy`.`id_sciname` = `species`.`id_sciname`) and (`scientific_names_hierarchy`.`id_hierarchy` = 18))) AS `genus`,(select `scientific_names_hierarchy`.`value` AS `value` from `scientific_names_hierarchy` where ((`scientific_names_hierarchy`.`id_sciname` = `species`.`id_sciname`) and (`scientific_names_hierarchy`.`id_hierarchy` = 21))) AS `species`,(select `scientific_names_hierarchy`.`value` AS `value` from `scientific_names_hierarchy` where ((`scientific_names_hierarchy`.`id_sciname` = `species`.`id_sciname`) and ((`scientific_names_hierarchy`.`id_hierarchy` = 22) or (`scientific_names_hierarchy`.`id_hierarchy` = 23))) order by `scientific_names_hierarchy`.`id_hierarchy` limit 1) AS `subspecies`,(select `scientific_names_hierarchy`.`author` AS `author` from (`scientific_names_hierarchy` join `hierarchy_def` on((`scientific_names_hierarchy`.`id_hierarchy` = `hierarchy_def`.`id_hierarchy`))) where ((`scientific_names_hierarchy`.`id_sciname` = `species`.`id_sciname`) and (`scientific_names_hierarchy`.`author` is not null)) order by `hierarchy_def`.`seq` desc limit 1) AS `scientificnameauthor`,`identifiedby`.`name` AS `identifiedby`,date_format(`str_identification`.`date`,_latin1'%Y') AS `yearidentified`,date_format(`str_identification`.`date`,_latin1'%m') AS `monthidentified`,date_format(`str_identification`.`date`,_latin1'%d') AS `dayidentified`,`str_type_lang`.`type` AS `typestatus`,NULL AS `collectornumber`,NULL AS `fieldnumber`,`collector`.`name` AS `collector`,date_format(`str_coll_event`.`date`,_latin1'%Y') AS `yearcollected`,date_format(`str_coll_event`.`date`,_latin1'%m') AS `monthcollected`,date_format(`str_coll_event`.`date`,_latin1'%d') AS `daycollected`,NULL AS `julianday`,NULL AS `timeOfday`,NULL AS `continentocean`,`loc_country_lang`.`country` AS `country`,`loc_state`.`state` AS `stateprovince`,`loc_city`.`city` AS `county`,replace(`str_coll_event`.`place`,_utf8'<br />',_utf8' ') AS `locality`,`str_coll_event`.`gps_longitude` AS `longitude`,`str_coll_event`.`gps_latitude` AS `latitude`,`str_coll_event`.`gps_precision` AS `coordinateprecision`,NULL AS `boundingbox`,NULL AS `minimumelevation`,NULL AS `maximumelevation`,NULL AS `minimumdepth`,NULL AS `maximumdepth`,NULL AS `sex`,NULL AS `preparationtype`,NULL AS `individualcount`,`strain`.`extra_codes` AS `previouscatalognumber`,`str_host_name`.`host_name` AS `relationshiptype`,NULL AS `relatedcatalogitem`,replace(`str_cha_catalogue`.`catalogue_notes`,_utf8'<br />',_utf8' ') AS `notes`,replace(`strain`.`history`,_utf8'<br />',_utf8' ') AS `historyofdeposit`,`depositor`.`name` AS `depositor`,date_format(`str_deposit`.`date`,_latin1'%Y') AS `yeardeposited`,date_format(`str_deposit`.`date`,_latin1'%m') AS `monthdeposited`,date_format(`str_deposit`.`date`,_latin1'%d') AS `daydeposited`,`str_substratum`.`substratum` AS `isolatedfrom`,`isolator`.`name` AS `isolator`,`str_iso_method`.`iso_method` AS `isolationmethod`,concat_ws(_utf8' ',(case when (`str_culture`.`temp` is not null) then concat_ws(_utf8' ',_utf8'Temp:',`str_culture`.`temp`) else NULL end),(case when (`str_culture`.`ph` is not null) then concat_ws(_utf8' ',_utf8'PH:',`str_culture`.`ph`) else NULL end)) AS `conditionsforgrowth`,`strain`.`is_ogm` AS `geneticallymodified`,`str_characs`.`genotypic` AS `genotype`,NULL AS `mutant`,NULL AS `race`,replace(replace(replace(replace(`alternative_names`.`sciname_no_auth`,_utf8'<b>',_utf8''),_utf8'<i>',_utf8''),_utf8'</b>',_utf8''),_utf8'</i>',_utf8'') AS `alternatestate`,`str_pro_properties`.`properties` AS `strainproperties`,`str_pro_applications`.`applications` AS `strainapplications`,NULL AS `formofsupply`,`str_cha_restrictions`.`restrictions` AS `restrictions`,`str_cha_biorisk_comments`.`biorisk_comments` AS `biologicalrisks`,`str_characs`.`pathogenic` AS `pathogenicity` from ((((((((((((((((((((((((((((`strain` left join `str_deposit` on(((`str_deposit`.`id_strain` = `strain`.`id_strain`) and (`str_deposit`.`id_coll` = `strain`.`id_coll`)))) left join `person` `depositor` on((`str_deposit`.`id_person` = `depositor`.`id_person`))) left join `species` on((`strain`.`id_species` = `species`.`id_species`))) left join `scientific_names` on((`species`.`id_sciname` = `scientific_names`.`id_sciname`))) left join `str_coll_event` on(((`str_coll_event`.`id_strain` = `strain`.`id_strain`) and (`str_coll_event`.`id_coll` = `strain`.`id_coll`)))) left join `person` `collector` on((`str_coll_event`.`id_person` = `collector`.`id_person`))) left join `str_identification` on(((`str_identification`.`id_coll` = `strain`.`id_coll`) and (`str_identification`.`id_strain` = `strain`.`id_strain`)))) left join `person` `identifiedby` on((`str_identification`.`id_person` = `identifiedby`.`id_person`))) left join `str_substratum` on(((`str_substratum`.`id_strain` = `strain`.`id_strain`) and (`str_substratum`.`id_coll` = `strain`.`id_coll`) and (`str_substratum`.`id_lang` = 2)))) left join `str_isolation` on(((`str_isolation`.`id_strain` = `strain`.`id_strain`) and (`str_isolation`.`id_coll` = `strain`.`id_coll`)))) left join `person` `isolator` on((`str_isolation`.`id_person` = `isolator`.`id_person`))) left join `str_iso_method` on(((`str_iso_method`.`id_strain` = `strain`.`id_strain`) and (`str_iso_method`.`id_coll` = `strain`.`id_coll`) and (`str_iso_method`.`id_lang` = 2)))) left join `str_culture` on(((`str_culture`.`id_strain` = `strain`.`id_strain`) and (`str_culture`.`id_coll` = `strain`.`id_coll`)))) left join `str_characs` on(((`str_characs`.`id_strain` = `strain`.`id_strain`) and (`str_characs`.`id_coll` = `strain`.`id_coll`)))) left join `str_pro_properties` on(((`str_pro_properties`.`id_strain` = `strain`.`id_strain`) and (`str_pro_properties`.`id_coll` = `strain`.`id_coll`) and (`str_pro_properties`.`id_lang` = 2)))) left join `str_pro_applications` on(((`str_pro_applications`.`id_strain` = `strain`.`id_strain`) and (`str_pro_applications`.`id_coll` = `strain`.`id_coll`) and (`str_pro_applications`.`id_lang` = 2)))) left join `str_cha_restrictions` on(((`str_cha_restrictions`.`id_strain` = `strain`.`id_strain`) and (`str_cha_restrictions`.`id_coll` = `strain`.`id_coll`) and (`str_cha_restrictions`.`id_lang` = 2)))) left join `str_cha_biorisk_comments` on(((`str_cha_biorisk_comments`.`id_strain` = `strain`.`id_strain`) and (`str_cha_biorisk_comments`.`id_coll` = `strain`.`id_coll`) and (`str_cha_biorisk_comments`.`id_lang` = 2)))) left join `str_cha_catalogue` on(((`str_cha_catalogue`.`id_strain` = `strain`.`id_strain`) and (`str_cha_catalogue`.`id_coll` = `strain`.`id_coll`) and (`str_cha_catalogue`.`id_lang` = 2)))) left join `str_host_name` on(((`str_host_name`.`id_strain` = `strain`.`id_strain`) and (`str_host_name`.`id_coll` = `strain`.`id_coll`) and (`str_host_name`.`id_lang` = 2)))) left join `taxon_group_lang` on(((`taxon_group_lang`.`id_taxon_group` = `species`.`id_taxon_group`) and (`taxon_group_lang`.`id_lang` = 2)))) left join `loc_country_lang` on(((`str_coll_event`.`id_country` = `loc_country_lang`.`id_country`) and (`loc_country_lang`.`id_lang` = 2)))) left join `loc_state` on((`str_coll_event`.`id_state` = `loc_state`.`id_state`))) left join `loc_city` on((`str_coll_event`.`id_city` = `loc_city`.`id_city`))) left join `species` `alternative` on((`species`.`id_alt_states` = `alternative`.`id_species`))) left join `scientific_names` `alternative_names` on((`alternative`.`id_sciname` = `alternative_names`.`id_sciname`))) left join `str_type_lang` on(((`strain`.`id_type` = `str_type_lang`.`id_type`) and (`str_type_lang`.`id_lang` = 2)))) join `roles_permissions` `rp` on(((`rp`.`id_item` = `strain`.`id_strain`) and (`rp`.`id_role` = 1) and (`rp`.`id_area` = 2)))) where ((`strain`.`go_catalog` = 1) and (`strain`.`status` = _utf8'active') and (`str_deposit`.`id_dep_reason` = 1)) */;

--
-- Final view structure for view `stock_report`
--

/*!50001 DROP TABLE `stock_report`*/;
/*!50001 DROP VIEW IF EXISTS `stock_report`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `stock_report` AS select `s`.`id_subcoll` AS `id_subcoll`,`s`.`id_strain` AS `id_strain`,`s`.`code` AS `strain_code`,`s`.`numeric_code` AS `strain_numeric_code`,`sn`.`sciname` AS `taxon`,`pml`.`method` AS `preservation_method`,`l`.`name` AS `lot`,concat_ws(_latin1'-',`c`.`id_container`,`lsal`.`id_container_hierarchy`,`lsal`.`row`,`lsal`.`col`) AS `position`,`lsal`.`available_qt` AS `available_qt` from (((((((((`lot_strain_available_locations` `lsal` join `lot_strain` `ls` on(((`lsal`.`id_lot` = `ls`.`id_lot`) and (`lsal`.`id_strain` = `ls`.`id_strain`)))) join `strain` `s` on((`ls`.`id_strain` = `s`.`id_strain`))) join `lot` `l` on((`ls`.`id_lot` = `l`.`id_lot`))) join `preservation` `p` on((`l`.`id_lot` = `p`.`id_lot`))) join `preservation_method_lang` `pml` on(((`p`.`id_preservation_method` = `pml`.`id_preservation_method`) and (`pml`.`id_lang` = `get_report_lang`())))) join `species` `sp` on((`s`.`id_species` = `sp`.`id_species`))) join `scientific_names` `sn` on((`sp`.`id_sciname` = `sn`.`id_sciname`))) join `container_hierarchy` `ch` on((`lsal`.`id_container_hierarchy` = `ch`.`id_container_hierarchy`))) join `container` `c` on((`ch`.`id_container` = `c`.`id_container`))) */;

--
-- Final view structure for view `strain_report`
--

/*!50001 DROP TABLE `strain_report`*/;
/*!50001 DROP VIEW IF EXISTS `strain_report`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `strain_report` AS select `st`.`id_strain` AS `id_strain`,`st`.`id_subcoll` AS `id_subcoll`,`dv`.`division` AS `division`,`st`.`code` AS `code`,`st`.`numeric_code` AS `numeric_code`,`st`.`internal_code` AS `origin_code`,`st`.`status` AS `status`,`tgl`.`taxon_group` AS `taxon_group`,`sn`.`sciname` AS `taxon`,`stl`.`type` AS `type`,`st`.`is_ogm` AS `is_ogm`,`st`.`infra_complement` AS `taxonomic_complement`,`st`.`history` AS `history`,`st`.`extra_codes` AS `other_codes`,`st`.`comments` AS `general_comments`,`sce`.`date` AS `coll_date`,year(`sce`.`date`) AS `coll_year`,month(`sce`.`date`) AS `coll_month`,`p1`.`name` AS `coll_person`,`i1`.`name` AS `coll_institution`,`lcl`.`country` AS `country`,`ls`.`code` AS `state_code`,`ls`.`state` AS `state_name`,`lc`.`city` AS `city`,`sce`.`place` AS `place`,`sce`.`gps_latitude` AS `gps_latitude`,`sce`.`gps_latitude_dms` AS `gps_latitude_dms`,`sce`.`gps_latitude_mode` AS `gps_latitude_mode`,`sce`.`gps_longitude` AS `gps_longitude`,`sce`.`gps_longitude_dms` AS `gps_longitude_dms`,`sce`.`gps_longitude_mode` AS `gps_longitude_mode`,`sgd`.`gps_datum` AS `gps_datum`,`sce`.`gps_precision` AS `gps_precision`,`sce`.`gps_comments` AS `gps_comments`,`ss`.`substratum` AS `substratum`,`shn`.`host_name` AS `host_name`,`sce`.`host_genus` AS `host_genus`,`sce`.`host_species` AS `host_species`,`sce`.`host_classification` AS `host_level`,`sce`.`host_infra_name` AS `host_subspecies`,`sce`.`host_infra_complement` AS `host_taxonomic_complement`,`sce`.`global_code` AS `international_code`,`scfl`.`code` AS `clinical_form_code`,`scfl`.`clinical_form` AS `clinical_form_name`,`sce`.`hiv` AS `hiv`,`scc`.`comments` AS `coll_comments`,`si`.`date` AS `iso_date`,year(`si`.`date`) AS `iso_year`,month(`si`.`date`) AS `iso_month`,`p2`.`name` AS `iso_person`,`i2`.`name` AS `iso_institution`,`sif`.`isolation_from` AS `isolation_from`,`sim`.`iso_method` AS `iso_method`,`si`.`comments` AS `iso_comments`,`sid`.`date` AS `ident_date`,year(`sid`.`date`) AS `ident_year`,month(`sid`.`date`) AS `ident_month`,`p3`.`name` AS `ident_person`,`i3`.`name` AS `ident_institution`,`sid`.`genus` AS `ident_genus`,`sid`.`species` AS `ident_species`,`sid`.`classification` AS `ident_level`,`sid`.`infra_name` AS `ident_subspecies`,`sid`.`infra_complement` AS `ident_taxonomic_complement`,`sidm`.`ident_method` AS `ident_method`,`sid`.`comments` AS `ident_comments`,`sd`.`date` AS `dep_date`,year(`sd`.`date`) AS `dep_year`,month(`sd`.`date`) AS `dep_month`,`p4`.`name` AS `dep_person`,`i4`.`name` AS `dep_institution`,`sd`.`genus` AS `dep_genus`,`sd`.`species` AS `dep_species`,`sd`.`classification` AS `dep_level`,`sd`.`infra_name` AS `dep_subspecies`,`sd`.`infra_complement` AS `dep_taxonomic_complement`,`sdrl`.`dep_reason` AS `dep_reason`,`sd`.`form` AS `dep_form`,`sd`.`preserv_method` AS `recom_preserv_method`,`sd`.`aut_date` AS `aut_date`,year(`sd`.`aut_date`) AS `aut_year`,month(`sd`.`aut_date`) AS `aut_month`,`p5`.`name` AS `aut_person`,`sd`.`aut_result` AS `aut_result`,`sd`.`comments` AS `dep_comments`,`scm`.`medium` AS `recom_growth_medium`,`sc`.`temp` AS `recom_temp`,`sit`.`incub_time` AS `incubation_time`,`sc`.`ph` AS `ph`,`sor`.`oxy_req` AS `oxygen_requirements`,`scuc`.`comments` AS `grow_comments`,`sch`.`morphologic` AS `morphological_characteristics`,`sch`.`molecular` AS `molecular_characteristics`,`sch`.`biochemical` AS `biochemical_characteristics`,`sch`.`immunologic` AS `immunologic_characteristics`,`sch`.`pathogenic` AS `pathogenic_characteristics`,`sch`.`genotypic` AS `genotypic_characteristics`,`sch`.`ogm` AS `ogm`,`scoc`.`ogm_comments` AS `ogm_comments`,`scbc`.`biorisk_comments` AS `biorisk_comments`,`scr`.`restrictions` AS `restrictions`,`scp`.`pictures` AS `pictures`,`scu`.`urls` AS `charac_references`,`scca`.`catalogue_notes` AS `catalogue_notes`,`spp`.`properties` AS `properties`,`spa`.`applications` AS `applications`,`spu`.`urls` AS `prop_references`,`st`.`go_catalog` AS `go_catalog` from ((((((((((((((((((((((((((((((((((((((((((((((`strain` `st` join `division` `dv` on((`st`.`id_division` = `dv`.`id_division`))) join `species` `sp` on((`st`.`id_species` = `sp`.`id_species`))) join `taxon_group_lang` `tgl` on(((`sp`.`id_taxon_group` = `tgl`.`id_taxon_group`) and (`tgl`.`id_lang` = `get_report_lang`())))) join `scientific_names` `sn` on((`sp`.`id_sciname` = `sn`.`id_sciname`))) left join `str_type_lang` `stl` on(((`st`.`id_type` = `stl`.`id_type`) and (`stl`.`id_lang` = `get_report_lang`())))) left join `str_coll_event` `sce` on((`st`.`id_strain` = `sce`.`id_strain`))) left join `person` `p1` on((`sce`.`id_person` = `p1`.`id_person`))) left join `institution` `i1` on((`sce`.`id_institution` = `i1`.`id_institution`))) left join `loc_country_lang` `lcl` on(((`sce`.`id_country` = `lcl`.`id_country`) and (`lcl`.`id_lang` = `get_report_lang`())))) left join `loc_state` `ls` on((`sce`.`id_state` = `ls`.`id_state`))) left join `loc_city` `lc` on((`sce`.`id_city` = `lc`.`id_city`))) left join `str_gps_datum` `sgd` on((`sce`.`id_gps_datum` = `sgd`.`id_gps_datum`))) left join `str_substratum` `ss` on(((`st`.`id_strain` = `ss`.`id_strain`) and (`ss`.`id_lang` = `get_report_lang`())))) left join `str_host_name` `shn` on(((`st`.`id_strain` = `shn`.`id_strain`) and (`shn`.`id_lang` = `get_report_lang`())))) left join `str_clinical_form_lang` `scfl` on(((`sce`.`id_clinical_form` = `scfl`.`id_clinical_form`) and (`scfl`.`id_lang` = `get_report_lang`())))) left join `str_coll_comments` `scc` on(((`st`.`id_strain` = `scc`.`id_strain`) and (`scc`.`id_lang` = `get_report_lang`())))) left join `str_isolation` `si` on((`st`.`id_strain` = `si`.`id_strain`))) left join `person` `p2` on((`si`.`id_person` = `p2`.`id_person`))) left join `institution` `i2` on((`si`.`id_institution` = `i2`.`id_institution`))) left join `str_isolation_from` `sif` on(((`st`.`id_strain` = `sif`.`id_strain`) and (`sif`.`id_lang` = `get_report_lang`())))) left join `str_iso_method` `sim` on(((`si`.`id_strain` = `sim`.`id_strain`) and (`sim`.`id_lang` = `get_report_lang`())))) left join `str_identification` `sid` on((`st`.`id_strain` = `sid`.`id_strain`))) left join `person` `p3` on((`sid`.`id_person` = `p3`.`id_person`))) left join `institution` `i3` on((`sid`.`id_institution` = `i3`.`id_institution`))) left join `str_ident_method` `sidm` on(((`st`.`id_strain` = `sidm`.`id_strain`) and (`sidm`.`id_lang` = `get_report_lang`())))) left join `str_deposit` `sd` on((`st`.`id_strain` = `sd`.`id_strain`))) left join `person` `p4` on((`sd`.`id_person` = `p4`.`id_person`))) left join `institution` `i4` on((`sd`.`id_institution` = `i4`.`id_institution`))) left join `str_dep_reason_lang` `sdrl` on(((`sd`.`id_dep_reason` = `sdrl`.`id_dep_reason`) and (`sdrl`.`id_lang` = `get_report_lang`())))) left join `person` `p5` on((`sd`.`aut_person` = `p5`.`id_person`))) left join `str_culture` `sc` on((`st`.`id_strain` = `sc`.`id_strain`))) left join `str_cult_medium` `scm` on(((`st`.`id_strain` = `scm`.`id_strain`) and (`scm`.`id_lang` = `get_report_lang`())))) left join `str_incub_time` `sit` on(((`st`.`id_strain` = `sit`.`id_strain`) and (`sit`.`id_lang` = `get_report_lang`())))) left join `str_oxy_req` `sor` on(((`st`.`id_strain` = `sor`.`id_strain`) and (`sor`.`id_lang` = `get_report_lang`())))) left join `str_cult_comments` `scuc` on(((`st`.`id_strain` = `scuc`.`id_strain`) and (`scuc`.`id_lang` = `get_report_lang`())))) left join `str_characs` `sch` on((`st`.`id_strain` = `sch`.`id_strain`))) left join `str_cha_ogm_comments` `scoc` on(((`st`.`id_strain` = `scoc`.`id_strain`) and (`scoc`.`id_lang` = `get_report_lang`())))) left join `str_cha_biorisk_comments` `scbc` on(((`st`.`id_strain` = `scbc`.`id_strain`) and (`scbc`.`id_lang` = `get_report_lang`())))) left join `str_cha_restrictions` `scr` on(((`st`.`id_strain` = `scr`.`id_strain`) and (`scr`.`id_lang` = `get_report_lang`())))) left join `str_cha_pictures` `scp` on(((`st`.`id_strain` = `scp`.`id_strain`) and (`scp`.`id_lang` = `get_report_lang`())))) left join `str_cha_urls` `scu` on(((`st`.`id_strain` = `scu`.`id_strain`) and (`scu`.`id_lang` = `get_report_lang`())))) left join `str_cha_catalogue` `scca` on(((`st`.`id_strain` = `scca`.`id_strain`) and (`scca`.`id_lang` = `get_report_lang`())))) left join `str_properties` `spr` on((`st`.`id_strain` = `spr`.`id_strain`))) left join `str_pro_properties` `spp` on(((`st`.`id_strain` = `spp`.`id_strain`) and (`spp`.`id_lang` = `get_report_lang`())))) left join `str_pro_applications` `spa` on(((`st`.`id_strain` = `spa`.`id_strain`) and (`spa`.`id_lang` = `get_report_lang`())))) left join `str_pro_urls` `spu` on(((`st`.`id_strain` = `spu`.`id_strain`) and (`spu`.`id_lang` = `get_report_lang`())))) */;

--
-- Final view structure for view `used_origin`
--

/*!50001 DROP TABLE `used_origin`*/;
/*!50001 DROP VIEW IF EXISTS `used_origin`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `used_origin` AS select `distribution_origin_location`.`id_origin_lot` AS `id_origin_lot`,`distribution_origin_location`.`id_origin_container_hierarchy` AS `id_origin_container_hierarchy`,`distribution_origin_location`.`origin_row` AS `origin_row`,`distribution_origin_location`.`origin_col` AS `origin_col`,`distribution_origin_location`.`quantity` AS `used_qt` from `distribution_origin_location` union select `str_quality_origin_location`.`id_origin_lot` AS `id_origin_lot`,`str_quality_origin_location`.`id_origin_container_hierarchy` AS `id_origin_container_hierarchy`,`str_quality_origin_location`.`origin_row` AS `origin_row`,`str_quality_origin_location`.`origin_col` AS `origin_col`,`str_quality_origin_location`.`quantity` AS `used_qt` from `str_quality_origin_location` union select `preservation_strain_locations`.`id_lot` AS `id_origin_lot`,`preservation_strain_locations`.`id_origin_container_hierarchy` AS `id_origin_container_hierarchy`,`preservation_strain_locations`.`origin_row` AS `origin_row`,`preservation_strain_locations`.`origin_col` AS `origin_col`,`preservation_strain_locations`.`quantity` AS `used_qt` from `preservation_strain_locations` where (`preservation_strain_locations`.`origin_type` = _utf8'lot') */;

--
-- Final view structure for view `used_origin_all`
--

/*!50001 DROP TABLE `used_origin_all`*/;
/*!50001 DROP VIEW IF EXISTS `used_origin_all`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `used_origin_all` AS select _utf8'distribution' AS `origin`,`distribution_origin_location`.`id_origin_lot` AS `id_origin_lot`,`distribution_origin_location`.`id_origin_container_hierarchy` AS `id_origin_container_hierarchy`,`distribution_origin_location`.`origin_row` AS `origin_row`,`distribution_origin_location`.`origin_col` AS `origin_col`,`distribution_origin_location`.`quantity` AS `used_qt` from `distribution_origin_location` union select _utf8'quality' AS `origin`,`str_quality_origin_location`.`id_origin_lot` AS `id_origin_lot`,`str_quality_origin_location`.`id_origin_container_hierarchy` AS `id_origin_container_hierarchy`,`str_quality_origin_location`.`origin_row` AS `origin_row`,`str_quality_origin_location`.`origin_col` AS `origin_col`,`str_quality_origin_location`.`quantity` AS `used_qt` from `str_quality_origin_location` union select _utf8'preservation' AS `origin`,`preservation_strain_locations`.`id_lot` AS `id_origin_lot`,`preservation_strain_locations`.`id_origin_container_hierarchy` AS `id_origin_container_hierarchy`,`preservation_strain_locations`.`origin_row` AS `origin_row`,`preservation_strain_locations`.`origin_col` AS `origin_col`,`preservation_strain_locations`.`quantity` AS `used_qt` from (`preservation_strain_locations` join `preservation_strain` `ps` on(((`ps`.`id_preservation` = `preservation_strain_locations`.`id_preservation`) and (`ps`.`id_strain` = `preservation_strain_locations`.`id_strain`)))) where (`ps`.`origin_type` = _utf8'lot') */;

--
-- Final view structure for view `view_hierarchy`
--

/*!50001 DROP TABLE `view_hierarchy`*/;
/*!50001 DROP VIEW IF EXISTS `view_hierarchy`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `view_hierarchy` AS select `hd`.`id_hierarchy` AS `id_hierarchy`,`hg`.`id_taxon_group` AS `id_taxon_group`,`hg`.`id_subcoll` AS `id_subcoll`,`hd`.`seq` AS `seq`,`hl`.`id_lang` AS `id_lang`,`hl`.`rank` AS `rank`,(case when isnull(`hg`.`hi_tax`) then `hd`.`hi_tax` else `hg`.`hi_tax` end) AS `hi_tax`,(case when isnull(`hg`.`has_author`) then `hd`.`has_author` else `hg`.`has_author` end) AS `has_author`,(case when isnull(`hg`.`use_author`) then `hd`.`use_author` else `hg`.`use_author` end) AS `use_author`,(case when isnull(`hg`.`in_sciname`) then `hd`.`in_sciname` else `hg`.`in_sciname` end) AS `in_sciname`,(case when isnull(`hg`.`required`) then `hd`.`required` else `hg`.`required` end) AS `required`,(case when isnull(`hg`.`important`) then `hd`.`important` else `hg`.`important` end) AS `important`,(case when isnull(`hg`.`string_format`) then `hd`.`string_format` else `hg`.`string_format` end) AS `string_format`,(case when isnull(`hg`.`string_case`) then `hd`.`string_case` else `hg`.`string_case` end) AS `string_case`,(case when isnull(`hg`.`prefix`) then `hd`.`prefix` else `hg`.`prefix` end) AS `prefix`,(case when isnull(`hg`.`suffix`) then `hd`.`suffix` else `hg`.`suffix` end) AS `suffix`,`hg`.`default_value` AS `default_value` from ((`hierarchy_group` `hg` join `hierarchy_def` `hd` on((`hg`.`id_hierarchy` = `hd`.`id_hierarchy`))) join `hierarchy_lang` `hl` on((`hd`.`id_hierarchy` = `hl`.`id_hierarchy`))) */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-07-24 19:48:42
