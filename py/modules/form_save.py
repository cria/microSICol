#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#python imports
from sys import exit
from os import path, rename,sep
from pickle import dump
from glob import glob
try:
    from hashlib import sha1 as new_sha
except ImportError:
    from sha import new as new_sha
from urllib.parse import urljoin

#project imports
from .session import Session
from .dbconnection import dbConnection
from .general import General
from .sciname import SciNameBuilder
from .loghelper import Logging
from .log import Log
from . import exception
#from dbgp.client import brk

class Save(object):
    g = General()

    root_dir = g.get_config('root_dir')
    doc_dir = path.join(root_dir, 'doc_file')
    index_url = g.get_config('index_url')

    #brk(host="localhost", port=9000)

    def __init__(self, cookie_value, form):
        self.cookie_value = cookie_value
        #Load session
        self.session = Session()
        self.session.load(cookie_value)

        #Logging
        self.logger = Logging.getLogger("form_save")
        self.d = self.logger.debug

        #Define Database
        self.dbconnection = dbConnection(cookie_value)
        self.execute = self.dbconnection.execute
        self.fetch = self.dbconnection.fetch
        self.cursor = self.dbconnection.cursor

        self.l = Log(cookie_value, self.dbconnection)

        #Define global variables
        self.action = form.getvalue('next_action')
        self.form = form
        self.data_lang = self.session.data['data_langs'] #ids for content languages
        self.data_lang_onedict = {}
        for lang_dict in self.data_lang:
            self.data_lang_onedict.update(lang_dict)
        self.html = {'message':'','submenu':''}

        if (form.getvalue('row')):
            row = form.getvalue('row')
        else:
            row = ''

        #Define Data Dict
        data = {}
        data['id'] = self.form.getvalue('id')
        data['id_coll'] = self.session.data['id_coll']
        data['id_subcoll'] = self.session.data['id_subcoll']
        data['id_user'] = self.session.data['id_user']
        data['row'] = row
        self.data = data

    def set(self, who):
        self.who_detail = 'py/%s.detail.py?id=' % who
        if who == 'species': self.species()
        elif who == 'strains': self.strains()
        elif who == 'doc': self.doc()
        elif who == 'ref': self.ref()
        elif who == 'people': self.people()
        elif who == 'institutions': self.inst()
        elif who == 'distribution': self.distribution()
        elif who == 'preservation': self.preservation()
        elif who == 'reports': self.reports()
        elif who == 'stockmovement': self.stockmovement()
        elif who == 'container': self.container()
        return self.html

    def verify_data(self, data_dict):
        data_dict['insert'] = False
        for item in data_dict:
            if item:
                data_dict['insert'] = True
                break
        return data_dict

    def verify_notnull_fields(self, fields='',who=''):
        '''
        Verify if all given fields are found in self.form
        If who is 'ref' or 'doc' then at least one 'title' must be found
        '''
        error = False
        from . import config
        out = config.http_header+'\n\n'
        out += '<b>%s</b>: %s:<br>\n' % (_("Error"), _("Obrigatory fields left blank"))
        main_title = '' #To be used when there is no other title in other languages
        for field in fields:
            if (who == 'doc' and field == 'title'):
                for lang in self.data_lang:
                    fields.append("%s_%s" %(field,list(lang.keys())[0]))
            elif (who == 'doc') and main_title == '' and field.startswith('title_') and self.form.getvalue(field):
                main_title = self.form.getvalue(field)
            elif self.form.getvalue(field) == None and who == '':
                error = True
                out += ' - %s <b>%s</b> %s<br>\n' % (_("field"), field.title(), _("must not be empty."))
                break
            elif not self.form.getvalue(field) and who == '':
                error = True
                out += ' - %s <b>%s</b> %s<br>\n' % (_("field"), field.title(), _("must not be empty."))

        if (who == 'doc'):
            if main_title == '': #There must be at least one title filled
                error = True
                out += ' - %s <b>%s</b> %s<br>\n' % (_("field"), field.title(), _("must not be empty."))
            else:
                return main_title
        if error:
            print(out.encode('utf8'))
            exit(1)

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
            raise Exception(_("Argument is invalid."))


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

    def sql_dateformat(self,date):
        '''
        Get locale date format ("dd/mm/YYYY", for example) and change it to SQL format: "YYYY-mm-dd"
        '''
        from time import strftime, strptime
        if date is None: return None
        if self.session.data['date_input_mask'] is not None and self.session.data['date_input_mask'] != "": date_format = self.session.data['date_input_mask']
        else: date_format = self.g.get_config('date_input_mask')
        #If we can't find date_format attribute in config.xml then use a default date format
        if date_format is None:
            date_format = '%d/%m/%Y'
        #Put received date string into default format
        date = date.replace('.','/')
        date = date.replace('-','/')
        date = date.split('/')
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
        sql_date = strftime("%Y-%m-%d",strptime(date,date_format))
        return sql_date

    def feedback(self, value, id_ok=None):
        if value == -1: #Errors
            import sys
            file_name = sys.exc_traceback.tb_frame.f_code.co_filename
            file_name = file_name[file_name.rfind(sep)+1:] #sep == os.sep - Operational System Separator '/' or '\\'
            ex_type = str(sys.exc_info()[0]).strip("'>").split('.')
            ex_type = str(ex_type[1])
            str_error = '<div class="user_error"><b>'+_("File")+'</b>: '+file_name+'<br />'
            str_error += '<b>'+_("Line")+'</b>: '+str(sys.exc_traceback.tb_lineno)+'<br />'
            str_error += '<b>'+_("Type")+'</b>: '+ex_type+'<br />'
            if not sys.exc_value.args:
                ex_error = "None"
            elif isinstance(sys.exc_value.args[0],int):
                ex_error = str(sys.exc_value.args[0])
            else:
                ex_error = sys.exc_value.args[0].encode('utf8')
            str_error += '<b>'+_("Value")+'</b>: %s</div>' % ex_error.decode('utf8')
            self.html['error_info'] = str_error
        elif value == 1: #Success
            self.session.data['feedback'] = 1
            self.session.save()

            data = self.data

            if ('row' in data and data['row'] != ''):
                str_row = '&row=' + data['row']
            else:
                str_row = ''

            from . import exception
            redirect_url = urljoin(self.index_url, self.who_detail + str(id_ok) + str_row)
            raise exception.SicolException("REDIRECT:" + redirect_url)

    def supportMultiLanguage(self, field_names):
        data_lang = self.data_lang
        form = self.form
        dataObject = {}
        for language in data_lang:
            lang = list(language.keys())[0]
            for field_name in field_names:
                if lang not in dataObject:
                    dataObject.update({lang:{}})
                if "%s_%s"%(field_name,lang) in form:
                    dataObject[lang].update({field_name:form.getvalue("%s_%s"%(field_name,lang))})
                else:
                    dataObject[lang].update({field_name:''})
        return dataObject


    #=========#
    # SPECIES #
    #=========#
    def species(self):
        #brk(host="localhost", port=9000)

        #Test NotNull Fields
        notnulls = ['taxon_group']
        return_sql = []
        if self.action != 'insert': notnulls.append('id')
        self.verify_notnull_fields(notnulls)

        form = self.form
        data = self.data
        data_fields = self.supportMultiLanguage(('ambient_risk', 'comments'));

        #Check whether item has already been included or updated
        is_first = True
        try:
            for lang in data_fields:
                #Species Data
                data['id_taxon_group'] = form.getvalue('taxon_group')
                data['taxon_ref'] = form.getvalue('taxon_ref')
                data['synonym'] = form.getvalue('synonym')
                data['hazard_group'] = form.getvalue('hazard_group')
                data['hazard_group_ref'] = form.getvalue('hazard_group_ref')
                data['id_alt_states'] = form.getvalue('id_alt_states')
                data['id_sciname'] = form.getvalue('id_sciname')
                data['sciname'] = form.getvalue('sciname_html')
                data['alt_state'] = form.getvalue('alt_state')
                if (form.getvalue('alt_state') != None):
                    data['alt_state_type'] = form.getvalue('alt_state_type')
                else:
                    data['alt_state_type'] = ''

                #multilanguage fields
                data_mlang = {}
                data_mlang['ambient_risk'] = data_fields[lang]['ambient_risk']
                data_mlang['comments'] = data_fields[lang]['comments']

                data['data_lang'] = self.data_lang_onedict[lang]
                data.update(data_mlang)

                if is_first:
                    sciname = SciNameBuilder(self.cookie_value, self.dbconnection)
                    if self.action == 'insert':
                        data['id_sciname'] = sciname.insert(self.session.data['id_subcoll'], self.session.data['id_lang'], form)
                        self.execute('insert_species', data)
                        #Get id_inserted and insert others Species parts
                        self.execute('last_insert_id')
                        data['id'] = self.dbconnection.fetch('one')
                    elif self.action == 'update':
                        #Verify using log
                        log = False
                        id_log_level = 1
                        if self.l.checkLogLevel(id_log_level):

                            #Verify change in 'name' field
                            self.execute('lookup_species_log', data)
                            fieldInDB = self.fetch('one')

                            if fieldInDB != data['sciname']:

                                #Verify in use screen 'strain' field 'sciname'
                                id_log_operation = 4
                                id_log_entity = 1

                                #General
                                self.execute('exists_sciname_usage_in_strain_general', data)
                                scinames = self.fetch('all')
                                
                                if scinames:
                                    log = True

                        sciname.update(self.session.data['id_subcoll'], self.session.data['id_lang'], data['id_sciname'], form)
                        self.execute('update_species', data)
                    #Security Info
                    self.g.apply_item_permission(self.dbconnection, 'species', form, data, self.action)
                    is_first = False

                if (self.action == 'update'):
                    #Update Species

                    #Test if insert or update Species parts
                    self.execute('count_species_parts_multilanguage', data)
                    counts = self.dbconnection.fetch('columns')
                    ambient_risk_exists = counts['count_ambient_risk']
                    comments_exists = counts['count_comments']

                    #update or insert ambient_risk
                    if (ambient_risk_exists):
                        if data_mlang['ambient_risk']: self.execute('update_spe_ambient_risk_multilanguage', data)
                        else: self.execute('delete_spe_ambient_risk_multilanguage',data)
                    elif data_mlang['ambient_risk']: self.execute('insert_spe_ambient_risk_multilanguage', data)

                    #update or insert comments
                    if (comments_exists):
                        if data_mlang['comments']: self.execute('update_spe_comments_multilanguage', data)
                        else: self.execute('delete_spe_comments_multilanguage', data)
                    elif data_mlang['comments']: self.execute('insert_spe_comments_multilanguage', data)
                    
                    #Log
                    if log:
                        log = False
                        
                        #General
                        for sci_name in scinames:
                            dict_temp = {'id_species' : data['id'], 'id' : data['id'], 'lang' : lang }
                            #Used the function 'checkModifiedFields' with parameter 'insert' just to generate the string insertion
                            return_sql.extend(self.l.checkModifiedFields('', dict_temp, sci_name['id_strain'], sci_name['code'], lang, 'insert', id_log_operation, id_log_entity,''))
                        scinames = []
        
                        #Write log
                        if return_sql:
                            dict_db_log = {}
                            dict_db_log = self.g.get_log_db({'id_base':self.session.data['id_base']})
        
                            #Define Database
                            self.db_log = dbConnection(base_descr = dict_db_log)
                            self.execute_log = self.db_log.execute
                            self.execute_log('insert_log', {'insert_values_log':"".join(return_sql)[0:len("".join(return_sql))-1]}, raw_mode = True)

                elif (self.action == 'insert'):
                    #Insert Species
                    if data_mlang['ambient_risk']: self.execute('insert_spe_ambient_risk_multilanguage', data)
                    if data_mlang['comments']: self.execute('insert_spe_comments_multilanguage', data)

                #Relation for alt_stat with other specie
                if (data['alt_state'] != None):
                    if (data['alt_state_type'] == 'ana'): alt_state_type = 'teleo'
                    else: alt_state_type = 'ana'
                    self.execute('update_remove_alt_state', {'id_alt_states': data['alt_state'], 'id_species': data['id']})
                    self.execute('update_alt_state', {'id_alt_states': data['id'], 'alt_states_type': alt_state_type, 'id_species': data['alt_state']})
                else:
                    if (data['id_alt_states'] != None):
                        self.execute('update_alt_state', {'id_alt_states': None, 'alt_states_type': None, 'id_species': data['id_alt_states']})

        except Exception as e:
            self.dbconnection.connect.rollback()
            if return_sql: self.db_log.connect.rollback()
            self.feedback(-1)
        else:
            self.dbconnection.connect.commit()
            if return_sql: self.db_log.connect.commit()
            self.feedback(1, data['id'])

    #=========#
    # STRAINS #
    #=========#
    def strains(self):
        #brk(host="localhost", port=9000)

        #Test NotNull Fields
        notnulls = ['numeric_code','id_species']
        if self.action != 'insert': notnulls.append('id')
        self.verify_notnull_fields(notnulls)

        form = self.form
        data = self.data
        data_fields = self.supportMultiLanguage((
            'coll_host_name', 'coll_substratum', 'coll_comments','iso_isolation_from','iso_method',
            'ident_method', 'cul_medium', 'cul_incub_time', 'cul_comments','cul_oxy_req',
            'cha_ogm_comments', 'cha_biorisk_comments', 'cha_restrictions',
            'cha_pictures', 'cha_urls', 'cha_catalogue','pro_properties',
            'pro_applications','pro_urls'));

        #id_log_entity for strains is 1
        id_log_entity = 1

        #id log operation for strain
        if (self.action == 'insert'):
            id_log_operation = 1
        else:
            id_log_operation = 2

        #Check whether item has already been included or updated
        is_first = True
        return_sql = []

        id_log_level = 1
        save_log = self.l.checkLogLevel(id_log_level)
        
        #Define Database log
        dict_db_log = {}
        dict_db_log = self.g.get_log_db({'id_base':self.session.data['id_base']})

        #execute log, if it is <> ''
        self.db_log = dbConnection(base_descr = dict_db_log)

        try:
            for lang in data_fields:

                #Strain Data
                self.html['id'] = data['id']
                data['data_lang'] =  self.data_lang_onedict[lang]

                #General
                general = {}
                general['id_division'] = form.getvalue('id_division')

                autonum = form.getvalue('autonum')
                if autonum: # user opted for auto numerated strain code
                    self.execute('get_next_strain_code', {'id_coll':self.session.data['id_coll']})
                    next_numeric_code = self.fetch('one')

                    general['numeric_code'] = next_numeric_code
                else:
                    general['numeric_code'] = form.getvalue('numeric_code')
                    
                if is_first:
                    count = 0
                    
                    if self.action == 'insert':
                        #Validate uniqueness of numeric_code and id_coll
                        self.execute('get_numeric_code_and_id_coll_usage_insert', {'numeric_code': general['numeric_code'], 'id_coll': self.session.data['id_coll']})
                        count = self.fetch('one')
                    elif self.action == 'update':
                        #Validate uniqueness of numeric_code and id_coll
                        self.execute('get_numeric_code_and_id_coll_usage_update', {'numeric_code': general['numeric_code'], 'id_coll': self.session.data['id_coll'], 'id_strain': data['id']})
                        count = self.fetch('one')
                        
                    if count > 0:
                        raise Exception(_("This numeric code already exists in database."))

                from .strain_formatter import StrainFormatter
                s = StrainFormatter(self.cookie_value)
                data['code'] = s.format_strain_code_with_division(general['numeric_code'],
                                                                  general['id_division'])

                general['internal_code'] = form.getvalue('internal_code')
                general['status'] = form.getvalue('status')
                general['id_species'] = form.getvalue('id_species')
                general['infra_complement'] = form.getvalue('infra_complement')
                general['id_type'] = form.getvalue('id_type')
                if 'is_ogm' in form:
                  general['is_ogm'] = 1
                else:
                  general['is_ogm'] = 0
                if 'go_catalog' in form:
                  general['go_catalog'] = 1
                else:
                  general['go_catalog'] = 0
                general['history'] = form.getvalue('history')
                general['extra_codes'] = form.getvalue('extra_codes')
                general['general_comments'] = form.getvalue('general_comments')
                general['id'] = data['id']
                data.update(general)

                if is_first and save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_general_log', general, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));

                #Deposit
                dep = {}
                dep['dep_id_person'] = form.getvalue('dep_person')
                dep['dep_id_institution'] = form.getvalue('dep_institution')
                dep['dep_genus'] = form.getvalue('dep_genus')
                dep['dep_species'] = form.getvalue('dep_species')
                dep['dep_classification'] = form.getvalue('dep_classification')
                dep['dep_infra_name'] = form.getvalue('dep_infra_name')
                dep['dep_infra_complement'] = form.getvalue('dep_infra_complement')
                dep['dep_date'] = self.sql_dateformat(form.getvalue('dep_date'))
                dep['dep_id_reason'] = form.getvalue('dep_reason')
                dep['dep_preserv_method'] = form.getvalue('dep_preserv_method')
                dep['dep_form'] = form.getvalue('dep_form')
                dep['dep_aut_date'] = self.sql_dateformat(form.getvalue('dep_aut_date'))
                dep['dep_aut_id_person'] = form.getvalue('dep_aut_person')
                dep['dep_aut_result'] = form.getvalue('dep_aut_result')
                dep['dep_comments'] = form.getvalue('dep_comments')
                dep['id'] = data['id']
                dep = self.verify_data(dep)
                data.update(dep)

                if is_first and save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_deposit_log', dep, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));

                #Collection Event
                coll = {}
                coll['coll_id_person'] = form.getvalue('coll_person')
                coll['coll_id_institution'] = form.getvalue('coll_institution')
                coll['coll_date'] = self.sql_dateformat(form.getvalue('coll_date'))
                coll['coll_id_country'] = form.getvalue('coll_country')
                coll['coll_state'] = form.getvalue('coll_state')
                coll['coll_city'] = form.getvalue('coll_city')

                #Check whether we have a new state or not
                coll['coll_id_state'] = ''
                if (coll['coll_state'] is not None):
                    #Erase csc.js (in order to force it to be updated when needed)
                    from os import path,unlink
                    js_csc = path.join(self.g.get_config("root_dir"),self.g.get_config("js_dir"),"csc_%s.js" % self.session.data['db_name'])
                    if (path.exists(js_csc)): unlink(js_csc)
                    #Get state name and state code
                    v_state = coll['coll_state'].rsplit('(',1)
                    v_code = v_state[1].split(')')
                    coll['coll_state'] = v_state[0]+v_code[1]
                    coll['coll_code'] = v_code[0]
                    self.execute('get_state_id',coll)
                    state_id = self.dbconnection.fetch('one')
                    if (state_id == ''):
                        #Then we have to insert a new one
                        #loc_state Table
                        self.execute('insert_state',coll)
                        self.execute('last_insert_id')
                        coll['coll_id_state'] = self.dbconnection.fetch('one')
                    else:
                        coll['coll_id_state'] = state_id
                    del coll['coll_code']

                del coll['coll_state']

                #Check whether we have a new city or not
                coll['coll_id_city'] = ''
                if (coll['coll_city'] is not None):
                    #Erase csc.js (in order to force it to be updated when needed)
                    from os import path,unlink
                    js_csc = path.join(self.g.get_config("root_dir"),self.g.get_config("js_dir"),"csc.js")
                    if (path.exists(js_csc)): unlink(js_csc)
                    #Get city info
                    self.execute('get_city_id',coll)
                    city_id = self.dbconnection.fetch('one')
                    if (city_id == ''):
                        if (coll['coll_id_state'] != ''):
                          #Then we have to insert a new one
                          #loc_city Table
                          self.execute('insert_city',coll)
                          self.execute('last_insert_id')
                          coll['coll_id_city'] = self.dbconnection.fetch('one')
                    else:
                        coll['coll_id_city'] = city_id
                del coll['coll_city']

                coll['coll_place'] = form.getvalue('coll_place')
                coll['coll_gps_latitude'] = form.getvalue('coll_gps_latitude')
                coll['coll_gps_longitude'] = form.getvalue('coll_gps_longitude')
                #Format value to DMS and DECIMAL standards
                import re
                #LATITUDE
                coll['coll_gps_latitude_mode'] = None
                coll['coll_gps_latitude_dms'] = None
                if coll['coll_gps_latitude'] != None and coll['coll_gps_latitude'] != '':
                  if re.search(r"[^-0-9.+]",coll['coll_gps_latitude']): #DMS input
                    dec = self.g.gps_dms2dec('latitude',coll['coll_gps_latitude'])
                    coll['coll_gps_latitude_mode'] = 'dms'
                    coll['coll_gps_latitude_dms'] = self.g.gps_dec2dms('latitude',dec)
                    coll['coll_gps_latitude'] = '%.8f' % round(float(dec), 8)
                  else: #DECIMAL input
                    coll['coll_gps_latitude_mode'] = 'decimal'
                    coll['coll_gps_latitude_dms'] = self.g.gps_dec2dms('latitude',coll['coll_gps_latitude'])
                    coll['coll_gps_latitude'] = '%.8f' % round(float(coll['coll_gps_latitude']), 8)

                #LONGITUDE
                coll['coll_gps_longitude_mode'] = None
                coll['coll_gps_longitude_dms'] = None
                if coll['coll_gps_longitude'] != None and coll['coll_gps_longitude'] != '':
                  if re.search(r"[^-0-9.+]",coll['coll_gps_longitude']): #DMS input
                    dec = self.g.gps_dms2dec('longitude',coll['coll_gps_longitude'])
                    coll['coll_gps_longitude_mode'] = 'dms'
                    coll['coll_gps_longitude_dms'] = self.g.gps_dec2dms('longitude',dec)
                    coll['coll_gps_longitude'] = '%.8f' % round(float(dec), 8)
                  else: #DECIMAL input
                    coll['coll_gps_longitude_mode'] = 'decimal'
                    coll['coll_gps_longitude_dms'] = self.g.gps_dec2dms('longitude',coll['coll_gps_longitude'])
                    coll['coll_gps_longitude'] = '%.8f' % round(float(coll['coll_gps_longitude']), 8)

                coll['coll_gps_precision'] = form.getvalue('coll_gps_precision')
                coll['coll_id_gps_datum'] = form.getvalue('coll_gps_datum')
                coll['coll_gps_comments'] = form.getvalue('gps_comments')
                coll['coll_host_genus'] = form.getvalue('coll_host_genus')
                coll['coll_host_species'] = form.getvalue('coll_host_species')
                coll['coll_host_classification'] = form.getvalue('coll_host_classification')
                coll['coll_host_infra_name'] = form.getvalue('coll_host_infra_name')
                coll['coll_host_infra_complement'] = form.getvalue('coll_host_infra_complement')
                coll['coll_global_code'] = form.getvalue('coll_global_code')
                coll['coll_id_clinical_form'] = form.getvalue('coll_clinical_form')
                coll['coll_hiv'] = form.getvalue('coll_hiv')
                coll['id'] = data['id']
                coll = self.verify_data(coll)
                data.update(coll)

                if is_first and save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_coll_event_log', coll, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));

                #Collection Event multilanguage fields
                coll_mlang = {}
                coll_mlang['coll_host_name'] = data_fields[lang]['coll_host_name']
                dict_temp = {'coll_host_name' : data_fields[lang]['coll_host_name'], 'id' : data['id'], 'lang' : lang }
                if save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_coll_host_name_log', dict_temp, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));

                coll_mlang['coll_substratum'] = data_fields[lang]['coll_substratum']
                dict_temp = {'coll_substratum' : data_fields[lang]['coll_substratum'], 'id' : data['id'], 'lang' : lang }
                if save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_substratum_log', dict_temp, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));

                coll_mlang['coll_comments'] = data_fields[lang]['coll_comments']
                dict_temp = {'coll_comments' : data_fields[lang]['coll_comments'], 'id' : data['id'], 'lang' : lang }
                if save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_coll_comments_log', dict_temp, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));

                data.update(coll_mlang)

                #Isolation
                iso = {}
                iso['iso_id_person'] = form.getvalue('iso_person')
                iso['iso_id_institution'] = form.getvalue('iso_institution')
                iso['iso_date'] = self.sql_dateformat(form.getvalue('iso_date'))
                #iso['iso_isolation_from'] = form.getvalue('iso_isolation_from')
                #iso['iso_method'] = form.getvalue('iso_method')
                iso['iso_comments'] = form.getvalue('iso_comments')
                iso['id'] = data['id']
                iso = self.verify_data(iso)
                data.update(iso)

                if is_first and save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_isolation_log', iso, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));

                #Isolation multilanguage fields
                iso_mlang = {}

                iso_mlang['iso_isolation_from'] = data_fields[lang]['iso_isolation_from']
                dict_temp = {'iso_isolation_from' : data_fields[lang]['iso_isolation_from'], 'id' : data['id'], 'lang' : lang }
                if save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_iso_isolation_from_log', dict_temp, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));

                iso_mlang['iso_method'] = data_fields[lang]['iso_method']
                dict_temp = {'iso_method' : data_fields[lang]['iso_method'], 'id' : data['id'], 'lang' : lang }
                if save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_iso_isolation_method_log', dict_temp, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));
                data.update(iso_mlang)

                #Identification
                ident = {}
                ident['ident_date'] = self.sql_dateformat(form.getvalue('ident_date'))
                ident['ident_id_person'] = form.getvalue('ident_person')
                ident['ident_id_institution'] = form.getvalue('ident_institution')
                ident['ident_genus'] = form.getvalue('ident_genus')
                ident['ident_species'] = form.getvalue('ident_species')
                ident['ident_classification'] = form.getvalue('ident_classification')
                ident['ident_infra_name'] = form.getvalue('ident_infra_name')
                ident['ident_infra_complement'] = form.getvalue('ident_infra_complement')
                #ident['ident_method'] = form.getvalue('ident_method')
                ident['ident_comments'] = form.getvalue('ident_comments')
                ident['id'] = data['id']
                ident = self.verify_data(ident)
                data.update(ident)

                if is_first and save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_identification_log', ident, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));

                #Identification multilanguage fields
                ident_mlang = {}
                ident_mlang['ident_method'] = data_fields[lang]['ident_method']
                dict_temp = {'ident_method' : data_fields[lang]['ident_method'], 'id' : data['id'], 'lang' : lang }
                if save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_ident_method_log', dict_temp, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));
                data.update(ident_mlang)

                #Check whether informed date is greater than identification date
                #self.execute('get_preservation_strain_date',data)
                #preservations = self.fetch('all')

                #errors_ident = []
                #for p in preservations:
                #    if ident['ident_date']:
                #        if str(ident['ident_date']) > str(p['date']):
                #            errors_ident.append("Lot: %s Date: %s" % (p['name'] , self.format_date('output', p['date'])))

                #if len(errors_ident) > 0:
                #    raise Exception, _("It is not possible to identify a lot after their date of preservation!") + "<br/>" + "<br/>".join(errors_ident)

                #Culture
                cul = {}
                cul['cul_temp'] = form.getvalue('cul_temp')
                cul['cul_ph'] = form.getvalue('cul_ph')
                cul['id'] = data['id']
                cul = self.verify_data(cul)
                data.update(cul)

                if is_first and save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_cul_log', cul, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));

                #Culture multilanguage fields
                cul_mlang = {}
                cul_mlang['cul_medium'] = data_fields[lang]['cul_medium']
                dict_temp = {'cul_medium' : data_fields[lang]['cul_medium'], 'id' : data['id'], 'lang' : lang }
                if save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_cul_medium_log', dict_temp, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));

                cul_mlang['cul_incub_time'] = data_fields[lang]['cul_incub_time']
                dict_temp = {'cul_incub_time' : data_fields[lang]['cul_incub_time'], 'id' : data['id'], 'lang' : lang }
                if save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_cul_incub_time_log', dict_temp, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));

                cul_mlang['cul_oxy_req'] = data_fields[lang]['cul_oxy_req']
                dict_temp = {'cul_oxy_req' : data_fields[lang]['cul_oxy_req'], 'id' : data['id'], 'lang' : lang }
                if save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_cul_oxy_req_log', dict_temp, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));

                cul_mlang['cul_comments'] = data_fields[lang]['cul_comments']
                dict_temp = {'cul_comments' : data_fields[lang]['cul_comments'], 'id' : data['id'], 'lang' : lang }
                if save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_cul_comments_log', dict_temp, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));
                data.update(cul_mlang)

                #Characteristics
                cha = {}
                cha['cha_biochemical'] = form.getvalue('cha_biochemical')
                cha['cha_immunologic'] = form.getvalue('cha_immunologic')
                cha['cha_morphologic'] = form.getvalue('cha_morphologic')
                cha['cha_molecular'] = form.getvalue('cha_molecular')
                cha['cha_pathogenic'] = form.getvalue('cha_pathogenic')
                cha['cha_genotypic'] = form.getvalue('cha_genotypic')
                cha['cha_ogm'] = form.getvalue('cha_ogm')
                cha['id'] = data['id']
                cha = self.verify_data(cha)
                data.update(cha)

                if is_first and save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_cha_log', cha, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));

                #Characteristics multilanguage fields
                cha_mlang = {}
                cha_mlang['cha_ogm_comments'] = data_fields[lang]['cha_ogm_comments']
                dict_temp = {'cha_ogm_comments' : data_fields[lang]['cha_ogm_comments'], 'id' : data['id'], 'lang' : lang }
                if save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_cha_ogm_comments_log', dict_temp, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));

                cha_mlang['cha_biorisk_comments'] = data_fields[lang]['cha_biorisk_comments']
                dict_temp = {'cha_biorisk_comments' : data_fields[lang]['cha_biorisk_comments'], 'id' : data['id'], 'lang' : lang }
                if save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_cha_biorisk_comments_log', dict_temp, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));

                cha_mlang['cha_restrictions'] = data_fields[lang]['cha_restrictions']
                dict_temp = {'cha_restrictions' : data_fields[lang]['cha_restrictions'], 'id' : data['id'], 'lang' : lang }
                if save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_cha_restrictions_log', dict_temp, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));

                cha_mlang['cha_pictures'] = data_fields[lang]['cha_pictures']
                dict_temp = {'cha_pictures' : data_fields[lang]['cha_pictures'], 'id' : data['id'], 'lang' : lang }
                if save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_cha_pictures_log', dict_temp, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));

                cha_mlang['cha_urls'] = data_fields[lang]['cha_urls']
                dict_temp = {'cha_urls' : data_fields[lang]['cha_urls'], 'id' : data['id'], 'lang' : lang }
                if save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_cha_urls_log', dict_temp, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));

                cha_mlang['cha_catalogue'] = data_fields[lang]['cha_catalogue']
                dict_temp = {'cha_catalogue' : data_fields[lang]['cha_catalogue'], 'id' : data['id'], 'lang' : lang }
                if save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_cha_catalogue_log', dict_temp, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));
                data.update(cha_mlang)

                #Properties
                pro = {}
                pro = self.verify_data(pro)
                data.update(pro)

                #Stock                
                string_stock_minimum_list = form.getvalue('stock_minimum_list')
                if string_stock_minimum_list:
                    try:
                        stock_minimum_list = dict(eval(string_stock_minimum_list,{"__builtins__":None}))
                    except:
                        stock_minimum_list = None
                else:
                    stock_minimum_list = None

                #Properties multilanguage fields
                pro_mlang = {}
                pro_mlang['pro_properties'] = data_fields[lang]['pro_properties']
                dict_temp = {'pro_properties' : data_fields[lang]['pro_properties'], 'id' : data['id'], 'lang' : lang }
                if save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_pro_properties_log', dict_temp, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));

                pro_mlang['pro_applications'] = data_fields[lang]['pro_applications']
                dict_temp = {'pro_applications' : data_fields[lang]['pro_applications'], 'id' : data['id'], 'lang' : lang }
                if save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_pro_applications_log', dict_temp, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));

                pro_mlang['pro_urls'] = data_fields[lang]['pro_urls']
                dict_temp = {'pro_urls' : data_fields[lang]['pro_urls'], 'id' : data['id'], 'lang' : lang }
                if save_log:
                    return_sql.extend(self.l.checkModifiedFields('get_str_pro_urls_log', dict_temp, data['id'], data['code'], lang, self.action, id_log_operation, id_log_entity,''));

                data.update(pro_mlang)

                if is_first:
                    if self.action == 'insert':
                        self.execute('insert_strain',data)
                        self.execute('last_insert_id')
                        data['id'] = self.dbconnection.fetch('one')
                        if dep['insert']: self.execute('insert_str_deposit',data)
                        if coll['insert']: self.execute('insert_str_coll_event',data)
                        if iso['insert']: self.execute('insert_str_isolation',data)
                        if ident['insert']: self.execute('insert_str_identification',data)
                        if cul['insert']: self.execute('insert_str_culture',data)
                        if cha['insert']: self.execute('insert_str_characs',data)
                        if pro['insert']: self.execute('insert_str_properties',data)
                    elif self.action == 'update':
                        self.execute('update_strain',data)

                        #Test if update or insert strain parts
                        self.execute('count_strain_parts_multilanguage',data)
                        counts = self.dbconnection.fetch('columns')
                        dep_exists = counts['count_deposit']
                        coll_exists = counts['count_coll']
                        iso_exists = counts['count_isolation']
                        ident_exists = counts['count_identification']
                        cul_exists = counts['count_culture']
                        cha_exists = counts['count_characs']
                        pro_exists = counts['count_pro']

                        #update or insert str_deposit
                        if (dep_exists): self.execute('update_str_deposit',data)
                        elif dep['insert']: self.execute('insert_str_deposit',data)

                        #update or insert str_collection_event
                        if (coll_exists): self.execute('update_str_coll_event',data)
                        elif coll['insert']: self.execute('insert_str_coll_event',data)

                        #update or insert str_isolation
                        if (iso_exists): self.execute('update_str_isolation',data)
                        elif iso['insert']: self.execute('insert_str_isolation',data)

                        #update or insert str_identification
                        if (ident_exists): self.execute('update_str_identification',data)
                        elif ident['insert']: self.execute('insert_str_identification',data)

                        #update or insert str_culture
                        if (cul_exists): self.execute('update_str_culture',data)
                        elif cul['insert']: self.execute('insert_str_culture',data)

                        #update or insert str_characteristics
                        if (cha_exists): self.execute('update_str_characs',data)
                        elif cha['insert']: self.execute('insert_str_characs',data)

                        #update or insert str_properties
                        if (pro_exists): self.execute('update_str_properties',data)
                        elif pro['insert']: self.execute('insert_str_properties',data)

                    #Security Info
                    self.g.apply_item_permission(self.dbconnection, 'strains', form, data, self.action)
                    is_first = False

                #====================#
                # UPDATE STRAIN DATA #
                #====================#
                if (self.action=='update'):
                    #Test whether we are updating or inserting new strain parts
                    if not is_first: self.execute('count_strain_parts_multilanguage',data)
                    counts = self.dbconnection.fetch('columns')
                    coll_hostname_exists = counts['count_host_name']
                    coll_substratum_exists = counts['count_substratum']
                    coll_comments_exists = counts['count_comments']
                    iso_isolation_from_exists = counts['count_isolations_from']
                    iso_method_exists = counts['count_methods']
                    ident_method_exists = counts['count_ident_methods']
                    cul_medium_exists = counts['count_cultmedium']
                    cul_incub_time_exists = counts['count_incubtime']
                    cul_oxy_req_exists = counts['count_oxy_req']
                    cul_comments_exists = counts['count_cultcomment']
                    cha_ogm_comments_exists = counts['count_ogm']
                    cha_bio_risk_comments_exists = counts['count_biorisks']
                    cha_restrictions_exists = counts['count_restrictions']
                    cha_pictures_exists = counts['count_pictures']
                    cha_urls_exists = counts['count_urls']
                    cha_catalogue_exists = counts['count_catalogue']
                    pro_properties_exists = counts['count_properties']
                    pro_applications_exists = counts['count_applications']
                    pro_urls_exists = counts['count_p_urls']

                    #update or insert str_coll_host_name
                    if (coll_hostname_exists):
                        if coll_mlang['coll_host_name']: self.execute('update_str_host_name_multilanguage', data)
                        else: self.execute('delete_str_host_name_multilanguage', data)
                    elif coll_mlang['coll_host_name']:
                        self.execute('insert_str_host_name_multilanguage', data)

                    #update or insert str_coll_substratum
                    if (coll_substratum_exists):
                        if coll_mlang['coll_substratum']: self.execute('update_str_substratum_multilanguage', data)
                        else: self.execute('delete_str_substratum_multilanguage', data)
                    elif coll_mlang['coll_substratum']:
                        self.execute('insert_str_substratum_multilanguage', data)

                    #update or insert str_coll_comments
                    if (coll_comments_exists):
                        if coll_mlang['coll_comments']: self.execute('update_str_coll_comments_multilanguage', data)
                        else: self.execute('delete_str_coll_comments_multilanguage', data)
                    elif coll_mlang['coll_comments']: self.execute('insert_str_coll_comments_multilanguage', data)

                    #update or insert str_isolation_from
                    if (iso_isolation_from_exists):
                        if iso_mlang['iso_isolation_from']: self.execute('update_str_iso_isolation_from_multilanguage', data)
                        else: self.execute('delete_str_iso_isolation_from_multilanguage', data)
                    elif iso_mlang['iso_isolation_from']: self.execute('insert_str_iso_isolation_from_multilanguage', data)

                    #update or insert str_iso_methods
                    if (iso_method_exists):
                        if iso_mlang['iso_method']: self.execute('update_str_iso_method_multilanguage', data)
                        else: self.execute('delete_str_iso_method_multilanguage', data)
                    elif iso_mlang['iso_method']: self.execute('insert_str_iso_method_multilanguage', data)

                    #update or insert str_ident_methods
                    if (ident_method_exists):
                        if ident_mlang['ident_method']: self.execute('update_str_ident_method_multilanguage', data)
                        else: self.execute('delete_str_ident_method_multilanguage', data)
                    elif ident_mlang['ident_method']: self.execute('insert_str_ident_method_multilanguage', data)

                    #update or insert str_cult_medium
                    if (cul_medium_exists):
                        if cul_mlang['cul_medium']: self.execute('update_str_cult_medium_multilanguage',data)
                        else: self.execute('delete_str_cult_medium_multilanguage',data)
                    elif cul_mlang['cul_medium']:
                        self.execute('insert_str_cult_medium_multilanguage',data)

                    #update or insert str_incub_time
                    if (cul_incub_time_exists):
                        if cul_mlang['cul_incub_time']: self.execute('update_str_incub_time_multilanguage',data)
                        else: self.execute('delete_str_incub_time_multilanguage',data)
                    elif cul_mlang['cul_incub_time']:
                        self.execute('insert_str_incub_time_multilanguage',data)

                    #update or insert str_oxy_req
                    if (cul_oxy_req_exists):
                        if cul_mlang['cul_oxy_req']: self.execute('update_str_oxy_req_multilanguage',data)
                        else: self.execute('delete_str_oxy_req_multilanguage',data)
                    elif cul_mlang['cul_oxy_req']:
                        self.execute('insert_str_oxy_req_multilanguage',data)

                    #update or insert str_cult_comments
                    if (cul_comments_exists):
                        if cul_mlang['cul_comments']: self.execute('update_str_cult_comments_multilanguage',data)
                        else: self.execute('delete_str_cult_comments_multilanguage',data)
                    elif cul_mlang['cul_comments']:
                        self.execute('insert_str_cult_comments_multilanguage',data)

                    #update or insert str_charac_ogm_comments
                    if (cha_ogm_comments_exists):
                        if cha_mlang['cha_ogm_comments']: self.execute('update_str_cha_ogm_comments_multilanguage',data)
                        else: self.execute('delete_str_cha_ogm_comments_multilanguage',data)
                    elif cha_mlang['cha_ogm_comments']:
                        self.execute('insert_str_cha_ogm_comments_multilanguage',data)

                    #update or insert str_charac_bio_risk_comments
                    if (cha_bio_risk_comments_exists):
                        if cha_mlang['cha_biorisk_comments']: self.execute('update_str_cha_biorisk_comments_multilanguage',data)
                        else: self.execute('delete_str_cha_biorisk_comments_multilanguage',data)
                    elif cha_mlang['cha_biorisk_comments']:
                        self.execute('insert_str_cha_biorisk_comments_multilanguage',data)

                    #update or insert str_charac_restrictions
                    if (cha_restrictions_exists):
                        if cha_mlang['cha_restrictions']: self.execute('update_str_cha_restrictions_multilanguage', data)
                        else: self.execute('delete_str_cha_restrictions_multilanguage', data)
                    elif cha_mlang['cha_restrictions']:
                        self.execute('insert_str_cha_restrictions_multilanguage', data)

                    #update or insert str_charac_pictures
                    if (cha_pictures_exists):
                        if cha_mlang['cha_pictures']: self.execute('update_str_cha_pictures_multilanguage',data)
                        else: self.execute('delete_str_cha_pictures_multilanguage',data)
                    elif cha_mlang['cha_pictures']:
                        self.execute('insert_str_cha_pictures_multilanguage',data)

                    #update or insert str_charac_urls
                    if (cha_urls_exists):
                        if cha_mlang['cha_urls']: self.execute('update_str_cha_urls_multilanguage', data)
                        else: self.execute('delete_str_cha_urls_multilanguage', data)
                    elif cha_mlang['cha_urls']:
                        self.execute('insert_str_cha_urls_multilanguage', data)

                    #update or insert str_charac_catalogue_notes
                    if (cha_catalogue_exists):
                        if cha_mlang['cha_catalogue']: self.execute('update_str_cha_catalogue_multilanguage', data)
                        else: self.execute('delete_str_cha_catalogue_multilanguage', data)
                    elif cha_mlang['cha_catalogue']:
                        self.execute('insert_str_cha_catalogue_multilanguage', data)

                    #update or insert str_pro_properties
                    if (pro_properties_exists):
                        if pro_mlang['pro_properties']: self.execute('update_str_pro_properties_multilanguage',data)
                        else: self.execute('delete_str_pro_properties_multilanguage',data)
                    elif pro_mlang['pro_properties']:
                        self.execute('insert_str_pro_properties_multilanguage',data)

                    #update or insert str_pro_applications
                    if (pro_applications_exists):
                        if pro_mlang['pro_applications']: self.execute('update_str_pro_applications_multilanguage',data)
                        else: self.execute('delete_str_pro_applications_multilanguage',data)
                    elif pro_mlang['pro_applications']:
                        self.execute('insert_str_pro_applications_multilanguage',data)

                    #update or insert str_pro_urls
                    if (pro_urls_exists):
                        if pro_mlang['pro_urls']: self.execute('update_str_pro_urls_multilanguage',data)
                        else: self.execute('delete_str_pro_urls_multilanguage',data)
                    elif pro_mlang['pro_urls']:
                        self.execute('insert_str_pro_urls_multilanguage',data)

                    if (isinstance(stock_minimum_list, dict)):
                        # deletes minimum stocks for the strain
                        self.execute("delete_str_stock_minimum",data)

                        # now we insert the new values
                        for id_preservation_method, quantity in stock_minimum_list.items():
                            d = {}
                            d["id_strain"] = data['id']
                            d["id_preservation_method"] = id_preservation_method
                            d["quantity"] = quantity
                            self.execute("insert_str_stock_minimum", d)
                            del d

                #====================#
                # INSERT STRAIN DATA #
                #====================#
                elif (self.action=='insert'):
                    if coll_mlang['coll_host_name']: self.execute('insert_str_host_name_multilanguage',data)
                    if coll_mlang['coll_substratum']: self.execute('insert_str_substratum_multilanguage',data)
                    if coll_mlang['coll_comments']: self.execute('insert_str_coll_comments_multilanguage',data)

                    if cul_mlang['cul_medium']: self.execute('insert_str_cult_medium_multilanguage',data)
                    if cul_mlang['cul_incub_time']: self.execute('insert_str_incub_time_multilanguage',data)
                    if cul_mlang['cul_oxy_req']: self.execute('insert_str_oxy_req_multilanguage',data)
                    if cul_mlang['cul_comments']: self.execute('insert_str_cult_comments_multilanguage',data)

                    if iso_mlang['iso_isolation_from']: self.execute('insert_str_iso_isolation_from_multilanguage', data)
                    if iso_mlang['iso_method']: self.execute('insert_str_iso_method_multilanguage',data)

                    if ident_mlang['ident_method']: self.execute('insert_str_ident_method_multilanguage',data)

                    if cha_mlang['cha_ogm_comments']: self.execute('insert_str_cha_ogm_comments_multilanguage',data)
                    if cha_mlang['cha_biorisk_comments']: self.execute('insert_str_cha_biorisk_comments_multilanguage',data)
                    if cha_mlang['cha_restrictions']: self.execute('insert_str_cha_restrictions_multilanguage',data)
                    if cha_mlang['cha_pictures']: self.execute('insert_str_cha_pictures_multilanguage',data)
                    if cha_mlang['cha_urls']: self.execute('insert_str_cha_urls_multilanguage',data)
                    if cha_mlang['cha_catalogue']: self.execute('insert_str_cha_catalogue_multilanguage',data)

                    if pro_mlang['pro_properties']: self.execute('insert_str_pro_properties_multilanguage',data)
                    if pro_mlang['pro_applications']: self.execute('insert_str_pro_applications_multilanguage',data)
                    if pro_mlang['pro_urls']: self.execute('insert_str_pro_urls_multilanguage',data)


            if return_sql and save_log:
                self.execute_log = self.db_log.execute
                sql_final = "".join(return_sql)[0:len("".join(return_sql))-1]

                if self.action == 'insert':
                    sql_final = sql_final.replace('|%|ID|%|',str(data['id']))

                self.execute_log('insert_log', {'insert_values_log':sql_final}, raw_mode = True)

        except Exception as e:
            self.dbconnection.connect.rollback()
            self.db_log.connect.rollback()
            self.feedback(-1)
        else:
            self.dbconnection.connect.commit()
            self.db_log.connect.commit()
            self.feedback(1, data['id'])

    #===========#
    # QUALITY #
    #===========#
    def strainQuality(self):
        def get_doc_titles(id_doc):
            self.execute('get_doc_title_by_id', {'id_doc' : id_doc})
            titles = self.fetch('all')

            str_titles = ""
            for one_title in titles:
                if str_titles != "":
                    str_titles += "/"
                str_titles += self.ConvertStrUnicode(one_title['title'])
            return str_titles

        try:
            data = self.data
            form = self.form

            #Define Database LOG
            dict_db_log = {}
            dict_db_log = self.g.get_log_db({'id_base':self.session.data['id_base']})

            self.db_log = dbConnection(base_descr = dict_db_log)
            self.execute_log = self.db_log.execute

            #verify log level
            id_log_level = 3
            id_log_entity = 1
            save_log = self.l.checkLogLevel(id_log_level)

            return_sql = []

            if (self.action == 'insert' or self.action == 'update'):
                #Test NotNull Fields
                notnulls = ['date', 'tec_resp', 'num_amp', 'lot']
                if self.action != 'insert': notnulls.append('id_quality')
                self.verify_notnull_fields(notnulls)

                global_counter = int(form.getvalue('global_counter_total'))
                if global_counter < 2:
                    raise Exception(_("Please, choose at least one test."))

                #Quality Data
                data['id_lot'] = form.getvalue('lot')
                data['date'] = self.sql_dateformat(self.form.getvalue('date'))
                data['tec_resp'] = form.getvalue('tec_resp')
                data['id_lot_old'] = form.getvalue('id_lot_old')
                data['id_strain'] = form.getvalue('id_strain')
                data['num_ampoules'] = form.getvalue('num_amp')

                self.logger.debug(' ===> form: %s', form)
                self.logger.debug(' ===> data: %s', self.data)

                dic_temp = {}
                dic_temp['id_lot_qc'] = form.getvalue('lot')
                dic_temp['date_qc'] = self.sql_dateformat(self.form.getvalue('date'))
                dic_temp['tec_resp'] = form.getvalue('tec_resp')
                dic_temp['id'] = form.getvalue('id_quality')

                #get lot name
                self.execute('get_lot',{'id_lot': data['id_lot']})
                lot_name = self.fetch('one', 'name')

                #get strain code
                id_strain = form.getvalue('id_strain')
                self.execute('get_strain_code',{'id_strain': data['id_strain']})
                strain_code = self.fetch('one', 'code')

                id_log_operation = ''
                
                if save_log:
                    if self.action == 'insert':
                        id_log_operation = 14
                    elif self.action == 'update':
                        id_log_operation = 15

                    return_sql.extend(self.l.checkModifiedFields('get_str_quality_log', dic_temp, id_strain, strain_code, '', self.action, id_log_operation, id_log_entity, lot_name))

                data_tests = ()
                if (self.action == 'insert'):
                    self.execute('insert_str_quality', self.data)
                    self.execute('last_insert_id')
                    data['id_quality'] = self.dbconnection.fetch('one')

                    from .location import LocationHelper
                    self.d(form)
                    self.d(form.getvalue('locations_data'))
                    origin_data_list = LocationHelper.parseLocations(form.getvalue('locations_data'))

                    for origin_data in origin_data_list:
                        origin_data['id_quality'] = data['id_quality']
                        origin_data['id_origin_lot'] = data['id_lot']
                        self.execute('insert_str_quality_origin_location', origin_data)

                        from .location import LocationBuilder
                        self.location = LocationBuilder(self.cookie_value)

                        dic_qt = {}
                        dic_qt['id_strain'] = data['id_strain']
                        dic_qt['id_container_hierarchy'] = origin_data['id_origin_container_hierarchy']
                        dic_qt['row'] = origin_data['origin_row']
                        dic_qt['col'] = origin_data['origin_col']

                        #get actual quantity of location after quality control
                        self.execute('get_location_qt_log', dic_qt)
                        qt_lot = self.fetch('one', 'available_qt')
                        location_qt = self.location.get_incomplete_location(origin_data['id_origin_container_hierarchy'], origin_data['origin_row'], origin_data['origin_col'], None, qt_lot)

                        #get lot name
                        self.execute('get_lot', {'id_lot' : data['id_lot']})
                        lot_name = self.fetch('one', 'name')

                        #get strain name
                        self.execute('get_strain_code', {'id_strain': data['id_strain']})
                        strain_code = self.fetch('one')

                        if save_log:
                            id_log_operation = 14

                            lista_tmp = []
                            dict_temp = {'stock' : location_qt, 'id' : data['id_lot'], 'lang' : '' }
                            lista_tmp = self.l.checkModifiedFields('', dict_temp, data['id_strain'], strain_code, '', 'insert', id_log_operation, id_log_entity, lot_name)
                            return_sql.append(lista_tmp[len(lista_tmp) - 1].replace('|%|ID|%|',str(data['id_strain'])))

                    #if save_log:
                        #sql_final = "".join(return_sql)[0:len("".join(return_sql))-1]

                        #Save log data
                        #self.execute_log('insert_log', {'insert_values_log':sql_final}, raw_mode = True)

                elif (self.action == 'update'):
                    data['id_quality'] = form.getvalue('id_quality')
                    self.execute('update_str_quality', data)

                    #get quality tests to compare after
                    self.execute('get_str_quality_test_by_id_quality', {'id_quality': data['id_quality']})
                    data_tests = self.fetch('all')

                    self.execute('delete_str_quality_tests', data)

                str_tests = ""
                data_db_tests = ""
                value_field = ""

                #get_first_doc_title_found

                for test in data_tests:
                    str_tests += str(test['id_doc_qc']) + str(test['purity']) + self.ConvertStrUnicode(test['counting']) + str(test['counting_not_apply']) + self.ConvertStrUnicode(test['result']) + self.ConvertStrUnicode(test['comments'])

                #Get Data related to each test
                for i in range(1,global_counter):
                    if 'test_'+str(i) not in form: continue #Ignore this test, was removed by user
                    data['id_quality'] = data['id_quality']
                    data['id_doc'] = form.getvalue('test_'+str(i))

                    data['purity'] = form.getvalue('purity_'+str(i))
                    if data['purity'] != 'ok':
                        data['purity'] = 'n'
                    else:
                        data['purity'] = 'y'
                    data['counting'] = form.getvalue('counting_'+str(i))
                    data['counting_not_apply'] = form.getvalue('counting_not_apply_'+str(i))
                    str_not_apply = ""
                    if data['counting_not_apply'] is None:
                        data['counting_not_apply'] = 'n'
                    else:
                        data['counting_not_apply'] = 'y'
                        str_not_apply = "(" + "_('Does not apply')" + ")"

                    data['result'] = form.getvalue('result_'+str(i))
                    data['comments'] = form.getvalue('comments_'+str(i))
                    self.execute('insert_str_quality_test', data)
                    
                    #brk(host="localhost", port=9000)
                    data_db_tests += str(data['id_doc']) + str(data['purity']) + str(data['counting']) + str(data['counting_not_apply']) + str(data['result']) + str(data['comments'])

                    #formatted value to log field
                    value_field += "_('Used Test'): " +  get_doc_titles(str(data['id_doc'])) + "<br />"
                    if data['purity'] == 'y':
                        value_field += "_('Purity'):" + "_('OK')" + "<br />"
                    else:
                        value_field += "_('Purity'):" + "_('Contaminated')" + "<br />"

                    value_field += "_('Counting'):" + self.ConvertStrUnicode(data['counting']) + str_not_apply + "<br />"
                    value_field += "_('Result'):" + self.ConvertStrUnicode(data['result']) + "<br />"
                    value_field += "_('Comments'):" + self.ConvertStrUnicode(data['comments']) + "<br /><br />"

                if (self.action == 'insert'):
                    data['id_lot_old'] = data['id_lot']

                if str_tests != data_db_tests:
                    #brk(host="localhost", port=9000)
                    dic_tmp = {}
                    dic_tmp['test'] = value_field
                    dic_tmp['id'] = ''                    
                    return_sql.extend(self.l.checkModifiedFields('', dic_tmp, id_strain, strain_code, '', 'insert', id_log_operation, id_log_entity, lot_name))

                #Save log data
                if save_log:
                    sql_final = "".join(return_sql)[0:len("".join(return_sql))-1]
                    if len(sql_final) > 0:
                        self.execute_log('insert_log', {'insert_values_log':sql_final}, raw_mode = True)
            else: #delete
                data['id_lot'] = form.getvalue('lot')
                data['id_strain'] = form.getvalue('id_strain')
                data['id_quality'] = form.getvalue('id_quality')

                self.execute('get_quality_usage_information', data)
                count = self.fetch('one')
                if count:
                    raise Exception(_("This quality control can not be deleted because the original places are taken by another preservation."))
                else:
                    dic_qt = {}

                    if save_log:
                        self.execute('get_quality_origin_location', {'id' : self.data['id_quality']})
                        locations = self.fetch('all')

                    from .quality import Quality
                    quality = Quality('delete', self.cookie_value, self.form)
                    #Update ampoules for this lot
                    self.execute('delete_str_quality_origin', {'id_quality': data['id_quality']})
                    self.execute('delete_str_quality', {'id_quality': data['id_quality']})

                    if save_log:
                        return_sql = []
                        from .location import LocationBuilder
                        self.location = LocationBuilder(self.cookie_value)

                        id_log_operation = 16

                        #get strain code
                        self.execute('get_strain_code', {'id_strain': data['id_strain']})
                        strain_code = self.fetch('one')
                        is_first = True

                        for location_data in locations:
                            dic_qt['id_strain'] = data['id_strain']
                            dic_qt['id_container_hierarchy'] = location_data['id_origin_container_hierarchy']
                            dic_qt['row'] = location_data['origin_row']
                            dic_qt['col'] = location_data['origin_col']
                            dic_qt['quantity'] = location_data['quantity']
                            dic_qt['id_lot'] = location_data['id_origin_lot']

                            #get lot name
                            self.execute('get_lot', {'id_lot' : dic_qt['id_lot']})
                            lot_name = self.fetch('one', 'name')

                            if is_first:
                                dic_temp = {'date_qc': ''}

                                return_sql.extend(self.l.checkModifiedFields('', dic_temp, data['id_strain'], strain_code, '', 'delete', id_log_operation, id_log_entity, lot_name))
                                is_first = False

                            #get actual quantity location after distribution
                            self.execute('get_location_qt_log', dic_qt)
                            qt_lot = self.fetch('one', 'available_qt')
                            location_qt = self.location.get_incomplete_location(location_data['id_origin_container_hierarchy'], location_data['origin_row'], location_data['origin_col'], None, qt_lot)

                            dict_temp = {'stock' : location_qt, 'id' : dic_qt['id_lot'], 'lang' : '' }
                            return_sql.extend(self.l.checkModifiedFields('', dict_temp, data['id_strain'], strain_code, '', 'insert', id_log_operation, id_log_entity, lot_name))

                    sql_final = "".join(return_sql)[0:len("".join(return_sql))-1]

                    #Save log data
                    if save_log:
                        self.execute_log('insert_log', {'insert_values_log':sql_final}, raw_mode = True)

        except Exception as e:
            self.dbconnection.connect.rollback()
            self.db_log.connect.rollback()
            self.feedback(-1)
        else:
            self.dbconnection.connect.commit()
            self.db_log.connect.commit()
            self.who_detail = "py/strains.quality.list.py?type=other&id="
            self.feedback(1, data['id_strain'])

        return self.html

    #===========#
    # DOCUMENTS #
    #===========#
    def doc(self):
        form = self.form
        data = self.data

        #Test NotNull Fields
        notnulls = ['code','qualifier','title']
        if self.action != 'insert': notnulls.append('id')
        main_title = self.verify_notnull_fields(notnulls,'doc')

        data_fields = self.supportMultiLanguage(('title', 'description', 'new_file', 'file_name', 'file'));
        #Assert that all titles have an input (use main_title if needed)
        for lang in data_fields:
          if data_fields[lang]['title'] == '':
            data_fields[lang]['title'] = main_title

        #Check whether document has already been inserted or updated
        is_first = True
        try:
            for lang in data_fields:
                data['data_lang'] = self.data_lang_onedict[lang]

                #Document Data
                data['code'] = form.getvalue('code')
                data['id_qualifier'] = form.getvalue('qualifier')
                if int(data['id_qualifier']) == 5:
                    data['id_category'] = form.getvalue('test_category')
                else:
                    data['id_category'] = None

                if 'go_catalog' in form:
                    data['go_catalog'] = 1
                else:
                    data['go_catalog'] = 0

                #Document Data multilanguage fields
                data_mlang = {}
                data_mlang['title'] = data_fields[lang]['title']
                data_mlang['description'] = data_fields[lang]['description']
                data.update(data_mlang)

                if 'new_file_%s'%lang in form:
                    #Get file_name if 'new_file' or same file
                    if form['new_file_%s'%lang].filename:
                        #fix bug for IE 6.0 or less, because it sends the complete path of file
                        data['file_name'] = path.split(form['new_file_%s'%lang].filename)[1]
                        #fix bug for to break of file name at download
                        data['file_name'] = data['file_name'].replace(' ','_')
                    else:
                        data['file_name'] = form.getvalue('file_%s'%lang)

                    #Doc File
                    doc_file = form['new_file_%s'%lang].file

                    if is_first:
                        if self.action == 'insert':
                            self.execute('get_doc_code',data)
                            #Check whether this code already exists and show friendly error message
                            if self.fetch('one') > 0:
                              raise Exception(_("Code value already exists in database!") + "<br />" + _("Please insert a different value."))
                            self.execute('insert_doc',data)
                            self.execute('last_insert_id')
                            data['id'] = self.dbconnection.fetch('one')
                        elif self.action == 'update':
                            self.execute('update_doc',data)
                        #Security Info
                        self.g.apply_item_permission(self.dbconnection, 'doc', form, data, self.action)
                        is_first = False

                    if (self.action == 'update'):
                        self.execute('count_doc_parts_multilanguage',data)
                        counts = self.dbconnection.fetch('columns')
                        title_exists = counts['count_title']
                        description_exists = counts['count_description']

                        #update or insert doc_title
                        if (title_exists): self.execute('update_doc_title_multilanguage', data)
                        elif data_mlang['title']: self.execute('insert_doc_title_multilanguage', data)

                        #update or insert doc_descriptions
                        if (description_exists):
                            if data_mlang['description']: self.execute('update_doc_description_multilanguage', data)
                            else: self.execute('delete_doc_description', data)
                        elif data_mlang['description']: self.execute('insert_doc_description_multilanguage', data)

                        #File Processing #
                        if form['new_file_%s'%lang].filename:
                            #update doc_file_name

                            #Check whether we should overwrite or insert file
                            self.execute('get_doc_file_name_multilanguage',data)
                            file_lang_exists = self.dbconnection.fetch('one')
                            if (file_lang_exists):
                                self.execute('update_doc_file_name_multilanguage', data)
                            else:
                                self.execute('insert_doc_file_name_multilanguage', data)

                            #Generate internal file code
                            file_code = str(data['id']) + str(data['data_lang'])
                            file_code = new_sha(file_code).hexdigest()

                            #Make and Open File
                            file_dir = path.join(self.doc_dir, file_code)
                            file_open = open(file_dir, "wb")

                            #Update Data from File and close
                            max_file_size = self.g.get_config('upload_limit')
                            while True:
                                chunk = doc_file.read()
                                if not chunk: break
                                if max_file_size != '' and (int(len(chunk)) > int(max_file_size)): raise Exception(_("Exceeded maximum size limit of")+" "+str(max_file_size)+" "+_("bytes"))
                                file_open.write(chunk)
                            file_open.close()

                    elif (self.action == 'insert'):
                            if data_mlang['title']: self.execute('insert_doc_title_multilanguage', data)
                            if data_mlang['description']: self.execute('insert_doc_description_multilanguage', data)

                            if data['file_name']: self.execute('insert_doc_file_name_multilanguage', data)

                            #File Processing #
                            #Generate internal file code
                            #file_code = str(data['id']) + str(data['id_lang'])
                            file_code = str(data['id']) + str(data['data_lang'])
                            file_code = new_sha(file_code).hexdigest()

                            #Make and Open File
                            file_dir = path.join(self.doc_dir, file_code)
                            file_open = open(file_dir, "wb")

                            #Save data in File and close
                            max_file_size = self.g.get_config('upload_limit')
                            while True:
                                chunk = doc_file.read()
                                if not chunk: break #could not read file
                                if max_file_size != '' and (int(len(chunk)) > int(max_file_size)): raise Exception(_("Exceeded maximum size limit of")+" "+str(max_file_size)+" "+_("bytes"))
                                file_open.write(chunk)
                            file_open.close()


        except Exception as e:
            self.dbconnection.connect.rollback()
            self.feedback(-1)
        else:
            self.dbconnection.connect.commit()
            self.feedback(1, data['id'])



    #============#
    # REFERENCES #
    #============#
    def ref(self):
        #brk(host="localhost", port=9000)

        #Test NotNull Fields
        notnulls = ['title']
        if self.action != 'insert': notnulls.append('id')
        self.verify_notnull_fields(notnulls)

        form = self.form
        data = self.data
        data_fields = self.supportMultiLanguage((None,'comments'));

        #Check whether item has already been inserted or updated
        is_first = True
        try:
            for lang in data_fields:
                data['data_lang'] = self.data_lang_onedict[lang]

                #Reference Data
                data['title'] = form.getvalue('title')
                data['author'] = form.getvalue('author')
                data['year'] = form.getvalue('year')
                data['url'] = form.getvalue('url')

                if 'go_catalog' in form:
                    data['go_catalog'] = 1
                else:
                    data['go_catalog'] = 0

                #Reference Data multilanguage fields
                data_mlang = {}
                data_mlang['comments'] = data_fields[lang]['comments']
                data.update(data_mlang)
                if is_first:
                    if self.action == 'insert':
                        self.execute('insert_ref',data)
                        self.execute('last_insert_id')
                        data['id'] = self.dbconnection.fetch('one')
                    elif self.action == 'update':
                        self.execute('update_ref',data)
                    #Security Info
                    self.g.apply_item_permission(self.dbconnection, 'ref', form, data, self.action)
                    is_first = False

                if (self.action == 'update'):
                    self.execute('count_ref_parts_multilanguage',data)
                    counts = self.dbconnection.fetch('columns')
                    comments_exists = counts['count_comments']
                    #update or insert ref_comments
                    if (comments_exists):
                        if data_mlang['comments']: self.execute('update_ref_comments_multilanguage',data)
                        else: self.execute('delete_ref_comments_multilanguage',data)
                    elif data_mlang['comments']: self.execute('insert_ref_comments_multilanguage',data)

                elif (self.action == 'insert'):

                    if data_mlang['comments']: self.execute('insert_ref_comments_multilanguage',data)

        except Exception as e:
            self.dbconnection.connect.rollback()
            self.feedback(-1)
        else:
            self.dbconnection.connect.commit()
            self.feedback(1, data['id'])


    #========#
    # PEOPLE #
    #========#
    def people(self):
        #brk(host="localhost", port=9000)

        #Test NotNull Fields
        notnulls = ['name']
        return_sql = []
        if self.action != 'insert': notnulls.append('id')
        self.verify_notnull_fields(notnulls)

        form = self.form
        data = self.data
        data_fields = self.supportMultiLanguage(('aux', 'comments'));

        #Check whether item has already been included or updated
        is_first = True
        try:
            for lang in data_fields:
                data['data_lang'] = self.data_lang_onedict[lang]

                #Person Data
                data['name'] = form.getvalue('name')
                data['nickname'] = form.getvalue('nickname')
                data['address'] = form.getvalue('address')
                data['phone'] = form.getvalue('phone')
                data['email'] = form.getvalue('email')
                #last_update updated by sql function "NOW()"

                if 'go_catalog' in form:
                    data['go_catalog'] = 1
                else:
                    data['go_catalog'] = 0

                #Person Data Multilanguage Field
                data_mlang = {}
                data_mlang['comments'] = data_fields[lang]['comments']
                data.update(data_mlang)

                #data = self.verify_data(data)

                ####INNER FUNCTION ###################################
                def insert_relations(index, contacts):
                    self.execute ("delete_all_contact_relations", data)
                    if index is not None:
                        for contact in contacts:
                            contact['id'] = data['id']
                            self.dbconnection.execute("insert_contact_relations", contact)
                ####INNER FUNCTION ###################################

                if is_first:
                    #Person  Intitution Relations
                    contacts = []
                    #Input name prefixes: select_inst_, check_contact_, text_dep_, text_email_
                    index = None
                    for key in list(form.keys()):
                        if not key.startswith('select_inst_'): continue
                        index = int (key.split('_')[-1])
                        if 'check_contact_%d' % index in form: is_contact = 'yes'
                        else: is_contact = None
                        contacts.append ({'id':             data['id'],
                                          'id_institution': form.getvalue('select_inst_%d' % index),
                                          'contact':        is_contact,
                                          'department':     form.getvalue('text_dep_%d' % index),
                                          'email':          form.getvalue('text_email_%d' % index)
                                        })

                    if self.action == 'insert':
                        self.execute('insert_person',data)
                        self.execute('last_insert_id')
                        data['id'] = self.dbconnection.fetch('one')
                    elif self.action == 'update':
                        #Verify using log
                        log = False
                        id_log_level = 1
                        if self.l.checkLogLevel(id_log_level):

                            #Verify change in 'name' field
                            self.execute('lookup_person_log', data)
                            fieldInDB = self.fetch('one')

                            if fieldInDB != data['name']:

                                #Verify in use screen 'strain' field 'person'
                                id_log_operation = 6
                                id_log_entity = 1

                                data['subcolls'] = "".join(self.l.listSubcollsLevel(id_log_level))[0:len("".join(self.l.listSubcollsLevel(id_log_level)))-1]

                                #Origin
                                self.execute('exists_person_usage_in_strain_origin', data, raw_mode = True)
                                origins = self.fetch('all')

                                #Isolation
                                self.execute('exists_person_usage_in_strain_isolation', data, raw_mode = True)
                                isolations = self.fetch('all')

                                #Identification
                                self.execute('exists_person_usage_in_strain_identification', data, raw_mode = True)
                                identifications = self.fetch('all')

                                #Deposit - person
                                self.execute('exists_person_usage_in_strain_deposit', data, raw_mode = True)
                                deposits = self.fetch('all')

                                #Deposit - responsible for authentication
                                self.execute('exists_responsible_usage_in_strain_deposit', data, raw_mode = True)
                                responsibles = self.fetch('all')
                                
                                if origins or isolations or identifications or deposits or responsibles:
                                    log = True

                        self.execute('update_person',data)
                    #Contact Relations
                    insert_relations(index, contacts)

                    #Security Info
                    self.g.apply_item_permission(self.dbconnection, 'people', form, data, self.action)
                    is_first = False

                if (self.action == 'update'):
                    data["id_person"] = form.getvalue("id")

                    self.execute('count_person_parts_multilanguage', data)
                    counts = self.dbconnection.fetch('columns')
                    comments_exists = counts['count_comments']
                    #update or insert person_comments
                    if (comments_exists):
                        if data_mlang['comments']: self.execute('update_person_comments_multilanguage', data)
                        else: self.execute('delete_person_comments_multilanguage', data)
                    elif data_mlang['comments']: self.execute('insert_person_comments_multilanguage', data)

                    #Log
                    if log:
                        log = False
                        
                        #Origin
                        for origin in origins:
                            dict_temp = {'coll_id_person' : data['id'], 'id' : data['id'], 'lang' : lang }
                            #Used the function 'checkModifiedFields' with parameter 'insert' just to generate the string insertion
                            return_sql.extend(self.l.checkModifiedFields('', dict_temp, origin['id_strain'], origin['code'], lang, 'insert', id_log_operation, id_log_entity,''))
                        origins = []
    
                        #Isolation
                        for isolation in isolations:
                            dict_temp = {'iso_id_person' : data['id'], 'id' : data['id'], 'lang' : lang }
                            #Used the function 'checkModifiedFields' with parameter 'insert' just to generate the string insertion
                            return_sql.extend(self.l.checkModifiedFields('', dict_temp, isolation['id_strain'], isolation['code'], lang, 'insert', id_log_operation, id_log_entity,''));
                        isolations = []
    
                        #Identification
                        for identification in identifications:
                            dict_temp = {'ident_id_person' : data['id'], 'id' : data['id'], 'lang' : lang }
                            #Used the function 'checkModifiedFields' with parameter 'insert' just to generate the string insertion
                            return_sql.extend(self.l.checkModifiedFields('', dict_temp, identification['id_strain'], identification['code'], lang, 'insert', id_log_operation, id_log_entity,''));
                        identifications = []
    
                        #Deposit - person
                        for deposit in deposits:
                            dict_temp = {'dep_id_person' : data['id'], 'id' : data['id'], 'lang' : lang }
                            #Used the function 'checkModifiedFields' with parameter 'insert' just to generate the string insertion
                            return_sql.extend(self.l.checkModifiedFields('', dict_temp, deposit['id_strain'], deposit['code'], lang, 'insert', id_log_operation, id_log_entity,''));
                        deposits = []
    
                        #Deposit - responsible for authentication
                        for responsible in responsibles:
                            dict_temp = {'dep_aut_id_person' : data['id'], 'id' : data['id'], 'lang' : lang }
                            #Used the function 'checkModifiedFields' with parameter 'insert' just to generate the string insertion
                            return_sql.extend(self.l.checkModifiedFields('', dict_temp, responsible['id_strain'], responsible['code'], lang, 'insert', id_log_operation, id_log_entity,''));
                        responsibles = []
    
                        #Write log
                        if return_sql:
                            dict_db_log = {}
                            dict_db_log = self.g.get_log_db({'id_base':self.session.data['id_base']})
    
                            #Define Database
                            self.db_log = dbConnection(base_descr = dict_db_log)
                            self.execute_log = self.db_log.execute
                            self.execute_log('insert_log', {'insert_values_log':"".join(return_sql)[0:len("".join(return_sql))-1]}, raw_mode = True)

                elif (self.action == 'insert'):

                    if data_mlang['comments']: self.execute('insert_person_comments_multilanguage', data)

        except Exception as e:
            self.dbconnection.connect.rollback()
            if return_sql: self.db_log.connect.rollback()
            self.feedback(-1)
        else:
            self.dbconnection.connect.commit()
            if return_sql: self.db_log.connect.commit()
            self.feedback(1, data['id'])


    #==============#
    # INSTITUTIONS #
    #==============#
    def inst(self):
        #brk(host="localhost", port=9000)

        #Test NotNull Fields
        notnulls = ['name']
        return_sql = []
        if self.action != 'insert': notnulls.append('id')
        self.verify_notnull_fields(notnulls)

        form = self.form
        data = self.data
        data_fields = self.supportMultiLanguage(('aux', 'comments'));

        #Check whether item has already been included or updated
        is_first = True
        try:
            for lang in data_fields:
                data['data_lang'] = self.data_lang_onedict[lang]

                #Institution Data
                data['code1'] = form.getvalue('code1')
                data['code2'] = form.getvalue('code2')
                data['code3'] = form.getvalue('code3')
                data['complement'] = form.getvalue('complement')
                data['nickname'] = form.getvalue('nickname')
                data['name'] = form.getvalue('name')
                data['address'] = form.getvalue('address')
                data['phone'] = form.getvalue('phone')
                data['email'] = form.getvalue('email')
                data['website'] = form.getvalue('website')

                if 'go_catalog' in form:
                    data['go_catalog'] = 1
                else:
                    data['go_catalog'] = 0

                #Institution Data Multilanguage Fields
                data_mlang = {}
                data_mlang['comments'] = data_fields[lang]['comments']

                data.update(data_mlang)

                if is_first:
                    if self.action == 'insert':
                        self.execute('insert_institution', data)
                        self.execute('last_insert_id')
                        data['id'] = self.dbconnection.fetch('one')
                    elif self.action == 'update':
                        #Verify using log
                        log = False
                        id_log_level = 1
                        if self.l.checkLogLevel(id_log_level):

                            #Verify change in 'name' field
                            self.execute('lookup_institution_log', data)
                            fieldInDB = self.fetch('one')

                            if fieldInDB != data['name']:

                                #Verify in use screen 'strain' field 'institution'
                                id_log_operation = 5
                                id_log_entity = 1

                                data['subcolls'] = "".join(self.l.listSubcollsLevel(id_log_level))[0:len("".join(self.l.listSubcollsLevel(id_log_level)))-1]

                                #Origin
                                self.execute('exists_institution_usage_in_strain_origin', data, raw_mode = True)
                                origins = self.fetch('all')

                                #Isolation
                                self.execute('exists_institution_usage_in_strain_isolation', data, raw_mode = True)
                                isolations = self.fetch('all')

                                #Identification
                                self.execute('exists_institution_usage_in_strain_identification', data, raw_mode = True)
                                identifications = self.fetch('all')

                                #Deposit
                                self.execute('exists_institution_usage_in_strain_deposit', data, raw_mode = True)
                                deposits = self.fetch('all')
                                
                                if origins or isolations or identifications or deposits:
                                    log = True

                        self.execute('update_institution', data)
                    #Security Info
                    self.g.apply_item_permission(self.dbconnection, 'institutions', form, data, self.action)
                    is_first = False

                if (self.action == 'update'):

                    self.execute('count_inst_parts_multilanguage', data)
                    counts = self.dbconnection.fetch('columns')
                    comments_exists = counts['count_comments']

                    #update or insert inst_comments
                    if (comments_exists):
                        if data_mlang['comments']: self.execute('update_inst_comments_multilanguage',data)
                        else: self.execute('delete_inst_comments_multilanguage',data)
                    elif data_mlang['comments']: self.execute('insert_inst_comments_multilanguage',data)
                    
                    #Log
                    if log:
                        log = False
                        
                        #Origin
                        for origin in origins:
                            dict_temp = {'coll_id_institution' : data['id'], 'id' : data['id'], 'lang' : lang }
                            #Used the function 'checkModifiedFields' with parameter 'insert' just to generate the string insertion
                            return_sql.extend(self.l.checkModifiedFields('', dict_temp, origin['id_strain'], origin['code'], lang, 'insert', id_log_operation, id_log_entity,''))
                        origins = []
    
                        #Isolation
                        for isolation in isolations:
                            dict_temp = {'iso_id_institution' : data['id'], 'id' : data['id'], 'lang' : lang }
                            #Used the function 'checkModifiedFields' with parameter 'insert' just to generate the string insertion
                            return_sql.extend(self.l.checkModifiedFields('', dict_temp, isolation['id_strain'], isolation['code'], lang, 'insert', id_log_operation, id_log_entity,''));
                        isolations = []
    
                        #Identification
                        for identification in identifications:
                            dict_temp = {'ident_id_institution' : data['id'], 'id' : data['id'], 'lang' : lang }
                            #Used the function 'checkModifiedFields' with parameter 'insert' just to generate the string insertion
                            return_sql.extend(self.l.checkModifiedFields('', dict_temp, identification['id_strain'], identification['code'], lang, 'insert', id_log_operation, id_log_entity,''));
                        identifications = []
    
                        #Deposit
                        for deposit in deposits:
                            dict_temp = {'dep_id_institution' : data['id'], 'id' : data['id'], 'lang' : lang }
                            #Used the function 'checkModifiedFields' with parameter 'insert' just to generate the string insertion
                            return_sql.extend(self.l.checkModifiedFields('', dict_temp, deposit['id_strain'], deposit['code'], lang, 'insert', id_log_operation, id_log_entity,''));
                        deposits = []
    
                        #Write log
                        if return_sql:
                            dict_db_log = {}
                            dict_db_log = self.g.get_log_db({'id_base':self.session.data['id_base']})
    
                            #Define Database
                            self.db_log = dbConnection(base_descr = dict_db_log)
                            self.execute_log = self.db_log.execute
                            self.execute_log('insert_log', {'insert_values_log':"".join(return_sql)[0:len("".join(return_sql))-1]}, raw_mode = True)

                elif (self.action == 'insert'):

                    if data_mlang['comments']: self.execute('insert_inst_comments_multilanguage', data)

        except Exception as e:
            self.dbconnection.connect.rollback()
            if return_sql: self.db_log.connect.rollback()
            self.feedback(-1)
        else:
            self.dbconnection.connect.commit()
            if return_sql: self.db_log.connect.commit()
            self.feedback(1, data['id'])

    #==============#
    # DISTRIBUTION #
    #==============#
    def distribution(self):

        #Test NotNull Fields
        notnulls = ['distribution_date', 'distribution_quantity']
        if self.action != 'insert': notnulls.append('id')
        self.verify_notnull_fields(notnulls)

        form = self.form
        data = self.data

        #Define LOG Database
        dict_db_log = {}
        dict_db_log = self.g.get_log_db({'id_base':self.session.data['id_base']})

        self.db_log = dbConnection(base_descr = dict_db_log)
        self.execute_log = self.db_log.execute

        #verify log level
        id_log_level = 3
        id_log_entity = 1
        save_log = self.l.checkLogLevel(id_log_level)

        return_sql = []

        #Check whether item has already been included or updated
        is_first = True
        try:

            #Distribution Data
            data['date'] = self.sql_dateformat(form.getvalue('distribution_date'))
            data['id_lot'] = form.getvalue('distribution_lot')
            data['id_user'] = form.getvalue('distribution_user')
            data['id_institution'] = form.getvalue('distribution_institution')
            data['id_person'] = form.getvalue('distribution_person')
            data['reason'] = form.getvalue('distribution_reason')

            data['id_lot_old'] = form.getvalue('distribution_lot_old')
            data['num_ampoules'] = form.getvalue('distribution_quantity')
            data['id_strain'] = form.getvalue('distribution_strain')
            data['locations_data'] = form.getvalue('locations_data')

            dic_temp = {}
            dic_temp['date'] = self.sql_dateformat(form.getvalue('distribution_date'))
            dic_temp['id_lot'] = form.getvalue('distribution_lot')
            dic_temp['id_user'] = form.getvalue('distribution_user')
            dic_temp['id_institution'] = form.getvalue('distribution_institution')
            dic_temp['id_person'] = form.getvalue('distribution_person')
            dic_temp['reason'] = form.getvalue('distribution_reason')
            dic_temp['id'] = data['id']

            if save_log:
                #get lot name
                self.execute('get_lot',{'id_lot': data['id_lot']})
                lot_name = self.fetch('one', 'name')

                #get strain code
                id_strain = form.getvalue('distribution_strain')
                self.execute('get_strain_code',{'id_strain': data['id_strain']})
                strain_code = self.fetch('one', 'code')

                if self.action == 'insert':
                    id_log_operation = 11
                elif self.action == 'update':
                    id_log_operation = 12

                return_sql.extend(self.l.checkModifiedFields('get_one_distribution', dic_temp, id_strain, strain_code, '', self.action, id_log_operation, id_log_entity, lot_name))

            if is_first:
                if self.action == 'update':
                    self.execute('update_distribution', data)

                elif self.action == 'insert':
                    self.execute('insert_distribution', data)
                    self.execute('last_insert_id')
                    data['id'] = self.dbconnection.fetch('one')

                    from .location import LocationHelper
                    self.d(data['locations_data'])
                    origin_data_list = LocationHelper.parseLocations(data['locations_data'])

                    for origin_data in origin_data_list:
                        from .location import LocationBuilder
                        self.location = LocationBuilder(self.cookie_value)

                        self.logger.debug('**** Origin lot: %s', origin_data)
                        origin_data['id_distribution'] = data['id']
                        origin_data['id_origin_lot'] = data['id_lot']
                        self.execute('insert_distribution_origin_location', origin_data)

                        dic_qt = {}
                        dic_qt['id_strain'] = data['id_strain']
                        dic_qt['id_container_hierarchy'] = origin_data['id_origin_container_hierarchy']
                        dic_qt['row'] = origin_data['origin_row']
                        dic_qt['col'] = origin_data['origin_col']

                        #get actual quantity location after distribution
                        self.execute('get_location_qt_log', dic_qt)
                        qt_lot = self.fetch('one', 'available_qt')
                        location_qt = self.location.get_incomplete_location(origin_data['id_origin_container_hierarchy'], origin_data['origin_row'], origin_data['origin_col'], None, qt_lot)

                        self.execute('get_lot', {'id_lot' : data['id_lot']})
                        lot_name = self.fetch('one', 'name')

                        #get lot name
                        self.execute('get_strain_code', {'id_strain': data['id_strain']})
                        strain_code = self.fetch('one')

                        if save_log:
                            id_log_operation = 11

                            lista_tmp = []
                            dict_temp = {'stock' : location_qt, 'id' : data['id_lot'], 'lang' : '' }
                            lista_tmp = self.l.checkModifiedFields('', dict_temp, data['id_strain'], strain_code, '', 'insert', id_log_operation, id_log_entity, lot_name)
                            return_sql.append(lista_tmp[len(lista_tmp) - 1].replace('|%|ID|%|',str(data['id_strain'])))

                if save_log and len(return_sql) > 0:
                    sql_final = "".join(return_sql)[0:len("".join(return_sql))-1]

                    #Save log data
                    self.execute_log('insert_log', {'insert_values_log':sql_final}, raw_mode = True)

                is_first = False

        except Exception as e:
            self.dbconnection.connect.rollback()
            if save_log:
                self.db_log.connect.rollback()
            self.feedback(-1)
        else:
            #Security Info
            self.g.apply_item_permission(self.dbconnection, 'distribution', form, data, self.action)

            self.dbconnection.connect.commit()
            if save_log:
                self.db_log.connect.commit()
            self.feedback(1, data['id'])
            
    def stockmovement(self):        
        #Test NotNull Fields
        notnulls = ['date','description']
        self.verify_notnull_fields(notnulls)
        
        form = self.form
        data = self.data
        
        #Define LOG Database
        dict_db_log = {}
        dict_db_log = self.g.get_log_db({'id_base':self.session.data['id_base']})

        self.db_log = dbConnection(base_descr = dict_db_log)
        self.execute_log = self.db_log.execute
        
        #id_log_entity for strains is 1
        id_log_entity = 1

        #id log operation for Stock Movement Insert
        id_log_operation = 17

        id_log_level = 2
        save_log = self.l.checkLogLevel(id_log_level)
        
        #brk("localhost", 9000)        
        
        from .location import LocationBuilder
        self.location = LocationBuilder(self.cookie_value)
               
        
        try:            
            data['date'] = self.sql_dateformat(form.getvalue('date'))
            data['description'] = form.getvalue('description')
            data['id_preservation_method'] = form.getvalue('preservation_method')
            
            if self.action == 'insert':                
                global_counter = int(form.getvalue('global_counter_total'))
                if global_counter < 2:
                    raise Exception(_("At least one stock position must me chosen."))
                
                self.execute('insert_stock_movement', data)
                self.execute('last_insert_id')
                data['id'] = self.fetch('one')
                return_sql = []
                for i in range(1, global_counter):
                    origin_form = form.getvalue('stockmovement_origin_location_' + str(i))
                    if (origin_form is not None and origin_form != ""):
                        origin = origin_form.split('_')
                        self.execute('get_location_data_for_stock_movement', {'id_container_hierarchy': origin[0], 'row': origin[1], 'col': origin[2]})
                        location_data = self.fetch('columns')
                        
                        location_qt_from = self.location.get_incomplete_location(location_data['id_container_hierarchy'], location_data['row'], location_data['col'], None, 0)
                        
                        #get lot name
                        self.execute('get_lot',{'id_lot': location_data['id_lot']})
                        lot_name = self.fetch('one', 'name')

                        #get strain code
                        self.execute('get_strain_code', {'id_strain': location_data['id_strain']})
                        strain_code = self.fetch('one')

                        if save_log:                            
                            lista_tmp = []
                            dict_temp = {'stock' : location_qt_from, 'id' : location_data['id_lot'], 'lang' : '' }
                            lista_tmp = self.l.checkModifiedFields('', dict_temp, location_data['id_strain'], strain_code, '', 'insert', id_log_operation, id_log_entity, lot_name)
                            return_sql.append(lista_tmp[len(lista_tmp) - 1].replace('|%|ID|%|',str(location_data['id_strain'])))
                            
                        destination_form = form.getvalue('stockmovement_destination_location_' + str(i))                
                        if (destination_form is not None and destination_form != ""):
                            destination = destination_form.split('_')
                            location_data['id_container_hierarchy'] = destination[0]
                            location_data['row'] = destination[1]
                            location_data['col'] = destination[2]
                            
                            self.execute('insert_lot_strain_location', location_data)
                            self.execute('last_insert_id')
                            id_lot_strain_location_to = self.fetch('one')
                        else:
                            id_lot_strain_location_to = "NULL"
                        
                        movement_data = {'id_stock_movement': str(data['id']), 'id_lot_strain_location_from': str(location_data['id_lot_strain_location']), 'id_lot_strain_location_to': str(id_lot_strain_location_to)}                
                        self.execute('insert_stock_movement_location', movement_data, raw_mode = True)
                        
                        if (destination_form is not None and destination_form != ""):    
                            location_qt_to = self.location.get_incomplete_location(location_data['id_container_hierarchy'], location_data['row'], location_data['col'], None, location_data['quantity'])
                        
                            #get lot name
                            self.execute('get_lot',{'id_lot': location_data['id_lot']})
                            lot_name = self.fetch('one', 'name')
                            
                            #get strain code
                            self.execute('get_strain_code', {'id_strain': location_data['id_strain']})
                            strain_code = self.fetch('one')
                            
                            if save_log:
                                lista_tmp = []
                                dict_temp = {'stock' : location_qt_to, 'id' : location_data['id_lot'], 'lang' : '' }
                                lista_tmp = self.l.checkModifiedFields('', dict_temp, location_data['id_strain'], strain_code, '', 'insert', id_log_operation, id_log_entity, lot_name)
                                return_sql.append(lista_tmp[len(lista_tmp) - 1].replace('|%|ID|%|',str(location_data['id_strain'])))                            
                            
                        #Write log
                        if return_sql:
                            dict_db_log = {}
                            dict_db_log = self.g.get_log_db({'id_base':self.session.data['id_base']})
        
                            #Define Database
                            self.db_log = dbConnection(base_descr = dict_db_log)
                            self.execute_log = self.db_log.execute
                            self.execute_log('insert_log', {'insert_values_log':"".join(return_sql)[0:len("".join(return_sql))-1]}, raw_mode = True)

            elif self.action == 'update':
                self.execute('update_stock_movement', data)
        except Exception as e:
            self.dbconnection.connect.rollback()
            self.db_log.connect.rollback()
            self.feedback(-1)
        else:
            self.dbconnection.connect.commit()
            self.db_log.connect.commit()
            self.feedback(1, data['id'])

    #==============#
    # PRESERVATION #
    #==============#
    def preservation(self):

        def retrieve_form_data(dic_temp, n):
            #brk("localhost",9000)
            dic_temp['origin'] = form.getvalue('preservation_origin_'+str(n))
            dic_temp['original_name'] = form.getvalue('preservation_original_name_'+str(n))
            dic_temp['stock_minimum'] = form.getvalue('preservation_stock_limit_'+str(n))
            dic_temp['id_culture_medium'] = form.getvalue('preservation_culture_medium_'+str(n))
            dic_temp['temp'] = form.getvalue('preservation_temp_'+str(n))
            dic_temp['incub_time'] = form.getvalue('preservation_incub_time_'+str(n))
            dic_temp['cryo'] = form.getvalue('preservation_cryo_'+str(n))
            dic_temp['type'] = form.getvalue('preservation_type_'+str(n))
            dic_temp['purity'] = form.getvalue('preservation_purity_'+str(n))
            if form.getvalue('hdnReusedStrain') != "[]" and form.getvalue('hdnReusedStrain') != None:
                dic_temp['hdnReusedStrain'] = eval(form.getvalue('hdnReusedStrain'))
            else:
                dic_temp['hdnReusedStrain'] = []
                            
            if dic_temp['purity'] != 'ok':
                dic_temp['purity'] = 'n'
            else:
                dic_temp['purity'] = 'y'
            dic_temp['counting'] = form.getvalue('preservation_counting_'+str(n))
            dic_temp['counting_na'] = form.getvalue('preservation_counting_na_'+str(n))
            if dic_temp['counting_na'] is None:
                dic_temp['counting_na'] = 'n'
            else:
                dic_temp['counting_na'] = 'y'
            dic_temp['macro'] = form.getvalue('preservation_macro_characs_'+str(n))
            dic_temp['micro'] = form.getvalue('preservation_micro_characs_'+str(n))
            dic_temp['result'] = form.getvalue('preservation_result_'+str(n))
            dic_temp['obs'] = form.getvalue('preservation_obs_'+str(n))
            dic_temp['origin_lot'] = form.getvalue('preservation_origin_lot_'+str(n))
            if dic_temp['origin'] == 'original':
               dic_temp['origin_lot'] = None


        #Test NotNull Fields
        notnulls = ['preservation_date','preservation_lot']
        if self.action != 'insert': notnulls.append('id')
        self.verify_notnull_fields(notnulls)

        form = self.form
        data = self.data

        #Define LOG Database
        dict_db_log = {}
        dict_db_log = self.g.get_log_db({'id_base':self.session.data['id_base']})

        self.db_log = dbConnection(base_descr = dict_db_log)
        self.execute_log = self.db_log.execute

        from .location import LocationBuilder
        self.location = LocationBuilder(self.cookie_value)

        id_log_level = 3
        id_log_entity = 1
        save_log = self.l.checkLogLevel(id_log_level)

        return_sql = []
        dic_qt = {}

        #Check whether item has already been inserted or updated
        is_first = True
        try:
            global_counter = int(form.getvalue('global_counter_total'))
            if global_counter < 2:
                raise Exception(_("At least one strain must me chosen."))
            #Transform string in data structure
            aux = form.getvalue('global_lot_strain_values')
            lot_strain_ampoules = {}
            if aux != '' and aux is not None:
                aux = aux.split(",")
                for a in aux:
                    a = a.split("-")
                    try:
                        lot_strain_ampoules[a[0]][a[1]] = {'old':int(a[2]),'used':int(a[3])}
                    except:
                        lot_strain_ampoules[a[0]] = {}

            #Preservation Data
            data['date'] = self.sql_dateformat(form.getvalue('preservation_date'))
            data['lot_name'] = form.getvalue('preservation_lot')
            prev_name = form.getvalue('previous_lot_number')
            dic_lot_name = {}
            if prev_name != data['lot_name']:
                dic_lot_name['lot_name'] = data['lot_name']
                #Check whether name already exists
                self.execute('get_lot_name_exists',data)
                name_exists = self.fetch('one')
                if str(name_exists) == '': name_exists = False
                else: name_exists = True
                if name_exists:
                    raise Exception(_("Lot Number already exists in database!") + "<br />" + _("Please insert a different value."))
                if prev_name is not None: #change Lot Name
                    self.execute('update_lot_name',{'new_name':data['lot_name'],'old_name':prev_name})
            data['id_user'] = form.getvalue('preservation_user')
            self.logger.debug('getting this far')
            data['id_method'] = form.getvalue('preservation_method')
            data['info'] = form.getvalue('preservation_process_data')
            self.logger.debug('data = %s' % str(data))

            dic_temp_master = {}
            dic_temp_master['date_preservation'] = data['date']
            dic_temp_master['lot_name'] = data['lot_name']
            
            self.execute('get_one_person', {'id' : data['id_user']})
            dic_temp_master['id_user_preservation'] = self.fetch('one', 'name')
             
            dic_temp_master['id_method'] = data['id_method']
            dic_temp_master['info'] = data['info']
            dic_temp_master['id'] = data['id']

            if (self.action == 'update'):
                #Get Lot ID
                self.execute('get_preservation_lot',data)
                data['inserted_lot_id'] = self.dbconnection.fetch('one')

            #Check whether strain-lot combination has changed
            old_combo = form.getvalue('old_combination')
            new_combo = form.getvalue('new_combination')
            added_combo = {}
            combo_changed = False
            if old_combo is not None and new_combo is not None and old_combo != new_combo:
                combo_changed = True
                #Change common string into data structure (dictionary)
                old_combo = old_combo.split(",")
                temp = {}
                for i in old_combo:
                    i = i.split("-")
                    temp[i[0]] = i[1]
                old_combo = temp
                new_combo = new_combo.split(",")
                temp = {}
                for i in new_combo:
                    i = i.split("-")
                    temp[i[0]] = i[1]
                new_combo = temp

                #####
                #Check which Strains were removed
                #####
                removed_combo = {}
                for i in list(old_combo.keys()):
                    if i not in new_combo:
                        removed_combo[i] = old_combo[i]
                #####
                #Check which Strains were added
                #####
                for i in list(new_combo.keys()):
                    if i not in old_combo:
                        added_combo[i] = new_combo[i]
                #####
                #Check which Strains had their origin changed
                #####
                changed_combo = {}
                for i in list(old_combo.keys()):
                    if (i in new_combo) and (old_combo[i] != new_combo[i]):
                        changed_combo[i] = {'old':old_combo[i],'new':new_combo[i]}

            #raise str(removed_combo)
            if combo_changed:
                #Delete removed combinations
                for i in removed_combo:

                    lot_id = data['inserted_lot_id']
                    id_strain = i

                    self.execute('get_location_by_strain_log', {'id_strain' : id_strain, 'id_lot' :  lot_id})
                    locations = self.fetch('all')

                    #get lot name
                    self.execute('get_lot', {'id_lot' : lot_id})
                    lot_name = self.fetch('one', 'name')

                    #get strain code
                    self.execute('get_strain_code', {'id_strain': id_strain})
                    strain_code = self.fetch('one')

                    id_log_operation = 9
                    #log for delete strain - not stock
                    return_sql.extend(self.l.checkModifiedFields('', {'numeric_code':''}, id_strain, strain_code, '', 'delete', id_log_operation, id_log_entity, lot_name))

                    self.execute('get_preservation_strain_origin_data', {'id': self.data['id'], 'id_strain': id_strain});
                    origin_data = self.fetch('all')[0]

                    self.delete_preservation_strain(True, id_strain, lot_id)

                    if origin_data['origin_type'] == 'lot':
                        dic_qt = {}
                        dic_qt['id_strain'] = id_strain
                        dic_qt['id_container_hierarchy'] = origin_data['id_origin_container_hierarchy']
                        dic_qt['row'] = origin_data['origin_row']
                        dic_qt['col'] = origin_data['origin_col']

                        #get lot name
                        self.execute('get_lot', {'id_lot' : origin_data['id_lot']})
                        lot_origin_name = self.fetch('one', 'name')

                        self.execute('get_location_qt_log', dic_qt)
                        qt_origin = self.fetch('one','available_qt')

                        origin_qt = self.location.get_incomplete_location(origin_data['id_origin_container_hierarchy'], origin_data['origin_row'], origin_data['origin_col'], None, qt_origin)

                        #log for delete strain - origin lot stock
                        lista_tmp = []
                        dict_temp = {'stock' : origin_qt, 'id' : lot_id, 'lang' : '' }
                        lista_tmp = self.l.checkModifiedFields('', dict_temp, id_strain, strain_code, '', 'insert', id_log_operation, id_log_entity, lot_origin_name)
                        return_sql.append(lista_tmp[len(lista_tmp) - 1].replace('|%|ID|%|',str(id_strain)))

                    for location_data in locations:

                        location_qt = self.location.get_incomplete_location(location_data['id_container_hierarchy'], location_data['row'], location_data['col'], None, 0)
                        location_qt = location_qt.replace("()", "(0)")

                        #log for delete strain - stock
                        lista_tmp = []
                        dict_temp = {'stock' : location_qt, 'id' : lot_id, 'lang' : '' }
                        lista_tmp = self.l.checkModifiedFields('', dict_temp, id_strain, strain_code, '', 'insert', id_log_operation, id_log_entity, lot_name)
                        return_sql.append(lista_tmp[len(lista_tmp) - 1].replace('|%|ID|%|',str(id_strain)))

                #Strain changed Lot Origin
                for i in changed_combo:
                    #If previous origin was "Original Culture" then ignore it
                    if int(changed_combo[i]['old']) != 0:
                        #Adjust ampoule usage
                        self.delete_preservation_strain(True,i,data['inserted_lot_id'])

            #Get Data related to each strain
            for i in range(1,global_counter):
                if 'preservation_strain_'+str(i) not in form:
                    continue #Ignore this strain, was removed by user
                
                data['id_strain'] = form.getvalue('preservation_strain_'+str(i))
                data['origin'] = form.getvalue('preservation_origin_'+str(i))
                data['original_name'] = form.getvalue('preservation_original_name_'+str(i))
                data['origin_lot'] = form.getvalue('preservation_origin_lot_'+str(i))
                data['origin_location'] = form.getvalue('preservation_origin_location_'+str(i))
                data['not_identified'] = 0
                self.logger.debug("Origin location: %s" % data['origin_location'])
                if data['origin'] == 'lot':
                    parts = data['origin_location']
                    if not parts:
                        parts = '___'
                    if parts == '___':
                        data['not_identified'] = 1
                    parts = parts.split('_')
                    data['id_origin_container_hierarchy'] = parts[0]
                    data['origin_row'] = parts[1]
                    data['origin_col'] = parts[2]
                    data['origin_quantity'] = parts[3]
                else:
                    data['decrease_stock'] = None
                    data['id_origin_container_hierarchy'] = ""
                    data['origin_row'] = ""
                    data['origin_col'] = ""
                    data['origin_quantity'] = ""
                self.logger.debug("Data now: %s" % str(data))

                data['used'] = form.getvalue('preservation_used_ampoules_'+str(i))
                if data['origin'] == 'original':
                    data['origin_lot'] = None

                data['prepared'] = form.getvalue('preservation_prepared_'+str(i))
                data['stock_pos'] = form.getvalue('preservation_stock_pos_'+str(i))
                data['stock_minimum'] = form.getvalue('preservation_stock_limit_'+str(i))
                data['id_culture_medium'] = form.getvalue('preservation_culture_medium_'+str(i))
                data['temp'] = form.getvalue('preservation_temp_'+str(i))
                data['incub_time'] = form.getvalue('preservation_incub_time_'+str(i))
                data['cryo'] = form.getvalue('preservation_cryo_'+str(i))
                data['type'] = form.getvalue('preservation_type_'+str(i))
                data['purity'] = form.getvalue('preservation_purity_'+str(i))
                if data['purity'] != 'ok':
                    data['purity'] = 'n'
                else:
                    data['purity'] = 'y'
                data['counting'] = form.getvalue('preservation_counting_'+str(i))
                data['counting_na'] = form.getvalue('preservation_counting_na_'+str(i))
                if data['counting_na'] is None:
                    data['counting_na'] = 'n'
                else:
                    data['counting_na'] = 'y'
                data['macro'] =  form.getvalue('preservation_macro_characs_'+str(i))
                data['micro'] =  form.getvalue('preservation_micro_characs_'+str(i))
                data['result'] = form.getvalue('preservation_result_'+str(i))
                data['obs'] =    form.getvalue('preservation_obs_'+str(i))

                #get strain code for strain in selected in loop
                self.execute('get_strain_code', {'id_strain': data['id_strain']})
                strain_code = self.fetch('one')

                #brk("localhost", 9000)
                if is_first:
                    old_prepared_amps = {}
                    dic_temp_detail = {}
                    
                    if (self.action == 'update'):
                        id_log_operation = 9

                        #check changed data strain in preservation (used in log)
                        for n in range(1,global_counter):
                            if 'preservation_strain_'+str(n) not in form:
                                    continue

                            id_strain = form.getvalue('preservation_strain_'+str(n))
                            #get strain code
                            self.execute('get_strain_code', {'id_strain': id_strain})
                            str_code = self.fetch('one')

                            #get id_preserv_strain
                            tmp = {'id_preservation': data['id'], 'id_strain': id_strain}
                            self.execute('get_id_preservation_strain_log', tmp)
                            dic_temp_detail['id'] = self.fetch('one', 'id_preserv_str')
                            retrieve_form_data(dic_temp_detail, n)

                            #generates log for each strain. id_log_entity will be id_strain
                            if save_log:
                                #if lot_name was changed, generates log for each strain
                                if len(dic_lot_name) > 0:
                                    return_sql.extend(self.l.checkModifiedFields('', dic_lot_name, id_strain, str_code, '', 'insert', id_log_operation, id_log_entity, self.ConvertStrUnicode(data['lot_name'])))

                                return_sql.extend(self.l.checkModifiedFields('get_preservation_data_log', dic_temp_master, id_strain, str_code, '', 'update', id_log_operation, id_log_entity, self.ConvertStrUnicode(data['lot_name'])))
                                if id_strain in added_combo:
                                    return_sql.extend(self.l.checkModifiedFields('get_preservation_strain_log', dic_temp_detail, id_strain, str_code, '', 'insert', id_log_operation, id_log_entity, self.ConvertStrUnicode(data['lot_name'])))
                                else:
                                    return_sql.extend(self.l.checkModifiedFields('get_preservation_strain_log', dic_temp_detail, id_strain, str_code, '', 'update', id_log_operation, id_log_entity, self.ConvertStrUnicode(data['lot_name'])))

                        self.execute('update_preservation',data)

                        #Delete previous data
                        self.logger.debug(str(data))
                        self.execute('delete_preservation_strain',data)

                    elif (self.action == 'insert'):
                        #First, insert Lot and get its ID
                        self.execute('insert_lot',data)
                        self.execute('last_insert_id')
                        data['inserted_lot_id'] = self.dbconnection.fetch('one')
                        #Insert data
                        self.logger.debug("insert_preservation %s", data)
                        self.execute('insert_preservation',data)
                        self.execute('last_insert_id')
                        data['id'] = self.dbconnection.fetch('one')

                        #check changed data strain in preservation
                        for n in range(1,global_counter):
                            if 'preservation_strain_'+str(n) not in form:
                                    continue

                            id_strain = form.getvalue('preservation_strain_'+str(n))
                            #get strain code
                            self.execute('get_strain_code', {'id_strain': id_strain})
                            str_code = self.fetch('one')

                            #get id_preserv_strain
                            tmp = {'id_preservation': data['id'], 'id_strain': id_strain}
                            self.execute('get_id_preservation_strain_log', tmp)
                            dic_temp_detail['id'] = self.fetch('one', 'id_preserv_str')
                            retrieve_form_data(dic_temp_detail, n)

                            #generates log for each strain. id_log_entity will be id_strain
                            if save_log:
                                id_log_operation = 8
                                return_sql.extend(self.l.checkModifiedFields('', dic_temp_master, id_strain, str_code, '', 'insert', id_log_operation, id_log_entity, self.ConvertStrUnicode(data['lot_name'])))
                                return_sql.extend(self.l.checkModifiedFields('', dic_temp_detail, id_strain, str_code, '', 'insert', id_log_operation, id_log_entity, self.ConvertStrUnicode(data['lot_name'])))


                    #Security Info
                    self.g.apply_item_permission(self.dbconnection, 'preservation', form, data, self.action)

                    is_first = False

                self.execute('insert_preservation_strain', data)
                self.execute('last_insert_id')

                data['id_preserv_str'] = self.dbconnection.fetch('one')
                
                location_data_del = {}

                if self.action == 'update' and int(data['id_strain']) in old_prepared_amps:
                    #Amount of prepared ampoules changed for this Strain
                    old_val = int(old_prepared_amps[int(data['id_strain'])])
                    new_val = int(data['prepared'])
                    self.execute('get_ampoules_lot_strain', {'id_lot':data['inserted_lot_id'],'id_strain':data['id_strain']})
                    num_ampoules = self.dbconnection.fetch('one')
                    if old_val != new_val:
                        #raise error if count is negative
                        if num_ampoules + (new_val - old_val) < 0:
                            raise Exception(_("The preservation has less than ampoules has already been used."))

                new_strain = False
                #Verify if lot-strain combination already exists
                self.execute('exists_lot_strain_ampoules_combo',{'id_lot':data['inserted_lot_id'],'id_strain':data['id_strain']})
                if (int(self.dbconnection.fetch('one')) == 0): #does not exist yet
                    #Insert amount of ampoules for this lot-strain combination
                    self.execute('insert_lot_strain_ampoules_combo',data)
                    new_strain = True

                found_strain = False;
                for item in dic_temp_detail["hdnReusedStrain"]:
                    if str(item) == data['id_strain']:
                        found_strain = True
                        
                if self.action == 'update':
                    lsl_data = {}
                    lsl_data['id_lot'] = form.getvalue('id_lot') #data['inserted_lot_id']
                    lsl_data['id_strain'] = data['id_strain']
                    self.logger.debug('delete lsl: %s' % str(lsl_data))
                    
                    if found_strain:
                        pass
                    else:
                        if save_log:
                            self.execute('get_lot_strain_location', lsl_data)
                            location_data_del = self.fetch('all')

                        self.execute('delete_lot_strain_location', lsl_data)

                #Retrieve stock location data
                from .json import JsonBuilder
                self.logger.debug(data)
                locations = JsonBuilder.parse(form.getvalue('current_locations_'+str(i)))
                loc_pos = -1

                if new_strain and data['origin'] == 'lot':
                    if save_log:
                        id_log_operation = 8

                        dic_qt = {}
                        dic_qt['id_strain'] = data['id_strain']
                        dic_qt['id_container_hierarchy'] = data['id_origin_container_hierarchy']
                        dic_qt['row'] = data['origin_row']
                        dic_qt['col'] = data['origin_col']

                        self.execute('get_location_qt_log', dic_qt)
                        origin_actual_qt = self.fetch('one','available_qt')

                        origin_qt = self.location.get_incomplete_location(dic_qt['id_container_hierarchy'], dic_qt['row'], dic_qt['col'], None, origin_actual_qt)

                        #get lot name
                        self.execute('get_lot', {'id_lot' : data['origin_lot']})
                        lot_origin_name = self.fetch('one', 'name')

                        lista_tmp = []
                        dict_temp = {'stock' : origin_qt, 'id' : data['origin_lot'], 'lang' : '' }
                        lista_tmp = self.l.checkModifiedFields('', dict_temp, data['id_strain'], strain_code, '', 'insert', id_log_operation, id_log_entity, lot_origin_name)
                        return_sql.append(lista_tmp[len(lista_tmp) - 1].replace('|%|ID|%|',str(data['id_strain'])))

                if not found_strain:
                    for location in locations:
                        loc_pos += 1
                        loc_data = {}
                        loc_data['id_lot'] = data['inserted_lot_id']
                        loc_data['id_strain'] = data['id_strain']
                        loc_data['id_container_hierarchy'] = str(location['id_container_hierarchy'])
                        loc_data['row'] = str(location['row'])
                        loc_data['col'] = str(location['col'])
                        loc_data['quantity'] = location['quantity']
                        self.logger.debug('insert lsl: %s' % str(loc_data))
                        self.execute('get_movement_lot_strain_usage_information_all', {'id_lot': loc_data['id_lot'],'id_strain': loc_data['id_strain']}, force_debug=False)
                        if self.fetch('all') and len(self.fetch('all')) > 0:
                            pass
                        else:
                            self.execute('insert_lot_strain_location', loc_data)
    
                            if save_log:
                                if (self.action == 'insert'):
                                    id_log_operation = 8
    
                                    lista_tmp = []
                                    dict_temp = {'stock' : data['stock_pos'].splitlines()[loc_pos], 'id' : loc_data['id_lot'], 'lang' : '' }
                                    lista_tmp = self.l.checkModifiedFields('', dict_temp, loc_data['id_strain'], strain_code, '', 'insert', id_log_operation, id_log_entity, self.ConvertStrUnicode(data['lot_name']))
                                    return_sql.append(lista_tmp[len(lista_tmp) - 1].replace('|%|ID|%|',str(data['id_strain'])))
    
                                elif (self.action == 'update'):
                                    id_log_operation = 9
    
                                    found = False
                                    for data_del in location_data_del:
                                        #if location has changed quantity
                                        if str(data_del['id_container_hierarchy']) == str(loc_data['id_container_hierarchy']) and str(data_del['row']) == str(loc_data['row']) and str(data_del['col']) == str(loc_data['col']):
                                            if str(data_del['quantity']) != str(loc_data['quantity']):
                                                lista_tmp = []
                                                dict_temp = {'stock' : data['stock_pos'].splitlines()[loc_pos], 'id' : loc_data['id_lot'], 'lang' : '' }
                                                lista_tmp = self.l.checkModifiedFields('', dict_temp, data['id_strain'], strain_code, '', 'insert', id_log_operation, id_log_entity, self.ConvertStrUnicode(data['lot_name']))
                                                return_sql.append(lista_tmp[len(lista_tmp) - 1].replace('|%|ID|%|',str(data['id_strain'])))
                                            data_del['used'] = True
                                            found = True
                                            break
    
                                    #if any item was added
                                    if not found:
                                        lista_tmp = []
                                        dict_temp = {'stock' : data['stock_pos'].splitlines()[loc_pos], 'id' : loc_data['id_lot'], 'lang' : '' }
                                        lista_tmp = self.l.checkModifiedFields('', dict_temp, data['id_strain'], strain_code, '', 'insert', id_log_operation, id_log_entity, self.ConvertStrUnicode(data['lot_name']))
                                        return_sql.append(lista_tmp[len(lista_tmp) - 1].replace('|%|ID|%|',str(data['id_strain'])))

                #items with 'used' = 0, are items than was deleted
                if self.action == 'update':
                    for data_del in location_data_del:
                        if (data_del['used'] == '0'):
                            deleted_location = self.location.get_incomplete_location(data_del['id_container_hierarchy'], data_del['row'], data_del['col'], None, '0')
                            lista_tmp = []
                            dict_temp = {'stock' : deleted_location, 'id' : loc_data['id_lot'], 'lang' : '' }
                            lista_tmp = self.l.checkModifiedFields('', dict_temp, data['id_strain'], strain_code, '', 'insert', id_log_operation, id_log_entity, self.ConvertStrUnicode(data['lot_name']))
                            return_sql.append(lista_tmp[len(lista_tmp) - 1].replace('|%|ID|%|',str(data['id_strain'])))

            if save_log and return_sql:
                sql_final = "".join(return_sql)[0:len("".join(return_sql))-1]

                #Save log data
                self.execute_log('insert_log', {'insert_values_log':sql_final}, raw_mode = True)


        except Exception as e:
            #self.session.data['preservation_form_data'] = form
            self.dbconnection.connect.rollback()
            self.db_log.connect.rollback()
            self.feedback(-1)
        else:
            self.dbconnection.connect.commit()
            self.db_log.connect.commit()
            self.feedback(1, data['id'])

    def delete_preservation_strain(self,isRootNode,id_strain,id_lot):
        '''
        Recursively delete all info associated with this "id_strain-id_lot" combo
        '''
        #Grab children
        self.execute('get_preservation_strain_descendants',{'id_strain':id_strain,'id_lot':id_lot})
        children = self.dbconnection.fetch('all')
        for child in children:
            #Visit them first
            child_id_strain = int(child['id_strain'])
            child_id_lot = int(child['p_id_lot'])
            self.delete_preservation_strain(False, child_id_strain, child_id_lot)

        #Get Node Info
        self.execute('get_preservation_strain_info',{'id_strain':id_strain,'id_lot':id_lot})
        info = self.dbconnection.fetch('columns')

        #Delete node
        self.execute('delete_preservation_strain_by_id',{'id_preserv_str':info['id_preserv_str']})
        #Delete this lot_strain_location combination (cascades automatically)
        self.execute('delete_lot_strain_location',{'id_strain':id_strain,'id_lot':id_lot})
        #Delete this lot_strain combination (cascades automatically)
        self.execute('delete_lot_strain',{'id_strain':id_strain,'id_lot':id_lot})
        
    def container(self):
        #brk(host="localhost", port=9000)
        
        form_action = self.form.getvalue('form_action')

        if not form_action == 'partial_edit':
            #Test NotNull Fields
            notnulls = ['abbreviation', 'description', 'preservation_method']
        else:
            notnulls = ['description']

        self.verify_notnull_fields(notnulls)

        form = self.form
        data = self.data

        try:
            data['description'] = form.getvalue('description')
            
            if not form_action == 'partial_edit':
                data['abbreviation'] = form.getvalue('abbreviation')
                data['preservation_method'] = form.getvalue('preservation_method')

            if self.action == 'insert':
                #brk("localhost", 9000)
                self.execute('get_container_by_abbreviation', {'abbreviation': data['abbreviation'], 'id':' '}, True)
                qt = self.fetch('one')
                
                if (qt > 0):
                    raise Exception(_("A container with the same abbreviation already exists."))
                
                self.execute('insert_container', data)
                self.execute('last_insert_id')
                data['id'] = self.dbconnection.fetch('one')
                self.execute('insert_container_subcoll', {'id_container': data['id'], 'id_subcoll': data['id_subcoll']})

                for preservation_method in data['preservation_method']:
                    self.execute('insert_container_preservation_method', {'id_container': data['id'], 'id_preservation_method': preservation_method })

                #brk("localhost", 9000)
                complete_structure = eval(form.getvalue('complete_structure')[:-2])
                if type(complete_structure) != tuple:
                    from . import config
                    out = config.http_header+'\n\n'
                    out += ' - %s <b>%s</b> %s<br>\n' % (_("field"), _('structure'), _("must not be empty."))
                    print(out.encode('utf8'))
                    exit(1)
 
                for node in complete_structure:
                    self.logger.debug(node)
                    self._insert_node(node, data['id'])

            elif self.action == 'update':                
                data['id_container'] = form.getvalue('id')
                                
                self.execute('get_container_by_abbreviation', {'abbreviation': data['abbreviation'], 'id': " AND id_container <> '" + data['id_container'] + "'"},True)
                qt = self.fetch('one')
                
                if (qt > 0):
                    raise Exception(_("A container with the same abbreviation already exists."))
                    
                self.execute('update_container', data)
                
                self.execute('delete_container_subcoll', {'id': data['id_container']})
                self.execute('delete_container_preservation_method', {'id': data['id_container']})
                self.execute('delete_container_location', {'id': data['id_container']})                                        
                self.execute('delete_container_hierarchy', {'id': data['id_container']})                                      

                self.execute('insert_container_subcoll', {'id_container': data['id'], 'id_subcoll': data['id_subcoll']})

                for preservation_method in data['preservation_method']:
                    self.execute('insert_container_preservation_method', {'id_container': data['id'], 'id_preservation_method': preservation_method })
                
                complete_structure = eval(form.getvalue('complete_structure')[:-2])
                if type(complete_structure) != tuple:
                    from . import config
                    out = config.http_header+'\n\n'
                    out += ' - %s <b>%s</b> %s<br>\n' % (_("field"), _('structure'), _("must not be empty."))
                    print(out.encode('utf8'))
                    exit(1)
 
                for node in complete_structure:
                    self.logger.debug(node)
                    self._insert_node(node, data['id'])
        except Exception as e:
            self.dbconnection.connect.rollback()
            self.feedback(-1)
        else:
            self.dbconnection.connect.commit()
            self.feedback(1, data['id'])

    def _insert_node(self, node, id_container, id_parent=None):
        #brk(host="localhost", port=9000)
        #self.logger.debug('Inserting container node [data: {0}]'.format(node))
        node_data = node[0]

        data = {}
        node_info = node_data.split('|:|')
        data['abbreviation'] = node_info[0]
        data['description'] = node_info[1]
        data['id_container'] = id_container
        data['id_parent'] = id_parent

        self.execute('insert_container_hierarchy', data)
        self.execute('last_insert_id')
        data['id'] = self.dbconnection.fetch('one')

        self.logger.debug('Node lenght: ' + str(len(node)))
        if len(node) > 1: # if node has childrens
            self.logger.debug('Node has children')
            node_childrens = node[1:]
            for children in node_childrens:
                self._insert_node(children, id_container, id_parent=data['id'])

        else: # if the node has no childrens it must have location data
            data_location = {}
            location = node_info[2]
            location_info = location.split('|-|')
            data_location['rows'] = location_info[0]
            data_location['cols'] = location_info[1]
            data_location['ini_row'] = location_info[2]
            data_location['ini_col'] = location_info[3]
            data_location['pattern'] = location_info[4].replace("<>", "%(row)s").replace("[]", "%(col)s")
            data_location['id_container_hierarchy'] = data['id']
            self.execute('insert_location', data_location)


    #==============#
    # REPORTS      #
    #==============#
    def reports(self):
        try:
            #brk(host="localhost", port=9000)
                
            new_report = self.session.data['new_report']
            
            xml = ''
            
            xml += '<?xml version="1.0" encoding="utf-8"?>'
            xml += '<report>'
            
            xml += '<fields>'
            xml += '<select>'
            if new_report['select']:
                for item in new_report['select']:
                    xml += '<field name="' + item + '" />'
            xml += '</select>'
            xml += '<group>'
            if new_report['group']:
                for item in new_report['group']:
                    xml += '<field name="' + item + '" />'
            xml += '</group>'
            xml += '<total>'
            if new_report['total']:
                xml += '<field name="' + new_report['total']['name'] + '" function="' + new_report['total']['function'] + '" />'
            xml += '</total>'
            xml += '</fields>'
            
            xml += '<filters>'
            if new_report['filters']:
                for item in new_report['filters']:
                    xml += self.mount_filter_xml(item)
            xml += '</filters>'
            
            xml += '<format '
            if 'format' in new_report:
                xml += 'type="' + str(new_report['format']) + '" '
            if 'header_position' in new_report:
                xml += 'header_position="' + str(new_report['header_position']) + '" '
            if 'append_subcoll_templates' in new_report:
                xml += 'append_subcoll_templates="' + str(new_report['append_subcoll_templates']) + '" '
            if 'separator' in new_report:
                xml += 'separator="' + str(new_report['separator']) + '" '
            if 'header' in new_report:
                xml += 'header="' + str(new_report['header']) + '" '
            if 'chart_type' in new_report:
                xml += 'chart_type="' + str(new_report['chart_type']) + '" '
            xml += '/>'
            
            if new_report['format'] == "custom":
                import base64                                
                xml += '<template>'
                xml += '    <main>'
                xml += '        <header><![CDATA[' + (new_report['templates']['main'].get('header', '')) + ']]></header>'
                xml += '        <footer><![CDATA[' + (new_report['templates']['main'].get('footer', '')) + ']]></footer>'
                xml += '        <css><![CDATA['    + (new_report['templates']['main'].get('css'   , '')) + ']]></css>'
                xml += '        <data><![CDATA['   + (new_report['templates']['main'].get('data'  , '')) + ']]></data>'
                xml += '    </main>'
                xml += '    <groups>'
                for template_group in new_report['templates']['group']:
                    xml += '        <group name="' + template_group + '">'
                    xml += '            <header><![CDATA[' + (new_report['templates']['group'][template_group]['header']) + ']]></header>'
                    xml += '            <footer><![CDATA[' + (new_report['templates']['group'][template_group]['footer']) + ']]></footer>'
                    xml += '        </group>'
                xml += '    </groups>'
                xml += '</template>'
            
            xml += '</report>'
            
            #Define Form
            form = self.form
            #Define Data Dict
            data = {}
            data['id_subcoll'] = self.session.data['id_subcoll']
            data['id_report_type'] = str(new_report['type'])           
            data['description'] = new_report['name']
            data['definition'] = xml
            
            if ('action' in self.session.data.get('new_report', {'action':''})) == False:
                self.execute('insert_report_xml', data)
                
                self.execute('last_insert_id')
                data['id'] = self.dbconnection.fetch('one')
                
                self.g.apply_item_permission(self.dbconnection, 'reports', form, data, "insert")
                
                self.session.data['new_report'] = {}
                self.session.save()
            
            else:
                data['id'] = self.session.data['new_report']['id']
                
                self.execute('update_report_xml', data)
                
                self.g.apply_item_permission(self.dbconnection, 'reports', form, data, "update")
                
                self.session.data['new_report'] = {}
                self.session.save()

        except Exception as e:
            self.dbconnection.connect.rollback()
            self.feedback(-1)
        else:
            self.dbconnection.connect.commit()
            self.feedback(1, data['id'])
            
    def mount_filter_xml(self, item):
        xml = '<filter '
        if 'field' in item:
            xml += 'field="'        + item['field']        + '" '
        if 'condition' in item:
            xml += 'condition="'    + item['condition']    + '" '
        if 'value' in item:
            xml += 'value="'        + item['value']        + '" '
        if 'user_defined' in item:
            xml += 'user_defined="' + item['user_defined'] + '" '
        if 'connector' in item:
            xml += 'connector="'    + item['connector']    + '" '
        if 'field_lookup' in item:
            xml += 'field_lookup="' + item['field_lookup'] + '" '
        if item['childs'] == []:
            xml += '/>'
        else:
            xml += '>'
            
            for noh in item['childs']:
                xml += self.mount_filter_xml(noh)
            
            xml += '</filter>'
        
        return xml
    
    def ConvertStrUnicode(self, valor):
        retorno = '';
        if isinstance(valor, (int, float)):
            return str(valor)
            
        if (isinstance(valor, str) == False):
            retorno = str(valor).decode("utf8")
        else:
            retorno = valor
        
        return retorno