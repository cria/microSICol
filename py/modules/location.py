#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

from .session import Session
from .cookie import Cookie
from .general import General
from .dbconnection import dbConnection
from .loghelper import Logging
from .json import JsonBuilder

def ppnode(node):
    try:
        return "<[ id: [%s] name: [%s (%s)] id_parent: [%s] children:[%s] ]> ==> count: %s" % (
            node['id_container_hierarchy'], 
            node['description'],
            node['abbreviation'],
            node['loc_count'],
            node['id_parent'],
            ('children' in node and [len(node['children'])] or ['N/A'])[0])
    except Exception as e:
        Logging.getLogger("LocationCache").error('Error on ppnode', e)
        Logging.getLogger("LocationCache").debugObj('Node: %s', node)
        return 'Error on ppnode: ' + str(e)
        
class LocationHelper(object):
    @staticmethod
    def parseLocations(locations):
        data = []
        locations_items = locations.split('|')
        for l in locations_items:
            parts = l.split(';')
            row = {
                'id_origin_container_hierarchy': parts[0],
                'origin_row': parts[1],
                'origin_col': parts[2],
                'quantity': parts[3]
            }
            data.append(row)
        
        return data
        
    def h(self, val):
        return val % self.model
        
    def __init__(self, action, model, data, cookie_value=None, decrease_stock_optional=False, quantity_field=None, query=None, css_classes=None):
        from .labels import label_dict
        self.label_dict = label_dict
        self.quantity_field = quantity_field
        
        # if action is edition or a new record, we'll render the display with editing
        # data, so the user can enter a new location or edit existing ones
        if action in ['edit', 'new']:
            self.view_template = 'edit'
        else:
            self.view_template = 'show'
        
        self.model = model
        self.data = data
        self.decrease_stock_optional = decrease_stock_optional
        self.req_locations = action in ['edit', 'view', 'list']
        self.query = query
        self.css_classes = css_classes
        
        #Logging
        #self.logger = Logging.getLogger("location_helper")

        if self.req_locations:
            if not cookie_value:
                raise Exception('cookie_value is mandatory when using edit action')

            self.cookie_value = cookie_value
            self.dbconnection = dbConnection(cookie_value)
            self.execute = self.dbconnection.execute
            self.fetch = self.dbconnection.fetch
            
        self.__templates = {
            'edit': """
            
                    <label for="%(id)s" id="%(qtd_label_id)s">%(qtd_label)s</label><br/>
                    <input type='hidden' name="%(id)s" id="%(id)s" value="%(qtd_value)s" />
                    <select class='%(select_css_class)s' name="%(target_id)s" id="%(target_id)s" disabled="true" size="2">
                        %(origins)s
                    </select>
                    <img src="../img/pick.png" id='img_source' class='%(image_css_class)s'>
                    """,

            'show': """
                    <label for="%(id)s" id="%(qtd_label_id)s">%(qtd_label)s</label><br/>
                    <span style='font-family: Courier New;'>
                        %(origins)s
                    </span>
                    """

        }

        self.__location_templates = {
            'edit': '<option>%s</option>',
            'show': '%s<br/>'
        }

        # self.__stock_templates = {
        #     'edit': {
        #         'values':   ('', ' checked="checked"'),
        #         'template': """<br/>
        #         
        #             <input class="checkbox" name="%(stock_id)s" id="%(stock_id)s" type="checkbox" value="on" %(stock_value)s/>
        #             <label for="%(stock_id)s">%(stock_label)s ?</label>
        #         
        #             """
        #     },
        #     'show': {
        #         'values':   (label_dict['label_Location_No'], label_dict['label_Location_Yes']),
        #         'template': '<label>%(stock_label)s ?</label><br/>%(stock_value)s'
        #     }
        # }

    def renderTag(self, not_identified=False):
        if self.quantity_field:
            id = self.quantity_field
        else:
            id = self.h('%s_quantity')
        
        idx = 0 # No
        #self.logger.debug(self.data)
        #self.logger.debug(self.data.get('decrease_stock'))
        if self.data.get('decrease_stock', '') == 'y':
            idx = 1 # Yes
        #self.logger.debug(idx)
        
        self.css_classes = self.css_classes or {
            'select' : 'origin_location',
            'image'  : 'source'
        }
        
        view_data = {
            'id': id,
            'target_id': self.h('%s_locations'),
            'qtd_label_id': self.h('label_%s_locations'),
            'qtd_label': self.label_dict[self.h('label_%s_Locations')],
            'qtd_value': self.data.get(id, 0),
            'select_css_class': self.css_classes['select'],
            'image_css_class': self.css_classes['image'],
        }
            
        # view_data['stock'] = stock_template['template'] % view_data
        
        options = []
        if not_identified:
            if self.view_template == 'edit':
                options.append("<option value='NI'>%s</option>" % _("Not identified"))
            elif self.view_template == 'show':
                options.append(self.__location_templates[self.view_template] % _("Not identified"))
        else:
            if self.req_locations:
                from .location import LocationBuilder
                loc_builder = LocationBuilder(self.cookie_value)
                
                if self.query:
                    query = self.query
                else:
                    query = self.h('get_%s_origin_location')
                    
                self.execute(query, self.data)
                data_rows = self.fetch('all')
                
                for row in data_rows:
                    location_name = loc_builder.get_location_from_dict(row)
                    options.append(self.__location_templates[self.view_template] % location_name)
        
        view_data['origins'] = "\n".join(options)
        #self.logger.debug('stock: %s' % view_data['origins'])
        
        return self.__templates[self.view_template] % view_data

class LocationBuilder(object):
    g = General()
    containerCache = None
    
    class LocationCache(object):
        def __init__(self, cookie_value):
            #Logging
            #self.logger = Logging.getLogger("LocationCache")

            self.dbconnection = dbConnection(cookie_value)
            self.execute = self.dbconnection.execute
            self.cursor = self.dbconnection.cursor
            self.fetch = self.dbconnection.fetch
            
            self.containers = {}
            self.heads = {}
            self.tails = {}
            self.all = {}
            
            #self.logger.debug("*** INIT BEGIN")
            self.execute('get_all_location_data')
            for row in self.fetch('all'):
                self.containers[row['id_container']] = row
            
            self.execute('get_complete_container_hierarchy')
            for row in self.fetch('all'):
                id = row['id_container_hierarchy']
                self.all[id] = row
                
            for id in self.all:
                id_parent = row['id_parent'] 
                
                if not id_parent:
                    self.heads[id] = rowc
                else:
                    parent = self.all[id_parent]
                    if not parent:
                        self.logger.error('Cannot find parent with id %s for container hierarchy with id %s' % (id_parent, id))
                    else:
                        if not 'children' in self.all[id_parent]:
                            self.all[id_parent]['children'] = []
                        self.all[id_parent]['children'].append(row)
            
            for id in self.all:
                this = self.all[id]
                if not 'children' in this:
                    id_parent = this['id_parent']
                    if id_parent:
                        this['parent'] = self.all[id_parent]
                    self.tails[id] = this
            #self.logger.debug("*** INIT END")
            
    def __init__(self, cookie_value, dbconnection = None):
        #Cookies
        self.cookie_value = cookie_value
        
        #Logging
        #self.logger = Logging.getLogger("locationBuilder")

        #Define Cookie
        self.cookie = Cookie()
        self.cookie_value = self.cookie.read('Sicol_Session')

        #Load Session
        self.session = Session()
        self.session.load(cookie_value)
        
        #Define Sqlite Connection
        if dbconnection:
            self.dbconnection = dbconnection
        else:
            self.dbconnection = dbConnection(cookie_value)
        self.execute = self.dbconnection.execute
        self.cursor = self.dbconnection.cursor
        self.fetch = self.dbconnection.fetch
        
    @classmethod
    def get_label(cls, ini_value, value):
        value = int(value)
        try:
            ini_val = int(ini_value)
        except ValueError:
            ini_val = str(ini_value)
            
        if isinstance(ini_val, int):
            return ini_val + value
        else:
            return chr(ord(ini_val) + value)

    def get_cache(self):
        if not LocationBuilder.containerCache:
            LocationBuilder.containerCache = LocationBuilder.LocationCache(self.cookie_value)
        return LocationBuilder.containerCache
    
    def encode_locations(self, tempLocations, id_strain):
        chs = []
        ret = []
        
        for c in tempLocations:
            for rowCol in tempLocations[c]:
                #self.logger.debug("container: %s - rowCol: %s" % (c, rowCol))
                item = tempLocations[c][rowCol]
                if item['id_strain'] == id_strain:
#                    self.logger.debug('tails: %s' % str(self.get_cache().tails[int(item['id_container_hierarchy'])]))
                    #self.logger.debug('item: %s' % str(item['id_container_hierarchy']))
                    ch = self.get_cache().tails[int(item['id_container_hierarchy'])].copy()
                    ch['row'], ch['col'] = rowCol.split("_")
                    #self.logger.debug('appending: %s' % str(ch))
                    chs.append(ch)
                    
        for ch in chs:
            #self.logger.debug('retrieving: %s' % str(ch))
            hierarchyDesc = ''
            cur = ch
            while 'parent' in cur:
                hierarchyDesc = cur['abbreviation'] + ' ' + hierarchyDesc
                cur = cur['parent']
                
            container = self.get_cache().containers[ch['id_container']]
            ch['row'] = LocationBuilder.get_label(container['ini_row'], ch['row'])
            ch['col'] = LocationBuilder.get_label(container['ini_col'], ch['col'])
            pattern = container['pattern']
            
            hierarchyDesc = cur['abbreviation'] + ' ' + hierarchyDesc + (pattern % ch)
            ret.append(hierarchyDesc)

        return ret

    def get_incomplete_location(self, id_container_hierarchy, row, col, decrease_stock=None, quantity=0):
        self.execute('get_container_by_hierarchy', { 'id_container_hierarchy': id_container_hierarchy })
        id_container = self.fetch('one', 'id_container')
        return self.get_location(id_container, id_container_hierarchy, row, col, decrease_stock, quantity)

    def get_location_from_dict(self, row):
        return self.get_incomplete_location(row['id_origin_container_hierarchy'], row['origin_row'], row['origin_col'], None, row['quantity'])
        
    def get_location(self, id_container, id_container_hierarchy, row, col, decrease_stock=None, quantity=0):
        data = { 'id_container': id_container }
        
        self.execute('get_container', data)
        container = self.fetch('columns')['abbreviation']
        
        self.execute('get_container_hierarchy_tree', data)
        rows = self.fetch('all')
        
        data["id_container_hierarchy"] = id_container_hierarchy
        
        self.execute('get_location_data', data)
        row_data = self.fetch('columns')
        loc_data = { 
                'row': LocationBuilder.get_label(row_data['ini_row'], int(row)), 
                'col': LocationBuilder.get_label(row_data['ini_col'], int(col)) }
        
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
        if (quantity != -1):
            location_name.append(' (%s)' % quantity)

        #self.logger.debug(location_name)

        return "".join(location_name)

    def get_containers(self, id_subcoll, id_preservation_method):
        data = { 'id_subcoll': id_subcoll, 'id_preservation_method': id_preservation_method }
        self.execute('get_containers', data)
        rows = self.fetch('all')
        
        return rows

    def get_containers_for_lot_strain(self, id_lot, id_strain, id_subcoll, id_preservation_method):
        data = { 
            'id_lot': id_lot,
            'id_strain': id_strain,
            'id_subcoll': id_subcoll,
            'id_preservation_method': id_preservation_method }
            
        self.execute('get_containers_for_lot_strain', data)
        rows = self.fetch('all')

        return rows

    def get_lot_strain_locations(self, id_origin_lot, id_strain):
        data = { 'id_lot': id_origin_lot, 'id_strain': id_strain }
        self.execute('get_lot_strain_location', data)
        rows = self.fetch('all')
        
        return rows
        
    def get_strain_locations(self, id_strain, id_lot, id_subcoll):
        data = { 'id_strain': id_strain, 'id_lot': id_lot, 'id_subcoll': id_subcoll }

        self.execute('get_strain_locations', data)

        dict = {}
        current_dict = {}
        cval = -1
        row = None
        for row in self.fetch('all'):
            #self.logger.debug("*** ROW: %s" % str(row))
            if cval == -1 or cval != row['id_container_hierarchy']: 
                if cval != -1:
                    #self.logger.debug('current_dict')
                    #self.logger.debug(current_dict)
                    #self.logger.debug(cval)
                    dict[cval] = current_dict
                    current_dict = {}

                cval = row['id_container_hierarchy']

            current_dict['%(row)s_%(col)s' % row] = row

        if cval != -1:
            #self.logger.debug('!current_dict')
            #self.logger.debug(current_dict)
            #self.logger.debug(cval)
            dict[cval] = current_dict
            current_dict = {}

        #self.logger.debug("!!! dict !!!")
        #self.logger.debug(dict)
        return dict
        
    def get_used_locations(self, id_subcoll, id_preservation_method, id_lot):
        data = { 'id_subcoll': id_subcoll, 'id_preservation_method': id_preservation_method, 'extra': ' ' }
        
        #self.logger.debug("*** id_lot: %s" % id_lot)

        if id_lot:
            #self.logger.debug('AND lsl.id_lot <> %s' % id_lot)
            data['extra'] = 'AND lsl.id_lot <> %s' % id_lot
            
        #self.logger.debug("*** data: %s" % str(data))
        
        self.execute('get_used_location_data', data, raw_mode = True)
        
        dict = {}
        current_dict = {}
        cval = -1
        row = None
        for row in self.fetch('all'):
            #self.logger.debug("*** ROW: %s" % str(row))
#           id_container_hierarchy, row, col, 
#           id_lot, id_strain, lot.name, strain.code, sciname.sciname_no_auth, 
#           id_lot_strain_location
            if cval == -1 or cval != row['id_container_hierarchy']: 
                if cval != -1:
                    #self.logger.debug('current_dict')
                    #self.logger.debug(current_dict)
                    #self.logger.debug(cval)
                    dict[cval] = current_dict
                    current_dict = {}
                    
                cval = row['id_container_hierarchy']
            
            current_dict['%(row)s_%(col)s' % row] = row

        #if row and cval <> row['id_container_hierarchy']: 
        if cval != -1:
            #self.logger.debug('!current_dict')
            #self.logger.debug(current_dict)
            #self.logger.debug(cval)
            dict[cval] = current_dict
            current_dict = {}
                
        #self.logger.debug("!!! dict !!!")
        #self.logger.debug(dict)
        
        return dict
    
    def get_location_settings(self, id_subcoll, id_preservation_method):
        data = { 'id_subcoll': id_subcoll, 'id_preservation_method': id_preservation_method }
        self.execute('get_filtered_location_data', data)

        dict = {}
        for row in self.fetch('all'):
            c = row['id_container_hierarchy']
            dict[c] = row
        
        return dict

    def get_location_settings_for_lot_strain(self, id_lot, id_strain, id_subcoll):
        data = {
            'id_lot': id_lot,
            'id_strain': id_strain,
            'id_subcoll': id_subcoll 
        }
        
        self.execute('get_location_data_for_lot_strain', data)
        
        dict = {}
        for row in self.fetch('all'):
            c = row['id_container_hierarchy']
            dict[c] = row
        
        return dict

    def get_hierarchy_for_lot_strain(self, data, container_abbrev=''):
        return self.get_hierarchy(
            data['id_container'], data, 
            execute = 'get_container_hierarchy_tree_for_lot_strain', 
            filter_empty = True, container_abbrev=container_abbrev)
            
    def get_hierarchy(self, id_container = None, extra_data = {}, 
        execute = 'get_container_hierarchy_tree', filter_empty = False, 
        container_abbrev = ''):
        """Creates two collections: the first is a list of all the items within the
        container hierarchy, and the list is flat (you can iterate through all the
        items within a given container hierarchy, without fetching each node children).
        The second collection is a dict that maps each hierarchy item using its id.
        Both collections items provide a children array that references all the children
        of a given item."""
        
        items = {}
        map = {}
        
        #self.logger.debugObj('extra_data:\n%s', extra_data)
        
        filter = {'id_container': id_container}
        filter.update(extra_data)
        
        self.execute(execute, filter)
        rows = self.fetch('all')
        
        #self.logger.debugObj('rows:\n%s', rows)
        
        for row in rows:
            row['children'] = []
            items[row['id_container_hierarchy']] = row
        
        for row in rows:
            if row['id_parent']:
                items[row['id_parent']]['children'].append(row)
        
        hierarchy = []
        for key in items:
            i = items[key]
            if not i['id_parent']:
                hierarchy.append(i)
        
        map, leaves = self.createMap(hierarchy)

        for key in items:
            i = items[key]
            if len(i['children']) < 1:
                parent = i
                h = ''
                while parent:
                    # self.logger.debug('parent: %s' % str(parent))
                    h = parent['abbreviation'] + ' ' + h
                    if parent['id_parent']:
                        parent = map[parent['id_parent']]
                    else:
                        parent = None
                        
                items[key]['hierarchy'] = "%s %s" % (container_abbrev, h.rstrip())

        #self.logger.debugObj('map:\n%s',       map)
        
        if filter_empty:
            for leaf in leaves:
                #self.logger.debug('About to count items for leaf: %s', ppnode(leaf))
                self.count_branches_items(map, leaf)

        return hierarchy, map
        
    def count_branches_items(self, hierarchy, current_node, level = 0):
        """Normalizes the loc_count attribute for each node. If a child has a loc_count, it is
        added to the parent's loc_count as well. This way, only branches without the given
        lot and strain are filtered out by remove_empty_branches method"""
        node = current_node
        #self.logger.debug('-> Current node: %s', ppnode(current_node))
        
        def has_parent(node):
            return 'id_parent' in node and node['id_parent'] and node['id_parent'] in hierarchy
        
        while has_parent(node):
            #self.logger.debug('   Node: %s => has_parent? %s', ppnode(node), has_parent(node))
            parent = hierarchy[node['id_parent']]
            #self.logger.debug('   Parent: %s', ppnode(parent))
            parent['loc_count'] += node['loc_count']
            #self.logger.debug('   Parent after: %s', ppnode(parent))
            
            node = self.count_branches_items(hierarchy, parent)
            
        #self.logger.debug('<- Exiting count_branches_items for node: %s', ppnode(current_node))
        return node
    
    def remove_node_from(self, node, from_obj):
        is_list = isinstance(from_obj, list)
        if is_list:
            type_str = 'list'
        else:
            type_str = 'dict'
        
        if not is_list and not isinstance(from_obj, dict):
            raise TypeError("remove_from_node can't handle %s: only lists and dicts allowed")
        
        to_remove = None
        if is_list:
            for i in range(len(from_obj)):
                #self.logger.debug("   #%s - %s <=> %s ? %s", i, ppnode(node), from_obj[i], node == from_obj[i])
                if from_obj[i] == node:
                    to_remove = i
                    break
        else:
            for k in from_obj:
                #self.logger.debug("   #[%s] - %s <=> %s ? %s", k, node, from_obj[k], node == from_obj[k])
                if from_obj[k] == node:
                    to_remove = k
                    break
                    
        #if to_remove is not None:
            #self.logger.debug('   <**> [%s] Removed: %s', type_str, ppnode(from_obj.pop(to_remove)))
        #else:
            #self.logger.debugObj('   <**> [%s] %s was not found on %s', type_str, 'Node %s' % ppnode(node), from_obj)
    
    def remove_empty_branches(self, from_collection, current_node):
        node = current_node
        #self.logger.debug('Current node: %s', ppnode(current_node))

        def has_parent(node):
            return 'id_parent' in node and node['id_parent'] and node['id_parent'] in from_collection

        if not has_parent(node) and node['loc_count'] < 1:
            self.remove_node_from(node, from_collection)

        while has_parent(node):
            #self.logger.debug('   Node: %s => has_parent? %s', ppnode(node), has_parent(node))
            parent = from_collection[node['id_parent']]
            #self.logger.debug('   Parent: %s', ppnode(parent))
            
            # removes this node from its parent children collection
            # if the number of locations of this node is less than one
            if node['loc_count'] < 1:
                children = parent['children']
                
                if children and len(children) > 0:
                    self.remove_node_from(node, children)

            #self.logger.debug('   Parent after: %s', ppnode(parent))

            from_collection, node = self.remove_empty_branches(from_collection, parent)

        #self.logger.debug('Exiting normalize_brand for node: %s', ppnode(current_node))
        return from_collection, node

    def createMap(self, hierarchy, map = {}, leaves = []):
        for h in hierarchy:
            map[h['id_container_hierarchy']] = h
            if h['children']:
                self.createMap(h['children'], map, leaves)
                
            if not h['children'] or len(h['children']) < 1:
                leaves.append(h)
        
        return map, leaves
        
    def parse(self, rows, dict):
        lines = []
        header = ['\t\t']
        sep = []
        for key in dict:
            field = key
            size = dict[key]
            if size < 0:
                header.append(field)
                sep.append("".ljust(len(key), '-'))
            else:
                header.append(field.strip().ljust(size))
                sep.append("".ljust(size, '-'))
            header.append(' ')
            sep.append(' ')
        
        lines.append("".join(header))
        lines.append("".join(sep))
            
        for row in rows:
            line = []
            for key in dict:
                if isinstance(row[key], str):
                    field = row[key]
                else:
                    field = str(row[key]).strip()
                    
                size = dict[key]
                
                if size == -1:
                    line.append(field.rjust(len(key)))
                elif size == -2:
                    line.append(field.ljust(len(key)))
                else:
                    line.append(field.ljust(size))
                line.append(' ')
            
            lines.append("".join(line))
            
        return "\n\t\t".join(lines)
                