drop view specieslinkdwc;

CREATE VIEW specieslinkdwc AS
select	strain.id_strain AS record_uid,
	strain.last_update AS datelastmodified,
	'Fiocruz' AS institutioncode,
	(case strain.id_coll	when  1 then 'CLIOC'
				when  2 then 'CCBH'
				when  3 then 'CCGB'
				when  4 then 'CCFF'
				when  5 then 'CMT'
				when  6 then 'COLTRYP'
				when  7 then 'CFP'
				when  8 then 'CBMA'	-- futura CBAS
				when  9 then 'INCQS'
				when 10 then 'CLIST'
				when 11 then 'CCAMP'
				when 12 then 'CENT'
				when 13 then 'CLEP'
				when 14 then 'COLPROT'
				when 15 then 'CYP'
				when 16 then 'CBAM'
				when 17 then 'CFAM'
				       else NULL
	 end)	AS collectioncode,
	strain.id_subcoll AS subcollectioncode,
	strain.code AS catalognumber,
	replace(replace(replace(replace(scientific_names.sciname_no_auth,'<b>',''),'<i>',''),'</b>',''),'</i>','') AS scientificname,
	'L' AS basisofrecord,
	(select scientific_names_hierarchy.value AS value from scientific_names_hierarchy where ((scientific_names_hierarchy.id_sciname = species.id_sciname) and (scientific_names_hierarchy.id_hierarchy = 2))) AS kingdom,
	(select scientific_names_hierarchy.value AS value from scientific_names_hierarchy where ((scientific_names_hierarchy.id_sciname = species.id_sciname) and (scientific_names_hierarchy.id_hierarchy = 4))) AS phylum,
	(select scientific_names_hierarchy.value AS value from scientific_names_hierarchy where ((scientific_names_hierarchy.id_sciname = species.id_sciname) and (scientific_names_hierarchy.id_hierarchy = 9))) AS class,
	(select scientific_names_hierarchy.value AS value from scientific_names_hierarchy where ((scientific_names_hierarchy.id_sciname = species.id_sciname) and (scientific_names_hierarchy.id_hierarchy = 11))) AS  "order",
	(select scientific_names_hierarchy.value AS value from scientific_names_hierarchy where ((scientific_names_hierarchy.id_sciname = species.id_sciname) and (scientific_names_hierarchy.id_hierarchy = 14))) AS family,
	(select scientific_names_hierarchy.value AS value from scientific_names_hierarchy where ((scientific_names_hierarchy.id_sciname = species.id_sciname) and (scientific_names_hierarchy.id_hierarchy = 18))) AS genus,
	(select scientific_names_hierarchy.value AS value from scientific_names_hierarchy where ((scientific_names_hierarchy.id_sciname = species.id_sciname) and (scientific_names_hierarchy.id_hierarchy = 21))) AS species,
	(select scientific_names_hierarchy.value AS value from scientific_names_hierarchy where ((scientific_names_hierarchy.id_sciname = species.id_sciname) and (scientific_names_hierarchy.id_hierarchy = 22 or scientific_names_hierarchy.id_hierarchy = 23)) order by scientific_names_hierarchy.id_hierarchy limit 1) AS subspecies,
	(select scientific_names_hierarchy.author from scientific_names_hierarchy inner join hierarchy_def on (scientific_names_hierarchy.id_hierarchy = hierarchy_def.id_hierarchy) where scientific_names_hierarchy.id_sciname = species.id_sciname and scientific_names_hierarchy.author is not null order by hierarchy_def.seq desc limit 1) AS scientificnameauthor,
	identifiedby.name AS identifiedby,
	date_format(str_identification.date,'%Y') AS yearidentified,
	date_format(str_identification.date,'%m') AS monthidentified,
	date_format(str_identification.date,'%d') AS dayidentified,
	str_type_lang.type AS typestatus,
	NULL AS collectornumber,
	NULL AS fieldnumber,
	collector.name AS collector,
	date_format(str_coll_event.date,'%Y') AS yearcollected,
	date_format(str_coll_event.date,'%m') AS monthcollected,
	date_format(str_coll_event.date,'%d') AS daycollected,
	NULL AS julianday,
	NULL AS timeOfday,
	NULL AS continentocean,
	loc_country_lang.country AS country,
	loc_state.state AS stateprovince,
	loc_city.city AS county,
	replace(str_coll_event.place,'<br />',' ') AS locality,
	str_coll_event.gps_longitude AS longitude,
	str_coll_event.gps_latitude AS latitude,
	str_coll_event.gps_precision AS coordinateprecision,
	NULL AS boundingbox,
	NULL AS minimumelevation,
	NULL AS maximumelevation,
	NULL AS minimumdepth,
	NULL AS maximumdepth,
	NULL AS sex,
	NULL AS preparationtype,
	NULL AS individualcount,
	strain.extra_codes AS previouscatalognumber,
	str_host_name.host_name AS relationshiptype,
	NULL AS relatedcatalogitem,
	replace(str_cha_catalogue.catalogue_notes,'<br />',' ') AS notes,
	replace(strain.history,'<br />',' ') AS historyofdeposit,
	depositor.name AS depositor,
	date_format(str_deposit.date,'%Y') AS yeardeposited,
	date_format(str_deposit.date,'%m') AS monthdeposited,
	date_format(str_deposit.date,'%d') AS daydeposited,
	str_substratum.substratum AS isolatedfrom,
	isolator.name AS isolator,
	str_iso_method.iso_method AS isolationmethod,
	concat_ws(' ',(case when str_culture.temp is not null then concat_ws(' ','Temp:',str_culture.temp) else NULL end),(case when str_culture.ph is not null then concat_ws(' ','PH:',str_culture.ph) else NULL end)) as conditionsforgrowth,
	strain.is_ogm AS geneticallymodified,
	str_characs.genotypic AS genotype,
	NULL AS mutant,
	NULL AS race,
	replace(replace(replace(replace(alternative_names.sciname_no_auth,'<b>',''),'<i>',''),'</b>',''),'</i>','') AS alternatestate,
	str_pro_properties.properties AS strainproperties,
	str_pro_applications.applications AS strainapplications,
	NULL AS formofsupply,
	str_cha_restrictions.restrictions AS restrictions,
	str_cha_biorisk_comments.biorisk_comments AS biologicalrisks,
	str_characs.pathogenic AS pathogenicity
from ((((((((((((((((((((((((((((strain left join str_deposit on(((str_deposit.id_strain = strain.id_strain) and (str_deposit.id_coll = strain.id_coll)))) left join person depositor on((str_deposit.id_person = depositor.id_person))) left join species on((strain.id_species = species.id_species))) left join scientific_names on((species.id_sciname = scientific_names.id_sciname))) left join str_coll_event on(((str_coll_event.id_strain = strain.id_strain) and (str_coll_event.id_coll = strain.id_coll)))) left join person collector on((str_coll_event.id_person = collector.id_person))) left join str_identification on(((str_identification.id_coll = strain.id_coll) and (str_identification.id_strain = strain.id_strain)))) left join person identifiedby on((str_identification.id_person = identifiedby.id_person))) left join str_substratum on(((str_substratum.id_strain = strain.id_strain) and (str_substratum.id_coll = strain.id_coll) and (str_substratum.id_lang = 2)))) left join str_isolation on(((str_isolation.id_strain = strain.id_strain) and (str_isolation.id_coll = strain.id_coll)))) left join person isolator on((str_isolation.id_person = isolator.id_person))) left join str_iso_method on(((str_iso_method.id_strain = strain.id_strain) and (str_iso_method.id_coll = strain.id_coll) and (str_iso_method.id_lang = 2)))) left join str_culture on(((str_culture.id_strain = strain.id_strain) and (str_culture.id_coll = strain.id_coll)))) left join str_characs on(((str_characs.id_strain = strain.id_strain) and (str_characs.id_coll = strain.id_coll)))) left join str_pro_properties on(((str_pro_properties.id_strain = strain.id_strain) and (str_pro_properties.id_coll = strain.id_coll) and (str_pro_properties.id_lang = 2)))) left join str_pro_applications on(((str_pro_applications.id_strain = strain.id_strain) and (str_pro_applications.id_coll = strain.id_coll) and (str_pro_applications.id_lang = 2)))) left join str_cha_restrictions on(((str_cha_restrictions.id_strain = strain.id_strain) and (str_cha_restrictions.id_coll = strain.id_coll) and (str_cha_restrictions.id_lang = 2)))) left join str_cha_biorisk_comments on(((str_cha_biorisk_comments.id_strain = strain.id_strain) and (str_cha_biorisk_comments.id_coll = strain.id_coll) and (str_cha_biorisk_comments.id_lang = 2)))) left join str_cha_catalogue on(((str_cha_catalogue.id_strain = strain.id_strain) and (str_cha_catalogue.id_coll = strain.id_coll) and (str_cha_catalogue.id_lang = 2)))) left join str_host_name on(((str_host_name.id_strain = strain.id_strain) and (str_host_name.id_coll = strain.id_coll) and (str_host_name.id_lang = 2)))) left join taxon_group_lang on(((taxon_group_lang.id_taxon_group = species.id_taxon_group) and (taxon_group_lang.id_lang = 2)))) left join loc_country_lang on(((str_coll_event.id_country = loc_country_lang.id_country) and (loc_country_lang.id_lang = 2)))) left join loc_state on((str_coll_event.id_state = loc_state.id_state))) left join loc_city on((str_coll_event.id_city = loc_city.id_city))) left join species alternative on((species.id_alt_states = alternative.id_species))) left join scientific_names alternative_names on((alternative.id_sciname = alternative_names.id_sciname))) left join str_type_lang on(((strain.id_type = str_type_lang.id_type) and (str_type_lang.id_lang = 2)))) join roles_permissions rp on(((rp.id_item = strain.id_strain) and (rp.id_role = 1) and (rp.id_area = 2)))) where ((strain.go_catalog = 1) and (strain.status = 'active') and (str_deposit.id_dep_reason = 1));



