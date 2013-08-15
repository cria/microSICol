/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

SET FOREIGN_KEY_CHECKS=0;

USE `sicol_v109`;

INSERT INTO `container` (`id_container`, `id_coll`, `abbreviation`, `description`) VALUES 
  (1,1,'CAN','Cânister'),
  (2,1,'ARM','Armario'),
  (3,1,'ULT','Ultrafreezer');
COMMIT;

INSERT INTO `container_hierarchy` (`id_container_hierarchy`, `id_container`, `id_parent`, `abbreviation`, `description`) VALUES 
  (1,1,NULL,'CBN1','Cânister 1'),
  (2,1,NULL,'CBN2','Cânister 2'),
  (3,1,NULL,'CBN3','Cânister 3'),
  (4,1,1,'CCN11','Cânister 1-1'),
  (5,1,1,'CCN12','Cânister 1-2'),
  (6,1,2,'CCN21','Cânister 2-1'),
  (7,1,2,'CCN22','Cânister 2-2'),
  (8,1,3,'CCN31','Cânister 3-1'),
  (9,1,3,'CCN32','Cânister 3-2'),
  (10,2,NULL,'ARM1','Armário 1'),
  (11,2,NULL,'ARM2','Armário 2'),
  (12,2,NULL,'ARM3','Armário 3'),
  (13,2,10,'ARM11','Armário 1-1'),
  (14,2,10,'ARM12','Armário 1-2'),
  (15,2,11,'ARM21','Armário 2-1'),
  (16,2,11,'ARM22','Armário 2-2'),
  (17,2,12,'ARM31','Armário 3-1'),
  (18,2,12,'ARM32','Armário 3-2'),
  (19,3,NULL,'CAN1','Canister 1'),
  (20,3,NULL,'CAN2','Canister 2'),
  (21,3,19,'SUB1','Subdivisão 1'),
  (22,3,19,'SUB2','Subdivisão 2'),
  (23,3,20,'SUB1','Subdivisão 1'),
  (24,3,20,'SUB2','Subdivisão 2'),
  (25,3,21,'PAR1','Parte 1'),
  (26,3,21,'PAR2','Parte 2'),
  (27,3,22,'PAR1','Parte 1'),
  (28,3,22,'PAR2','Parte 2'),
  (29,3,23,'PAR1','Parte 1'),
  (30,3,23,'PAR2','Parte 2'),
  (31,3,24,'PAR1','Parte 1'),
  (32,3,24,'PAR2','Parte 2');
COMMIT;

INSERT INTO `container_preservation_method` (`id_container`, `id_preservation_method`) VALUES 
  (1,2),
  (2,2),
  (3,2);
COMMIT;

INSERT INTO `container_subcoll` (`id_container`, `id_subcoll`) VALUES 
  (1,1),
  (2,1),
  (3,1);
COMMIT;

INSERT INTO `doc` (`id_doc`, `id_coll`, `id_subcoll`, `code`, `id_qualifier`, `id_test_group`, `last_update`) VALUES 
  (1,1,1,'1',3,NULL,'2008-12-12 10:13:25'),
  (2,1,1,'2',1,NULL,'2008-12-12 10:14:24'),
  (3,1,1,'3',4,NULL,'2008-12-12 10:15:26'),
  (4,1,1,'4',2,NULL,'2008-12-12 10:16:02'),
  (5,1,1,'5',5,2,'2008-12-12 10:16:59');
COMMIT;

INSERT INTO `doc_file` (`id_doc`, `id_coll`, `id_lang`, `file_name`) VALUES 
  (1,1,2,'documento.teste.txt'),
  (2,1,2,'documento.teste.txt'),
  (3,1,2,'documento.teste.txt'),
  (4,1,2,'documento.teste.txt'),
  (5,1,2,'documento.teste.txt');
COMMIT;

INSERT INTO `doc_title` (`id_doc`, `id_coll`, `id_lang`, `title`) VALUES 
  (1,1,1,'Documento Teste 1'),
  (1,1,2,'Documento Teste 1'),
  (2,1,1,'Foto Teste 1'),
  (2,1,2,'Foto Teste 1'),
  (3,1,1,'Meio Teste 1'),
  (3,1,2,'Meio Teste 1'),
  (4,1,1,'Sequência Teste 1'),
  (4,1,2,'Sequência Teste 1'),
  (5,1,1,'Teste Teste 1'),
  (5,1,2,'Teste Teste 1');
COMMIT;

INSERT INTO `institution` (`id_institution`, `code1`, `code2`, `code3`, `complement`, `nickname`, `name`, `address`, `phone`, `email`, `website`, `last_update`) VALUES 
  (1,NULL,NULL,NULL,NULL,'UNIUM','Universidade 1',NULL,NULL,NULL,NULL,'2008-12-12 10:05:36'),
  (2,NULL,NULL,NULL,NULL,'UNIDOIS','Universidade 2',NULL,NULL,NULL,NULL,'2008-12-12 10:06:28');
COMMIT;

INSERT INTO `location` (`id_location`, `id_container`, `rows`, `cols`, `ini_row`, `ini_col`, `pattern`) VALUES 
  (1,1,10,10,'0','0','%(row)s:%(col)s'),
  (2,2,20,20,'A','1','%(row)s-%(col)s'),
  (3,3,8,10,'A','1','%(row)sx%(col)s');
COMMIT;

INSERT INTO `lot` (`id_lot`, `id_subcoll`, `name`) VALUES 
  (4,1,'Lote 1'),
  (5,1,'Lote 2'),
  (17,1,'Lote 3'),
  (25,1,'Lote 5'),
  (27,1,'Lote 7'),
  (28,1,'Lote 001A'),
  (29,1,'Lote 001B'),
  (31,1,'Lote 001C');
COMMIT;

INSERT INTO `lot_strain` (`id_lot`, `id_strain`) VALUES 
  (5,1),
  (17,1),
  (25,1),
  (27,1),
  (28,1),
  (29,1),
  (31,1),
  (4,2);
COMMIT;

INSERT INTO `lot_strain_location` (`id_lot_strain_location`, `id_lot`, `id_strain`, `id_container_hierarchy`, `row`, `col`) VALUES 
  (29,4,2,4,0,1),
  (30,4,2,13,0,1),
  (22,5,1,4,1,0),
  (23,5,1,13,0,2),
  (24,5,1,13,1,2),
  (21,17,1,4,2,0),
  (26,25,1,4,0,0),
  (28,27,1,4,1,1),
  (31,28,1,25,0,0),
  (32,28,1,25,0,1),
  (33,29,1,4,6,6),
  (34,29,1,4,6,7),
  (35,29,1,30,4,5),
  (36,29,1,30,5,6),
  (37,29,1,30,6,7),
  (40,31,1,4,2,1);
COMMIT;

INSERT INTO `person` (`id_person`, `name`, `nickname`, `address`, `phone`, `email`, `last_update`) VALUES 
  (1,'Jônatas',NULL,NULL,NULL,NULL,'2008-11-05 17:24:25'),
  (2,'João',NULL,NULL,NULL,NULL,'2008-12-12 10:07:06'),
  (3,'José',NULL,NULL,NULL,NULL,'2008-12-12 10:10:54'),
  (4,'Manoel',NULL,NULL,NULL,NULL,'2008-12-12 10:11:21');
COMMIT;

INSERT INTO `preservation` (`id_preservation`, `id_user`, `id_lot`, `id_preservation_method`, `date`, `info`, `last_update`) VALUES 
  (4,1,4,2,'2008-11-01',NULL,'2008-11-18 11:31:46'),
  (5,1,5,2,'2008-11-01',NULL,'2008-11-13 21:32:55'),
  (6,1,17,2,'2007-01-01',NULL,'2008-11-13 21:12:31'),
  (16,1,27,2,'2007-01-01',NULL,'2008-11-18 11:20:09'),
  (17,1,28,2,'2008-01-01',NULL,'2008-12-03 08:56:13'),
  (18,1,29,2,'2008-01-01',NULL,'2008-12-03 14:53:34'),
  (20,1,31,2,'2008-01-01',NULL,'2008-12-09 15:50:12');
COMMIT;

INSERT INTO `preservation_strain` (`id_preserv_str`, `id_preservation`, `id_strain`, `origin_type`, `origin`, `id_lot`, `id_origin_container_hierarchy`, `origin_row`, `origin_col`, `stock_position`, `stock_minimum`, `id_doc`, `temperature`, `incub_time`, `cryoprotector`, `preservation_type`, `purity`, `counting`, `counting_not_apply`, `macro_charac`, `micro_charac`, `result`, `obs`) VALUES 
  (13,6,1,'original',NULL,NULL,NULL,NULL,NULL,'CBN1 CCN11 2:0\r\n',1,NULL,NULL,NULL,NULL,'none','y',NULL,'n',NULL,NULL,NULL,NULL),
  (14,5,1,'original',NULL,NULL,NULL,NULL,NULL,'CBN1 CCN11 1:0\r\nARM1 ARM11 A-3\r\nARM1 ARM11 B-3\r\n',2,NULL,NULL,NULL,NULL,'none','y',NULL,'n',NULL,NULL,NULL,NULL),
  (18,16,1,'original',NULL,NULL,NULL,NULL,NULL,'CBN1 CCN11 1:1\r\n',1,NULL,NULL,NULL,NULL,'none','y',NULL,'n',NULL,NULL,NULL,NULL),
  (19,4,2,'original',NULL,NULL,NULL,NULL,NULL,'CBN1 CCN11 0:1\r\nARM1 ARM11 A-2\r\n',1,NULL,NULL,NULL,NULL,'none','y',NULL,'n',NULL,NULL,NULL,NULL),
  (20,17,1,'original',NULL,NULL,NULL,NULL,NULL,'CAN1 SUB1 PAR1 Ax1\r\nCAN1 SUB1 PAR1 Ax2\r\n',1,NULL,NULL,NULL,NULL,'none','y',NULL,'n',NULL,NULL,NULL,NULL),
  (21,18,1,'original',NULL,NULL,NULL,NULL,NULL,'CBN1 CCN11 6:6\r\nCBN1 CCN11 6:7\r\nCAN2 SUB1 PAR2 Ex6\r\nCAN2 SUB1 PAR2 Fx7\r\nCAN2 SUB1 PAR2 Gx8\r\n',1,NULL,NULL,NULL,NULL,'none','y',NULL,'n',NULL,NULL,NULL,NULL),
  (24,20,1,'lot',NULL,29,4,6,6,'CBN1 CCN11 2:1\r\n',1,NULL,NULL,NULL,NULL,'none','y',NULL,'n',NULL,NULL,NULL,NULL);
COMMIT;

INSERT INTO `ref` (`id_ref`, `id_coll`, `id_subcoll`, `title`, `author`, `year`, `url`, `last_update`) VALUES 
  (1,1,1,'Refer&#234;ncia Teste 1',NULL,NULL,NULL,'2008-12-12 10:23:51'),
  (2,1,1,'Refer&#234;ncia Teste 2',NULL,NULL,NULL,'2008-12-12 10:24:22');
COMMIT;

INSERT INTO `roles_permissions` (`id_item`, `id_role`, `id_area`, `permission`) VALUES 
  (1,1,1,'w'),
  (1,1,2,'w'),
  (1,1,3,'w'),
  (1,1,4,'w'),
  (1,1,5,'w'),
  (1,1,6,'w'),
  (2,1,1,'w'),
  (2,1,2,'w'),
  (2,1,3,'w'),
  (2,1,4,'w'),
  (2,1,5,'w'),
  (2,1,6,'w'),
  (3,1,2,'w'),
  (3,1,3,'w'),
  (3,1,5,'w'),
  (3,1,7,'w'),
  (4,1,2,'w'),
  (4,1,3,'w'),
  (4,1,5,'w'),
  (4,1,7,'w'),
  (5,1,5,'w'),
  (5,1,7,'w'),
  (6,1,7,'w'),
  (14,1,7,'w'),
  (16,1,7,'w'),
  (17,1,7,'w'),
  (18,1,7,'w'),
  (20,1,7,'w');
COMMIT;

INSERT INTO `scientific_names` (`id_sciname`, `hi_tax`, `sciname`, `sciname_no_auth`) VALUES 
  (1,'<i>Bacteria</i>','<i>Bacillus</i> <i>cereus</i>','<i>Bacillus</i> <i>cereus</i> '),
  (2,'<i>Eukarya</i> <i>Fungi</i>','<i>Fungoteu</i> <i>fungus</i>','<i>Fungoteu</i> <i>fungus</i> ');
COMMIT;

INSERT INTO `scientific_names_hierarchy` (`id_sciname`, `id_hierarchy`, `value`, `author`) VALUES 
  (1,18,'Bacillus',NULL),
  (1,21,'Cereus',NULL),
  (2,18,'Fungoteu',NULL),
  (2,21,'fungus',NULL);
COMMIT;

INSERT INTO `species` (`id_species`, `id_coll`, `id_subcoll`, `id_taxon_group`, `id_sciname`, `id_name_qualifier`, `taxon_ref`, `synonym`, `hazard_group`, `hazard_group_ref`, `id_alt_states`, `alt_states_type`, `last_update`) VALUES 
  (1,1,1,1,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2008-11-05 16:27:53'),
  (2,1,1,2,2,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2008-12-12 09:59:39');
COMMIT;

INSERT INTO `str_characs` (`id_coll`, `id_strain`, `biochemical`, `molecular`, `immunologic`, `morphologic`, `pathogenic`, `genotypic`, `ogm`) VALUES 
  (1,1,NULL,NULL,NULL,NULL,NULL,NULL,'0'),
  (1,2,NULL,NULL,NULL,NULL,NULL,NULL,'0'),
  (1,3,NULL,NULL,NULL,NULL,NULL,NULL,'0'),
  (1,4,NULL,NULL,NULL,NULL,NULL,NULL,'0');
COMMIT;

INSERT INTO `str_coll_event` (`id_strain`, `id_coll`, `id_person`, `id_institution`, `date`, `id_country`, `id_state`, `id_city`, `place`, `gps_latitude`, `gps_latitude_dms`, `gps_latitude_mode`, `gps_longitude`, `gps_longitude_dms`, `gps_longitude_mode`, `gps_precision`, `id_gps_datum`, `gps_comments`, `host_genus`, `host_species`, `host_classification`, `host_infra_name`, `host_infra_complement`, `global_code`, `id_clinical_form`, `hiv`) VALUES 
  (1,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (2,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (3,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (4,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
COMMIT;

INSERT INTO `str_culture` (`id_coll`, `id_strain`, `temp`, `ph`) VALUES 
  (1,1,NULL,NULL),
  (1,2,NULL,NULL),
  (1,3,NULL,NULL),
  (1,4,NULL,NULL);
COMMIT;

INSERT INTO `str_deposit` (`id_strain`, `id_coll`, `id_person`, `id_institution`, `genus`, `species`, `classification`, `infra_name`, `infra_complement`, `date`, `id_dep_reason`, `preserv_method`, `form`, `comments`, `aut_date`, `aut_person`, `aut_result`) VALUES 
  (1,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (2,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (3,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (4,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
COMMIT;

INSERT INTO `str_identification` (`id_strain`, `id_coll`, `date`, `id_person`, `id_institution`, `genus`, `species`, `classification`, `infra_name`, `infra_complement`, `comments`) VALUES 
  (1,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (2,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (3,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (4,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
COMMIT;

INSERT INTO `str_isolation` (`id_strain`, `id_coll`, `id_person`, `id_institution`, `date`, `comments`) VALUES 
  (1,1,NULL,NULL,NULL,NULL),
  (2,1,NULL,NULL,NULL,NULL),
  (3,1,NULL,NULL,NULL,NULL),
  (4,1,NULL,NULL,NULL,NULL);
COMMIT;

INSERT INTO `str_properties` (`id_strain`, `id_coll`) VALUES 
  (1,1),
  (2,1),
  (3,1),
  (4,1);
COMMIT;

INSERT INTO `strain` (`id_strain`, `id_coll`, `id_subcoll`, `code`, `internal_code`, `status`, `id_species`, `infra_complement`, `id_type`, `history`, `extra_codes`, `comments`, `last_update`, `is_ogm`, `go_catalog`) VALUES 
  (1,1,1,'L1',NULL,'active',1,NULL,NULL,NULL,NULL,NULL,'2008-11-05 16:28:16',0,0),
  (2,1,1,'L2',NULL,'active',1,NULL,NULL,NULL,NULL,NULL,'2008-11-05 16:28:33',0,0),
  (3,1,1,'L3',NULL,'active',1,NULL,NULL,NULL,NULL,NULL,'2008-11-05 17:21:15',0,0),
  (4,1,1,'L4',NULL,'active',2,NULL,NULL,NULL,NULL,NULL,'2008-12-12 10:02:47',0,0);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

