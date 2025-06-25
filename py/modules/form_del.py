#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#python imports
from sys import exit
from os import remove, path
try:
    from hashlib import sha1 as new_sha
except ImportError:
    from sha import new as new_sha
from urllib.parse import urljoin

#project imports
from .session import Session
from .dbconnection import dbConnection
from .general import General
from .log import Log
#from dbgp.client import brk

class Delete(object):

    g = General()
    root_dir = g.get_config('root_dir')
    doc_dir = path.join(root_dir, 'doc_file')
    index_url = g.get_config('index_url')

    def __init__(self, cookie_value, form):
        #Load session
        self.session = Session()
        self.session.load(cookie_value)
        self.cookie_value = cookie_value

        #Define global variables
        self.form = form
        self.html = {'message':'','submenu':''}

        #Define Database
        self.dbconnection = dbConnection(cookie_value)
        self.execute = self.dbconnection.execute
        self.fetch = self.dbconnection.fetch
        self.cursor = self.dbconnection.cursor

        #brk(host="localhost", port=9000)
        #Define LOG Database
        dict_db_log = {}
        dict_db_log = self.g.get_log_db({'id_base':self.session.data['id_base']})

        self.db_log = dbConnection(base_descr = dict_db_log)
        self.execute_log = self.db_log.execute

        self.l = Log(cookie_value, self.dbconnection)

        #Define Data Dict
        data = {}
        data['id'] = form.getvalue('id')
        data['id_coll'] = self.session.data['id_coll']
        self.data = data

    def set(self, who):
        #brk("localhost", 9000)
        self.who_list = 'py/%s.list.py' % who
        if who == 'species':
            self.execute('get_alternate_state', {'id':self.data['id']})
            alt_state = self.fetch('rows')
            if (len(alt_state) > 0):
                self.feedback(-1, _("This taxon can not be deleted because this is alternate state of the other taxon."))
            else:
                self.execute('get_sciname_for_species', {'id':self.data['id']})
                self.data['id_sciname'] = self.fetch('one')

                self.delete('delete_species')
                if 'error_info' not in self.html:
                    self.delete('delete_sciname')
                if 'error_info' not in self.html:
                    self.delete('delete_species_security')
        elif who=='strains':
            id_log_level = 1
            id_log_entity = 1
            id_log_operation = 3

            if self.l.checkLogLevel(id_log_level):
                return_sql = []

                self.execute('get_str_general_log', self.data)
                dict_temp = self.fetch('all')[0]
                tmp = {'numeric_code': ''}
                return_sql.extend(self.l.checkModifiedFields('', tmp, self.data['id'], dict_temp['code'], '', 'delete', id_log_operation, id_log_entity,''));

                sql_final = "".join(return_sql)[0:len("".join(return_sql))-1]

            self.delete('delete_strain')
            if 'error_info' not in self.html:
                self.delete('delete_strain_security')

            if 'error_info' not in self.html:
                self.execute_log('insert_log', {'insert_values_log':sql_final}, raw_mode = True)
                self.db_log.connect.commit();

        elif who=='doc':
            self.del_doc()
            if 'error_info' not in self.html:
                self.delete('delete_doc_security')
        elif who=='ref':
            self.delete('delete_ref')
            if 'error_info' not in self.html:
                self.delete('delete_ref_security')
        elif who=='people':
            self.delete('delete_person')
            if 'error_info' not in self.html:
                self.delete('delete_person_security')
        elif who=='institutions':
            self.delete('delete_institution')
            if 'error_info' not in self.html:
                self.delete('delete_institution_security')
        elif who=='reports':
            self.delete('delete_reports')
            if 'error_info' not in self.html:
                self.delete('delete_reports_security')
        elif who=='distribution':
            self.execute('get_distribution_usage_information', {'id_distribution': self.data['id']})
            count = self.fetch('one')
            if count:
                self.feedback(-1, _("This distribution can not be deleted because the original positions are taken by another preservation or stock movement."))
            else:
                try:
                    self.execute('get_one_distribution',{'id':self.data['id']})
                    distribution = self.fetch('columns')

                    id_log_level = 3
                    id_log_entity = 1
                    save_log = self.l.checkLogLevel(id_log_level)
                    dic_qt = {}

                    if save_log:

                        self.execute('get_one_distribution', {'id' : self.data['id']})
                        dist_data = self.fetch('all')[0]

                        self.execute('get_distribution_origin_location', {'id' : self.data['id']})
                        location_data = self.fetch('all')[0]

                        dic_qt['id_strain'] = dist_data['id_strain']
                        dic_qt['id_container_hierarchy'] = location_data['id_origin_container_hierarchy']
                        dic_qt['row'] = location_data['origin_row']
                        dic_qt['col'] = location_data['origin_col']
                        dic_qt['quantity'] = location_data['quantity']

                    self.execute('delete_distribution_origin',{'id':self.data['id']})
                    self.delete('delete_distribution')
                    if 'error_info' not in self.html:
                        self.delete('delete_distribution_security')

                    if save_log:
                        return_sql = []
                        from .location import LocationBuilder
                        self.location = LocationBuilder(self.cookie_value)

                        #get actual quantity location after distribution
                        self.execute('get_location_qt_log', dic_qt)
                        qt_lot = self.fetch('one', 'available_qt')
                        location_qt = self.location.get_incomplete_location(location_data['id_origin_container_hierarchy'], location_data['origin_row'], location_data['origin_col'], None, qt_lot)

                        self.execute('get_lot', {'id_lot' : dist_data['id_lot']})
                        lot_name = self.fetch('one', 'name')

                        #get lot name
                        self.execute('get_strain_code', {'id_strain': dist_data['id_strain']})
                        strain_code = self.fetch('one')

                        id_log_operation = 13

                        lista_tmp = []
                        dict_temp = {'stock' : location_qt, 'id' : dist_data['id_lot'], 'lang' : '' }
                        lista_tmp = self.l.checkModifiedFields('', dict_temp, dist_data['id_strain'], strain_code, '', 'insert', id_log_operation, id_log_entity, lot_name)
                        return_sql.append(lista_tmp[len(lista_tmp) - 1].replace('|%|ID|%|',str(dist_data['id_strain'])))

                        dic_temp = {'id_lot': ''}
                        return_sql.extend(self.l.checkModifiedFields('', dic_temp, self.data['id'], strain_code, '', 'delete', id_log_operation, id_log_entity, lot_name))

                        sql_final = "".join(return_sql)[0:len("".join(return_sql))-1]

                        #Save log data
                        self.execute_log('insert_log', {'insert_values_log':sql_final}, raw_mode = True)

                except Exception as e:
                    self.dbconnection.connect.rollback()
                    if return_sql and save_log: self.db_log.connect.rollback()
                    self.feedback(-1)
                else:
                    self.dbconnection.connect.commit()
                    if return_sql and save_log: self.db_log.connect.commit()

        elif who=='preservation':
            #Get Lot ID
            self.execute('get_preservation_lot',{'id':self.data['id']})
            lot_id = self.fetch('one')

            # Checks if the destination locations generated by
            # this preservation is already reused by other
            # preservation / distribution / QC / stock movement

            self.execute('get_lot_count_usage_information_no_myself', {'id_lot': lot_id}, force_debug=False)
            if int(self.fetch('one')) > 0:
                self.feedback(-1,
                    _("This preservation can not be deleted because it has been used as origin of another preservation, a quality control, a distribution, or a stock movement."))
            else:
                self.execute('get_preservation_lot_usage_information_all', {'id_lot': lot_id}, force_debug=False)
                if self.fetch('all') and len(self.fetch('all')) > 0:
                    self.feedback(-1,
                    _("This preservation can not be deleted because it has been used as origin of another preservation, a quality control, a distribution, or a stock movement."))

                self.execute('get_distribution_lot_usage_information_all', {'id_lot': lot_id}, force_debug=False)
                if self.fetch('all') and len(self.fetch('all')) > 0:
                    self.feedback(-1,
                    _("This preservation can not be deleted because it has been used as origin of another preservation, a quality control, a distribution, or a stock movement."))

                self.execute('get_quality_lot_usage_information_all', {'id_lot': lot_id}, force_debug=False)
                if self.fetch('all') and len(self.fetch('all')) > 0:
                    self.feedback(-1,
                    _("This preservation can not be deleted because it has been used as origin of another preservation, a quality control, a distribution, or a stock movement."))

                self.execute('get_movement_lot_usage_information_all', {'id_lot': lot_id}, force_debug=False)
                if self.fetch('all') and len(self.fetch('all')) > 0:
                    self.feedback(-1,
                    _("This preservation can not be deleted because it has been used as origin of another preservation, a quality control, a distribution, or a stock movement."))


                id_log_level = 3
                id_log_entity = 1
                save_log = self.l.checkLogLevel(id_log_level)
                return_sql = []
                dic_qt = {}

                try:

                    if 'error_info' not in self.html:
                        #Get Strains related to this preservation
                        self.execute('get_preservation_strains',{'id':self.data['id']})
                        strains = self.fetch('rows')
                        for id_strain in strains:

                            self.execute('get_location_by_strain_log', {'id_strain' : id_strain, 'id_lot' :  lot_id})
                            locations = self.fetch('all')

                            self.execute('get_lot', {'id_lot' : lot_id})
                            lot_name = self.fetch('one', 'name')

                            #get lot name
                            self.execute('get_strain_code', {'id_strain': id_strain})
                            strain_code = self.fetch('one')

                            id_log_operation = 10

                            from .location import LocationBuilder
                            self.location = LocationBuilder(self.cookie_value)

                            self.execute('get_preservation_strain_origin_data', {'id': self.data['id'], 'id_strain': id_strain });
                            origin_data = self.fetch('all')[0]
                            
                            self.delete_preservation_strain(True,id_strain,lot_id)
                            #Delete LOT accordingly
                            self.execute('delete_lot',{'id':lot_id})

                            if origin_data['origin_type'] == 'lot':

                                dic_qt['id_strain'] = id_strain
                                dic_qt['id_container_hierarchy'] = origin_data['id_origin_container_hierarchy']
                                dic_qt['row'] = origin_data['origin_row']
                                dic_qt['col'] = origin_data['origin_col']

                                self.execute('get_location_qt_log', dic_qt)
                                qt_origin = self.fetch('one','available_qt')

                                origin_qt = self.location.get_incomplete_location(origin_data['id_origin_container_hierarchy'], origin_data['origin_row'], origin_data['origin_col'], None, qt_origin)

                                lista_tmp = []
                                dict_temp = {'stock' : origin_qt, 'id' : lot_id, 'lang' : '' }
                                lista_tmp = self.l.checkModifiedFields('', dict_temp, id_strain, strain_code, '', 'insert', id_log_operation, id_log_entity, lot_name)
                                return_sql.append(lista_tmp[len(lista_tmp) - 1].replace('|%|ID|%|',str(id_strain)))

                            for location_data in locations:

                                location_qt = self.location.get_incomplete_location(location_data['id_container_hierarchy'], location_data['row'], location_data['col'], None, 0)
                                location_qt = location_qt.replace("()", "(0)")

                                lista_tmp = []
                                dict_temp = {'stock' : location_qt, 'id' : lot_id, 'lang' : '' }
                                lista_tmp = self.l.checkModifiedFields('', dict_temp, id_strain, strain_code, '', 'insert', id_log_operation, id_log_entity, lot_name)
                                return_sql.append(lista_tmp[len(lista_tmp) - 1].replace('|%|ID|%|',str(id_strain)))

                        #self.commit()
                        #Delete PRESERVATION DATA
                        self.delete('delete_preservation')
                        if 'error_info' not in self.html:
                            self.delete('delete_preservation_security')

                        sql_final = "".join(return_sql)[0:len("".join(return_sql))-1]

                        #Save log data
                        if save_log:
                            self.execute_log('insert_log', {'insert_values_log':sql_final}, raw_mode = True)

                except Exception as e:
                    self.dbconnection.connect.rollback()
                    self.db_log.connect.rollback()
                else:
                    self.dbconnection.connect.commit()
                    self.db_log.connect.commit()
        elif who=='stockmovement':
            self.execute('get_lot_count_usage_information_stock_movement_no_myself', {'id':self.data['id']})
            if int(self.fetch('one')) > 0:
                self.feedback(-1,
                    _("This stock movement can not be deleted because one or more destination positions has been used as origin of a preservation, a quality control, a distribution, or another stock movement."))
            else:
                self.execute('get_stock_movement_usage_information', {'id':self.data['id']})
                if int(self.fetch('one')) > 0:
                    self.feedback(-1, _("This stock movement can not be deleted because the original positions are taken by another preservation or stock movement."))
            
            if 'error_info' not in self.html:
                #brk(host="localhost", port=9000)
                #id_log_entity for strains is 1
                id_log_entity = 1
                
                #id log operation for Stock Movement Delete
                id_log_operation = 18
                
                id_log_level = 2
                save_log = self.l.checkLogLevel(id_log_level)                
                return_sql = []
                
                try:
                    if (save_log):
                        self.execute('get_stock_movement_location_data', {'id': self.data['id']})
                        locations_movements = self.fetch('all')
                        from .location import LocationBuilder
                        self.location = LocationBuilder(self.cookie_value)                    
                        
                        for location_data_from_to in locations_movements:
                        
                            #get lot name
                            self.execute('get_lot',{'id_lot': location_data_from_to['id_lot']})
                            lot_name = self.fetch('one', 'name')
                            
                            #get strain code
                            self.execute('get_strain_code', {'id_strain': location_data_from_to['id_strain']})
                            strain_code = self.fetch('one')
    
                            #prepare log to the location_from
                            location_qt_from = self.location.get_incomplete_location(location_data_from_to['id_container_hierarchy_from'], location_data_from_to['row_from'], location_data_from_to['col_from'], None, location_data_from_to['qtd_from'])
                            lista_tmp = []
                            dict_temp = {'stock' : location_qt_from, 'id' : location_data_from_to['id_lot']}
                            lista_tmp = self.l.checkModifiedFields('', dict_temp, location_data_from_to['id_strain'], strain_code, '', 'insert', id_log_operation, id_log_entity, lot_name)
                            return_sql.append(lista_tmp[len(lista_tmp) - 1].replace('|%|ID|%|',str(location_data_from_to['id_strain'])))
                                                
                            #if exists, prepare log to the location_to
                            if (location_data_from_to['id_container_hierarchy_to']):
                                location_qt_to = self.location.get_incomplete_location(location_data_from_to['id_container_hierarchy_to'], location_data_from_to['row_to'], location_data_from_to['col_to'], None, 0)
                                lista_tmp = []
                                dict_temp = {'stock' : location_qt_to, 'id' : location_data_from_to['id_lot']}
                                lista_tmp = self.l.checkModifiedFields('', dict_temp, location_data_from_to['id_strain'], strain_code, '', 'insert', id_log_operation, id_log_entity, lot_name)
                                return_sql.append(lista_tmp[len(lista_tmp) - 1].replace('|%|ID|%|',str(location_data_from_to['id_strain'])))
                    
                    #Write log
                    if return_sql:                        
                        self.db_log.execute('insert_log', {'insert_values_log':"".join(return_sql)[0:len("".join(return_sql))-1]}, raw_mode = True)
                    
                    self.execute('delete_lot_strain_locations_to',{'id':self.data['id']})
                    self.delete('delete_stock_movement')
                        
                except Exception as e:
                    self.dbconnection.connect.rollback()
                    self.db_log.connect.rollback()
                else:
                    self.dbconnection.connect.commit()
                    self.db_log.connect.commit()
                    
        elif who == 'container':
            #brk(host="localhost", port=9000)
            self.execute('get_used_container', self.data)
            if len(self.fetch('rows')) > 0:
                self.feedback(-1, _("This container can not be deleted."))
            else:
                if 'error_info' not in self.html:
                    self.delete('delete_container_subcoll', {'id': self.data['id']})
                    self.delete('delete_container_preservation_method', {'id': self.data['id']})
                    self.delete('delete_container_location', {'id': self.data['id']})                                        
                    self.delete('delete_container_hierarchy', {'id': self.data['id']})                                      
                    self.delete('delete_container', {'id': self.data['id']})

        return self.html

    def feedback(self, value, error=''):
        if value == -1:
            self.html['error_info'] = error
        elif value > 0:
            self.session.data['feedback'] = value
            self.session.save()

    def rollback(self, error):
        self.dbconnection.connect.rollback()
        self.feedback(-1, error)

    def commit(self):
        self.dbconnection.connect.commit()
        self.feedback(2)

    def delete(self, sql, function=''):
        #self.dbconnection.connect.begin()
        try:
          self.execute(sql, self.data)
          self.commit()
          print(self.g.redirect(urljoin(self.index_url, self.who_list)))
        except Exception as e:
          self.rollback(e)

    def del_doc(self):
        #self.dbconnection.connect.begin()
        try:
            #Get all uploaded files in all languages
            self.execute('get_languages_by_doc', self.data)
            languages = self.dbconnection.fetch('rows','id_lang')

            #Delete Document Data
            self.execute('delete_doc', self.data)

            #Delete Files Uploaded
            for language in languages:
                file_code = self.data['id'] + str(language)
                file_code = new_sha(file_code).hexdigest()
                file = path.join(self.doc_dir, file_code)
                try: remove(file)
                except OSError: pass

        except Exception as e: self.rollback(e)
        else: self.commit()

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
            self.delete_preservation_strain(False,child_id_strain,child_id_lot)
        #Delete node
        self.execute('delete_preservation_strain_by_ids',{'id_strain':id_strain,'id_lot':id_lot})
        #Delete this lot_strain combination (cascades automatically)
        self.execute('delete_lot_strain_location',{'id_strain':id_strain,'id_lot':id_lot})
        #Delete this lot_strain combination (cascades automatically)
        self.execute('delete_lot_strain',{'id_strain':id_strain,'id_lot':id_lot})
