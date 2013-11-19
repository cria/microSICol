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
#from dbgp.client import brk


class CSV_Report(Reports_Common):
    
   
    def __init__(self, param, cookie_value, conn=None):
        
        self.report_params = param
        self.fields_definition = {}
        self.code = ""
        
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
    
   
        
    def write_report(self, param, num_group_by, append_where, look_back):
        
        output = ""

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
                
                for line in list:
                    string = ""
                    i = 0
                    for value in look_back:
                        string = string + self.process_field(param['group'][i], value) + str(param['separator']).decode("utf-8")
                        i = i + 1
                    
                    if param['total']['function'] == 'count':
                        string = string + self.process_field(param['total']['name'], line[param['total']['name']]) + str(param['separator']).decode("utf-8")
                        
                    string = string + self.ConvertStrUnicode(line[aggr]) + str(param['separator']).decode("utf-8")
                
                    string = string + "\n"
                                
                    output = output + string
            
            else:
                list = self.get_data(param['select'], param['filters'], append_where, [])
                
                
                
                for line in list:
                    string = ""
                    i = 0
                    for value in look_back:
                        string = string + self.process_field(param['group'][i], value) + str(param['separator']).decode("utf-8")
                        i = i + 1
                        
                    
                    for field in param['select']:
                        string = string + self.process_field(field, line[field]) + str(param['separator']).decode("utf-8")
                    
                    string = string + "\n"         
                    
                    output = output + string
                    
        else:        
            select = []
            select.append(param['group'][num_group_by])
            group = []
            group.append(param['group'][num_group_by])
               
            try:             
                list_group = self.get_data(select, param['filters'], append_where, group, True)
            except Exception, err:
                    raise err
            
            for item in list_group:
               #brk(host="localhost", port=9000)
               #value = 
                tmp = look_back[:]
                tmp.append(self.ConvertStrUnicode(item[param['group'][num_group_by]]))
                
                group_value = ''
                tmp2 = type(item[param['group'][num_group_by]]).__name__
                if tmp2 != "str":
                    group_value = param['group'][num_group_by] + " LIKE x'" + self.ConvertStrUnicode(item[param['group'][num_group_by]]).encode("utf-8").encode("hex") + "' "
                else:
                    group_value = param['group'][num_group_by] + " IS NULL "
               
                output = output + self.write_report(param, 1 + num_group_by, append_where + " AND " + group_value, tmp)                                
                
        return output

          
    
    def get_report_info(self):
        sql = '''
                SELECT report_types.code as code,
                    report_types.fields_definition as fields_definition
                    FROM
                    (reports JOIN report_types on reports.id_report_type = report_types.id_report_type)
                    WHERE reports.id_report = '''
        sql = sql + str(self.report_params['id_report'])
        
        self.execute("", fixed_sql = sql)
        data = self.fetch('all')              
                
        tmp = Xml("field", data[0]['fields_definition'])        
        self.fields_definition = tmp.get_dict('name', ['label', 'data_type', 'aggregate_function', 'label_value_lookup', 'function_lookup'])
        
        self.code              =              data[0]['code']
               
    
    
    def mount_report_file(self):              
              
        self.timeout = 0  
        output = ""
        #brk(host="localhost", port=9000)
        
        if self.report_params['header'] == 'true':
            
            for field in self.report_params['group']:
                output = output + label_dict[self.fields_definition[field]['label']] + str(self.report_params['separator']).decode("utf-8")
            
            for field in self.report_params['select']:
                output = output + label_dict[self.fields_definition[field]['label']] + str(self.report_params['separator']).decode("utf-8")
                
            if len(self.report_params.get('total','')) > 0:
                output = output + label_dict[self.fields_definition[self.report_params['total']['name']]['label']] + str(self.report_params['separator']).decode("utf-8")
                if self.report_params['total']['function'] == 'count':
                    output = output + "Total" + str(self.report_params['separator']).decode("utf-8")
            
            #output = output + "<br/>"
            output = output + "\n"
        
        
        
        try:
            table = self.write_report(self.report_params, 0, "", [])
        except Exception, err:
                    raise err
        
        output = output + table
        
        import sys
        
        sys.stdout.write("Content-Type: application/octet-stream\n")
        sys.stdout.write("Content-Length: " + str(len(output)) + "\n")
        sys.stdout.write("Content-Disposition: attachment; filename=\"sicol_report.csv\"\r\n\n")
        sys.stdout.write(output.encode("utf-8-sig"))
                        
        return output
        
        
  