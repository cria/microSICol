DROP VIEW IF EXISTS `speciesLinkDwC`;
CREATE VIEW `speciesLinkDwC` AS 
    select
        strain.last_update AS DateLastModified, -- OK
        'Unicamp' AS InstitutionCode, -- OK, tem no SQLITE
        strain.id_coll AS CollectionCode, -- OK
        strain.id_subcoll AS SubCollectionCode, -- OK
        strain.code AS CatalogNumber, -- OK
        REPLACE(REPLACE(REPLACE(REPLACE(scientific_names.sciname, '<b>', ''), '<i>', ''), '</b>', ''), '</i>', '') AS ScientificName, -- OK
        'L' AS BasisOfRecord, -- OK
        taxon_group_lang.taxon_group AS Kingdom, -- OK
        (SELECT `value` FROM scientific_names_hierarchy WHERE id_sciname = species.id_sciname AND id_hierarchy = 4) AS Phylum, -- OK
        (SELECT `value` FROM scientific_names_hierarchy WHERE id_sciname = species.id_sciname AND id_hierarchy = 9) AS `Class`, -- OK
        (SELECT `value` FROM scientific_names_hierarchy WHERE id_sciname = species.id_sciname AND id_hierarchy = 11) AS `Order`, -- OK
        (SELECT `value` FROM scientific_names_hierarchy WHERE id_sciname = species.id_sciname AND id_hierarchy = 14) AS Family, -- OK
        (SELECT `value` FROM scientific_names_hierarchy WHERE id_sciname = species.id_sciname AND id_hierarchy = 18) AS Genus, -- OK
        (SELECT `value` FROM scientific_names_hierarchy WHERE id_sciname = species.id_sciname AND id_hierarchy = 21) AS Species, -- OK
        (SELECT `value` FROM scientific_names_hierarchy WHERE id_sciname = species.id_sciname AND id_hierarchy = 22) AS Subspecies, -- OK
        REPLACE(REPLACE(REPLACE(REPLACE(scientific_names.sciname_no_auth, '<b>', ''), '<i>', ''), '</b>', ''), '</i>', '') AS ScientificNameAuthor, -- OK
        identifiedby.name AS IdentifiedBy, -- OK
        date_format(str_identification.date,_latin1'%Y') AS YearIdentified, -- OK
        date_format(str_identification.date,_latin1'%m') AS MonthIdentified, -- OK
        date_format(str_identification.date,_latin1'%d') AS DayIdentified, -- OK
        str_type_lang.type AS TypeStatus, -- OK
        NULL AS CollectorNumber, -- blank OK
        NULL AS FieldNumber, -- blank OK
        collector.name AS Collector, -- OK
        date_format(str_coll_event.date,_latin1'%Y') AS YearCollected, -- OK
        date_format(str_coll_event.date,_latin1'%m') AS MonthCollected, -- OK
        date_format(str_coll_event.date,_latin1'%d') AS DayCollected, -- OK
        NULL AS JulianDay, -- blank OK
        NULL AS TimeOfDay, -- blank OK
        NULL AS ContinentOcean, -- blank OK
        loc_country_lang.country AS Country, -- OK
        loc_state.state AS StateProvince, -- OK
        loc_city.city AS County, -- OK
        str_coll_event.place AS Locality, -- OK
        str_coll_event.gps_longitude AS Longitude, -- OK
        str_coll_event.gps_latitude AS Latitude, -- OK
        str_coll_event.gps_precision AS CoordinatePrecision, -- OK
        NULL AS BoundingBox, -- blank OK
        NULL AS MinimumElevation, -- blank OK
        NULL AS MaximumElevation, -- blank OK
        NULL AS MinimumDepth, -- blank OK
        NULL AS MaximumDepth, -- blank OK
        NULL AS Sex, -- blank OK
        NULL AS PreparationType, -- blank OK
        NULL AS IndividualCount, -- blank OK
        NULL AS PreviousCatalogNumber, -- blank OK
        str_host_name.host_name AS RelationshipType, -- OK
        NULL AS RelatedCatalogItem,  -- blank OK
        str_cha_catalogue.catalogue_notes AS Notes, -- OK
        strain.history AS HistoryOfDeposit, -- OK
        depositor.name AS Depositor, -- OK
        date_format(str_deposit.date,_latin1'%Y') AS YearDeposited, -- OK
        date_format(str_deposit.date,_latin1'%m') AS MonthDeposited, -- OK
        date_format(str_deposit.date,_latin1'%d') AS DayDeposited, -- OK
        str_substratum.substratum AS Substrate, -- OK
        isolator.name AS Isolator, -- OK
        str_iso_method.iso_method AS IsolationMethod, -- OK
        concat_ws(' ', _utf8'Temp:',str_culture.temp,_utf8'PH:',str_culture.ph) AS ConditionsForGrowth, -- OK
        strain.is_ogm AS GeneticallyModified, -- OK
        str_characs.genotypic AS Genotype,  -- blank OK
        NULL AS Mutant,  -- blank OK
        NULL AS Race,  -- blank OK
        REPLACE(REPLACE(REPLACE(REPLACE(alternative_names.sciname_no_auth, '<b>', ''), '<i>', ''), '</b>', ''), '</i>', '') AlternateState, -- OK
        str_pro_properties.properties AS StrainProperties, -- OK
        str_pro_applications.applications AS StrainApplications, -- OK
        NULL AS FormOfSupply, -- blank OK
        str_cha_restrictions.restrictions AS Restrictions, -- OK
        str_cha_biorisk_comments.biorisk_comments AS BiologicalRisks, -- OK
        str_characs.pathogenic AS Pathogenicity -- OK
    from 
        strain

    left join str_deposit on
        (str_deposit.id_strain = strain.id_strain  and
        str_deposit.id_coll = strain.id_coll) 

    left join person depositor on
        (str_deposit.id_person = depositor.id_person) 

    left join species on
        (strain.id_species = species.id_species) 
    
    left join scientific_names on
        (species.id_sciname = scientific_names.id_sciname)

    left join str_coll_event on
        (str_coll_event.id_strain = strain.id_strain  and
        str_coll_event.id_coll = strain.id_coll)

    left join person collector on
        (str_coll_event.id_person = collector.id_person) 

    left join str_identification on
        (str_identification.id_coll = strain.id_coll  and
        str_identification.id_strain = strain.id_strain)

    left join person identifiedby on
        (str_identification.id_person = identifiedby.id_person)

    left join str_substratum on
        (str_substratum.id_strain = strain.id_strain  and
        str_substratum.id_coll = strain.id_coll  and
        str_substratum.id_lang = 2)

    left join str_isolation on
        (str_isolation.id_strain = strain.id_strain  and
        str_isolation.id_coll = strain.id_coll)

    left join person isolator on
        (str_isolation.id_person = isolator.id_person)

    left join str_iso_method on
        (str_iso_method.id_strain = strain.id_strain  and
        str_iso_method.id_coll = strain.id_coll  and
        str_iso_method.id_lang = 2)

    left join str_culture on
        (str_culture.id_strain = strain.id_strain  and
        str_culture.id_coll = strain.id_coll)

    left join str_characs on
        (str_characs.id_strain = strain.id_strain  and
        str_characs.id_coll = strain.id_coll)

    left join str_pro_properties on
        (str_pro_properties.id_strain = strain.id_strain  and
        str_pro_properties.id_coll = strain.id_coll  and
        str_pro_properties.id_lang = 2)

    left join str_pro_applications on
        (str_pro_applications.id_strain = strain.id_strain  and
        str_pro_applications.id_coll = strain.id_coll  and
        str_pro_applications.id_lang = 2)

    left join str_cha_restrictions on
        (str_cha_restrictions.id_strain = strain.id_strain  and
        str_cha_restrictions.id_coll = strain.id_coll  and
        str_cha_restrictions.id_lang = 2)

    left join str_cha_biorisk_comments on
        (str_cha_biorisk_comments.id_strain = strain.id_strain  and
        str_cha_biorisk_comments.id_coll = strain.id_coll  and
        str_cha_biorisk_comments.id_lang = 2)

    left join str_cha_catalogue on
        (str_cha_catalogue.id_strain = strain.id_strain  and
        str_cha_catalogue.id_coll = strain.id_coll  and
        str_cha_catalogue.id_lang = 2)

    left join str_host_name on
        (str_host_name.id_strain = strain.id_strain  and
        str_host_name.id_coll = strain.id_coll  and
        str_host_name.id_lang = 2)

    left join taxon_group_lang on
        (taxon_group_lang.id_taxon_group = species.id_taxon_group and
        taxon_group_lang.id_lang = 2)

    left join loc_country_lang on
        (str_coll_event.id_country = loc_country_lang.id_country and
        loc_country_lang.id_lang = 2)

    left join loc_state on
        (str_coll_event.id_state = loc_state.id_state)

    left join loc_city on
        (str_coll_event.id_city = loc_city.id_city)

    left join species alternative on
        (species.id_alt_states = alternative.id_species)
        
    left join scientific_names alternative_names on
        (alternative.id_sciname = alternative_names.id_sciname)

    left join str_type_lang on
        (strain.id_type = str_type_lang.id_type and 
        str_type_lang.id_lang = 2)
        
    where
        strain.go_catalog = 1 and strain.status <> 'inactive' and str_deposit.id_dep_reason = 1
;