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


class Custom_Html_Report(Reports_Common):    
   

    def __init__(self, param, cookie_value, conn=None):
        
        self.report_params = param
        self.fields_definition = {}
        self.code   = ""
        self.header = ""
        self.footer = ""
        self.css    = ""
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
        #brk("localhost", 9000)
        output = ""            
        
        if len(param['group']) == 0 or num_group_by >= len(param['group']):
            #brk("localhost", 9000)               
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
                    template = self.fill_template("FIELD", select, line, param['templates']['main']['data'])
                    output = output + template                
            else:
                import base64
                list = self.get_data(param['select'], param['filters'], append_where, [])
                
                #Parei aqui !!!!!!
                for line in list:
                    template = self.fill_template("FIELD", param['select'], line, param['templates']['main']['data'])
                    output = output + template                    
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
              
                #Get custom group header html
                template = self.fill_template("FIELD", select, {param['group'][num_group_by]:item[param['group'][num_group_by]]}, param['templates']['group'][param['group'][num_group_by]]['header'])                       
                output = output + template
                
                group_value = ''
                tmp = type(item[param['group'][num_group_by]]).__name__
                if tmp != "str":
                    group_value = param['group'][num_group_by] + " LIKE x'" + self.ConvertStrUnicode(item[param['group'][num_group_by]]).encode("utf-8").encode("hex") + "' "
                else:
                    group_value = param['group'][num_group_by] + " IS NULL "
                    
                output = output + self.write_report(param, 1 + num_group_by, append_where + " AND " + group_value)                
                
                
                #Get custom group footer html
                template = self.fill_template("FIELD", select, {param['group'][num_group_by]:item[param['group'][num_group_by]]}, param['templates']['group'][param['group'][num_group_by]]['footer'])                       
                output = output + template
                    
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
        
        self.header            =     data_sqlite[0]['header']
        self.footer            =     data_sqlite[0]['footer']
        self.css               =     data_sqlite[0]['styles']
        
        self.reserved_fields['code_coll']       = data_sqlite[0]['code_coll']
        self.reserved_fields['name_coll']       = data_sqlite[0]['name_coll']
        self.reserved_fields['code_subcoll']    = data_sqlite[0]['code_subcoll']
        self.reserved_fields['name_subcoll']    = data_sqlite[0]['name_subcoll']
        
        self.reserved_fields['user']            = self.session.data['user_name']
        
        
        self.code              =              data[0]['code']
        
    
    
    def mount_report_file(self):              
        
        self.timeout = 0
        
        import base64
        #brk(host="localhost", port=9000)
        output = "<html>\n"
        output = output + "<head>\n"
        output = output + self.getPageTitle()
        output = output + "<style type=\"text/css\">\n"
        
        #pegar css do report        
        output = output +  self.ConvertStrUnicode(base64.b64decode(self.report_params['templates']['main']['css'])) + "\n"
        
        #verifica se deve pegar css da subcoll        
        if self.report_params.get('append_subcoll_templates', 'false') == 'true':
            output = output + self.ConvertStrUnicode(base64.b64decode(self.css)) + "\n"
            
        
        output = output + "</style>\n</head>\n"
        output = output + "<body>\n"
        
        #verifica se deve pegar header da subcoll        
        if self.report_params.get('append_subcoll_templates', 'false') == 'true':
            output = output + self.fill_reserved_fields(self.header) + "\n"
        
        #pegar header do report
        output = output +  self.fill_reserved_fields(self.report_params['templates']['main']['header']) + "\n"
        
        try:       
            output = output + self.write_report(self.report_params, 0, "")
        except Exception, err:
                    raise err
        
        # pegar footer do report
        output = output +  self.fill_reserved_fields(self.report_params['templates']['main']['footer']) + "\n"
        
        #verifica se deve pegar footer da subcoll        
        if self.report_params.get('append_subcoll_templates', 'false') == 'true':
            output = output + self.fill_reserved_fields(self.footer) + "\n"
        
        output = output + "</body>\n"
        output = output + "</html>\n"      
        
        return output.replace('%', '%%')
                    
   