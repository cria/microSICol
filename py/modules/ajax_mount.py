#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

from sys import exit,platform
from os import path
#from dbgp.client import brk

import pprint

if platform == "win32": #Windows reads upload/download as Text instead of Binary...
    import msvcrt
    from os import O_BINARY
    msvcrt.setmode(0, O_BINARY) #stdin
    msvcrt.setmode(1, O_BINARY) #stdout

import cgitb; cgitb.enable()
#python imports
from string import join
from cgi import FieldStorage
from urllib.parse import urljoin

#project imports
from .i18n import I18n
from . import exception
from .session import Session
from .cookie import Cookie
from .general import General,DefDict
from .dbconnection import dbConnection
from .loghelper import Logging
from .ajax import AjaxBuilder
from .location import LocationBuilder, LocationHelper

class Principal(object):
    i18n = I18n()
    g = General()
    
    #brk(host="localhost", port=9000)

    def __init__(self):
        '''
        Class Constructor
        '''
        #Define Logging
        self.logger = Logging.getLogger("ajax_mount")
        self.d = self.logger.debug
        
        #Define Cookie
        self.cookie = Cookie()
        self.cookie_value = self.cookie.read('Sicol_Session')

        #Set Language according to user preference
        self.i18n = I18n(cookie_value=self.cookie_value)
        from .labels import label_dict
        self.label_dict = label_dict

        #Define Sqlite Connection
        self.dbconnection = dbConnection(self.cookie_value)
        self.execute = self.dbconnection.execute
        self.cursor = self.dbconnection.cursor
        self.fetch = self.dbconnection.fetch

        #Define AjaxBuilder
        self.page = AjaxBuilder()
        self.get_param = self.page.get_param
        self.get_params = self.page.get_params
        self.send_response = self.page.send_response
        self.dump = self.page.dump

        #Define LocationBuilder -- helps get location info
        self.l = LocationBuilder(self.cookie_value)

        #Define others global vars
        self.form = FieldStorage()
        self.session = Session()
        self.html = None
        
        
    def mount(self, page, action = None):
        try:
            if not action:
                action = self.page.get_param('action')

            self.logger.debug('Mount AJAX page for: %s - %s' % (page, action))
            
            if page == 'location':
                self.html = self.handle_location(action)

        except Exception as e:
            # import traceback
            # self.logger.error('Error while running Ajax interaction: %s', traceback.format_exc(e))
            self.logger.error('Error while running Ajax interaction: %s', e)
            self.html = self.dump({'result': 'error', 'error': str(e)})
            if self.page.get_param('raise'):
                raise
            
        self.send_response(self.html)
        
    def parse_data_params(self):
        data = {}
        
        for p in self.page.get_all_params():
            if p.startswith('data_'):
                data[p[5:]] = self.page.get_param(p)
                
        return data
         
    def handle_location(self, action):
        if action == 'render_location':
            data = self.parse_data_params()
            render_action = self.page.get_param('render_action')
            strain_num = self.page.get_param('strain_num')
            
            self.logger.debug('Render action: %s' % render_action)
            
            location_helper = LocationHelper(
                action=render_action,
                model='preservation', 
                data=data,
                cookie_value=self.cookie_value,
                decrease_stock_optional=True,
                query='get_lot_strain_location',
                css_classes={
                    'select': 'stock_pos',
                    'image' : 'new'
                },
            )
        
            return location_helper.renderTag()
        
        if action == 'main':            
            params = self.get_params('id_subcoll', 'id_preservation_method', 'id_lot')
            
            id_lot = params[2]
            self.logger.debug('id_lot before: %s' % id_lot)
            if id_lot[0] == '-':
                id_lot = None
            self.logger.debug('id_lot before: %s' % id_lot)

            containers = self.l.get_containers(params[0], params[1])
            
            if not containers:
                return self.dump({ 'error': _('No containers found for this preservation method on this subcollection') })
            
            usedLocations = self.l.get_used_locations(params[0], params[1], id_lot)
            locationSettings = self.l.get_location_settings(params[0], params[1])
            
            self.logger.debugObj('containers:\n%s',       containers)
            self.logger.debugObj('usedLocations:\n%s',    usedLocations)
            self.logger.debugObj('locationSettings:\n%s', locationSettings)
            
            hierarchy = {}
            hierarchyMap = {}
            for c in containers:
                id = c['id_container']
                hierarchy[id], hierarchyMap[id] = self.l.get_hierarchy(id, container_abbrev=c['abbreviation'])
                
            self.logger.debugObj('hierarchy:\n%s',      hierarchy)
            self.logger.debugObj('hierarchyMap:\n%s',   hierarchyMap)

            data = self.label_dict.copy()
            data['operation'] = ''
            data['id_strain'] = self.get_param('id_strain')
            data['strain'] = self.get_param('strain')
            data['sel_location'] = ''
            
            ret = {}
            html_content = self.g.read_html('location.form')
            if isinstance(html_content, bytes):
                html_content = html_content.decode('utf-8')
            ret['html'] = html_content % (data)
            ret['containers'] = containers
            ret['hierarchy'] = hierarchy
            ret['hierarchyMap'] = hierarchyMap
            ret['usedLocations'] = usedLocations
            ret['locationSettings'] = locationSettings
           
            # self.logger.debug('Ret:\n%s' % str(ret))
            
            return self.dump(ret)
        
        if action == 'remove_main':      
            self.d('remove_main')      
            params = self.get_params('id_coll', 'id_subcoll', 'id_preservation_method', 'id_origin_lot', 'id_strain')

            id_subcoll = params[1]
            id_lot = params[3]
            id_strain = params[4]
            id_preservation_method = '0'
            
            # stock movement case
            if (id_lot == '0' and id_strain == '0'):
                id_preservation_method = params[2]
            
            # retrieves all containers
            containers = self.l.get_containers_for_lot_strain(id_lot, id_strain, id_subcoll, id_preservation_method)
            
            # stock movement case
            if (id_lot == '0' and id_strain == '0' and not containers):
                return self.dump({ 'error': _('No containers with stock found for this preservation method on this subcollection') })
            
            # retrieves all locations where the strain is currently located for the selected lot
            strainAvailableLocations = self.l.get_strain_locations(id_strain, id_lot, id_subcoll)
            
            # retrieves location settings for containers
            locationSettings = self.l.get_location_settings_for_lot_strain(id_lot, id_strain, id_subcoll)
            
            hierarchy = {}
            hierarchyMap = {}
            for c in containers:
                id = c['id_container']
                hierarchy[id], hierarchyMap[id] = self.l.get_hierarchy_for_lot_strain({
                    'id_container': id,
                    'id_lot': id_lot,
                    'id_strain': id_strain }, container_abbrev=c['abbreviation'])

            data = self.label_dict.copy()
            data['operation'] = ''
            data['id_strain'] = self.get_param('id_strain')
            data['strain'] = self.get_param('strain')
            data['sel_location'] = ''
            
            ret = {}
            html_content = self.g.read_html('location.form')
            if isinstance(html_content, bytes):
                html_content = html_content.decode('utf-8')
            ret['html'] = html_content % (data)
            ret['containers'] = containers
            ret['hierarchy'] = hierarchy
            ret['hierarchyMap'] = hierarchyMap
            ret['usedLocations'] = strainAvailableLocations
            ret['locationSettings'] = locationSettings
            
            pp = pprint.PrettyPrinter(indent=4)
            #self.logger.debug('containers:\n%s', pp.pformat(containers))
            #self.logger.debug('strainAvailableLocations:\n%s', pp.pformat(strainAvailableLocations))
            #self.logger.debug('locationSettings:\n%s', pp.pformat(locationSettings))

            return self.dump(ret)

        if action == 'lot_strain_location':
            params = self.get_params('id_origin_lot', 'id_strain')
            
            origin_locations = self.l.get_lot_strain_locations(params[0], params[1])
            #origin_locations = [{'id_container': 1, 'id_container_hierarchy': 4, 'row': 0, 'col': 1}]
            
            id_container_hierarchys = []
            rows = []
            cols = []
            labels = []
            for o in origin_locations:
                id_container_hierarchys.append(o['id_container_hierarchy'])
                rows.append(o['row'])
                cols.append(o['col'])
                labels.append(self.l.get_location(o['id_container'], o['id_container_hierarchy'], o['row'], o['col']))
                
            return self.dump({'id_container_hierarchys': id_container_hierarchys, 'rows': rows, 'cols': cols, 'labels': labels})
        
        if action == 'encode':
            id_strain = self.get_param('id_strain')
            tempLocations = AjaxBuilder.parse(self.get_param('temporaryPageLocations'));
            
            self.logger.debug('locations: %s' % str(tempLocations))
            
            return self.dump(self.l.encode_locations(tempLocations, id_strain))