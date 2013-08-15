#!/usr/bin/env python
#-*- coding: utf-8 -*-

#python imports
#from dbgp.client import brk
from cgi import escape
from urlparse import urljoin
from re import findall
from sys import exit
from urllib import urlencode
import cgi

#project imports
from session import Session
from dbconnection import dbConnection
from reports_common import Reports_Common
from labels import label_dict
from dom_xml import Xml
from label_values_reports import label_values_dict
from label_values_reports import values_dict

class XML_Report(Reports_Common):
    
    def __init__(self, param, cookie_value, conn=None):
        
        self.report_params = param
        self.fields_definition = {}
        self.code   = ""
        self.reserved_fields = {}        
                                
        
        if (conn == None):
            conn = dbConnection(cookie_value)
            
        self.sqliteConnection = dbConnection()        
        self.executesqlite = self.sqliteConnection.execute
        self.fetchsqlite = self.sqliteConnection.fetch
            
        self.dbconnection = conn   
                
        self.execute = conn.execute
        self.fetch = conn.fetch
        self.cursor = conn.cursor
        
        self.session = Session()
        self.session.load(cookie_value)
        
        self.get_report_info()
        
        self.execute('get_lang_by_code', {'code': self.report_params['id_language']} )
        self.id_report_lang = self.fetch('one')
        
        
    def write_report(self, param, num_group_by, append_where):
        
        output = ""
            
        space = " "
        i = 0

        if len(param['group']) == 0 or num_group_by >= len(param['group']):
                        
            #print space, "Final"
            if len(param.get('total','')) > 0:
                select, aggr = self.mount_total(param['total']['name'], param['total']['function'])      
                
                group = []
                group.append(param['total']['name'])
                
                try:
                    list = self.get_data(select, param['filters'], append_where, group)
                except Exception, err:
                    raise err
                
                #brk(host="localhost", port=9000)
                for line in list:
                    string = "<record>\n" + space
                    
                    if param['total']['function'] == 'count':
                        string = string + "<field" + space + "name=\"" + self.ConvertStrUnicode(label_dict[self.fields_definition[param['total']['name']]['label']]) +"\"" + space + "value=\"" + self.process_field(param['total']['name'], line[param['total']['name']]) + "\"/>\n"
                        string = string + "<field" + space + "name=\"Total\"" + space + "value=\"" + str(line[aggr]) + "\"/>\n"
                    else:
                        string = string + "<field" + space + "name=\"" + self.ConvertStrUnicode(label_dict[self.fields_definition[param['total']['name']]['label']]) +"\"" + space  + "aggregation=\"" + param['total']['function'] + "\"" + space + "value=\"" + str(line[aggr]) + "\"/>\n"
                    
                    string = string + "</record>\n"     
                    output = output + string
            
            else:
                try:
                    list = self.get_data(param['select'], param['filters'], append_where, [])
                except Exception, err:
                    raise err
                
                for line in list:
                    string = "<record>\n" + space            
                    for field in param['select']:
                        string = string + "<field" + space + "name=\"" + field + "\"" + "label=\"" + label_dict[self.fields_definition[field]['label']] + "\"" + space + "value=\"" + self.process_field(field, line[field]) + "\"/>\n"
                            
                    string = string + "</record>\n"     
                    output = output + string
        else:        
            select = []
            select.append(param['group'][num_group_by])        
            group = []
            group.append(param['group'][num_group_by])
                            
            list_group = self.get_data(select, param['filters'], append_where, group, True)
            
            for item in list_group:
                colspan = len(param['group']) + len(param['select']) - num_group_by
                if len(param.get('total','')) > 0:
                    colspan = colspan + 1
                
                output = output + "<group" + space + "field=\"" + param['group'][num_group_by] + "\"" + space + "value=\"" + self.process_field(param['group'][num_group_by], item[param['group'][num_group_by]]) + "\">\n"
                
                group_value = ''
                tmp = type(item[param['group'][num_group_by]]).__name__
                if tmp != "str":
                    group_value = param['group'][num_group_by] + " LIKE x'" + self.ConvertStrUnicode(item[param['group'][num_group_by]]).encode("utf-8").encode("hex") + "' "
                else:
                    group_value = param['group'][num_group_by] + " IS NULL "
                    
                output = output + self.write_report(param, 1 + num_group_by, append_where + " AND " + group_value)                
                
                output = output + "</group>\n"
                    
        return output
     
    
    def get_report_info(self):
        sql = '''
                SELECT reports.id_subcoll as id_subcoll,
                    report_types.code as code,
                    report_types.fields_definition as fields_definition
                    FROM
                    (reports JOIN report_types on reports.id_report_type = report_types.id_report_type)
                    WHERE reports.id_report = '''
        sql = sql + str(self.report_params['id_report'])
        
        self.execute("", fixed_sql = sql)
        data = self.fetch('all')              
        
        sqlite = '''
                    SELECT coll.code as code_coll,
                    coll.name as name_coll,
                    subcoll.code as code_subcoll,
                    subcoll.name as name_subcoll                
                    
                        FROM
                        subcoll_report_conf JOIN subcoll on (subcoll_report_conf.id_subcoll = subcoll.id_subcoll)
                        JOIN coll on (subcoll.id_coll = coll.id_coll)
                        
                        WHERE subcoll_report_conf.id_subcoll = '''
        sqlite = sqlite + str(data[0]['id_subcoll'])
        
        self.executesqlite("", fixed_sql = sqlite)
        data_sqlite = self.fetchsqlite('all')
       
        
        
        tmp = Xml("field", data[0]['fields_definition'])        
        self.fields_definition = tmp.get_dict('name', ['label', 'data_type', 'aggregate_function', 'label_value_lookup', 'function_lookup'])
        
        #brk(host="localhost", port=9000)
        
        self.reserved_fields['code_coll']       = data_sqlite[0]['code_coll']
        self.reserved_fields['name_coll']       = data_sqlite[0]['name_coll']
        self.reserved_fields['code_subcoll']    = data_sqlite[0]['code_subcoll']
        self.reserved_fields['name_subcoll']    = data_sqlite[0]['name_subcoll']
        
        self.reserved_fields['user']            = self.session.data['user_name']
        
        
        self.code              =              data[0]['code']
        
      
    def mount_report_file(self):              
        
        self.timeout = 0        
        output = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        output = output + "<report>\n"
         
        try:       
            table = self.write_report(self.report_params, 0, "")
        except Exception, err:
            raise err
        
        output = output + table
        
        output = output + "</report>\n"    
       
        
        import sys
        
        sys.stdout.write("Content-Type: text/xml\n")
        sys.stdout.write("Content-Length: " + str(len(output)) + "\n")
        sys.stdout.write("Content-Disposition: attachment; filename=\"sicol_report.xml\"\r\n\n")
        sys.stdout.write(output.encode("utf-8"))
       
        return output