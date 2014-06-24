#!/usr/bin/env python
#-*- coding: utf-8 -*-

#python imports
from cgi import escape
from urlparse import urljoin
from re import findall
from sys import exit
from urllib import urlencode
import cgi

#project imports
from session import Session
from dbconnection import dbConnection
from general import General, DefDict
from lists import Lists
from textlinkfactory import TextLinkFactory
from loghelper import Logging
from location import LocationBuilder
from os import path
from datetime import datetime
#from dbgp.client import brk

class Log(object):

    #Configs
    g = General()
    page_parts = {'top':'', 'submenu':'', 'hidden_forms':''}

    def __init__(self, cookie_value, conn=None):
        if (conn == None):
            conn = sel.dbConnection(cookie_value)
            
        self.dbconnection = conn
        self.execute = conn.execute
        self.fetch = conn.fetch
        self.cursor = conn.cursor
        
        self.session = Session()
        self.session.load(cookie_value)
        
    def ConvertStrUnicode(self, valor):
        retorno = '';
        if (isinstance(valor, unicode) == False):
            retorno = str(valor).decode("utf8")
        else:
            retorno = valor
        
        return retorno        
        
    def checkModifiedFields(self, sql, data, id_entity, code_entity, lang, action, id_log_operation, id_log_entity, lot_name):
        return_value = []
        x = datetime.now()
        id_subcoll = self.session.data['id_subcoll']
       
        if (lot_name != '' and lot_name != "NULL"):
            lot_name_final = "'" + lot_name + "'"
        else:
            lot_name_final = "NULL"
                
        if (action == "update"):
            self.execute(sql, data)
            entity_selected = self.fetch('all')
            
            if (len(entity_selected) == 0):
                data_entity = data.copy()
                for key, value in data.items():
                    data_entity[key] = ''
            else:
                data_entity = entity_selected[0]
            
            for key, value in data.items():
                if ((key != 'insert') and (key != 'update') and (key != 'id') and (key != 'lang') and (key != 'hdnReusedStrain')):
                    valorForm = self.ConvertStrUnicode(data[key])
                    valorBanco = self.ConvertStrUnicode(data_entity[key])
                    if ((valorForm == 'None' and data_entity[key] == '') or (valorForm == valorBanco)):
                        continue
                    else:
                        #brk(host="localhost", port=9000)
                        if key == "numeric_code":
                            data_lookup = code_entity
                        else:
                            data_lookup = valorForm if valorForm != None else ""
                            if (log_dict[key]['lookup'] != ""):
                                look = {}
                                look['id'] = valorForm
                                if key == "numeric_code_division":
                                    look['id'] = id_entity;
                                self.execute(log_dict[key]['lookup'], look)
                                data_lookup = self.fetch('one')                    
                        
                        lang_name = "NULL"
                        if ((key in log_dict) and (log_dict[key]['is_mlang'] == True)):
                            if lang != '':
                                lang_name = "'" + lang + "'"
                        
                        return_value.append("('"  + x.strftime('%Y-%m-%d %H:%M:%S') + "', '" + self.session.data['user_name'] + "'," + str(id_log_operation) + "," + str(id_subcoll) + "," + str(id_log_entity) + "," + str(id_entity) + ", '" + code_entity + "'," + lot_name_final + ", " + str(log_dict[key]['id']) + "," + lang_name + ",'" + data_lookup.replace("'", "\\'") + "'),")
        elif(action == "insert"):
            for key, value in data.items():
                if ((key != 'insert') and (key != 'update') and (key != 'id') and (key != 'lang') and (key != 'hdnReusedStrain')):
                    
                    valor = self.ConvertStrUnicode((data[key]))
                    if ((valor != None) and (self.ConvertStrUnicode(valor) != "") and (self.ConvertStrUnicode(valor) != 'None')):
                        if key == "numeric_code":
                            data_lookup = code_entity
                        else:
                            data_lookup = valor if valor != None else ""
                            if ((key in log_dict) and (log_dict[key]['lookup'] != "")):
                                look = {}
                                look['id'] = valor
                                if key == "numeric_code_division":
                                    look['id'] = id_entity;
                                self.execute(log_dict[key]['lookup'], look)
                                data_lookup = self.fetch('one')                    
                            
                        lang_name = "NULL"
                        if ((key in log_dict) and (log_dict[key]['is_mlang'] == True)):
                            if lang != '':
                                lang_name = "'" + lang + "'"
                            
                        if id_entity != None and id_entity != '':
                            id_entity_final = id_entity
                        else:
                            id_entity_final = "'|%|ID|%|'"
                            
                        return_value.append("('"  + x.strftime('%Y-%m-%d %H:%M:%S') + "', '" + self.session.data['user_name'] + "'," + str(id_log_operation) + "," + str(id_subcoll) + "," + str(id_log_entity) + "," + str(id_entity_final) + ",'" + code_entity + "'," + lot_name_final + ", " + str(log_dict[key]['id']) + "," + lang_name + ",'" + data_lookup.replace("'", "\\'") + "'),")
        elif(action == "delete"):
            id_log_field = ""
            
            for key, value in data.items():
                if len(data) > 0:
                    id_log_field = str(log_dict[key]['id'])
                else:
                    id_log_field = "NULL"
            
                return_value.append("('"  + x.strftime('%Y-%m-%d %H:%M:%S') + "', '" + self.session.data['user_name'] + "'," + str(id_log_operation) + "," + str(id_subcoll) + "," + str(id_log_entity) + "," + str(id_entity) + ",'" + code_entity + "'," + lot_name_final + ", " + id_log_field + ", NULL, NULL ),")
            
        return return_value
        
    def checkLogLevel(self, id_log_level):
        id_subcoll = self.session.data['id_subcoll']
        data = {'id_subcoll':id_subcoll}
        
        #Start SQLite database
        db_sqlite = dbConnection()
        
        db_sqlite.execute('get_subcoll_log_level', data)
        return_log_level = db_sqlite.fetch('all')
        
        for log_level in return_log_level:
            if log_level['log_level'] == id_log_level:
                return True
                
        return False
        
    def listSubcollsLevel(self, id_log_level):
        #Start SQLite database
        db_sqlite = dbConnection()
        
        data = {'log_level':id_log_level}
        
        db_sqlite.execute('get_subcolls_level', data)
        return_subcolls = db_sqlite.fetch('all')
        
        list_id_subcolls = ''
        for subcoll in return_subcolls:
            list_id_subcolls += str(subcoll['id_subcoll']) + ','
                
        return list_id_subcolls
        
#dict for using in log records
log_dict = {

    #Strains General
    "id_division": {"id": "1", "lookup": "lookup_division_log", "is_mlang": False},
    "numeric_code": {"id": "2", "lookup": "lookup_pattern_log", "is_mlang": False},
    "numeric_code_division": {"id": "2", "lookup": "lookup_pattern_log", "is_mlang": False},
    "internal_code": {"id": "3", "lookup": "", "is_mlang": False},
    "status": {"id": "4", "lookup": "", "is_mlang": False},
    "id_species": {"id": "5", "lookup": "lookup_species_log", "is_mlang": False},
    "id_type": {"id": "6", "lookup": "", "is_mlang": False},
    "is_ogm": {"id": "7", "lookup": "", "is_mlang": False},
    "infra_complement": {"id": "8", "lookup": "", "is_mlang": False},
    "history": {"id": "9", "lookup": "", "is_mlang": False},
    "go_catalog": {"id": "89", "lookup": "", "is_mlang": False},
    "extra_codes": {"id": "10", "lookup": "", "is_mlang": False},
    "general_comments": {"id": "11", "lookup": "", "is_mlang": False},
        
    #Strains Origin
    "coll_date": {"id": "12", "lookup": "", "is_mlang": False},
    "coll_id_person": {"id": "13", "lookup": "lookup_person_log", "is_mlang": False},
    "coll_id_institution": {"id": "14", "lookup": "lookup_institution_log", "is_mlang": False},
    "coll_id_country": {"id": "15", "lookup": "", "is_mlang": False},
    "coll_id_state": {"id": "16", "lookup": "lookup_coll_state_log", "is_mlang": False},
    "coll_id_city": {"id": "17", "lookup": "lookup_coll_city_log", "is_mlang": False},
    "coll_place": {"id": "18", "lookup": "", "is_mlang": False},
    "coll_gps_latitude": {"id": "19", "lookup": "", "is_mlang": False},
    "coll_gps_longitude": {"id": "20", "lookup": "", "is_mlang": False},
    "coll_id_gps_datum": {"id": "21", "lookup": "lookup_gps_datum_log", "is_mlang": False},
    "coll_gps_precision": {"id": "22", "lookup": "", "is_mlang": False},
    "coll_gps_comments": {"id": "23", "lookup": "", "is_mlang": False},
    "coll_substratum": {"id": "24", "lookup": "", "is_mlang": True},
    "coll_host_name": {"id": "25", "lookup": "", "is_mlang": True},
    "coll_host_genus": {"id": "26", "lookup": "", "is_mlang": False},
    "coll_host_species": {"id": "27", "lookup": "", "is_mlang": False},
    "coll_host_classification": {"id": "28", "lookup": "", "is_mlang": False},
    "coll_host_infra_name": {"id": "29", "lookup": "", "is_mlang": False},
    "coll_host_infra_complement": {"id": "30", "lookup": "", "is_mlang": False},
    "coll_global_code": {"id": "31", "lookup": "", "is_mlang": False},
    "coll_id_clinical_form": {"id": "32", "lookup": "", "is_mlang": False},
    "coll_hiv": {"id": "33", "lookup": "", "is_mlang": False},
    "coll_comments": {"id": "34", "lookup": "", "is_mlang": True},
    "coll_gps_latitude_dms": {"id": "125", "lookup": "", "is_mlang": False},
    "coll_gps_latitude_mode": {"id": "126", "lookup": "", "is_mlang": False},
    "coll_gps_longitude_dms": {"id": "127", "lookup": "", "is_mlang": False},
    "coll_gps_longitude_mode": {"id": "128", "lookup": "", "is_mlang": False},
        
    #Strains Isolation
    "iso_date": {"id": "35", "lookup": "", "is_mlang": False},
    "iso_id_person": {"id": "36", "lookup": "lookup_person_log", "is_mlang": False},
    "iso_id_institution": {"id": "37", "lookup": "lookup_institution_log", "is_mlang": False},
    "iso_isolation_from": {"id": "38", "lookup": "", "is_mlang": True},
    "iso_method": {"id": "39", "lookup": "", "is_mlang": True},
    "iso_comments": {"id": "40", "lookup": "", "is_mlang": False},
        
    #Strains Identification
    "ident_date": {"id": "41", "lookup": "", "is_mlang": False},
    "ident_id_person": {"id": "42", "lookup": "lookup_person_log", "is_mlang": False},
    "ident_id_institution": {"id": "43", "lookup": "lookup_institution_log", "is_mlang": False},
    "ident_genus": {"id": "44", "lookup": "", "is_mlang": False},
    "ident_species": {"id": "45", "lookup": "", "is_mlang": False},
    "ident_classification": {"id": "46", "lookup": "", "is_mlang": False},
    "ident_infra_name": {"id": "47", "lookup": "", "is_mlang": False},
    "ident_infra_complement": {"id": "48", "lookup": "", "is_mlang": False},
    "ident_method": {"id": "49", "lookup": "", "is_mlang": True},
    "ident_comments": {"id": "50", "lookup": "", "is_mlang": False},        
        
    #Strains Deposit
    "dep_date": {"id": "51", "lookup": "", "is_mlang": False},
    "dep_id_person": {"id": "52", "lookup": "lookup_person_log", "is_mlang": False},
    "dep_id_institution": {"id": "53", "lookup": "lookup_institution_log", "is_mlang": False},
    "dep_genus": {"id": "54", "lookup": "", "is_mlang": False},
    "dep_species": {"id": "55", "lookup": "", "is_mlang": False},
    "dep_classification": {"id": "56", "lookup": "", "is_mlang": False},
    "dep_infra_name": {"id": "57", "lookup": "", "is_mlang": False},
    "dep_infra_complement": {"id": "58", "lookup": "", "is_mlang": False},
    "dep_id_reason": {"id": "59", "lookup": "", "is_mlang": False},
    "dep_form": {"id": "60", "lookup": "", "is_mlang": False},
    "dep_preserv_method": {"id": "61", "lookup": "", "is_mlang": False},
    "dep_aut_date": {"id": "62", "lookup": "", "is_mlang": False},
    "dep_aut_id_person": {"id": "63", "lookup": "lookup_person_log", "is_mlang": False},
    "dep_aut_result": {"id": "64", "lookup": "", "is_mlang": False},
    "dep_comments": {"id": "65", "lookup": "", "is_mlang": False},
        
    #Strains Growth
    "cul_medium": {"id": "66", "lookup": "", "is_mlang": True},
    "cul_temp": {"id": "67", "lookup": "", "is_mlang": False},
    "cul_incub_time": {"id": "68", "lookup": "", "is_mlang": True},
    "cul_ph": {"id": "69", "lookup": "", "is_mlang": False},     
    "cul_oxy_req": {"id": "70", "lookup": "", "is_mlang": True},
    "cul_comments": {"id": "71", "lookup": "", "is_mlang": True},
        
    #Strains Characteristcs        
    "cha_morphologic": {"id": "72", "lookup": "", "is_mlang": False},
    "cha_molecular": {"id": "73", "lookup": "", "is_mlang": False},
    "cha_biochemical": {"id": "74", "lookup": "", "is_mlang": False},
    "cha_immunologic": {"id": "75", "lookup": "", "is_mlang": False},        
    "cha_pathogenic": {"id": "76", "lookup": "", "is_mlang": False},
    "cha_genotypic": {"id": "77", "lookup": "", "is_mlang": False},
    "cha_ogm": {"id": "78", "lookup": "", "is_mlang": False},
    "cha_ogm_comments": {"id": "79", "lookup": "", "is_mlang": True},
    "cha_biorisk_comments": {"id": "80", "lookup": "", "is_mlang": True},
    "cha_restrictions": {"id": "81", "lookup": "", "is_mlang": True},
    "cha_pictures": {"id": "82", "lookup": "", "is_mlang": True},
    "cha_urls": {"id": "83", "lookup": "", "is_mlang": True},
    "cha_catalogue": {"id": "84", "lookup": "", "is_mlang": True},
        
    #Strains Properties
    "pro_properties": {"id": "85", "lookup": "", "is_mlang": True},
    "pro_applications": {"id": "86", "lookup": "", "is_mlang": True},
    "pro_urls": {"id": "87", "lookup": "", "is_mlang": True},
        
    #Field Stock
    "stock": {"id": "88", "lookup": "", "is_mlang": False},

    #Preservation
    "date_preservation": {"id": "90", "lookup": "", "is_mlang": False},
    "lot_name": {"id": "91", "lookup": "", "is_mlang": False},
    "id_user_preservation": {"id": "92", "lookup": "", "is_mlang": False},
    "id_method": {"id": "93", "lookup": "", "is_mlang": False},
    "info": {"id": "94", "lookup": "", "is_mlang": False},    
    "origin": {"id": "95", "lookup": "", "is_mlang": False},
    "original_name": {"id": "96", "lookup": "", "is_mlang": False},
    "stock_minimum": {"id": "97", "lookup": "", "is_mlang": False},
    "id_culture_medium": {"id": "98", "lookup": "", "is_mlang": False},
    "temp": {"id": "99", "lookup": "", "is_mlang": False},
    "incub_time": {"id": "100", "lookup": "", "is_mlang": False},
    "cryo": {"id": "101", "lookup": "", "is_mlang": False},
    "type": {"id": "102", "lookup": "", "is_mlang": False},
    "purity": {"id": "103", "lookup": "", "is_mlang": False},
    "counting": {"id": "104", "lookup": "", "is_mlang": False},
    "counting_na": {"id": "105", "lookup": "", "is_mlang": False},
    "macro": {"id": "106", "lookup": "", "is_mlang": False},
    "micro": {"id": "107", "lookup": "", "is_mlang": False},
    "result": {"id": "108", "lookup": "", "is_mlang": False},
    "obs": {"id": "109", "lookup": "", "is_mlang": False},
    "origin_lot": {"id": "120", "lookup": "", "is_mlang": False},        
        
    #Distribution
    "date": {"id": "110", "lookup": "", "is_mlang": False},    
    "id_user": {"id": "111", "lookup": "lookup_person_log", "is_mlang": False},
    "id_lot": {"id": "112", "lookup": "lookup_lot_log", "is_mlang": False},
    "id_institution": {"id": "113", "lookup": "lookup_institution_log", "is_mlang": False},
    "id_person": {"id": "114", "lookup": "lookup_person_log", "is_mlang": False},
    "reason": {"id": "115", "lookup": "", "is_mlang": False},
        
    #Quality Control
    "date_qc": {"id": "116", "lookup": "", "is_mlang": False},    
    "tec_resp": {"id": "117", "lookup": "lookup_person_log", "is_mlang": False},
    "id_lot_qc": {"id": "118", "lookup": "lookup_lot_log", "is_mlang": False},
    "test": {"id": "119", "lookup": "", "is_mlang": False},
  
}