#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#python imports
#from dbgp.client import brk
from cgi import escape
from urllib.parse import urljoin
from re import findall
from sys import exit
from urllib.parse import urlencode
import cgi

#project imports
from .session import Session
from .dbconnection import dbConnection
from .reports_common import Reports_Common
from .labels import label_dict
from .dom_xml import Xml
from .label_values_reports import label_values_dict
from .label_values_reports import values_dict

class Default_Html_Report(Reports_Common):    
    

    def __init__(self, param, cookie_value, conn=None):
        
        self.report_params = param
        self.fields_definition = {}
        self.code   = ""
        self.header = ""
        self.footer = ""
        self.css    = ""
        self.reserved_fields = {}
        self.timeout = 0
        
       
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
        #brk(host="localhost", port=9000)
        
        output = ""
            
        space = ""
        i = 0
        
        while i < num_group_by:
            space = space + "<td>&nbsp &nbsp &nbsp &nbsp</td>"
            i = i + 1
               
        #
        if len(param['group']) == 0 or num_group_by >= len(param['group']):
                        
            #print space, "Final"
            if  param.get('total',{}) != {}:
                #brk(host="localhost", port=9000)
                select, aggr = self.mount_total(param['total']['name'], param['total']['function'])
                
                
                group = []
                group.append(param['total']['name'])
                
                try:
                    list = self.get_data(select, param['filters'], append_where, group)
                except Exception as err:
                    raise err
                
                if param['header_position'] == 'internal':
                    string = "<tr>" + space
                    string = string + "<td>" + label_dict[self.fields_definition[param['total']['name']]['label']] + "</td>"
                    
                    if param['total']['function'] == 'count':
                        string = string + "<td align=\"right\">" + "Total" + "</td>"
                    
                    output = output + string + "</tr>\n"                
                
                for line in list:
                    string = "<tr>" + space
                    if param['total']['function'] == 'count':
                        string = string + "<td>" + self.process_field(param['total']['name'], line[param['total']['name']]) + "</td>"
                        
                    string = string + "<td align=\"right\">" + str(line[aggr]) + "</td>"
                    
                    string = string + "</tr>\n"     
                    output = output + string
            
            else:
                try:
                    list = self.get_data(param['select'], param['filters'], append_where, [])
                except Exception as err:
                    raise err
                
                if param['header_position'] == 'internal':
                    string = "<tr>" + space
                    for field in param['select']:
                        string = string + "<th>" + label_dict[self.fields_definition[field]['label']] + "</th>"                
                    string = string + "</tr>\n"     
                    output = output + string
                
                for line in list:
                    string = "<tr>" + space            
                    for field in param['select']:
                        string = string + "<td>" + self.process_field(field, line[field]) + "</td>"
                            
                    string = string + "</tr>\n"     
                    output = output + string
        else:        
            select = []
            select.append(param['group'][num_group_by])        
            group = []
            group.append(param['group'][num_group_by])
            #brk(host="localhost", port=9000)
            try:
                list_group = self.get_data(select, param['filters'], append_where, group, True)
            except Exception as err:
                    raise err
            
            
            for item in list_group:
                colspan = len(param['group']) + len(param['select']) - num_group_by
                colspan = colspan + 1
                if len(param.get('total','')) > 0 and param['total']['function'] == 'count':
                    colspan = colspan + 1
                
                output = output + "<tr>" + space + "<td class=\"group\" colspan=\"" + str(colspan) + "\">" +  self.process_field(param['group'][num_group_by], item[param['group'][num_group_by]]) + "</td>" + "</tr>\n"
                
                group_value = ''
                #group_value = param['group'][num_group_by] + " = '" + self.ConvertStrUnicode(item[param['group'][num_group_by]]).encode("utf8") + "' "
                tmp = type(item[param['group'][num_group_by]]).__name__
                if tmp != "str":
                    group_value = param['group'][num_group_by] + " LIKE x'" + self.ConvertStrUnicode(item[param['group'][num_group_by]]).encode("utf-8").encode("hex") + "' "
                else:
                    group_value = param['group'][num_group_by] + " IS NULL "
                    
                output = output + self.write_report(param, 1 + num_group_by, append_where + " AND " + group_value)        
                    
        return output    
    
    def get_report_info(self):
        sql = '''
                SELECT reports.id_subcoll as id_subcoll,
                    reports.description as description,
                    report_types.code as code,
                    report_types.fields_definition as fields_definition
                    FROM
                    (reports JOIN report_types on reports.id_report_type = report_types.id_report_type)
                    WHERE reports.id_report = '''
        sql = sql + str(self.report_params['id_report'])
        
        self.execute("", fixed_sql = sql)
        data = self.fetch('all')
        
        self.reserved_fields['description'] = data[0]['description']
        
        sqlite = '''
                    SELECT subcoll_report_conf.header as header,
                    subcoll_report_conf.footer as footer,
                    subcoll_report_conf.styles as styles,
                    coll.code as code_coll,
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
        
        self.header            =     data_sqlite[0]['header']
        self.footer            =     data_sqlite[0]['footer']
        self.css               =     data_sqlite[0]['styles']
        
        self.reserved_fields['code_coll']       = data_sqlite[0]['code_coll']
        self.reserved_fields['name_coll']       = data_sqlite[0]['name_coll']
        self.reserved_fields['code_subcoll']    = data_sqlite[0]['code_subcoll']
        self.reserved_fields['name_subcoll']    = data_sqlite[0]['name_subcoll']
        
        self.reserved_fields['user']            = self.session.data['user_name']
        
        
        self.code = data[0]['code']
    
    
    def mount_report_file(self):
        import base64
        
        self.timeout = 0
        
        output = "<html>\n"
        output = output + "<head>\n"
        output = output + self.getPageTitle()
        output = output + "<style type=\"text/css\">\n"
        output = output +  self.ConvertStrUnicode(base64.b64decode(self.css)) + "\n"
        output = output + "</style>\n</head>\n"
        output = output + "<body>\n"
        output = output + self.fill_reserved_fields(self.header) + "\n"       
        
        output = output + "<table border=\"1\">\n"
        
        if self.report_params['header_position'] == 'external':
            output = output + "<tr>"
            if len(self.report_params['group']) > 0:
                space = "<td colspan = '" + str(len(self.report_params['group'])) + "'>"
                output = output + space

            for field in self.report_params['select']:
                output = output + "<th>" + label_dict[self.fields_definition[field]['label']] + "</th>"
            
            if self.report_params.get('total',{}) != {}:
                output = output + "<th>" + label_dict[self.fields_definition[self.report_params.get('total',{'name':''}).get('name', '')]['label']] + "</th>"
                if self.report_params['total']['function'] == 'count':
                    output = output + "<th>Total</th>"
                
                
            
            output = output + "</tr>\n"
        
        
        
        try:
            table = self.write_report(self.report_params, 0, "")
        except Exception as err:
                    raise err
        
        output = output + table
        
        output = output + "</table>\n"
        output = output + self.fill_reserved_fields(self.footer) + "\n"
        output = output + "</body>\n"
        output = output + "</html>\n"    
       
        return output.replace('%', '%%')
       
    
    