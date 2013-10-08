-- MySQL Administrator dump 1.4
--
-- ------------------------------------------------------
-- Server version	5.0.27-community-nt

USE sicol_v110;
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
INSERT INTO `sicol_v110`.`doc_qualifier` (`id_qualifier`,`qualifier`) VALUES 
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
INSERT INTO `sicol_v110`.`lang` (`id_lang`,`code`,`lang`,`lang_en`) VALUES 
 (1,'en','English','English'),
 (2,'ptbr','Brazilian Portuguese','Português Brasileiro');
/*!40000 ALTER TABLE `lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `loc_city` DISABLE KEYS */;
/*!40000 ALTER TABLE `loc_city` ENABLE KEYS */;

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
INSERT INTO `sicol_v110`.`taxon_group` (`id_taxon_group`) VALUES
 (1),
 (2),
 (3),
 (4),
 (5);
/*!40000 ALTER TABLE `taxon_group` ENABLE KEYS */;

/*!40000 ALTER TABLE `taxon_group_subcoll` DISABLE KEYS */;
INSERT INTO `sicol_v110`.`taxon_group_subcoll` (`id_taxon_group`,`id_subcoll`) VALUES
 (5,1)
;
/*!40000 ALTER TABLE `taxon_group_subcoll` ENABLE KEYS */;

/*!40000 ALTER TABLE `taxon_group_lang` DISABLE KEYS */;
INSERT INTO `sicol_v110`.`taxon_group_lang` (`id_taxon_group`,`id_lang`,`taxon_group`) VALUES
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

/*!40000 ALTER TABLE `str_coll_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_coll_comments` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_coll_event` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_coll_event` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_cult_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_cult_comments` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_culture` DISABLE KEYS */;
/*!40000 ALTER TABLE `str_culture` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_dep_reason` DISABLE KEYS */;
INSERT INTO `sicol_v110`.`str_dep_reason` (`id_dep_reason`) VALUES 
 (1),
 (2),
 (3);
/*!40000 ALTER TABLE `str_dep_reason` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_dep_reason_subcoll` DISABLE KEYS */;
INSERT INTO `sicol_v110`.`str_dep_reason_subcoll` (`id_dep_reason`,`id_subcoll`) VALUES 
 (1,1),
 (2,1),
 (3,1);
/*!40000 ALTER TABLE `str_dep_reason_subcoll` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_dep_reason_lang` DISABLE KEYS */;
INSERT INTO `sicol_v110`.`str_dep_reason_lang` (`id_dep_reason`,`id_lang`,`dep_reason`) VALUES 
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
INSERT INTO `sicol_v110`.`str_type` (`id_type`) VALUES 
 (1),
 (2),
 (3);
/*!40000 ALTER TABLE `str_type` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_type_subcoll` DISABLE KEYS */;
INSERT INTO `sicol_v110`.`str_type_subcoll` (`id_type`,`id_subcoll`) VALUES 
 (1,1),
 (2,1),
 (3,1);
/*!40000 ALTER TABLE `str_type_subcoll` ENABLE KEYS */;

/*!40000 ALTER TABLE `str_type_lang` DISABLE KEYS */;
INSERT INTO `sicol_v110`.`str_type_lang` (`id_type`,`id_lang`,`type`) VALUES 
 (1,1,'Reference'),
 (1,2,'Referência'),
 (2,1,'Type'),
 (2,2,'Tipo'),
 (3,1,'Genotype'),
 (3,2,'Genotipo');
/*!40000 ALTER TABLE `str_type_lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `preservation_method` DISABLE KEYS */;
INSERT INTO `sicol_v110`.`preservation_method` (`id_preservation_method`) VALUES 
 (1),
 (2),
 (3),
 (4),
 (5);
/*!40000 ALTER TABLE `preservation_method` ENABLE KEYS */;

/*!40000 ALTER TABLE `preservation_method_subcoll` DISABLE KEYS */;
INSERT INTO `sicol_v110`.`preservation_method_subcoll` (`id_preservation_method`,`id_subcoll`) VALUES 
 (2,1);
/*!40000 ALTER TABLE `preservation_method_subcoll` ENABLE KEYS */;

/*!40000 ALTER TABLE `preservation_method_lang` DISABLE KEYS */;
INSERT INTO `sicol_v110`.`preservation_method_lang` (`id_preservation_method`,`id_lang`,`method`,`unit_measure`) VALUES 
 (1,1,'Liophilization','Ampoules'),
 (1,2,'Liofilização','Ampolas'),
 (2,1,'Cryopreservation','Ampoules'),
 (2,2,'Criopreservação','Ampolas');
/*!40000 ALTER TABLE `preservation_method_lang` ENABLE KEYS */;

/*!40000 ALTER TABLE `test_group` DISABLE KEYS */;
INSERT INTO `sicol_v110`.`test_group` (`id_test_group`) VALUES 
 (1),
 (2);
/*!40000 ALTER TABLE `test_group` ENABLE KEYS */;

/*!40000 ALTER TABLE `test_group_subcoll` DISABLE KEYS */;
INSERT INTO `sicol_v110`.`test_group_subcoll` (`id_test_group`,`id_subcoll`) VALUES 
 (1,1),
 (2,1);
/*!40000 ALTER TABLE `test_group_subcoll` ENABLE KEYS */;

/*!40000 ALTER TABLE `test_group_lang` DISABLE KEYS */;
INSERT INTO `sicol_v110`.`test_group_lang` (`id_test_group`,`id_lang`,`category`) VALUES 
 (1,1,'Parasitologic Test'),
 (1,2,'Exame Parasitológico'),
 (2,1,'Molecular Characterization'),
 (2,2,'Caracterização Molecular');
/*!40000 ALTER TABLE `test_group_lang` ENABLE KEYS */;


/*!40000 ALTER TABLE `str_gps_datum` DISABLE KEYS */;
INSERT INTO `sicol_v110`.`str_gps_datum` (`id_gps_datum`,`gps_datum`) VALUES 
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
(8,'distribution','Distribution Tab'),
(9,'reports','Reports Tab');
/*!40000 ALTER TABLE `system_areas` ENABLE KEYS */;

-- Insert "ALL" role, "Administrator" level and "Standard System User" in database
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO roles(id_role,name,type) VALUES 
(1,'all','all'),
(2,'Administrator','level'),
(3,'Usuario Padrao do Sistema','user'),
(4,'Curador','level');
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
INSERT INTO areas_permissions(id_role,id_area,allow_delete,allow_create)
	VALUES (2,1,'y','y'),(2,2,'y','y'),(2,3,'y','y'),(2,4,'y','y'),(2,5,'y','y'),(2,6,'y','y'),(2,7,'y','y'),(2,8,'y','y'),(2,9,'y','y');
/*!40000 ALTER TABLE `areas_permissions` ENABLE KEYS */;


-- The Curador role has create/delete permissions to all areas
/*!40000 ALTER TABLE `areas_permissions` DISABLE KEYS */;
INSERT INTO areas_permissions(id_role,id_area,allow_delete,allow_create)
	VALUES (4,1,'y','y'),(4,2,'y','y'),(4,3,'y','y'),(4,4,'y','y'),(4,5,'y','y'),(4,6,'y','y'),(4,7,'y','y'),(4,8,'y','y'),(4,9,'y','y');
/*!40000 ALTER TABLE `areas_permissions` ENABLE KEYS */;

--
-- Dumping data for table `report_types`
--

LOCK TABLES `report_types` WRITE;
/*!40000 ALTER TABLE `report_types` DISABLE KEYS */;
INSERT INTO `report_types` VALUES (1,'species','<?xml version=\"1.0\" encoding=\"UTF-8\"?><fields><field name=\"id_species\" label=\"label_Rep_Spe_ID\" data_type=\"integer\" aggregate_function=\"count\" /><field name=\"taxon_group\" label=\"label_Rep_Spe_Taxon_Group\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"hi_tax\" label=\"label_Rep_Spe_Hi_Tax\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"sciname\" label=\"label_Rep_Spe_Sciname\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"sciname_no_auth\" label=\"label_Rep_Spe_Sciname_No_Auth\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"taxon_ref\" label=\"label_Rep_Spe_Taxon_Ref\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"synonym\" label=\"label_Rep_Spe_Synonym\" data_type=\"text\" aggregate_function=\"count\"/><field name=\"hazard_group\" label=\"label_Rep_Spe_Hazard_Group\" data_type=\"enum\" aggregate_function=\"count\" label_value_lookup=\"true\" /><field name=\"hazard_group_ref\" label=\"label_Rep_Spe_Hazard_Group_Ref\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"ambient_risk\" label=\"label_Rep_Spe_Ambient_Risk\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"sciname_alt_state\" label=\"label_Rep_Spe_Sciname_Alt_State\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"alt_states_type\" label=\"label_Rep_Spe_Alt_States_Type\" data_type=\"enum\" aggregate_function=\"count\" label_value_lookup=\"true\" /><field name=\"comments\" label=\"label_Rep_Spe_Comments\" data_type=\"text\" aggregate_function=\"count\" /></fields>'),(2,'strain','<?xml version=\"1.0\" encoding=\"UTF-8\"?><fields><field name=\"id\" label=\"label_Rep_ID\" data_type=\"integer\" aggregate_function=\"count\" /><field name=\"division\" label=\"label_Rep_Division\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"code\" label=\"label_Rep_Code\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"numeric_code\" label=\"label_Rep_Numeric_Code\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"origin_code\" label=\"label_Rep_Origin_Code\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"status\" label=\"label_Rep_Status\" data_type=\"enum\" aggregate_function=\"count\" label_value_lookup=\"true\"/><field name=\"taxon_group\" label=\"label_Rep_Taxon_Group\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"taxon\" label=\"label_Rep_Taxon\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"type\" label=\"label_Rep_Type\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"is_ogm\" label=\"label_Rep_Is_Ogm\" data_type=\"tinyint\" aggregate_function=\"count\" label_value_lookup=\"true\" /><field name=\"taxonomic_complement\" label=\"label_Rep_Taxonomic_Complement\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"history\" label=\"label_Rep_History\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"other_codes\" label=\"label_Rep_Other_Codes\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"general_comments\" label=\"label_Rep_General_Comments\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"coll_date\" label=\"label_Rep_Collect_Date\" data_type=\"date\" aggregate_function=\"count\" /><field name=\"coll_year\" label=\"label_Rep_Collect_Year\" data_type=\"integer\" aggregate_function=\"count\" /><field name=\"coll_month\" label=\"label_Rep_Collect_Month\" data_type=\"integer\" aggregate_function=\"count\"  label_value_lookup=\"true\"/><field name=\"coll_person\" label=\"label_Rep_Collect_Person\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"coll_institution\" label=\"label_Rep_Collect_Institution\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"country\" label=\"label_Rep_Country\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"state_code\" label=\"label_Rep_State_Code\" data_type=\"char\" aggregate_function=\"count\" /><field name=\"state_name\" label=\"label_Rep_State_Name\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"city\" label=\"label_Rep_City\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"place\" label=\"label_Rep_Place\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"gps_latitude\" label=\"label_Rep_Latitude\" data_type=\"decimal\" aggregate_function=\"count\" /><field name=\"gps_latitude_dms\" label=\"label_Rep_Latitude_DMS\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"gps_latitude_mode\" label=\"label_Rep_Latitude_Mode\" data_type=\"enum\" aggregate_function=\"count\" label_value_lookup=\"true\"/><field name=\"gps_longitude\" label=\"label_Rep_Longitude\" data_type=\"decimal\" aggregate_function=\"count\" /><field name=\"gps_longitude_dms\" label=\"label_Rep_Longitude_DMS\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"gps_longitude_mode\" label=\"label_Rep_Longitude_Mode\" data_type=\"enum\" aggregate_function=\"count\" label_value_lookup=\"true\"/><field name=\"gps_datum\" label=\"label_Rep_Datum\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"gps_precision\" label=\"label_Rep_GPS_Precision\" data_type=\"integer\" aggregate_function=\"count\" /><field name=\"gps_comments\" label=\"label_Rep_GPS_Comments\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"substratum\" label=\"label_Rep_Substratum\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"host_name\" label=\"label_Rep_Host_Name\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"host_genus\" label=\"label_Rep_Host_Genus\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"host_species\" label=\"label_Rep_Host_Species\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"host_level\" label=\"label_Rep_Host_Level\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"host_subspecies\" label=\"label_Rep_Host_Subspecies\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"host_taxonomic_complement\" label=\"label_Rep_Host_Taxonomic_Complement\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"international_code\" label=\"label_Rep_International_Code\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"clinical_form_code\" label=\"label_Rep_Clinical_Form_Code\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"clinical_form_name\" label=\"label_Rep_Clinical_Form_Name\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"hiv\" label=\"label_Rep_HIV\" data_type=\"enum\" aggregate_function=\"count\" label_value_lookup=\"true\"/><field name=\"coll_comments\" label=\"label_Rep_Collect_Comments\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"iso_date\" label=\"label_Rep_Isolation_Date\" data_type=\"date\" aggregate_function=\"count\" /><field name=\"iso_year\" label=\"label_Rep_Isolation_Year\" data_type=\"integer\" aggregate_function=\"count\" /><field name=\"iso_month\" label=\"label_Rep_Isolation_Month\" data_type=\"integer\" aggregate_function=\"count\"  label_value_lookup=\"true\"/><field name=\"iso_person\" label=\"label_Rep_Isolation_Person\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"iso_institution\" label=\"label_Rep_Isolation_Institution\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"isolation_from\" label=\"label_Rep_Isolation_From\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"iso_method\" label=\"label_Rep_Isolation_Method\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"iso_comments\" label=\"label_Rep_Isolation_Comments\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"ident_date\" label=\"label_Rep_Identification_Date\" data_type=\"date\" aggregate_function=\"count\" /><field name=\"ident_year\" label=\"label_Rep_Identification_Year\" data_type=\"integer\" aggregate_function=\"count\" /><field name=\"ident_month\" label=\"label_Rep_Identification_Month\" data_type=\"integer\" aggregate_function=\"count\"  label_value_lookup=\"true\"/><field name=\"ident_person\" label=\"label_Rep_Identification_Person\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"ident_institution\" label=\"label_Rep_Identification_Institution\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"ident_genus\" label=\"label_Rep_Identification_Genus\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"ident_species\" label=\"label_Rep_Identification_Species\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"ident_level\" label=\"label_Rep_Identification_Level\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"ident_subspecies\" label=\"label_Rep_Identification_Subspecies\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"ident_taxonomic_complement\" label=\"label_Rep_Identification_Taxonomic_Complement\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"ident_method\" label=\"label_Rep_Identification_Method\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"ident_comments\" label=\"label_Rep_Identification_Comments\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"dep_date\" label=\"label_Rep_Deposit_Date\" data_type=\"date\" aggregate_function=\"count\" /><field name=\"dep_year\" label=\"label_Rep_Deposit_Year\" data_type=\"integer\" aggregate_function=\"count\" /><field name=\"dep_month\" label=\"label_Rep_Deposit_Month\" data_type=\"integer\" aggregate_function=\"count\"  label_value_lookup=\"true\"/><field name=\"dep_person\" label=\"label_Rep_Deposit_Person\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"dep_institution\" label=\"label_Rep_Deposit_Institution\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"dep_genus\" label=\"label_Rep_Deposit_Genus\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"dep_species\" label=\"label_Rep_Deposit_Species\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"dep_level\" label=\"label_Rep_Deposit_Level\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"dep_subspecies\" label=\"label_Rep_Deposit_Subspecies\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"dep_taxonomic_complement\" label=\"label_Rep_Deposit_Taxonomic_Complement\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"dep_reason\" label=\"label_Rep_Deposit_Reason\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"dep_form\" label=\"label_Rep_Deposit_Form\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"recom_preserv_method\" label=\"label_Rep_Recommended_Preservation_Method\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"aut_date\" label=\"label_Rep_Authentication_Date\" data_type=\"datetime\" aggregate_function=\"count\" /><field name=\"aut_year\" label=\"label_Rep_Authentication_Year\" data_type=\"integer\" aggregate_function=\"count\" /><field name=\"aut_month\" label=\"label_Rep_Authentication_Month\" data_type=\"integer\" aggregate_function=\"count\"  label_value_lookup=\"true\"/><field name=\"aut_person\" label=\"label_Rep_Authentication_Person\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"aut_result\" label=\"label_Rep_Authentication_Result\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"dep_comments\" label=\"label_Rep_Deposit_Comments\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"recom_growth_medium\" label=\"label_Rep_Recommended_Growth_Medium\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"recom_temp\" label=\"label_Rep_Recommended_Temperature\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"incubation_time\" label=\"label_Rep_Incubation_Time\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"ph\" label=\"label_Rep_PH\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"oxygen_requirements\" label=\"label_Rep_Oxygen_Requirements\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"grow_comments\" label=\"label_Rep_Growth_Comments\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"morphological_characteristics\" label=\"label_Rep_Morphological_Characteristics\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"molecular_characteristics\" label=\"label_Rep_Molecular_Characteristics\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"biochemical_characteristics\" label=\"label_Rep_Biochemical_Characteristics\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"immunologic_characteristics\" label=\"label_Rep_Immunologic_Characteristics\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"pathogenic_characteristics\" label=\"label_Rep_Pathogenic_Characteristics\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"genotypic_characteristics\" label=\"label_Rep_Genotypic_Characteristics\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"ogm\" label=\"label_Rep_OGM\" data_type=\"enum\" aggregate_function=\"count\" label_value_lookup=\"true\"/><field name=\"ogm_comments\" label=\"label_Rep_OGM_Comments\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"biorisk_comments\" label=\"label_Rep_Biorisk_Comments\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"restrictions\" label=\"label_Rep_Restrictions\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"pictures\" label=\"label_Rep_Pictures\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"charac_references\" label=\"label_Rep_Characteristics_References\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"catalogue_notes\" label=\"label_Rep_Catalogue_Notes\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"properties\" label=\"label_Rep_Properties\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"applications\" label=\"label_Rep_Applications\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"prop_references\" label=\"label_Rep_Properties_References\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"go_catalog\" label=\"label_Rep_Go_Catalog\" data_type=\"tinyint\" aggregate_function=\"count\" label_value_lookup=\"true\" />/fields>'),(3,'institution','<?xml version=\"1.0\" encoding=\"UTF-8\"?><fields><field name=\"id_institution\" label=\"label_Rep_Inst_ID\" data_type=\"integer\" aggregate_function=\"count\" /><field name=\"code1\" label=\"label_Rep_Inst_Code1\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"code2\" label=\"label_Rep_Inst_Code2\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"code3\" label=\"label_Rep_Inst_Code3\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"complement\" label=\"label_Rep_Inst_Complement\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"nickname\" label=\"label_Rep_Inst_Nickname\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"name\" label=\"label_Rep_Inst_Name\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"address\" label=\"label_Rep_Inst_Address\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"phone\" label=\"label_Rep_Inst_Phone\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"email\" label=\"label_Rep_Inst_Email\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"website\" label=\"label_Rep_Inst_Website\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"go_catalog\" label=\"label_Rep_Inst_Go_Catalog\" data_type=\"integer\" aggregate_function=\"count\"  label_value_lookup=\"true\"/><field name=\"comments\" label=\"label_Rep_Inst_Comments\" data_type=\"text\" aggregate_function=\"count\" /></fields>'),(4,'person','<?xml version=\"1.0\" encoding=\"UTF-8\"?><fields><field name=\"id_person\" label=\"label_Rep_Per_ID\" data_type=\"integer\" aggregate_function=\"count\" /><field name=\"name\" label=\"label_Rep_Per_Name\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"nickname\" label=\"label_Rep_Per_Nickname\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"address\" label=\"label_Rep_Per_Address\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"phone\" label=\"label_Rep_Per_Phone\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"email\" label=\"label_Rep_Per_Email\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"go_catalog\" label=\"label_Rep_Per_Go_Catalog\" data_type=\"integer\" aggregate_function=\"count\"  label_value_lookup=\"true\"/><field name=\"comments\" label=\"label_Rep_Per_Comments\" data_type=\"text\" aggregate_function=\"count\" /></fields>'),(5,'doc','<?xml version=\"1.0\" encoding=\"UTF-8\"?><fields><field name=\"id_doc\" label=\"label_Rep_Doc_ID\" data_type=\"integer\" aggregate_function=\"count\" /><field name=\"code\" label=\"label_Rep_Doc_Code\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"qualifier\" label=\"label_Rep_Doc_Qualifier\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"title\" label=\"label_Rep_Doc_Title\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"description\" label=\"label_Rep_Doc_Description\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"file_name\" label=\"label_Rep_Doc_File_Name\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"category\" label=\"label_Rep_Doc_Category\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"go_catalog\" label=\"label_Rep_Doc_Go_Catalog\" data_type=\"integer\" aggregate_function=\"count\"  label_value_lookup=\"true\"/></fields>'),(6,'ref','<?xml version=\"1.0\" encoding=\"UTF-8\"?><fields><field name=\"id_ref\" label=\"label_Rep_Ref_Code\" data_type=\"integer\" aggregate_function=\"count\" /><field name=\"title\" label=\"label_Rep_Ref_Title\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"author\" label=\"label_Rep_Ref_Author\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"year\" label=\"label_Rep_Ref_Year\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"url\" label=\"label_Rep_Ref_Url\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"comments\" label=\"label_Rep_Ref_Comments\" data_type=\"text\" aggregate_function=\"count\" /><field name=\"go_catalog\" label=\"label_Rep_Ref_Go_Catalog\" data_type=\"integer\" aggregate_function=\"count\"  label_value_lookup=\"true\"/></fields>'),(7,'stock','<?xml version=\"1.0\" encoding=\"UTF-8\"?><fields><field name=\"strain_code\" label=\"label_Rep_Stock_Strain_Code\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"strain_numeric_code\" label=\"label_Rep_Stock_Strain_Numeric_Code\" data_type=\"int\" aggregate_function=\"count\" /><field name=\"taxon\" label=\"label_Rep_Stock_Taxon\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"preservation_method\" label=\"label_Rep_Stock_Preservation_Method\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"lot\" label=\"label_Rep_Stock_Lot\" data_type=\"varchar\" aggregate_function=\"count\" /><field name=\"position\" label=\"label_Rep_Stock_Position\" data_type=\"varchar\" aggregate_function=\"count\" function_lookup=\"get_location\" /><field name=\"available_qt\" label=\"label_Rep_Stock_Quantity\" data_type=\"int\" aggregate_function=\"sum\" /></fields>');
/*!40000 ALTER TABLE `report_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `report_types_lang`
--

LOCK TABLES `report_types_lang` WRITE;
/*!40000 ALTER TABLE `report_types_lang` DISABLE KEYS */;
INSERT INTO `report_types_lang` VALUES (1,1,'Taxon'),(1,2,'Taxon'),(2,1,'Strain'),(2,2,'Linhagem'),(3,1,'Institution'),(3,2,'Instituição'),(4,1,'Person'),(4,2,'Pessoa'),(5,1,'Document'),(5,2,'Documento'),(6,1,'Reference'),(6,2,'Referência'),(7,1,'Stock'),(7,2,'Estoque');
/*!40000 ALTER TABLE `report_types_lang` ENABLE KEYS */;
UNLOCK TABLES;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
