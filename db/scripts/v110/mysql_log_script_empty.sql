DROP DATABASE IF EXISTS sicol_v110_log;
CREATE DATABASE IF NOT EXISTS sicol_v110_log CHARACTER SET utf8;
USE sicol_v110_log;

-- MySQL dump 10.11
--
-- Host: localhost    Database: sicol_v110_clioc_log
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
-- Table structure for table `log`
--

DROP TABLE IF EXISTS `log`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `log` (
  `id_log` bigint(20) unsigned NOT NULL auto_increment,
  `date_time` datetime NOT NULL,
  `user` varchar(255) NOT NULL,
  `id_log_operation` int(10) unsigned NOT NULL,
  `id_subcoll` tinyint(3) unsigned NOT NULL,
  `id_log_entity` int(10) unsigned NOT NULL,
  `id_entity` int(10) unsigned NOT NULL,
  `code_entity` varchar(255) NOT NULL,
  `lot` varchar(255) default NULL,
  `id_log_field` int(10) unsigned default NULL,
  `lang` varchar(10) default NULL,
  `value` text,
  PRIMARY KEY  (`id_log`),
  KEY `FK_log_operation` (`id_log_operation`),
  KEY `FK_log_entity` (`id_log_entity`),
  KEY `FK_log_field` (`id_log_field`),
  CONSTRAINT `log_ibfk_1` FOREIGN KEY (`id_log_operation`) REFERENCES `log_operations` (`id_log_operation`),
  CONSTRAINT `log_ibfk_2` FOREIGN KEY (`id_log_entity`) REFERENCES `log_entities` (`id_log_entity`),
  CONSTRAINT `log_ibfk_3` FOREIGN KEY (`id_log_field`) REFERENCES `log_fields` (`id_log_field`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `log_entities`
--

DROP TABLE IF EXISTS `log_entities`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `log_entities` (
  `id_log_entity` int(10) unsigned NOT NULL,
  `label` varchar(100) NOT NULL,
  PRIMARY KEY  (`id_log_entity`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `log_fields`
--

DROP TABLE IF EXISTS `log_fields`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `log_fields` (
  `id_log_field` int(10) unsigned NOT NULL,
  `label` varchar(100) NOT NULL,
  `mlang_value` tinyint(1) NOT NULL default '0' COMMENT '0 = false, 1 = true',
  `mlang_table` varchar(100) default NULL,
  `mlang_key` varchar(100) default NULL,
  `mlang_field` varchar(100) default NULL,
  `label_value_lookup` varchar(100) default NULL,
  PRIMARY KEY  (`id_log_field`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `log_operations`
--

DROP TABLE IF EXISTS `log_operations`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `log_operations` (
  `id_log_operation` int(10) unsigned NOT NULL,
  `label` varchar(100) NOT NULL,
  PRIMARY KEY  (`id_log_operation`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Dumping routines for database 'sicol_v110_clioc_log'
--
DELIMITER ;;
DELIMITER ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-07-24 19:49:41
