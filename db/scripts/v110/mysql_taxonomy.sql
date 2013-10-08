USE sicol_v110;
SET character_set_client = utf8;
insert into hierarchy_def values ( 1, 10,true,	false,	false,	false,	false,	true,	'italic','ucfirst',	null,	null);
insert into hierarchy_def values ( 2, 20,true,	false,	false,	false,	false,	true,	'italic','ucfirst',	null,	null);
insert into hierarchy_def values ( 3, 30,true,	false,	false,	false,	false,	false,	'italic','ucfirst',	null,	null);
insert into hierarchy_def values ( 4, 40,true,	false,	false,	false,	false,	true,	'italic','ucfirst',	null,	null);
insert into hierarchy_def values ( 5, 50,true,	false,	false,	false,	false,	false,	'italic','ucfirst',	null,	null);
insert into hierarchy_def values ( 6, 60,true,	false,	false,	false,	false,	true,	'italic','ucfirst',	null,	null);
insert into hierarchy_def values ( 7, 70,true,	false,	false,	false,	false,	false,	'italic','ucfirst',	null,	null);
insert into hierarchy_def values ( 8, 80,true,	false,	false,	false,	false,	false,	'italic','ucfirst',	null,	null);
insert into hierarchy_def values ( 9, 90,true,	false,	false,	false,	false,	true,	'italic','ucfirst',	null,	null);
insert into hierarchy_def values (10,100,true,	false,	false,	false,	false,	false,	'italic','ucfirst',	null,	null);
insert into hierarchy_def values (11,110,true,	false,	false,	false,	false,	true,	'italic','ucfirst',	null,	null);
insert into hierarchy_def values (12,120,true,	false,	false,	false,	false,	false,	'italic','ucfirst',	null,	null);
insert into hierarchy_def values (13,130,true,	false,	false,	false,	false,	false,	'italic','ucfirst',	null,	null);
insert into hierarchy_def values (14,140,true,	false,	false,	false,	false,	true,	'italic','ucfirst',	null,	null);
insert into hierarchy_def values (15,150,true,	false,	false,	false,	false,	false,	'italic','ucfirst',	null,	null);
insert into hierarchy_def values (16,160,true,	false,	false,	false,	false,	false,	'italic','ucfirst',	null,	null);
insert into hierarchy_def values (17,170,true,	false,	false,	false,	false,	false,	'italic','ucfirst',	null,	null);
insert into hierarchy_def values (18,180,false,	true,	false,	true,	true,	false,	'italic','ucfirst',	null,	null);
insert into hierarchy_def values (19,190,false,	false,	false,	false,	false,	false,	'italic','ucfirst',	'(',	')');
insert into hierarchy_def values (20,200,false,	false,	false,	false,	false,	false,	'italic','ucfirst',	'(',	')');
insert into hierarchy_def values (21,210,false,	true,	true,	true,	true,	false,	'italic','lower',	null,	null);
insert into hierarchy_def values (22,220,false,	true,	true,	true,	false,	false,	'italic','lower',	'subsp. ',null);
insert into hierarchy_def values (23,230,false,	true,	true,	true,	false,	false,	'italic','lower',	'var. ',null);
insert into hierarchy_def values (24,240,false,	true,	true,	true,	false,	false,	'italic','lower',	'subvar. ',null);
insert into hierarchy_def values (25,250,false,	false,	false,	true,	false,	false,	'italic','lower',	'f. ',	null);
insert into hierarchy_def values (26,260,false,	false,	false,	true,	false,	false,	'italic','lower',	'subf. ',null);
insert into hierarchy_def values (27,270,false,	false,	false,	true,	false,	false,	'italic','none',	'ser. ',null);
insert into hierarchy_def values (28,280,false,	false,	false,	true,	false,	false,	'italic','none',	'bv. ',	null);
insert into hierarchy_def values (29,290,false,	false,	false,	true,	false,	false,	'italic','none',	'pv. ',	null);
insert into hierarchy_def values (30,300,false,	true,	true,	true,	false,	false,	'italic','lower',	'f.sp. ',null);
insert into hierarchy_def values (31,310,false,	true,	true,	true,	false,	false,	'italic','none',	null,	null);

insert into hierarchy_lang values ( 1,1,'Domain');
insert into hierarchy_lang values ( 2,1,'Kingdom');
insert into hierarchy_lang values ( 3,1,'SubKingdom');
insert into hierarchy_lang values ( 4,1,'Phylum');
insert into hierarchy_lang values ( 5,1,'SubPhylum');
insert into hierarchy_lang values ( 6,1,'Division');
insert into hierarchy_lang values ( 7,1,'SubDivision');
insert into hierarchy_lang values ( 8,1,'SuperClass');
insert into hierarchy_lang values ( 9,1,'Class');
insert into hierarchy_lang values (10,1,'SubClass');
insert into hierarchy_lang values (11,1,'Order');
insert into hierarchy_lang values (12,1,'SubOrder');
insert into hierarchy_lang values (13,1,'SuperFamily');
insert into hierarchy_lang values (14,1,'Family');
insert into hierarchy_lang values (15,1,'SubFamily');
insert into hierarchy_lang values (16,1,'Tribe');
insert into hierarchy_lang values (17,1,'SubTribe');
insert into hierarchy_lang values (18,1,'Genus');
insert into hierarchy_lang values (19,1,'SubGenus');
insert into hierarchy_lang values (20,1,'Section');
insert into hierarchy_lang values (21,1,'species');
insert into hierarchy_lang values (22,1,'subspecies');
insert into hierarchy_lang values (23,1,'variety');
insert into hierarchy_lang values (24,1,'subvariety');
insert into hierarchy_lang values (25,1,'form');
insert into hierarchy_lang values (26,1,'subform');
insert into hierarchy_lang values (27,1,'serovar');
insert into hierarchy_lang values (28,1,'biovar');
insert into hierarchy_lang values (29,1,'pathovar');
insert into hierarchy_lang values (30,1,'forma specialis');
insert into hierarchy_lang values (31,1,'race');

insert into hierarchy_lang values ( 1,2,'Domínio');
insert into hierarchy_lang values ( 2,2,'Reino');
insert into hierarchy_lang values ( 3,2,'SubReino');
insert into hierarchy_lang values ( 4,2,'Filo');
insert into hierarchy_lang values ( 5,2,'SubFilo');
insert into hierarchy_lang values ( 6,2,'Divisão');
insert into hierarchy_lang values ( 7,2,'SubDivisão');
insert into hierarchy_lang values ( 8,2,'SuperClasse');
insert into hierarchy_lang values ( 9,2,'Classe');
insert into hierarchy_lang values (10,2,'SubClasse');
insert into hierarchy_lang values (11,2,'Ordem');
insert into hierarchy_lang values (12,2,'SubOrdem');
insert into hierarchy_lang values (13,2,'SuperFamília');
insert into hierarchy_lang values (14,2,'Família');
insert into hierarchy_lang values (15,2,'SubFamília');
insert into hierarchy_lang values (16,2,'Tribo');
insert into hierarchy_lang values (17,2,'SubTribo');
insert into hierarchy_lang values (18,2,'Gênero');
insert into hierarchy_lang values (19,2,'SubGênero');
insert into hierarchy_lang values (20,2,'Seção');
insert into hierarchy_lang values (21,2,'espécie');
insert into hierarchy_lang values (22,2,'subespécie');
insert into hierarchy_lang values (23,2,'variedade');
insert into hierarchy_lang values (24,2,'subvariedade');
insert into hierarchy_lang values (25,2,'forma');
insert into hierarchy_lang values (26,2,'subforma');
insert into hierarchy_lang values (27,2,'sorovar');
insert into hierarchy_lang values (28,2,'biovar');
insert into hierarchy_lang values (29,2,'patovar');
insert into hierarchy_lang values (30,2,'forma specialis');
insert into hierarchy_lang values (31,2,'raça');

-- id_taxon_group = 1 (Bacteria)

insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (1,1,1);					-- Domain
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (2,1,1);					-- Kingdom
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (4,1,1);					-- Phylum
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (9,1,1);					-- Class
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (11,1,1);					-- Order
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (14,1,1);					-- Family
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (18,1,1);					-- Genus
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (21,1,1);					-- species
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll,prefix) values (22,1,1,null);			-- subspecies
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (23,1,1);					-- variety

-- id_taxon_group = 2 (Fungi)

insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (1,2,1);					-- Domain	
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (2,2,1);					-- Kingdom
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (4,2,1);					-- Phylum
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (9,2,1);					-- Class
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (11,2,1);					-- Order
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (14,2,1);					-- Family
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (18,2,1);					-- Genus
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (21,2,1);					-- species
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll,prefix) values (22,2,1,null);			-- subspecies
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (25,2,1);					-- forma

-- id_taxon_group = 3 (Yeast)

insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (1,3,1);					-- Domain
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (2,3,1);					-- Kingdom
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (4,3,1);					-- Phylum
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (9,3,1);					-- Class
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (11,3,1);					-- Order
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (14,3,1);					-- Family
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (18,3,1);					-- Genus
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (21,3,1);					-- species
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll,prefix) values (22,3,1,null);			-- subspecies
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (23,3,1);					-- variety

-- id_taxon_group = 4 (Archaea)

insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (1,4,1);					-- Domain
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (2,4,1);					-- Kingdom
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (4,4,1);					-- Phylum
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (9,4,1);					-- Class
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (11,4,1);					-- Order
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (14,4,1);					-- Family
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (18,4,1);					-- Genus
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (21,4,1);					-- species
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll,prefix) values (22,4,1,null);			-- subspecies
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (23,4,1);					-- variety

-- id_taxon_group = 5 (Protozoa)

insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (1,5,1);					-- Domain
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (2,5,1);					-- Kingdom
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (4,5,1);					-- Phylum
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (9,5,1);					-- Class
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (11,5,1);					-- Order
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (12,5,1);					-- Suborder
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (14,5,1);					-- Family
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (18,5,1);					-- Genus
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll,important,in_sciname) values (19,5,1,true,true);	-- Subgenus
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll,important,in_sciname) values (20,5,1,true,false);	-- Section
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll) values (21,5,1);					-- species
insert into hierarchy_group (id_hierarchy,id_taxon_group,id_subcoll,prefix) values (22,5,1,null);			-- subspecies

