#!/usr/bin/env python3
#-*- coding: utf-8 -*-


#project imports
from .session import Session
from .general import General
from .dbconnection import dbConnection
from .getdata import Getdata
from .loghelper import Logging
from .log import Log
#from dbgp.client import brk
from .labels import label_dict

class Configuration(object):

    g = General()
    session = None

    #brk(host="localhost", port=9000)

    def __init__(self, cookie_value='',form=None):
        self.cookie_value = cookie_value
        #Load Session
        self.session = Session()
        self.session.load(cookie_value)

        #Make form a class attribute
        self.form = form

        #Define Databases
        #External
        self.db = dbConnection(cookie_value)
        #SQLite
        self.dbconnection = dbConnection()
        self.execute = self.dbconnection.execute
        self.cursor = self.dbconnection.cursor
        self.fetch = self.dbconnection.fetch
        
        self.l = Log(cookie_value, self.db)

        #Define Logging
        self.logger = Logging.getLogger("configuration")
        self.d = self.logger.debug

        #Load GetData class
        self.getdata = Getdata(self.cookie_value, self.form)

    def deleteUser(self):
        #Get all databases from all collections and subcollections
        self.dbconnection.execute('get_all_dbs')
        bases = self.dbconnection.fetch('all')

        #Deletes user from all MySQL databases for all subcollections
        bases_to_commit = []
        for base in bases:
            #Connects to the datababase of each subcollection
            base_db = dbConnection(base_descr=base)

            #Retrieves the user group (role with 'user' type)
            base_db.execute('get_user_group',{'id_user':str(self.form['util_user_id'].value)})
            group_user = base_db.fetch('one')

            #Deletes all roles associations for this user
            base_db.execute('delete_user_roles',{'id_user':str(self.form['util_user_id'].value)})
            #Deletes all access on that subcollection
            base_db.execute('delete_area_access',{'role_id':group_user})
            #Deletes the user role
            base_db.execute('delete_role',{'id_role':group_user})
            bases_to_commit.append(base_db)

        for base_db in bases_to_commit:
            #Commits
            base_db.connect.commit()

        #Deletes user from SQLite
        self.execute('delete_user',{'id_user':str(self.form['util_user_id'].value)})
        self.execute('delete_user_access',{'id_user':str(self.form['util_user_id'].value)})
        self.execute('delete_user_pref',{'id_user':str(self.form['util_user_id'].value)})

        self.session.data['feedback'] = 2
        self.session.save()

    def deleteSubcoll(self,id_subcoll=None):
        if id_subcoll is None:
          self.execute('delete_subcoll',{'subcoll_id':str(self.form['util_subcoll_id'].value)})
          self.execute('delete_subcoll_template',{'subcoll_id':str(self.form['util_subcoll_id'].value)})
          self.execute('delete_sys_config',{'subcoll_id':str(self.form['util_subcoll_id'].value)})
          self.execute('delete_subcoll_access',{'subcoll_id':str(self.form['util_subcoll_id'].value)})
          self.execute('delete_subcoll_data_lang', {'id_subcoll': str(self.form['util_subcoll_id'].value)})
          self.db.execute('delete_subcoll_combo_str_type', {'id_subcoll': str(self.form['util_subcoll_id'].value)})
          self.db.execute('delete_subcoll_combo_dep_reason', {'id_subcoll': str(self.form['util_subcoll_id'].value)})
          self.db.execute('delete_subcoll_combo_test_group', {'id_subcoll': str(self.form['util_subcoll_id'].value)})
          self.db.execute('delete_subcoll_combo_preservation_method', {'id_subcoll': str(self.form['util_subcoll_id'].value)})
          self.db.execute('delete_ref_by_subcoll', {'id_subcoll': str(self.form['util_subcoll_id'].value)})
          self.db.execute('delete_doc_by_subcoll', {'id_subcoll': str(self.form['util_subcoll_id'].value)})
          self.db.execute('delete_strain_by_subcoll', {'id_subcoll': str(self.form['util_subcoll_id'].value)})
          self.db.execute('delete_species_by_subcoll', {'id_subcoll': str(self.form['util_subcoll_id'].value)})
        else:
          self.execute('delete_subcoll',{'subcoll_id':id_subcoll})
          self.execute('delete_subcoll_template',{'subcoll_id':id_subcoll})
          self.execute('delete_sys_config',{'subcoll_id':id_subcoll})
          self.execute('delete_subcoll_access',{'subcoll_id':id_subcoll})
          self.execute('delete_subcoll_data_lang', {'id_subcoll':id_subcoll})
          self.db.execute('delete_subcoll_combo_str_type', {'id_subcoll': id_subcoll})
          self.db.execute('delete_subcoll_combo_dep_reason', {'id_subcoll': id_subcoll})
          self.db.execute('delete_subcoll_combo_test_group', {'id_subcoll': id_subcoll})
          self.db.execute('delete_subcoll_combo_preservation_method', {'id_subcoll': id_subcoll})
          self.db.execute('delete_ref_by_subcoll', {'id_subcoll': id_subcoll})
          self.db.execute('delete_doc_by_subcoll', {'id_subcoll': id_subcoll})
          self.db.execute('delete_strain_by_subcoll', {'id_subcoll': id_subcoll})
          self.db.execute('delete_species_by_subcoll', {'id_subcoll': id_subcoll})
        self.db.connect.commit()
        self.session.data['feedback'] = 2
        self.session.save()

    def deleteDivision(self):
        id_division = str(self.form['util_division_id'].value)

        from .strain_formatter import StrainFormatter, StrainFormatterError
        s = StrainFormatter(self.cookie_value)

        try:
            s.delete_division(id_division)
            self.session.data['feedback'] = 2
        except StrainFormatterError:
            self.session.data['feedback'] = -13
        self.session.save()

    def deleteColl(self):
        self.execute('get_subcolls_from_coll',{'coll_id':str(self.form['util_coll_id'].value)})
        subcolls = self.fetch('rows')
        for subcoll in subcolls:
          self.deleteSubcoll(subcoll)
        self.execute('delete_coll',{'coll_id':str(self.form['util_coll_id'].value)})
        self.session.data['feedback'] = 2
        self.session.save()

    def deleteDB(self):
        #database
        self.execute('delete_base',{'base_id':str(self.form['util_base_id'].value)})
        #tracebility
        self.execute('delete_base_log',{'base_id':str(self.form['util_base_id'].value)})

        self.session.data['feedback'] = 2
        self.session.save()

    def deleteRole(self):
        self.db.execute('delete_role',{'id_role':str(self.form['util_role_id'].value)})
        self.db.connect.commit()
        self.session.data['feedback'] = 2
        self.session.save()

    def saveConfigXML(self):
        config_indexurl = self.form['util_config_indexurl'].value
        config_rootdir = self.form['util_config_rootdir'].value
        config_startpage = self.form['util_config_startpage'].value
        config_dateinput = self.form['util_config_dateinput'].value
        config_dateoutput = self.form['util_config_dateoutput'].value
        config_lang = self.form['util_config_lang'].value
        config_upload = self.form['util_config_upload'].value
        #if (self.form.has_key('util_role_id')): #Empty fields are discarded automatically
        if (isinstance(self.form['util_config_data_lang'], list)):
            config_data_lang = []
            for x in self.form['util_config_data_lang']:
                config_data_lang.append(x.value)
            config_data_lang = ",".join(config_data_lang)
        else:
            config_data_lang = self.form['util_config_data_lang'].value
        #Save data in config.xml
        configxml = """<?xml version="1.0" encoding="utf-8"?>
<configs>
  <!-- Necessary "/" in the end -->
  <config name="index_url">%s</config>
  <config name="root_dir">%s</config>
  <!-- start_page: choose one of (species.list, strains.list, people.list,
  institutions.list, doc.list, ref.list) -->
  <config name="start_page">%s</config>
  <config name="label_lang">%s</config>
  <!-- insert value in bytes, leave blank to disable size limit -->
  <config name="upload_limit">%s</config>
  <!-- data_lang: insert comma separated language codes in desired order -->
  <config name="data_lang">%s</config>
  <config name="date_input_mask">%s</config>
  <config name="date_output_mask">%s</config>
  <!-- log_file: name of the file to use for logging, fully qualified -->
  <config name="log_file">./sicol.log</config>
  <!-- log_level: what is the minimum level to log (debug, info, warn/warning, error) -->
  <config name="log_level">error</config>
  <!-- debug_mode: if the software is on production mode or development mode -->
  <config name="debug_mode">false</config>
</configs>
""" % (config_indexurl,config_rootdir,config_startpage,config_lang,config_upload,config_data_lang,config_dateinput,config_dateoutput)
        from os import path
        try:
          open(path.join(config_rootdir,'config.xml'),'w').write(configxml)
          self.session.data['feedback'] = 1
          self.session.save()
        except IOError: #No permission to open file
          self.session.data['feedback'] = -2
          self.session.save()

    def saveRole(self):
        #Read form data
        role_id = ''
        if ('util_role_id' in self.form): #Empty fields are discarded automatically
          role_id = str(self.form['util_role_id'].value)
        role_name = str(self.form['util_role_name'].value)
        role_type = str(self.form['util_role_type'].value)
        role_descr = ''
        if ('util_role_descr' in self.form): #Empty fields are discarded automatically
          role_descr = str(self.form['util_role_descr'].value)
        if role_id == '': #New Role
            self.db.execute('insert_role', {'role_name': role_name,'role_type':role_type,'role_descr':role_descr})
            self.db.execute('last_insert_id')
            role_id = self.db.fetch('one')
        else: #Edited Role
            self.db.execute('update_role', {'id_role':role_id,'role_name': role_name,'role_type':role_type,'role_descr':role_descr})
        #Manage area access
        #Delete all previous area accesses of this group
        self.db.execute('delete_area_access',{'role_id':role_id})
        #Get all existing areas
        self.db.execute('get_all_areas')
        list_areas = self.db.fetch('all')
        js_areadel_list = []
        js_areacreate_list = []
        js_area_list = []
        for area in list_areas:
           js_areadel_list.append("areadel_"+str(area['id_area']))
           js_areacreate_list.append("areacreate_"+str(area['id_area']))
           js_area_list.append(str(area['id_area']))
        #Insert new area access configuration
        for item in js_area_list:
           areadel = 'n'
           areacreate = 'n'
           if 'areadel_'+item in self.form:
             areadel = 'y'
           if 'areacreate_'+item in self.form:
             areacreate = 'y'
           self.db.execute('insert_area_access',{'id_area':item,'id_role':role_id,'allow_delete':areadel,'allow_create':areacreate})
        #Associate users to current role
        #Delete previous associations
        self.db.execute('delete_role_users',{'id_role':role_id})
        if ('util_group_members' in self.form):
          if (isinstance(self.form['util_group_members'], list)):
             for x in self.form['util_group_members']:
                member_id = x.value
                self.db.execute('insert_user_role',{'id_user':member_id,'id_role':role_id})
          else:
             member_id = self.form['util_group_members'].value
             self.db.execute('insert_user_role',{'id_user':member_id,'id_role':role_id})
        self.db.connect.commit()
        self.session.data['feedback'] = 1
        self.session.save()

    def saveCombo(self):
        #Read form data
        combo_id = ''
        if ('util_combo_id' in self.form): #Empty fields are discarded automatically
           combo_id = str(self.form['util_combo_id'].value)
        #Update Taxon Group
        self.db.execute('delete_subcoll_combo_taxon_group', {'id_subcoll': combo_id})
        if (isinstance(self.form['util_combo_taxon_group'], list)):
            for taxon_group in self.form['util_combo_taxon_group']:
                self.db.execute('insert_subcoll_taxon_group', {'id_subcoll': combo_id, 'id_taxon_group': taxon_group.value})
        else:
            self.db.execute('insert_subcoll_taxon_group', {'id_subcoll': combo_id, 'id_taxon_group': self.form['util_combo_taxon_group'].value})
        #Update Strain - General - Type - combobox
        self.db.execute('delete_subcoll_combo_str_type', {'id_subcoll': combo_id})
        if (isinstance(self.form['util_combo_str_type'], list)):
            for str_type in self.form['util_combo_str_type']:
                self.db.execute('insert_subcoll_str_type', {'id_subcoll': combo_id, 'id_type': str_type.value})
        else:
            self.db.execute('insert_subcoll_str_type', {'id_subcoll': combo_id, 'id_type': self.form['util_combo_str_type'].value})
        new_type = {}
        for lang in self.form['util_combo_langs'].value.split(","):
            if 'combo_str_type_'+lang in self.form and self.form['combo_str_type_'+lang].value != '':
                new_type[lang] = self.form['combo_str_type_'+lang].value
        if new_type != {}: #A new item is to be inserted
            #Insert new item and get its id
            self.db.execute('insert_new_str_type')
            self.db.connect.commit()
            new_id = self.db.cursor.lastrowid
            #It now belongs to this subcollection
            self.db.execute('insert_subcoll_str_type', {'id_subcoll': combo_id, 'id_type': new_id})
            for item_lang,item_type in list(new_type.items()): #Add names for each language
                self.db.execute('insert_subcoll_str_type_lang', {'id_type': new_id,'type': item_type,'code': item_lang})
        #Update Strain - Deposit - Type - combobox
        self.db.execute('delete_subcoll_combo_dep_reason', {'id_subcoll': combo_id})
        if (isinstance(self.form['util_combo_dep_reason'], list)):
            for dep_reason in self.form['util_combo_dep_reason']:
                self.db.execute('insert_subcoll_dep_reason', {'id_subcoll': combo_id, 'id_dep_reason': dep_reason.value})
        else:
            self.db.execute('insert_subcoll_dep_reason', {'id_subcoll': combo_id, 'id_dep_reason': self.form['util_combo_dep_reason'].value})
        new_dep_reason = {}
        for lang in self.form['util_combo_langs'].value.split(","):
            if 'combo_dep_reason_'+lang in self.form and self.form['combo_dep_reason_'+lang].value != '':
                new_dep_reason[lang] = self.form['combo_dep_reason_'+lang].value
        if new_dep_reason != {}: #A new item is to be inserted
            #Insert new item and get its id
            self.db.execute('insert_new_dep_reason')
            self.db.connect.commit()
            new_id = self.db.cursor.lastrowid
            #It now belongs to this subcollection
            self.db.execute('insert_subcoll_dep_reason', {'id_subcoll': combo_id, 'id_dep_reason': new_id})
            for item_lang,item_dep_reason in list(new_dep_reason.items()): #Add names for each language
                self.db.execute('insert_subcoll_dep_reason_lang', {'id_dep_reason': new_id,'dep_reason': item_dep_reason,'code': item_lang})
        #Update Preservation Method - combobox
        self.db.execute('delete_subcoll_combo_preservation_method', {'id_subcoll': combo_id})
        if (isinstance(self.form['util_combo_preservation_method'], list)):
            for preservation_method in self.form['util_combo_preservation_method']:
                self.db.execute('insert_subcoll_preservation_method', {'id_subcoll': combo_id, 'id_preservation_method': preservation_method.value})
        else:
            self.db.execute('insert_subcoll_preservation_method', {'id_subcoll': combo_id, 'id_preservation_method': self.form['util_combo_preservation_method'].value})
        new_preservation_method = {}
        for lang in self.form['util_combo_langs'].value.split(","):
            if 'combo_preservation_method_'+lang in self.form and self.form['combo_preservation_method_'+lang].value != '' and self.form['combo_unit_measure_'+lang].value != '':
                new_preservation_method[lang] = {'method':self.form['combo_preservation_method_'+lang].value, 'unit':self.form['combo_unit_measure_'+lang].value}
        if new_preservation_method != {}: #A new item is to be inserted
            #Insert new item and get its id
            self.db.execute('insert_new_preservation_method')
            self.db.connect.commit()
            new_id = self.db.cursor.lastrowid
            #It now belongs to this subcollection
            self.db.execute('insert_subcoll_preservation_method', {'id_subcoll': combo_id, 'id_preservation_method': new_id})
            for item_lang,item_preservation_method in list(new_preservation_method.items()): #Add names for each language
                self.db.execute('insert_subcoll_preservation_method_lang', {'id_preservation_method': new_id,'method': item_preservation_method['method'],'code': item_lang,'unit_measure': item_preservation_method['unit']})
        #Update Test Group - combobox
        self.db.execute('delete_subcoll_combo_test_group', {'id_subcoll': combo_id})
        if (isinstance(self.form['util_combo_test_group'], list)):
            for test_group in self.form['util_combo_test_group']:
                self.db.execute('insert_subcoll_test_group', {'id_subcoll': combo_id, 'id_test_group': test_group.value})
        else:
            self.db.execute('insert_subcoll_test_group', {'id_subcoll': combo_id, 'id_test_group': self.form['util_combo_test_group'].value})
        new_test_group = {}
        for lang in self.form['util_combo_langs'].value.split(","):
            if 'combo_test_group_'+lang in self.form and self.form['combo_test_group_'+lang].value != '':
                new_test_group[lang] = self.form['combo_test_group_'+lang].value
        if new_test_group != {}: #A new item is to be inserted
            #Insert new item and get its id
            self.db.execute('insert_new_test_group')
            self.db.connect.commit()
            new_id = self.db.cursor.lastrowid
            #It now belongs to this subcollection
            self.db.execute('insert_subcoll_test_group', {'id_subcoll': combo_id, 'id_test_group': new_id})
            for item_lang,item_test_group in list(new_test_group.items()): #Add names for each language
                self.db.execute('insert_subcoll_test_group_lang', {'id_test_group': new_id,'category': item_test_group,'code': item_lang})
        #Commit
        self.db.connect.commit()
        self.session.data['feedback'] = 1
        self.session.save()

    def saveDivision(self):
        #brk(host="localhost", port=9000)
        
        #Read form data
        division_id = ''
        if ('util_division_id' in self.form): #Empty fields are discarded automatically
           division_id = str(self.form['util_division_id'].value)

        division_division = str(self.form['util_division_division'].value)
        division_pattern = str(self.form['util_division_pattern'].value)

        from .strain_formatter import StrainFormatter, StrainFormatterError
        s = StrainFormatter(self.cookie_value, self.db)
                
        log = False

        try:
            if division_id:
                #Verify using log                
                id_log_level = 1
                if self.l.checkLogLevel(id_log_level):

                    id_log_operation = 7
                    id_log_entity = 1
                    
                    data = {}
                    data['id'] = division_id
                    data['id_subcoll'] = self.session.data['id_subcoll']
                    data['subcolls'] = "".join(self.l.listSubcollsLevel(id_log_level))[0:len("".join(self.l.listSubcollsLevel(id_log_level)))-1]

                    #Verify change in 'division' field
                    self.db.execute('lookup_division_log', data)
                    fieldInDB_division = self.db.fetch('one')

                    #Verify change in 'pattern' field
                    self.db.execute('lookup_pattern_log', data)
                    fieldInDB_pattern = self.db.fetch('one')

                    if fieldInDB_division != division_division or fieldInDB_pattern != division_pattern:
                        #Verify in use screen 'strain' field 'division'
                        self.db.execute('exists_division_usage_in_strain_general', data)
                        divisions = self.db.fetch('all')
                        if divisions:
                            log = True
                            return_sql = []
                                
                s.update_division_pattern(division_id, division_division, division_pattern, commit = False)
            else:
                s.insert_division(self.session.data['id_subcoll'], division_pattern, division_division)
            
            if log:   
                #Log
                dict_temp_division = {'id_division' : data['id'], 'id' : data['id'], 'lang' : '' }
                dict_temp_pattern = {'numeric_code_division' : data['id'], 'id' : data['id'], 'lang' : '' }
                
                for division in divisions:
                    #division
                    if fieldInDB_division != division_division:
                        #Used the function 'checkModifiedFields' with parameter 'insert' just to generate the string insertion
                        return_sql.extend(self.l.checkModifiedFields('', dict_temp_division, division['id_strain'], division['code'], '', 'insert', id_log_operation, id_log_entity,''))
                        
                    #pattern
                    if fieldInDB_pattern != division_pattern:
                        #Used the function 'checkModifiedFields' with parameter 'insert' just to generate the string insertion
                        return_sql.extend(self.l.checkModifiedFields('', dict_temp_pattern, division['id_strain'], division['code'], '', 'insert', id_log_operation, id_log_entity,''))
    
                #Write log
                if return_sql:
                    dict_db_log = {}
                    dict_db_log = self.g.get_log_db({'id_base':self.session.data['id_base']})
    
                    #Define Database
                    self.db_log = dbConnection(base_descr = dict_db_log)
                    self.db.execute_log = self.db_log.execute
                    self.db.execute_log('insert_log', {'insert_values_log':"".join(return_sql)[0:len("".join(return_sql))-1]}, raw_mode = True)

        except StrainFormatterError:
            if division_id:
                self.db.connect.rollback()
                if log:   
                    self.db_log.connect.rollback()
            self.session.data['feedback'] = -12
        else:
            if division_id:
                self.db.connect.commit()
                if log:
                    self.db_log.connect.commit()
            self.session.data['feedback'] = 1
            
        self.session.save()


    def saveSubcollTemplate(self):
        
        #brk(host="localhost", port=9000)
        id_subcoll = self.session.data['id_subcoll']
        
        import base64
        
        header =''
        footer = ''
        styles = ''
               
        if 'header_template' in self.form:
            header = base64.b64encode(self.form['header_template'].value)            
        if 'footer_template' in self.form:
            footer = base64.b64encode(self.form['footer_template'].value)            
        if 'css_template' in self.form:
            styles = base64.b64encode(self.form['css_template'].value)
            
        self.execute('update_subcoll_template', {'id_subcoll':id_subcoll, 'header':header, 'footer':footer, 'styles':styles})
                
        self.session.data['feedback'] = 1
        self.session.save()

    def saveSubcoll(self):
        #Read form data
        subcoll_id = ''
        if ('util_subcoll_id' in self.form): #Empty fields are discarded automatically
          subcoll_id = str(self.form['util_subcoll_id'].value)
        subcoll_coll = str(self.form['util_subcoll_coll'].value)
        subcoll_code = str(self.form['util_subcoll_code'].value)
        subcoll_name = ''
        if ('util_subcoll_name' in self.form): #Empty fields are discarded automatically
          subcoll_name = str(self.form['util_subcoll_name'].value).decode('utf8')
        self.execute('count_subcoll',{'subcoll_code':subcoll_code,'subcoll_coll':subcoll_coll})
        count_subcoll = self.fetch('one')
        #raise str(count_subcoll)
        #sys_config data
        subcoll_inputmask = str(self.form['util_subcoll_dateinput'].value)
        subcoll_outputmask = str(self.form['util_subcoll_dateoutput'].value)
        subcoll_lang = str(self.form['util_subcoll_lang'].value)
        new_subcoll = True
        if (subcoll_lang == 'default'): subcoll_lang = ''
        if subcoll_id == '': #New Subcollection
            if count_subcoll < 1:
                self.execute('insert_subcoll',{'subcoll_coll':subcoll_coll,'subcoll_code':subcoll_code.decode('utf8'),'subcoll_name':subcoll_name})                
                self.execute('insert_blank_subcoll_template')
                subcoll_id = self.cursor.lastrowid
                self.execute('insert_sys_config',{'subcoll_id':subcoll_id,'date_input_mask':subcoll_inputmask,'date_output_mask':subcoll_outputmask,'label_lang':subcoll_lang})
                #Give access to administrator(s)
                self.db.execute('get_admins')
                admins = self.db.fetch('rows')
                for admin in admins:
                  self.execute('insert_access',{'id_user':admin,'id_subcoll':subcoll_id})
                #If Collection changed is the same one user is in, then change session data
                if int(subcoll_id) == int(self.session.data['id_subcoll']):
                    self.session.data['subcoll_code'] = subcoll_code
            else: new_subcoll = False
        else: #Edited Subcollection
            if count_subcoll < 1:
                self.execute('update_subcoll',{'subcoll_id':subcoll_id,'subcoll_coll':subcoll_coll,'subcoll_code':subcoll_code.decode('utf8'),'subcoll_name':subcoll_name})
                self.execute('update_sys_config',{'subcoll_id':subcoll_id,'date_input_mask':subcoll_inputmask,'date_output_mask':subcoll_outputmask,'label_lang':subcoll_lang})
            else:
                self.execute('get_subcoll_code',{'id_subcoll':subcoll_id, 'id_coll':subcoll_coll})
                subcoll_oldcode = self.fetch('one')
                if subcoll_oldcode == subcoll_code:
                    self.execute('update_subcoll',{'subcoll_id':subcoll_id,'subcoll_coll':subcoll_coll,'subcoll_code':subcoll_code.decode('utf8'),'subcoll_name':subcoll_name})
                    self.execute('update_sys_config',{'subcoll_id':subcoll_id,'date_input_mask':subcoll_inputmask,'date_output_mask':subcoll_outputmask,'label_lang':subcoll_lang})
                else: new_subcoll = False
        # Update data languages
        self.execute('delete_subcoll_data_lang', {'id_subcoll': subcoll_id})
        if (isinstance(self.form['util_subcoll_data_lang'], list)):
            i = 1
            for subcoll_data_lang in self.form['util_subcoll_data_lang']:
                self.execute('insert_sys_data_lang', {'id_subcoll': subcoll_id, 'data_lang': subcoll_data_lang.value, 'lang_index': str(i)})
                i += 1
        else:
            subcoll_data_lang = str(self.form['util_subcoll_data_lang'].value)
            self.execute('insert_sys_data_lang', {'id_subcoll': subcoll_id, 'data_lang': subcoll_data_lang, 'lang_index': "1"})

        #Return feedback value
        if not new_subcoll:
          self.session.data['feedback'] = -5
        else:
          self.session.data['feedback'] = 1
        self.session.save()

    def saveColl(self):
        #Read form data
        coll_id = ''
        if ('util_coll_id' in self.form): #Empty fields are discarded automatically
          coll_id = str(self.form['util_coll_id'].value)
        coll_base = str(self.form['util_coll_base'].value)
        coll_code = str(self.form['util_coll_code'].value)
        coll_name = ''
        if ('util_coll_name' in self.form): #Empty fields are discarded automatically
          coll_name = str(self.form['util_coll_name'].value).decode('utf8')
        coll_logo = '' #empty string = default image is used
        valid_logo = True
        if (self.form['util_coll_logo'].value != ''): #An image has been sent
          doc_file = self.form['util_coll_logo'].file
          logo = []
          if doc_file is not None:
            while True:
              chunk = doc_file.read()
              if not chunk: break
              logo.append(chunk)
          #Escape NUL (0x00) and ' (simple quote) in order to insert correctly in SQLite
          coll_logo = "".join(logo)
          import base64,imghdr
          img_type = imghdr.what('',coll_logo) #Read Image Header and see if it is a valid image or not
          if img_type is None:
            coll_logo = '' #Use default image
            valid_logo = False
          else:
            coll_logo = base64.encodestring(coll_logo)
        else:
            self.execute('get_coll_logo',{'id_coll':coll_id})
            coll_logo = self.fetch('one')
        new_coll = True
        if coll_id == '': #New Collection
            self.execute('count_coll',{'coll_code':coll_code})
            if self.fetch('one') < 1:
                self.execute('insert_coll',{'coll_base':coll_base,'coll_code':coll_code,'coll_name':coll_name,'coll_logo':coll_logo},raw_mode=True)
            else: new_coll = False
        else: #Edited Collection
            self.execute('update_coll',{'coll_id':coll_id,'coll_base':coll_base,'coll_code':coll_code,'coll_name':coll_name,'coll_logo':coll_logo},raw_mode=True)
            #If Collection changed is the same one user is in, then change session data
            if int(coll_id) == int(self.session.data['id_coll']):
              self.session.data['coll_name'] = coll_code
        #Return feedback value
        if not new_coll:
          self.session.data['feedback'] = -6
          if not valid_logo:
              self.session.data['feedback'] = -3
        else:
          self.session.data['feedback'] = 1
        self.session.save()

    def saveDB(self):
        #Read form data
        #database
        base_id = ''
        if ('util_base_id' in self.form): #Empty fields are discarded automatically
          base_id = str(self.form['util_base_id'].value)
        base_dbms = str(self.form['util_base_dbms'].value)
        base_host = str(self.form['util_base_host'].value)
        base_port = str(self.form['util_base_port'].value)
        base_name = str(self.form['util_base_name'].value)
        base_user = ''
        if ('util_base_user' in self.form): #Empty fields are discarded automatically
          base_user = str(self.form['util_base_user'].value)
        base_pwd = ''
        if ('util_base_pwd' in self.form): #Empty fields are discarded automatically
          base_pwd = str(self.form['util_base_pwd'].value)
        #tracebility
        base_tracebility_id = ''
        if ('util_base_tracebility_id' in self.form): #Empty fields are discarded automatically
          base_tracebility_id = str(self.form['util_base_tracebility_id'].value)
        base_tracebility_dbms = str(self.form['util_base_tracebility_dbms'].value)
        base_tracebility_host = str(self.form['util_base_tracebility_host'].value)
        base_tracebility_port = str(self.form['util_base_tracebility_port'].value)
        base_tracebility_name = str(self.form['util_base_tracebility_name'].value)
        base_tracebility_user = ''
        if ('util_base_tracebility_user' in self.form): #Empty fields are discarded automatically
          base_tracebility_user = str(self.form['util_base_tracebility_user'].value)
        base_tracebility_pwd = ''
        if ('util_base_tracebility_pwd' in self.form): #Empty fields are discarded automatically
          base_tracebility_pwd = str(self.form['util_base_tracebility_pwd'].value)

        #Connect in instance
        import MySQLdb as mysql
        try:
            connection = mysql.connect(base_host, base_user, base_pwd, base_name, int(base_port), use_unicode=True, charset='utf8')
            connection.close()

            if base_id == '': #New base
                self.execute('get_all_users')
                list_users = self.fetch('all')

                base_descr = {}
                base_descr['host'] = base_host
                base_descr['port'] = int(base_port)
                base_descr['db_name'] = base_name
                base_descr['user'] = base_user
                base_descr['pwd'] = base_pwd
                base_descr['dbms_name'] = 'mysql'
                base_descr['dbms'] = 'mysql'

                base_conn = dbConnection(base_descr=base_descr)
                for user in list_users:
                    # Do not create the default user, the migration script do it
                    if int(user['id_user']) == 1:
                        continue

                    base_conn.execute('insert_role',{
                                                     'role_name':user['name'],
                                                     'role_descr':'',
                                                     'role_type':'user',
                                                     })
                    base_conn.execute('last_insert_id')
                    id_role = base_conn.fetch('one')
                    base_conn.execute('insert_user_role',{
                                                          'id_user':user['id_user'],
                                                          'id_role':1,
                                                          })
                    base_conn.execute('insert_user_role',{
                                                          'id_user':user['id_user'],
                                                          'id_role':id_role,
                                                          })
                base_conn.connect.commit()

                self.execute('insert_base',{'dbms_id':base_dbms,'host':base_host,'port':base_port,'db_name':base_name.decode('utf8'),'base_pwd':base_pwd,'base_user':base_user.decode('utf8')})
                self.execute('last_insert_id')
                id_base_new = self.fetch('one')
                self.execute('insert_base_log',{'id_base':id_base_new,'dbms_id':base_tracebility_dbms,'host':base_tracebility_host,'port':base_tracebility_port,'db_name':base_tracebility_name.decode('utf8'),'base_pwd':base_tracebility_pwd,'base_user':base_tracebility_user.decode('utf8')})
            else: #Edited base
                self.execute('update_base',{'base_id':base_id,'dbms_id':base_dbms,'host':base_host,'port':base_port,'db_name':base_name.decode('utf8'),'base_pwd':base_pwd,'base_user':base_user.decode('utf8')})
                self.execute('update_base_log',{'base_id_log':base_tracebility_id,'dbms_id':base_tracebility_dbms,'host':base_tracebility_host,'port':base_tracebility_port,'db_name':base_tracebility_name.decode('utf8'),'base_pwd':base_tracebility_pwd,'base_user':base_tracebility_user.decode('utf8')})
            self.session.data['feedback'] = 1
            self.session.save()
        except mysql.Error as e:
            if (e.args[0] == 1045): #Error - Access Denied on MySQL database
                self.session.data['feedback'] = -10
            elif (e.args[0] == 1044): #Error - Access denied for user 'sicol'@'%' to database
                self.session.data['feedback'] = -9
            elif (e.args[0] == 2003): #Error - MySQL database has not been activated
                self.session.data['feedback'] = -8
            else:
                self.session.data['feedback'] = -7
            self.session.save()
        except:
            self.session.data['feedback'] = -11
            self.session.save()

    def saveUser(self):
        #emulates a distributed transaction
        bases_to_commit = []

        #Read form data
        user_id = ''
        if ('util_user_id' in self.form): #Empty fields are discarded automatically
          user_id = str(self.form['util_user_id'].value)
        user_login = str(self.form['util_user_login'].value)
        user_pwd = ''
        if ('util_user_pwd' in self.form and self.form['util_user_pwd'].value != ''): #Empty fields are discarded automatically
          #Hide user password
          try:
              from hashlib import md5 as new_md5
          except ImportError:
              from md5 import new as new_md5
          user_pwd = new_md5(str(self.form['util_user_pwd'].value)).hexdigest()
        user_name = str(self.form['util_user_name'].value).replace("'", "''")
        user_comments = ''
        if ('util_user_comments' in self.form): #Empty fields are discarded automatically
          user_comments = str(self.form['util_user_comments'].value)

        #Get all bases from all collections and subcollections
        self.dbconnection.execute('get_all_dbs')
        bases = self.dbconnection.fetch('all')

        if user_id == '': #New user
          #Inserts user on sqlite
          self.execute('insert_user',{'login':user_login.decode('utf8'),'name':user_name.decode("utf8"),'pwd':user_pwd,'comments':user_comments.decode("utf8")})
          #Retrieves the id
          user_id = self.cursor.lastrowid
          
          #brk(host="localhost", port=9000)

          try:
              for base in bases:
                  #Connects to the datababase of each subcollection
                  base_db = dbConnection(base_descr=base)
                  #self.logger.debug('Inserting group (role \'user\') for user %s-%s on base %s' % (user_id, user_name, base['db_name']))

                  #Associate user to 'all' group (id_role = 1, ALWAYS - it is a hardcoded group)
                  base_db.execute('insert_user_role',{'id_user':user_id,'id_role':1})
                  #Create 'user' group and associate him to it
                  base_db.execute('insert_role', {'role_name': user_name,'role_type':'user','role_descr':''})
                  base_db.execute('last_insert_id')
                  this_role_id = base_db.fetch('one')
                  base_db.execute('insert_user_role',{'id_user':user_id,'id_role':this_role_id})
                  #self.logger.debug("Appending base %s for commit insertion" % (base['db_name']))
                  bases_to_commit.append(base_db)
                  #base_db.connect.commit()

              self.db.execute('get_user_group',{'id_user':user_id})
              role_id = self.db.fetch('one')
              #self.logger.debug('Role id: %s' % (role_id))

              #Grant permission to create to all areas
              self.db.execute('grant_role_create_all_areas',{'id_role':role_id})

          except Exception as e:
              #In case of a problem on the insertion of the user on one of the
              #databases, we delete it from SQLite and rollback the insertion
              self.execute('delete_user',{'id_user':str(user_id)})
              for base in bases_to_commit:
                  base.connect.rollback()

              raise e

        else: #Edited user
          self.execute('get_user_name',{'id_user':user_id})
          old_name = self.fetch('one').encode('utf8')
          if old_name != user_name: #Update related group name
            if old_name == self.session.data['user_name'].encode('utf8'): #User changed his own name
              self.session.data['user_name'] = user_name
              self.session.save()

            for base in bases:
                #Connects to the datababase of each subcollection
                base_db = dbConnection(base_descr=base)
                #self.logger.debug('Updating group (role \'user\') for user %s-%s on base %s' % (user_id, user_name, base['db_name']))

                #Updates the user group (role with type 'user') name
                base_db.execute('get_user_group',{'id_user':user_id})
                group_user = base_db.fetch('one')
                base_db.execute('update_user_group_name',{'id_role':group_user,'name':user_name})
                #self.logger.debug("Appending base %s for commit editing" % (base['db_name']))
                bases_to_commit.append(base_db)
                #base_db.connect.commit()

          if user_pwd == '': #Keep previous password
            self.execute('update_user_no_pwd',{'id_user':user_id,'login':user_login.decode("utf8"),'name':user_name.decode("utf8"),'comments':user_comments.decode("utf8")})
          else: #Change user password
            self.execute('update_user',{'id_user':user_id,'login':user_login.decode("utf8"),'name':user_name.decode("utf8"),'pwd':user_pwd,'comments':user_comments.decode("utf8")})

        # commits all bases
        for base in bases_to_commit:
            base.connect.commit()

        #Manage user groups
        #Delete all previous groups
        self.db.execute('delete_user_common_roles',{'id_user':user_id})

        #Get all existing groups (rules where type != 'user' or 'group','level')
        self.db.execute('get_all_common_roles')
        list_roles = self.db.fetch('all')
        js_list = []

        for role in list_roles:
          #name format: 'userrole_' + <role_id>
          js_list.append("userrole_"+str(role['id_role']))

        #Insert new user-group configuration
        for item in js_list:
          if item in self.form:
            role_info = item.split("_") #userrole_<role>
            role_id = role_info[1]
            self.db.execute('insert_user_role',{'id_user':user_id,'id_role':role_id})

        self.db.connect.commit()

        #Manage user access
        self.db.execute('get_user_group',{'id_user':user_id})
        user_role_id = self.db.fetch('one')
        self.db.execute('get_admins')
        is_admin = self.db.fetch('rows')
        if int(user_id) in is_admin:
          is_admin = True
        else:
          is_admin = False

        #Delete all previous accesses
        self.execute('delete_user_access',{'id_user':user_id})
        if is_admin:
          #Administrator has access to all existing subcollections
          self.execute('set_all_accesses',{'id_user':user_id})
        else:
          #Get all existing collections
          self.execute('get_all_colls')
          list_colls = self.fetch('all')
          js_list = []
          for coll in list_colls:
            #name format: 'user_' + <coll_id> + '_' + <subcoll_id>
            js_list.append(str("user_"+str(coll['coll_id'])+"_"+str(coll['subcoll_id'])))

          #Insert new access configuration
          for item in js_list:
            if item in self.form:
              coll_info = item.split("_") #user_<coll>_<subcoll>. E.g: user_1_1
              coll_id = coll_info[1]
              subcoll_id = coll_info[2]
              self.execute('insert_access',{'id_user':user_id,'id_subcoll':subcoll_id})

        #Manage area access
        #Delete all previous area accesses of this group
        self.db.execute('delete_area_access',{'role_id':user_role_id})

        #Get all existing areas
        self.db.execute('get_all_areas')
        list_areas = self.db.fetch('all')
        js_areadel_list = []
        js_areacreate_list = []
        js_area_list = []
        for area in list_areas:
           js_areadel_list.append("userareadel_"+str(area['id_area']))
           js_areacreate_list.append("userareacreate_"+str(area['id_area']))
           js_area_list.append(str(area['id_area']))

        #Insert new area access configuration
        for item in js_area_list:
           areadel = 'n'
           areacreate = 'n'
           if 'userareadel_'+item in self.form:
             areadel = 'y'
           if 'userareacreate_'+item in self.form:
             areacreate = 'y'
           self.db.execute('insert_area_access',{'id_area':item,'id_role':user_role_id,'allow_delete':areadel,'allow_create':areacreate})

        # commits main
        self.db.connect.commit()
        self.session.data['feedback'] = 1
        self.session.save()

    def readForm(self):
        '''
        Reads form submission
        '''
        #Get Command Type
        util_type = str(self.form['util_type'].value)
        #Delete Command
        if util_type == 'user_delete': return  self.deleteUser()
        elif util_type == 'subcoll_delete': return  self.deleteSubcoll()
        elif util_type == 'coll_delete': return  self.deleteColl()
        elif util_type == 'dbs_delete': return  self.deleteDB()
        elif util_type == 'role_delete': return  self.deleteRole()
        elif util_type == 'division_delete': return self.deleteDivision()
        #Save Command
        elif util_type == 'configxml': return  self.saveConfigXML()
        elif util_type == 'role': return  self.saveRole()
        elif util_type == 'coll': return  self.saveColl()
        elif util_type == 'subcoll': return  self.saveSubcoll()
        elif util_type == 'combo': return  self.saveCombo()
        elif util_type == 'division': return self.saveDivision()
        elif util_type == 'dbs': return  self.saveDB()
        elif util_type == 'user': return self.saveUser()
        elif util_type == 'template': return self.saveSubcollTemplate()

    def loadJSData(self,data):
        '''
        Load Javascript global data
        '''
        #Display global varibles
        data['global_js'] = '''//Global variables
        var _current_id_user = %s;
        var _current_id_coll = %s;
        var _current_id_subcoll = %s;
        var _current_roles = new Array();
        ''' % (str(self.session.data['id_user']),str(self.session.data['id_coll']),str(self.session.data['id_subcoll']))
        #Get all existing collections
        self.execute('get_all_colls')
        list_colls = self.fetch('all')
        data['user_access'] = ''
        js_list = []
        for coll in list_colls:
          #checkbox name format: 'user_' + <coll_id> + '_' + <subcoll_id>
          if coll['subcoll_id'] == '': continue #Do not show collections without subcollections
          #if coll['subcoll_id']
          data['user_access'] += '<input type="checkbox" name="user_%s_%s" id="user_%s_%s" />%s - %s <br />' % \
                                     (str(coll['coll_id']),str(coll['subcoll_id']),
                                      str(coll['coll_id']),str(coll['subcoll_id']),
                                      str(coll['coll_code']),str(coll['subcoll_code'].encode('utf8')))
          js_list.append(str("user_"+str(coll['coll_id'])+"_"+str(coll['subcoll_id'])))
        #Get all existing groups (where types in ('group','level'))
        self.db.execute('get_all_common_roles')
        list_common_roles = self.db.fetch('all')
        data['user_roles'] = ''
        js_roles_list = []
        for role in list_common_roles:
          #checkbox name format: 'userrole_' + <role_id>
          data['user_roles'] += '<input onclick="javascript: return do_check(this);" type="checkbox" name="userrole_%s" id="userrole_%s" />(%s) %s <br />' % \
                                     (str(role['id_role']),str(role['id_role']),
                                      str(role['type']),role['name'])
          js_roles_list.append("userrole_"+str(role['id_role']))
        #Group areas
        self.db.execute('get_all_areas')
        list_areas = self.db.fetch('all')
        js_areadel_list = []
        js_areacreate_list = []
        js_userareadel_list = []
        js_userareacreate_list = []
        for area in list_areas:
           #checkbox name format: 'area_' + <id_area>
           area_description = area['description']
           if (area_description != ''): #Make database labels translatable
              if area_description == 'Taxa Tab': area_description = _("plural|Species")
              elif area_description == 'Strains Tab': area_description = _("Strains")
              elif area_description == 'People Tab': area_description = _("People")
              elif area_description == 'Institutions Tab': area_description = _("Institutions")
              elif area_description == 'Documents Tab': area_description = _("Documents")
              elif area_description == 'References Tab': area_description = _("References")
              elif area_description == 'Preservation Tab': area_description = _("Preservation")
              elif area_description == 'Distribution Tab': area_description = _("Distribution")
           data['role_areas'] += '<tr>\n\t<td>%s</td>\n\t<td><input type="checkbox" name="areadel_%s" id="areadel_%s" /></td>\n\t<td><input checked="checked" type="checkbox" name="areacreate_%s" id="areacreate_%s" /></td>\n</tr>\n' % \
                                     (area_description,str(area['id_area']),str(area['id_area']),str(area['id_area']),str(area['id_area']))
           data['user_areas'] += '<tr>\n\t<td>%s</td>\n\t<td><input type="checkbox" name="userareadel_%s" id="userareadel_%s" /></td>\n\t<td><input checked="checked" type="checkbox" name="userareacreate_%s" id="userareacreate_%s" /></td>\n</tr>\n' % \
                                     (area_description,str(area['id_area']),str(area['id_area']),str(area['id_area']),str(area['id_area']))
           js_areadel_list.append("areadel_"+str(area['id_area']))
           js_areacreate_list.append("areacreate_"+str(area['id_area']))
           js_userareadel_list.append("userareadel_"+str(area['id_area']))
           js_userareacreate_list.append("userareacreate_"+str(area['id_area']))
        #Create a bridge in order to let javascript access this kind of info
        data['js_list'] = '<script type="text/javascript">'
        if js_list == []:
          data['js_list'] += 'all_colls = new Array();'
        else:
          data['js_list'] += 'all_colls = new Array("'+'","'.join(js_list)+'");'
        if js_roles_list == []:
          data['js_list'] += 'all_roles = new Array();'
        else:
          data['js_list'] += 'all_roles = new Array("'+'","'.join(js_roles_list)+'");'
        if js_areadel_list == []:
          data['js_list'] += 'alldel_areas = new Array();'
        else:
          data['js_list'] += 'alldel_areas = new Array("'+'","'.join(js_areadel_list)+'");'
        if js_areacreate_list == []:
          data['js_list'] += 'allcreate_areas = new Array();'
        else:
          data['js_list'] += 'allcreate_areas = new Array("'+'","'.join(js_areacreate_list)+'");'
        if js_userareadel_list == []:
          data['js_list'] += 'useralldel_areas = new Array();'
        else:
          data['js_list'] += 'useralldel_areas = new Array("'+'","'.join(js_userareadel_list)+'");'
        if js_userareacreate_list == []:
          data['js_list'] += 'userallcreate_areas = new Array();'
        else:
          data['js_list'] += 'userallcreate_areas = new Array("'+'","'.join(js_userareacreate_list)+'");'
        data['js_list'] += '</script>'

    def loadUserTab(self,data):
        '''
        Load User Tab
        '''
        #List all existing users
        #Create row template
        user_table = '<tr %%s">\
            <td class="">%s</td>\
            <td class="">%s</td>\
            <td class="">%s</td>\
          </tr>'
        #SELECT id_user,login,pwd,name,comments
        self.execute('get_all_users')
        list_users = self.fetch('all')
        for user in list_users:
          #Table data
          line = user_table % (user['login'].encode("utf8"),user['name'].encode("utf8"),user['comments'].encode("utf8"))
          #Javascript data
          str_user_colls = []
          self.execute('get_user_colls',{'id_user':str(user['id_user'])})
          user_colls = self.fetch('all')
          for user_coll in user_colls:
            str_user_colls.append(str('user_'+str(user_coll['id_coll'])+'_'+str(user_coll['id_subcoll'])))
          str_user_roles = []
          str_roles = []
          self.db.execute('get_user_roles',{'id_user':str(user['id_user'])})
          user_roles = self.db.fetch('rows')
          for user_role in user_roles:
            str_user_roles.append('userrole_'+str(user_role))
            str_roles.append(str(user_role))
          if str_roles == []:
            data['global_js'] += '\t_current_roles["%s"] = %s;\n' % (user['id_user'],"''")
          else:
            data['global_js'] += '\t_current_roles["%s"] = %s;\n' % (user['id_user'],",".join(str_roles))
          #Javascript data for area access
          self.db.execute('get_user_group',{'id_user':str(user['id_user'])})
          user_role_id = self.db.fetch('one')
          str_areas = []
          self.db.execute('get_area_access',{'id_role':user_role_id})
          areas = self.db.fetch('all')
          for area in areas:
            if (area['allow_delete'] == 'y'):
               str_areas.append('userareadel_'+str(area['id_area']))
            if (area['allow_create'] == 'y'):
               str_areas.append('userareacreate_'+str(area['id_area']))
          jsparam = "onclick=\"edit_user('%s','%s','%s','%s','%s','%s','%s')\"" % (str(user['id_user']),user['login'].encode("utf8"),user['name'].encode("utf8"),user['comments'].encode("utf8"),",".join(str_user_colls),",".join(str_user_roles),",".join(str_areas))
          line = line % jsparam
          data['user_table'] += line.decode("utf8")

    def loadGroupTab(self,data):
        '''
        Load Group Tab
        '''
        #Create row template
        role_table = '<tr %%s>\
             <td>%s</td>\
             <td>%s</td>\
             <td>%s</td>\
           </tr>'
        self.db.execute('get_all_roles')
        list_roles = self.db.fetch('all')
        for role in list_roles:
           #Table data
           role_type = str(role['type'])
           if (role_type == 'all'): continue #Do not show the "all" type
           elif (role_type == 'group'): role_type = _("Group")
           elif (role_type == 'user'): continue #Do not show the "user" type
           elif (role_type == 'level'): role_type = _("Level ")
           line = role_table % (role['name'],role['description'],role_type)
           #Javascript data
           str_areas = []
           self.db.execute('get_area_access',{'id_role':str(role['id_role'])})
           areas = self.db.fetch('all')
           for area in areas:
             if (area['allow_delete'] == 'y'):
                str_areas.append('areadel_'+str(area['id_area']))
             if (area['allow_create'] == 'y'):
                str_areas.append('areacreate_'+str(area['id_area']))
           jsparam = ''
           if role['name'].encode('utf8') == 'Administrator' or role['name'].encode('utf8') == 'Curador': #Prevent Administrator and Curador group to be edited
             jsparam = "onclick=\"alert('%s');\"" % _("Unable to edit special groups")
             line = line.replace('<tr ','<tr class="non_editable" ')
           else:
             jsparam = "onclick=\"edit_group('%s','%s','%s','%s','%s','%s')\"" % (
                  str(role['id_role']),role['name'],role['description'],str(role['type']),
                  ",".join(str_areas),self.getdata.group_members(str(role['id_role'])))
           line = line % jsparam
           data['role_table'] += line
        #Create possible members
        data['group_possible_members'] = self.getdata.possible_members()

    def loadCollTab(self,data):
        '''
        Load Collection Tab
        '''
        #Create db list
        self.execute('get_all_dbs')
        list_dbs = self.fetch('all')
        data['coll_list'] = ''
        for onedb in list_dbs:
          data['coll_list'] += '<option value="%s">%s</option>' % (str(onedb['base_id']),onedb['db_name'].encode('utf8')+" - "+str(onedb['host'])+":"+str(onedb['port'])+" ("+str(onedb['dbms_name'])+")")
        #Create row template
        coll_table = '<tr onclick="edit_coll(%%s)">\
             <td class="">%s</td>\
             <td class="">%s</td>\
             <td class="">%s</td>\
           </tr>'
        self.execute('get_all_colls_only')
        list_colls = self.fetch('all')
        for coll in list_colls:
           #Table data
           line = coll_table % (str(coll['dbms_name']),str(coll['coll_code']),coll['coll_name'])
           has_logo = '0' #False
           if coll['coll_logo'] != '':
            has_logo = '1' #True
           jsparam = "'%s','%s','%s','%s','%s'" % (str(coll['coll_id']),str(coll['coll_base']),str(coll['coll_code']),coll['coll_name'],has_logo)
           line = line % jsparam
           data['coll_table'] += line

    def loadSubCollTab(self,data):
        '''
        Load Subcollection Tab
        '''
        #Create coll list
        self.execute('get_all_colls_only')
        list_colls = self.fetch('all')
        data['subcoll_list'] = ''
        for coll in list_colls:
          coll_info = str(coll['coll_code'])
          if coll['coll_name'] != '':
            coll_info += ' - ' + coll['coll_name']
          data['subcoll_list'] += '<option value="%s">%s</option>' % (str(coll['coll_id']),coll_info)
        #Create possible data_langs array
        data['possible_data_langs'] = self.getdata.possible_data_langs()
        #Create Language list
        data['languages'] = self.getdata.preferences('default')
        #Create row template
        subcoll_table = '<tr onclick="edit_subcoll(%%s)">\
             <td class="">%s</td>\
             <td class="">%s</td>\
             <td class="">%s</td>\
           </tr>'
        self.execute('get_all_subcolls')
        list_subcolls = self.fetch('all')
        for subcoll in list_subcolls:
           #Table data
           subcoll_data_langs = self.getdata.subcoll_data_langs(str(subcoll['subcoll_id']))
           coll_info = str(subcoll['coll_code'])
           if subcoll['coll_name'] != '':
             coll_info += ' - '+ subcoll['coll_name']
           line = subcoll_table % (coll_info,subcoll['subcoll_code'],subcoll['subcoll_name'])
           jsparam = "'%s','%s','%s','%s','%s','%s','%s',%s" % (
                                          str(subcoll['subcoll_id']),
                                          str(subcoll['coll_id']),
                                          subcoll['subcoll_code'],
                                          subcoll['subcoll_name'],
                                          str(subcoll['input']),
                                          str(subcoll['output']),
                                          str(subcoll['lang']),
                                          subcoll_data_langs
                                          )
           line = line % jsparam
           data['subcoll_table'] += line

    def loadComboTab(self,data,id_lang):
        '''
        Load Subcollection Combo Configuration Tab
        '''
        #Create input field in many languages
        data_langs = self.getdata.data_lang_list()
        data['combo_str_type_lang'] = []
        data['combo_dep_reason_lang'] = []
        data['combo_preservation_method_lang'] = []
        data['combo_test_group_lang'] = []
        for data_lang in data_langs:
           id_str_type = 'combo_str_type_'+str(data_lang['code'])
           id_dep_reason = 'combo_dep_reason_'+str(data_lang['code'])
           id_preservation_method = 'combo_preservation_method_'+str(data_lang['code'])
           id_unit_measure = 'combo_unit_measure_'+str(data_lang['code'])
           id_test_group = 'combo_test_group_'+str(data_lang['code'])
           data['combo_str_type_lang'].append('<li><label>' + data_lang['lang'] + ' / ' + data_lang['lang_en'] + ' (' + data_lang['code'] + ')' + '</label><br />')
           data['combo_str_type_lang'].append('<input type="text" name="'+id_str_type+'" maxlength="15" id="'+id_str_type+'" style="margin-bottom: 3px" /><br /></li>')
           data['combo_dep_reason_lang'].append('<li><label>' + data_lang['lang'] + ' / ' + data_lang['lang_en'] + ' (' + data_lang['code'] + ')' + '</label><br />')
           data['combo_dep_reason_lang'].append('<input type="text" name="'+id_dep_reason+'" maxlength="25" id="'+id_dep_reason+'" style="margin-bottom: 3px" /><br /></li>')
           data['combo_preservation_method_lang'].append('<li><label>' + data_lang['lang'] + ' / ' + data_lang['lang_en'] + ' (' + data_lang['code'] + ')' + '</label><br />')
           data['combo_preservation_method_lang'].append('<input type="text" name="'+id_preservation_method+'" maxlength="100" id="'+id_preservation_method+'" style="margin-bottom: 3px" />')
           data['combo_preservation_method_lang'].append('&nbsp;[ <input type="text" name="'+id_unit_measure+'" maxlength="100" id="'+id_unit_measure+'" title="'+_("Unit of Measure")+'" alt="'+_("Unit of Measure")+'" style="margin-bottom: 3px; width: 100px;" /> ]<br /></li>')
           data['combo_test_group_lang'].append('<li><label>' + data_lang['lang'] + ' / ' + data_lang['lang_en'] + ' (' + data_lang['code'] + ')' + '</label><br />')
           data['combo_test_group_lang'].append('<input type="text" name="'+id_test_group+'" maxlength="100" id="'+id_test_group+'" style="margin-bottom: 3px" /><br /></li>')
        data['combo_str_type_lang'] = "\n".join(data['combo_str_type_lang'])
        data['combo_dep_reason_lang'] = "\n".join(data['combo_dep_reason_lang'])
        data['combo_preservation_method_lang'] = "\n".join(data['combo_preservation_method_lang'])
        data['combo_test_group_lang'] = "\n".join(data['combo_test_group_lang'])
        #Create possible str_type array
        data['possible_taxon_group'] = self.getdata.possible_combo_values('taxon_group',id_lang)
        data['possible_str_type'] = self.getdata.possible_combo_values('str_type',id_lang)
        data['possible_dep_reason'] = self.getdata.possible_combo_values('dep_reason',id_lang)
        data['possible_preservation_method'] = self.getdata.possible_combo_values('preservation_method',id_lang)
        data['possible_test_group'] = self.getdata.possible_combo_values('test_group',id_lang)


        self.execute('get_all_subcolls')
        list_subcolls = self.fetch('all')
        for subcoll in list_subcolls:
            if str(subcoll['subcoll_id']) == str(self.session.data['id_subcoll']):
                combo_taxon_group = self.getdata.subcoll_combo_config(str(subcoll['subcoll_id']),'taxon_group')
                combo_str_type = self.getdata.subcoll_combo_config(str(subcoll['subcoll_id']),'str_type')
                combo_dep_reason = self.getdata.subcoll_combo_config(str(subcoll['subcoll_id']),'dep_reason')
                combo_preservation_method = self.getdata.subcoll_combo_config(str(subcoll['subcoll_id']),'preservation_method')
                combo_test_group = self.getdata.subcoll_combo_config(str(subcoll['subcoll_id']),'test_group')
                coll_info = str(subcoll['coll_code'])
                jsparam = "'%s','%s',%s,%s,%s,%s,%s" % (str(subcoll['subcoll_id']),coll_info + ' - ' + subcoll['subcoll_code'],
                                         combo_taxon_group,
                                         combo_str_type,
                                         combo_dep_reason,
                                         combo_preservation_method,
                                         combo_test_group
                                        )
                data['select_subcoll_js'] = """
                    <script type="text/javascript">
                    function startComboSettings(showButtons) {
                        var ignoreButtons = true;
                        if (showButtons == 1) {
                            ignoreButtons = false;
                        }
                        edit_combo(%s, false, ignoreButtons);
                    }
                    addEvent(window, 'load', startComboSettings);
                    </script>""" % jsparam


    def loadReportTemplatesTab(self, data):
        '''
        Load Templates Tab
        '''
        #brk(host="localhost", port=9000)
        
        import base64
        
        self.execute('get_subcoll_templates', {'id_subcoll': self.session.data['id_subcoll']})
        list_templates = self.fetch('all')
        data['value_header_template'] = base64.b64decode(list_templates[0]['header'])
        data['value_footer_template'] = base64.b64decode(list_templates[0]['footer'])
        data['value_css_template'] =    base64.b64decode(list_templates[0]['styles'])
        
        data['label_subcoll_select'] = label_dict['label_Configuration_Templates_Subcollection']
        
        
        data['label_header_template'] = label_dict['label_Rep_header_template']
        data['label_footer_template'] = label_dict['label_Rep_footer_template']
        data['label_css_template'] = label_dict['label_Rep_css_template']

    def loadDivisionTab(self,data):
        '''
        Load Division Tab
        '''

        from .strain_formatter import StrainFormatter
        s = StrainFormatter(self.cookie_value)
        divisions = s.get_division_list(self.session.data['id_subcoll'])

        html_tr = """<tr onclick='edit_division(%s, "%s", "%s");'>
            <td class="">%s</td>
            <td class="">%s</td>
        </tr>"""

        html_table = []
        for division in divisions:
            html_table.append(html_tr % (division['id_division'], division['division'], division['pattern'],
                                         division['division'],
                                         division['pattern']))

        data['division_table'] = "\n".join(html_table)

    def loadDBTab(self,data):
        '''
        Load Database Tab
        '''
        #Create dbms list
        self.execute('get_all_dbms')
        list_dbms = self.fetch('all')
        for dbms in list_dbms:
          data['dbms_list'] += '<option value="%s">%s</option>' % (str(dbms['id_dbms']),str(dbms['name']))
        #Create row template
        db_table = '<tr %%s>\
            <td class="">%s</td>\
            <td class="">%s</td>\
            <td class="">%s</td>\
            <td class="">%s</td>\
            <td class="">%s</td>\
            <td class="">%s</td>\
          </tr>'
        self.execute('get_all_dbs')
        list_dbs = self.fetch('all')
        
        #brk(host="localhost", port=9000)

        for onedb in list_dbs:
          #Table data
          line = db_table % (str(onedb['dbms_name']),str(onedb['host']),str(onedb['port']),
                             onedb['db_name'],onedb['user'],str(onedb['pwd'])
                            )
          if (self.session.data['dbms'] == onedb['dbms_name']
              and self.session.data['db_host'] == onedb['host']
              and self.session.data['db_port'] == onedb['port']
              and self.session.data['db_name'] == onedb['db_name']
              and self.session.data['db_user'] == onedb['user']
              and self.session.data['db_pwd'] == onedb['pwd']):
            jsparam = "onclick=\"alert('%s')\"" % _("Unable to edit current database.")
          else:
            self.execute('get_all_dbs_log',{'id_base':str(onedb['base_id'])})
            tracebility_onedb = self.fetch('all')
            if tracebility_onedb:
                tracebility_onedb = tracebility_onedb[0]
                jsparam = "onclick=\"edit_base('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')\"" % (str(onedb['base_id']),str(onedb['dbms_id']),str(onedb['host']),str(onedb['port']),onedb['db_name'],onedb['user'],str(onedb['pwd']),str(tracebility_onedb['base_id']),str(tracebility_onedb['dbms_id']),str(tracebility_onedb['host']),str(tracebility_onedb['port']),tracebility_onedb['db_name'],tracebility_onedb['user'],str(tracebility_onedb['pwd']))
            else:
                jsparam = "onclick=\"alert('%s')\"" % _("Unable to find the log database of this database.")
          line = line % jsparam
          data['dbs_table'] += line

    def loadConfigTab(self,data):
        '''
        Load Config.xml configuration Tab
        '''
        #Possible start pages
        data['startpage'] = self.getdata.possible_start_pages()
        #Create possible data_langs array
        data['config_possible_data_langs'] = self.getdata.possible_data_langs('config')
        #Create Language list
        self.db.execute('get_lang_by_code',{'code':self.g.get_config('label_lang')})
        data['config_languages'] = self.getdata.preferences(self.db.fetch('one'),False)
        #Create js call to initializa field values
        data['js_init_config'] = "<script type='text/javascript'>init_config_fields('%s','%s','%s','%s','%s','%s');</script>" % (
                                      self.g.get_config('index_url'),str(self.g.get_config('root_dir')).replace("\\","\\\\"),
                                      self.g.get_config('date_input_mask'),self.g.get_config('date_output_mask'),
                                      self.g.get_config('data_lang'),self.g.get_config('upload_limit'))


    def ConvertStrUnicode(self, valor):
        retorno = '';
        if isinstance(valor, (int, float)):
            return str(valor)
            
        if (isinstance(valor, str) == False):
            retorno = str(valor).decode("utf8")
        else:
            retorno = valor
        
        return retorno
    
   
