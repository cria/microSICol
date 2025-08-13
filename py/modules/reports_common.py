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
from .general import General, DefDict
from .lists import Lists
from .textlinkfactory import TextLinkFactory
from .loghelper import Logging
from .location import LocationBuilder
from os import path
from datetime import datetime
from .labels import label_dict
from .dom_xml import Xml
from .label_values_reports import label_values_dict
from .label_values_reports import values_dict


class Reports_Common(object):
    #brk(host="localhost", port=9000)
    #Configs
    g = General()
    page_parts = {'top':'', 'submenu':'', 'hidden_forms':''}
    maxTime = float(g.get_config('report_timeout'))

    def __init__(self, param, cookie_value, conn=None):
        
        self.report_params = param
        self.fields_definition = {}       
        self.reserved_fields = {}
        self.code = ""
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
        
        
    
    
    def ConvertStrUnicode(self, valor):
        retorno = '';
        if isinstance(valor, (int, float)):
            return str(valor)
            
        if (isinstance(valor, str) == False):
            retorno = str(valor).decode("utf8")
        else:
            retorno = valor
        
        return retorno
    
    def  mount_filter(self, param):
        
        string = ""
        
        for filter in param:
            string = string + self.rec_mount_filter(filter)
        
        if string == "":
            return ""
        else:
            return "(" + string + ")"
        
    
    def get_value(self, value):    
        
        if str(value) == "NULL":
            return "NULL"
        else:
            return  "'" + self.ConvertStrUnicode(value) + "'" 
    
        string = ""
        
        list = value.split(",")
        
        if len(list) > 1:
            string = string + "("
        
        for word in list:            
            string = string + "'" + self.ConvertStrUnicode(word) + "'" + ","
        
        string = string[:len(string)-1]
        
        if len(list) > 1:
            string = string + ")"
            
        return string
    
    def translate(self, condition, field, user_defined, value, field_lookup):
        #brk(host="localhost", port=9000)
        conv_val = ''
        if field_lookup != '':
            conv_val = field_lookup
        else:
            if user_defined == 'True':              
                conv_val = self.ConvertStrUnicode(value)
            else:
                import base64
                conv_val = self.ConvertStrUnicode(base64.b64decode(value))
        
        if condition.lower() == 'equal':
            if field_lookup != '':
                return field + " = " + field_lookup
            if (self.ConvertStrUnicode(conv_val).upper() == "NULL" or self.ConvertStrUnicode(conv_val).upper() == "BRANCO"):
                return "(" + field + " is NULL or " + field + " = '')"
            else:
                return field + " LIKE ('" + conv_val.replace("'", "''").replace('&#34;', '"').replace('&#60;', '<').replace('&#62;', '>') + "')"
        if condition.lower() == 'differs':
            if field_lookup != '':
                return field + " <> " + field_lookup
            if (self.ConvertStrUnicode(conv_val).upper() == "NULL" or self.ConvertStrUnicode(conv_val).upper() == "BRANCO"):
                return "(" + field + " is NOT NULL or " + field + " <> '')"
            else:
                return field + " <> ('" + conv_val.replace("'", "''").replace('&#34;', '"').replace('&#60;', '<').replace('&#62;', '>') + "')"
        elif condition.lower() == 'greater_or_equal':
            return field + '>=' + conv_val
        elif condition.lower() == 'less_or_equal':
            return field + '<=' + conv_val
        elif condition.lower() == 'different':
            return field + '<>' + conv_val
        elif condition.lower() == 'greater':
            return field + '>' + conv_val
        elif condition.lower() == 'less':
            return field + '<' + conv_val
        else:
            return field + " " + self.prepare_condition(conv_val, condition, field_lookup)
    
    def prepare_condition(self, value, condition, lookup):
        
        if lookup != '' and condition.lower() in ('contains', 'starting', 'ending'):
                return " LIKE " + lookup
        
        val = value.replace("'", "''").replace('&#34;', '"').replace('&#60;', '<').replace('&#62;', '>')
        if condition.lower() == 'contains':
            return " LIKE (CONCAT('%','" + val + "','%'))"
        elif condition.lower() == 'starting':
            return " LIKE (CONCAT('" + val + "','%'))"
        elif condition.lower() == 'ending':
            return " LIKE (CONCAT('%','" + val + "'))"
        elif condition.lower() == 'in' or condition.lower() == 'not_in':
            if lookup != '':
                if condition.lower() == 'in':  
                    return " IN (" + lookup + ")"
                else:
                    return " NOT IN (" + lookup + ")"
                
            value_split = val.split(";")
            new_value = ""            
            for val in value_split:
                new_value += "'" + val.lstrip().rstrip() + "', "              
                        
            new_value = new_value[0:len(new_value)-2]
            if condition.lower() == 'in':  
                return " IN (" + new_value + ")"
            else:
                return " NOT IN (" + new_value + ")"            
        else:
            if lookup != '':
                return " = " + lookup
            else:        
                return " = " + value
        
    def rec_mount_filter(self, param):
        #brk(host="localhost", port=9000)
        filter = ""
        
        if len(param) == 0:
            return filter
        
        filter = filter + param['connector']
        filter = filter + " "
        
        if len(param['childs']) > 0:
            filter = filter + "( "        
        
        filter = filter + " " + self.translate(param['condition'], param['field'], param['user_defined'], param['value'], param['field_lookup']) + " "
               
        for child in param['childs']:
            filter = filter + self.rec_mount_filter(child)
            
        if len(param['childs']) > 0:
            filter = filter + " ) "
            
        return filter   
    
    def get_data(self, fields, where, append_where, group_by, distinct = False):
        #brk(host="localhost", port=9000)
        select = "SELECT "
        
        if distinct == True:
            select = select + "DISTINCT "
        
        for field in fields:
            select = select + field + ", "
            
        select = select[0:len(select)-2]
        select = select + " FROM (SELECT @report_lang := " + str(self.id_report_lang) +  " l) lang , " + self.code + "_report"    
                        
        select = select + " WHERE " + self.sql_user_group_report()
        
        if len(where) > 0 or len(append_where) > 0:
            select = select + " AND " + self.mount_filter(where)        
            if len(where) == 0:
                append_where = append_where.replace(" AND ", "", 1)            
                    
            select = select  + " " + append_where + " "
            
        
        groupby = ""
        if len(group_by) > 0:
            groupby =" GROUP BY "
            for field in group_by:
                groupby = groupby + field + ", "               
            select = select + groupby[0:len(groupby)-2] + " "        
            
        order =" ORDER BY "
        for field in fields:
            order = order + field + ", "               
        select = select + order[0:len(order)-2] + " "                
        
        import time
        start = time.clock()        
        self.execute("", fixed_sql = select)
                
        elapsed = (time.clock() - start)
        
        
        self.timeout = self.timeout + elapsed
        #brk(host="localhost", port=9000)
       
       
        
        if self.timeout > self.maxTime:            
            import sys            
            err = Exception()
            err.message = "Timeout: " + str(self.timeout)
            raise err
                       
        
        
        
        data = self.fetch('all')
              
        return data
    
    def sql_user_group_report(self):
        is_manager = "false"
        roles = "(0)"
        if self.g.isManager(self.session.data['roles']):
            is_manager = "true"
        else:
            roles = str(self.session.data['roles']).replace("L","")
            roles = roles.replace("[","(")
            roles = roles.replace("]",")")
    
        if (self.code == "strain" or self.code == "stock"):
            sql ='''        
            (
                id_subcoll = %s AND
                (%s OR id_strain IN (SELECT id_item FROM roles_permissions
                    WHERE id_role IN %s AND id_item = id_strain AND id_area = 2))
             )
            '''
            return  sql % (self.session.data['id_subcoll'], is_manager, roles)
        elif (self.code == "institution"):
            sql ='''        
            (
                (%s OR id_institution IN (SELECT id_item FROM roles_permissions
                    WHERE id_role IN %s AND id_item = id_institution AND id_area = 4))
             )
            '''
            return  sql % (is_manager, roles)
        elif (self.code == "person"):
            sql ='''        
            (
                (%s OR id_person IN (SELECT id_item FROM roles_permissions
                    WHERE id_role IN %s AND id_item = id_person AND id_area = 3))
             )
            '''
            return  sql % (is_manager, roles)
        elif (self.code == "doc"):
            sql ='''        
            (
                (%s OR id_doc IN (SELECT id_item FROM roles_permissions
                    WHERE id_role IN %s AND id_item = id_doc AND id_area = 5))
             )
            '''
            return  sql % (is_manager, roles)
        elif (self.code == "ref"):
            sql ='''        
            (
                (%s OR id_ref IN (SELECT id_item FROM roles_permissions
                    WHERE id_role IN %s AND id_item = id_ref AND id_area = 6))
             )
            '''
            return  sql % (is_manager, roles)
        elif (self.code == "species"):
            sql ='''        
            (
                id_subcoll = %s AND
                (%s OR id_species IN (SELECT id_item FROM roles_permissions
                    WHERE id_role IN %s AND id_item = id_species AND id_area = 1))
             )
            '''
            return  sql % (self.session.data['id_subcoll'], is_manager, roles)
        
    def write_report(self, param, num_group_by, append_where):
        
        output = ""        
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
                    SELECT 
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
        
        self.reserved_fields['code_coll']       = data_sqlite[0]['code_coll']
        self.reserved_fields['name_coll']       = data_sqlite[0]['name_coll']
        self.reserved_fields['code_subcoll']    = data_sqlite[0]['code_subcoll']
        self.reserved_fields['name_subcoll']    = data_sqlite[0]['name_subcoll']
        
        self.reserved_fields['user']            = self.session.data['user_name']
        
        
        self.code              =              data[0]['code']
        
    
    
    def mount_report_file(self):              
        
        output = ""        
        
        table = self.write_report(self.report_params, 0, "") 
        
        output = output + table       
       
        return output
       
    
    def fill_reserved_fields(self, template):
                    
        #brk(host="localhost", port=9000)        
        import base64
        template = self.ConvertStrUnicode(base64.b64decode(template))
        
        template = template.replace("[FIELD:date]", self.get_atual_date())
        template = template.replace("[FIELD:time]", self.get_atual_time())        
        
        for key in list(self.reserved_fields.keys()):
            template = template.replace("[FIELD:" + key + "]", self.ConvertStrUnicode(self.reserved_fields[key]))
        
        return template
    
    def fill_template(self, label_key, fields, dict_values, template):
                       
        template = self.fill_reserved_fields(template)       
         
        for field in fields:
            replace = "[" + label_key + ":" + field + "]"
            
            template = template.replace(replace, self.process_field(field, dict_values[field]))
                   
        return template
    
    def get_atual_time(self):
        import time
        atual = time.localtime()
        
        atual_time = ""
        
        id_lang = self.session.data['id_lang']
        
        if id_lang == 2:
            if atual[3] < 10:
                atual_time = "0" + str(atual[3])
            else:
                atual_time = str(atual[3])
            if atual[4] < 10:
                atual_time = atual_time + ":0" + str(atual[4])
            else:
                atual_time = atual_time + ":" + str(atual[4])
            if atual[5] < 10:
                atual_time = atual_time + ":0" + str(atual[5])
            else:
                atual_time = atual_time + ":" + str(atual[5])
        
        elif id_lang == 1:            
            tmp = 0
            if atual[3] > 12:
                tmp = atual[3] - 12
            else:
                tmp = atual[3]
            if tmp < 10:
                atual_time = "0" + str(tmp)
            else:
                atual_time = str(tmp)
            
            if atual[4] < 10:
                atual_time = atual_time + ":0" + str(atual[4])
            else:
                atual_time = atual_time + ":" + str(atual[4])
            if atual[5] < 10:
                atual_time = atual_time + ":0" + str(atual[5])
            else:
                atual_time = atual_time + ":" + str(atual[5])
                
            if atual[3] > 12:
                atual_time = atual_time + " PM"
            else:
                atual_time = atual_time + " AM"                             
        
        return atual_time     
            
        
    def get_atual_date(self):
        import time
        atual_time = time.localtime()
        
        format = self.get_dateformat('output')
        
        atual_date = ""
        
        if format == '%d/%m/%Y':            
            if atual_time[2] < 10:
                atual_date = "0" + str(atual_time[2])
            else:
                atual_date = str(atual_time[2])
                
            if atual_time[1] < 10:
                atual_date = atual_date + "-0" + str(atual_time[1])
            else:
                atual_date = atual_date + "-" + str(atual_time[1])
                
            atual_date = atual_date + "-" + str(atual_time[0])
            
        elif format == '%m/%d/%Y':
            if atual_time[1] < 10:
                atual_date = "0" + str(atual_time[1])
            else:
                atual_date = str(atual_time[1])
            
            if atual_time[2] < 10:
                atual_date = atual_date + "-0" + str(atual_time[2])
            else:
                atual_date = atual_date + "-" + str(atual_time[2])
                            
            atual_date = atual_date + "-" + str(atual_time[0])
        
        elif format == '%Y/%m/%d':
            atual_date = str(atual_time[0])
            
            if atual_time[1] < 10:
                atual_date = atual_date + "-0" + str(atual_time[1])
            else:
                atual_date = atual_date + "-" + str(atual_time[1])
                
            if atual_time[1] < 10:
                atual_date = atual_date + "-0" + str(atual_time[2])
            else:
                atual_date = atual_date + "-" + str(atual_time[2])
            
            
        return atual_date
            
            
        
        
    def format_date(self,action,field):
        '''
        Formats SQL date format (YYYY-mm-dd) to current locale date format
        '''
        if field: #field is a datetime.date object
            from time import strftime,strptime
            if action == 'edit':
              return strftime(self.get_dateformat('input'),field.timetuple())
            else: #view
              return strftime(self.get_dateformat('output'),field.timetuple())
        else: return ''

    def sql_dateformat(self, date):
        '''
        Get locale date format ("dd/mm/YYYY", for example) and change it to SQL format: "YYYY-mm-dd"
        '''
        from time import strftime, strptime

        #Put received date string into default format
        date = date.replace('.','/')
        date = date.replace('-','/')
        date = date.split('/')

        #Not a valid date
        if len(date) != 3: return ''
        if len(date[2]) == 2 or len(date[2]) == 1: #Convert 1 or 2-digit year to 4-digit year
          import datetime
          date[2] = int(date[2])
          if date[2] <= int(str(datetime.date.today().year)[2:]):
            date[2] += 2000
            date[2] = str(date[2])
          else:
            date[2] += 1900
            date[2] = str(date[2])
        date = "/".join(date)
        sql_date = strftime("%Y-%m-%d",strptime(date,self.get_dateformat('input')))
        return sql_date
    
    def get_dateformat(self, act):
        '''
        Get locale date format for action. act values: (input|output)
        '''
        if act == 'input':
            if self.session.data['date_input_mask'] is not None and self.session.data['date_input_mask'] != "":
                return self.session.data['date_input_mask']
            elif self.g.get_config('date_input_mask') is not None and self.g.get_config('date_input_mask') != "":
                return self.g.get_config('date_input_mask')
            else:
                return '%d/%m/%Y'
        elif act == 'output':
            if self.session.data['date_output_mask'] is not None and self.session.data['date_output_mask'] != "":
                return self.session.data['date_output_mask']
            elif self.g.get_config('date_output_mask') is not None and self.g.get_config('date_output_mask') != "":
                return self.g.get_config('date_output_mask')
            else:
                return '%d/%m/%Y'
        else:
             Exception, _("Argument is invalid.")
             
    
    def process_field(self, field_name, value):
        #brk(host="localhost", port=9000)
               
        if field_name not in self.fields_definition:
            return str(value)
            
        if 'function_lookup' in self.fields_definition[field_name]:
            return getattr(self, self.fields_definition[field_name]['function_lookup'])(value)
        
        if 'label_value_lookup' in self.fields_definition[field_name]:
            if self.fields_definition[field_name]['label_value_lookup'] == 'true':
                tmp = values_dict[label_values_dict[field_name][value]]
                return tmp
        
        if self.fields_definition[field_name]['data_type'] == 'date':
            return self.format_date('view', value)
        else:
            return self.ConvertStrUnicode(value)
    
    def mount_total(self, name, function):
        vet = []        
        aggr = ''
        if function == 'count':
            aggr = 'count(*)'
            vet.append(name)            
            
        elif function == 'sum':
            aggr = 'sum(' + name + ')'
            
        vet.append(aggr)
        
        return vet, aggr    
        
    def getPageTitle(self):
        return "<title>" + label_dict["label_Rep_page_title"] + "</title>\n"
    
    def get_location(self, position): #, id_container-id_container_hierarchy-row-col
        #return ""
        position = position.split("-")
        id_container = int(position[0])
        id_container_hierarchy = int(position[1])
        row = int(position[2])
        col = int(position[3])
        
        data = { 'id_container': id_container }
        
        self.execute('get_container', data)
        container = self.fetch('columns')['abbreviation']
        
        self.execute('get_container_hierarchy_tree', data)
        rows = self.fetch('all')
        
        data["id_container_hierarchy"] = id_container_hierarchy
        
        self.execute('get_location_data', data)
        row_data = self.fetch('columns')
        loc_data = { 
                'row': LocationBuilder.get_label(row_data['ini_row'], row), 
                'col': LocationBuilder.get_label(row_data['ini_col'], col) }
        
        fmt_location = row_data['pattern'] % loc_data
        
        parent_row = {}
        start_row = None
        for row in rows:
            #self.logger.debug(row)
            if row['id_container_hierarchy']:
                parent_row[row['id_container_hierarchy']] = row
            if str(row['id_container_hierarchy']) == str(id_container_hierarchy):
                start_row = row
        
        #self.logger.debug("*** start_row: %s" % str(start_row))
        location_name = []
        if start_row:
            current_row = start_row
            while True:
                if len(location_name) > 0:
                    location_name.insert(0, ' ')
                location_name.insert(0, current_row['abbreviation'])
                if current_row['id_parent']:
                    current_row = parent_row[current_row['id_parent']]
                else:
                    break

        location_name.insert(0, container + ' ')
        location_name.append(' ')
        location_name.append(fmt_location)

        #self.logger.debug(location_name)

        return "".join(location_name)