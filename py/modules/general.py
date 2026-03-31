#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#python imports
from os import path
from sys import exit
#from dbgp.client import brk

class General( object ):

    def __init__(self):
        """
        Constructor
        """
        # Define root_dir como o diretório raiz do projeto
        from os import path, pardir
        self.root_dir = path.abspath(path.join(path.dirname(__file__), pardir, pardir))
        self.html_dir = path.join(self.root_dir, 'html')
        # Se quiser manter compatibilidade com config.xml:
        # self.html_dir = path.join(self.root_dir, self.get_config('html_dir'))

    def get_config(self, config_name):
        """
        Read installation config (config.xml)
        """
        from . import config
        if config_name in config.__dict__:
            return config.__dict__[config_name]
        else:
            from .dom_xml import Xml
            config_file = self.read_file(path.join(self.root_dir, 'config.xml'))
            xml = Xml('config', config_file)
            return xml.get(config_name)

    def redirect( self, url ):
        """
        Redirect user to "url"
        """
        if url.startswith('http://') or url.startswith('./'):
            return "Location: %s\n" % url
        else:
            from urllib.parse import urljoin
            return "Location: %s\n" % urljoin( 'http://', url )

    def read_file( self, dir ):
        """
        Read File and return it into a string
        """
        try:
            arq = open(dir, 'rb').read()
            return arq
        except IOError:
            header = self.get_config('http_header')
            if not header:
                header = "Content-type: text/html; charset=utf-8"
            out = header + '\n\n'
            out += '%s: %s' % ("No such file or directory", dir)
            return out.encode('utf-8')

    def read_html( self, html_name ):
        """
        Read html file and return it into a string
        """
        try:
            # Garante caminho absoluto a partir do root_dir
            dir = path.join(self.root_dir, 'html', html_name+'.html')
            arq = open(dir, 'rb').read()
        except IOError:
            out = self.get_config('http_header') + '\n\n'
            out += '%s: %s' % ("No such file or directory", dir)
            print(out)
            exit(1)
        else:
            arq = arq.replace(b'\r\n', b'\n') # remove double break lines
            arq = arq.replace(b'\t', b'  ') # pretty HTML source code
        return arq

    def replace_nonetypes(self, obj):
        """
        Replace Nonetype recursively, changing "None" by "Empty String"
        """
        retval = ''
        if (obj is None): retval = ''
        elif isinstance(obj,list):
            for i,item in enumerate(obj):
                obj[i] = self.replace_nonetypes(item)
            retval = obj
        elif isinstance(obj, tuple):
            retval = tuple(self.replace_nonetypes(list(obj)))
        elif isinstance(obj,dict):
            for key in obj:
                obj[key] = self.replace_nonetypes(obj[key])
            retval = obj
        else:
            retval = obj
        return retval

    def escape_quote (self, string, quote="'"):
        """
        Tranform ' into \'. Quote can be other characters, like " or \
        """
        return string.replace(quote, "\\%s" % quote)

    def get_area_permission(self, cookie_value, session, area, permission_type):
        '''
        Checks whether user has permission to create/delete in a certain area

        Parameters:
        cookie_value = value from session in order to start database connection
        session = user session
        area = 'species' | 'strains' | 'people' | 'institutions' | 'doc' | 'ref' | 'preservation' | 'distribution'
        permission_type = 'allow_create' | 'allow_delete'
        '''
        from .dbconnection import dbConnection
        #Define Database
        self.dbconnection = dbConnection(cookie_value)
        self.execute = self.dbconnection.execute
        self.fetch = self.dbconnection.fetch
        #Security
        #If user does not have permission to create then don't show the "new" button
        roles = str(session.data['roles']).replace("L","")
        roles = roles.replace("[","(")
        roles = roles.replace("]",")")
        self.execute('allow_area',{'allow':permission_type,'areaname':"'"+area+"'",'roles_list':roles},raw_mode = True)
        return self.fetch('one')

    def get_item_permission(self, cookie_value, session, area, id_item):
        '''
        Checks whether user has permission to see item details

        Parameters:
        cookie_value = value from session in order to start database connection
        session = user session
        area = 'species' | 'strains' | 'people' | 'institutions' | 'doc' | 'ref' | 'preservation' | 'distribution'
        id_item = unique id of item of chosen area
        '''
        from .dbconnection import dbConnection
        #Define Database
        self.dbconnection = dbConnection(cookie_value)
        self.execute = self.dbconnection.execute
        self.fetch = self.dbconnection.fetch
        #Security
        #If user does not have permission to create then don't show the "new" button
        roles = str(session.data['roles']).replace("L","")
        roles = roles.replace("[","(")
        roles = roles.replace("]",")")
        self.execute('allow_item',{'id_item':int(id_item),'areaname':"'"+area+"'",'roles_list':roles},raw_mode = True)
        return self.fetch('one')

    def apply_item_permission(self, dbconnection, area, form, data, action):
        '''
        Set user permission to an item.
        Encapsulates whether it is upon 'insertion' or 'update'

        Parameters:
        dbconnection = in order to read/write on database
        area = 'species' | 'strains' | 'people' | 'institutions' | 'doc' | 'ref' | 'preservation' | 'distribution' | 'reports'
        form = form data, to retrieve information
        data = page data, also to retrieve information
        action = 'update' | 'insert'
        '''
        if (action == 'update'):
            self.set_item_permission(dbconnection, area, form, data, True)
        elif (action == 'insert'):
            self.set_item_permission(dbconnection, area, form, data, False)
        else:
            raise _("Unknown action trying to execute apply_item_permission: ") + action
        return

    def set_item_permission(self, dbconnection, area, form, data, clear_first=False):
        '''
        Sets current user permissions on a particular item

        Parameters:
        dbconnection = in order to read/write on database
        area = 'species' | 'strains' | 'people' | 'institutions' | 'doc' | 'ref' | 'preservation' | 'distribution' | 'reports'
        form = form data, to retrieve information
        data = page data, also to retrieve information
        clear_first = erases data prior to insertion
        '''
        #Gets area id
        dbconnection.execute('get_area_id',{'name':area})
        id_area = dbconnection.fetch('one')

        if clear_first:
            dbconnection.execute('clear_security',{'id_item':data['id'],'id_area':id_area})

        #Insert permissions based on form submission
        perm = {}
        for i in form:
            i_parts = i.split('_')
            if i_parts[0] == 'perm':
              role_id = i_parts[1]
              perm = form.getvalue('perm_'+str(role_id))
              #brk(host="localhost", port=9000)
              if (perm == 'r'):
                dbconnection.execute('set_security_read',{'id_item':int(data['id']),'id_area':int(id_area),'id_role':int(role_id)})
              elif (perm == 'w'):
                dbconnection.execute('set_security_write',{'id_item':int(data['id']),'id_area':int(id_area),'id_role':int(role_id)})

        return

    def get_permissions(self, cookie_value, area, data):
        '''
        Initialize global "permissions" variable
        '''
        #brk(host="localhost", port=9000)
        from .dbconnection import dbConnection
        #Define Database
        self.dbconnection = dbConnection(cookie_value)
        self.execute = self.dbconnection.execute
        self.fetch = self.dbconnection.fetch

        self.execute('get_area_id',{'name':area})
        id_area = self.dbconnection.fetch('one')
        self.execute('get_security',{'id_item':data['id'],'id_area':id_area})
        security_data = self.dbconnection.fetch('all')
        
        permissions = {}
        for i in security_data:
            permissions[i['id_role']] = i['permission']

        return permissions

    def get_log_db(self, id_base):
        from .dbconnection import dbConnection

        #Define Database
        self.dbconnection = dbConnection()
        self.execute = self.dbconnection.execute
        self.fetch = self.dbconnection.fetch

        self.execute('get_db_log', id_base)
        db_log = self.fetch('columns')
        #self.logger.debug('db_info: %s' % str(db_log))
        dict_temp = {}
        dict_temp['host'] = db_log['host']
        dict_temp['port'] = db_log['port']
        dict_temp['db_name'] = db_log['dbname']
        dict_temp['user'] = db_log['user']
        dict_temp['pwd'] = db_log['pwd']
        dict_temp['dbms'] = db_log['dbms']

        return dict_temp

    def get_role_has_subcoll(self, id_role, id_subcoll):
        # retrieve id_user for this role (must be 1:1 since this is an user role)
        self.execute('get_group_members', {'id_role': id_role})
        id_user = self.fetch('one')

        #Start SQLite database
        from .dbconnection import dbConnection
        db = dbConnection()

        #Load this user's collection from Database
        db.execute('get_user_colls',{'id_user':id_user})
        colls = db.fetch('all')
        for c in colls:
            if str(c['id_subcoll']) == str(id_subcoll):
                return True

        return False

    def security_tab(self, cookie_value, action, data, area):
        #Load Session
        from .session import Session
        session = Session()
        session.load(cookie_value)
        #brk(host="localhost", port=9000)
        if 'groups_table' not in data:
            data['groups_table'] = ''
        #brk(host="localhost", port=9000)
        if 'new_report' in session.data and area == 'reports':
          if 'id' in session.data['new_report']:
            data['id'] = session.data['new_report']['id']
        
        permissions = self.get_permissions(cookie_value, area, data)
        self.execute('get_all_roles')
        all_roles = self.fetch('all')
        role_type = ''
        if action == 'view':
            for role in all_roles:
              # if user does not have this collection, skip it
              if role["type"] == "user" and not self.get_role_has_subcoll(role["id_role"], session.data["id_subcoll"]):
                  continue
              if (role['type'] == 'level'): role['type'] = 'group' #Force 'level' to be a 'group' type
              if role['type'] != role_type:
                role_type = role['type']
                if (role_type != 'all'):
                  if (role_type == 'group'): role_type_print = _("Group")
                  elif (role_type == 'user'): role_type_print = _("User")
                  #elif (role_type == 'level'): role_type_print = _("Level ")
                  data['groups_table'] += '<tr>\n\t<th align="right">%s</th>\n\t<td>&nbsp;</td>\n</tr>\n' % role_type_print.upper()
              permission = ''
              if role['id_role'] in permissions:
                if permissions[role['id_role']] == 'r':
                  permission = _("Read")
                elif permissions[role['id_role']] == 'w':
                  permission = _("Read")+'/'+_("Write")
              if role['name'] == 'all': role['name'] = _("All")
              #brk(host="localhost", port=9000)
              if role['id_role'] == 2 or role['id_role'] == 4:
                data['groups_table'] += '<tr>\n\t<td align="right">'+role['name']+'</td>\n\t<td>'+_("Read")+'/'+_("Write")+'</td>\n</tr>\n'
              else:
                data['groups_table'] += '<tr>\n\t<td align="right">%s</td>\n\t<td>%s</td>\n</tr>\n' % (role['name'],permission)
        else:
            if 'new_report' in session.data and area == 'reports':
              if 'report_permissions' in session.data['new_report']:
                permissions = session.data['new_report']['report_permissions']
   
            all_permissions = []
            for role in all_roles:
              # if user does not have this collection, skip it
              if role["type"] == "user" and not self.get_role_has_subcoll(role["id_role"], session.data["id_subcoll"]):
                  continue
              if (role['type'] == 'level'): role['type'] = 'group' #Force 'level' to be a 'group' type
              if role['type'] != role_type:
                role_type = role['type']
                if (role_type != 'all'):
                  if (role_type == 'group'): role_type_print = _("Group")
                  elif (role_type == 'user'): role_type_print = _("User")
                  #elif (role_type == 'level'): role_type_print = _("Level ")
                  data['groups_table'] += '<tr>\n\t<th align="right">%s</th>\n\t<td>&nbsp;</td>\n\t<td>&nbsp;</td>\n</tr>\n' % role_type_print.upper()
              all_permissions.append(str(role['id_role']))
              permission = '<select onchange="securityChanged(this.id);" name="perm_%s" id="perm_%s">\n' % (role['id_role'],role['id_role'])
              permission += '\t<option value="none">'+_("None")+'</option>\n'
              sel1 = ''
              sel2 = ''
              
              if role['id_role'] in permissions:
                if permissions[role['id_role']] == 'r':
                  sel1 = 'selected="selected"'
                elif permissions[role['id_role']] == 'w':
                  sel2 = 'selected="selected"'
              if action == 'new' and role['name'] == 'all':
                if area != 'reports':
                  sel2 = 'selected="selected"'
                elif 'report_permissions' not in session.data['new_report']:
                  sel2 = 'selected="selected"'
                    
              permission += '\t<option '+sel1+' value="r">'+_("Read")+'</option>\n'
              permission += '\t<option '+sel2+' value="w">'+_("Read")+'/'+_("Write")+'</option>\n'
              permission += '</select>'
              if role['name'] == 'all':
                role['name'] = _("All")
                data['js_securitychanged'] = ''
                try:
                  permissions[role['id_role']] #Check whether the "All" role has any permission whatsoever
                  #If no KeyError occurred then call securityChanged javascript
                  data['js_securitychanged'] += "<script type='text/javascript'>securityChanged('perm_1');</script>"
                except KeyError: #Permission == None
                  if action == 'new': data['js_securitychanged'] += "<script type='text/javascript'>securityChanged('perm_1');</script>"
                  pass
              if role['id_role'] == 2 or role['id_role'] == 4:
                data['groups_table'] += '<tr>\n\t<td align="right">'+role['name']+'</td>\n\t<td><select disabled="disabled"><option>'+_("Read")+'/'+_("Write")+'</option></select></td>\n</tr>\n'
              else:
                data['groups_table'] += '<tr>\n\t<td align="right">%s</td>\n\t<td>%s</td>\n</tr>\n' % (
                                                      role['name'],permission)
            data['all_permissions'] = ",".join(all_permissions)
            
        return

    def isAdmin(self,roles):
        '''
        Checks whether current user has administrator permissions or not
        (Administrator, id_role = 2 - HARDCODED)
        '''
        return (2 in roles)

    def isManager(self,roles):
        '''
        Checks whether current user has administrator or manager permissions or not
        (Administrator, id_role = 2, Manager, id_role = 4 HARDCODED)
        '''
        return ((2 in roles) or (4 in roles))
        
    def saveListOrder(self,id_user,id_subcoll,area,field):
        '''
        Save user's list order preference in Database
        '''
        #Start SQLite database
        from .dbconnection import dbConnection
        db = dbConnection()
        #Save changes inside Session and Database
        db.execute('load_area_list_order',{'id_user':id_user,'id_subcoll':id_subcoll,'area':area})
        order = db.fetch('columns')
        #Alternate between ASC and DESC modes
        if order['field'] == field and order['mode'] == 'ASC':
          order['mode'] = 'DESC'
        else:
          order['mode'] = 'ASC'
        db.execute('update_list_order',{'id_user':id_user,'id_subcoll':id_subcoll,'area':area,'field':field,'mode':order['mode']})
        db.connect.commit()
        db.cursor.close()

    def getListOrder(self, id_user, id_subcoll, area):
        '''
        Get list order from Database
        Returns (field,mode) tuple
        '''
        #Start SQLite database
        from .dbconnection import dbConnection
        db = dbConnection()
        #Load List Order from Database
        db.execute('load_area_list_order',{'id_user':id_user,'id_subcoll':id_subcoll,'area':area})
        order = []
        order = db.fetch('columns')
        
        return (order['field'], order['mode'])

    def loadListOrder(self,id_user,id_subcoll):
        '''
        Load list order from Database
        Returns dictionary: {'area':{'field':...,'mode':...} , 'area2':{'field':...,'mode':...} , ... }
        '''
        
        #brk(host="localhost", port=9000)
        
        #Start SQLite database
        from .dbconnection import dbConnection
        db = dbConnection()
        #Load List Order from Database to Session
        db.execute('load_list_order',{'id_user':id_user,'id_subcoll':id_subcoll})
        order = db.fetch('all')
        list_order = {}
        if order == []:
          #Fill in with default values and save in Database
          list_order['species'] = {'field':'taxongroup','mode':'ASC'}
          db.execute('save_list_order',{'id_user':id_user,'id_subcoll':id_subcoll,'area':'species','field':'taxongroup','mode':'ASC'})
          list_order['strains'] = {'field':'code','mode':'ASC'}
          db.execute('save_list_order',{'id_user':id_user,'id_subcoll':id_subcoll,'area':'strains','field':'code','mode':'ASC'})
          list_order['people'] = {'field':'name','mode':'ASC'}
          db.execute('save_list_order',{'id_user':id_user,'id_subcoll':id_subcoll,'area':'people','field':'name','mode':'ASC'})
          list_order['inst'] = {'field':'complement','mode':'ASC'}
          db.execute('save_list_order',{'id_user':id_user,'id_subcoll':id_subcoll,'area':'inst','field':'complement','mode':'ASC'})
          list_order['doc'] = {'field':'qualifier','mode':'ASC'}
          db.execute('save_list_order',{'id_user':id_user,'id_subcoll':id_subcoll,'area':'doc','field':'qualifier','mode':'ASC'})
          list_order['ref'] = {'field':'id_ref','mode':'ASC'}
          db.execute('save_list_order',{'id_user':id_user,'id_subcoll':id_subcoll,'area':'ref','field':'id_ref','mode':'ASC'})
          list_order['preservation'] = {'field':'date','mode':'ASC'}
          db.execute('save_list_order',{'id_user':id_user,'id_subcoll':id_subcoll,'area':'preservation','field':'date','mode':'ASC'})
          list_order['distribution'] = {'field':'date','mode':'ASC'}
          db.execute('save_list_order',{'id_user':id_user,'id_subcoll':id_subcoll,'area':'distribution','field':'date','mode':'ASC'})
          list_order['reports'] = {'field':'type','mode':'ASC'}
          db.execute('save_list_order',{'id_user':id_user,'id_subcoll':id_subcoll,'area':'reports','field':'type','mode':'ASC'})
          list_order['utilities'] = {'field':'date_time','mode':'DESC'}
          db.execute('save_list_order',{'id_user':id_user,'id_subcoll':id_subcoll,'area':'utilities','field':'date_time','mode':'DESC'})
          list_order['stockmovement'] = {'field':'date','mode':'DESC'}
          db.execute('save_list_order',{'id_user':id_user,'id_subcoll':id_subcoll,'area':'container','field':'abbreviation','mode':'DESC'})
          list_order['container'] = {'field':'abbreviation','mode':'DESC'}
          db.execute('save_list_order',{'id_user':id_user,'id_subcoll':id_subcoll,'area':'stockmovement','field':'date','mode':'DESC'})
          list_order['traceability'] = {'field':'date_time','mode':'DESC'}
          db.execute('save_list_order',{'id_user':id_user,'id_subcoll':id_subcoll,'area':'traceability','field':'date_time','mode':'DESC'})
        return

    def gps_dms2dec(self,gps_type,value):
        """
        Convert DMS (loose) FORMAT to DECIMAL FORMAT
        """
        import re
        if gps_type == 'latitude':
          dmsRegex = re.compile(r"([-+])?(\d{1,3})([^-0-9+])((\d{1,2})(\.\d+)?['`]((\d{1,2})(\.\d+)?(\"|''|``))?)?([NSns])?")
          m = dmsRegex.search(value)
          if m:
            #Find out the direction
            factor = 1
            if m.group(1) != None:
              if m.group(1) == '-': factor = -1
            if m.group(3) in ('S','s'): factor = -1
            if m.group(11) != None:
              if m.group(11) in ('S','s'): factor = -1
            #Calculate decimal value
            dec = 0
            #Degrees
            dec = int(m.group(2))
            #Minutes
            if m.group(4) != None:
              minutes = m.group(5)
              if m.group(6) != None:
                minutes += m.group(6)
              dec += float(float(minutes) / 60.0)
            #Seconds
            if m.group(7) != None:
              seconds = m.group(8)
              if m.group(9) != None:
                seconds += m.group(9)
              dec += float(float(seconds) / 3600.0)
            dec *= factor
            return str(dec)
          else:
            return "0"
        elif gps_type == 'longitude':
          dmsRegex = re.compile(r"([-+])?(\d{1,3})([^-0-9+])((\d{1,2})(\.\d+)?['`]((\d{1,2})(\.\d+)?(\"|''|``))?)?([WEwe])?")
          m = dmsRegex.search(value)
          if m:
            #Find out the direction
            factor = 1
            if m.group(1) != None:
              if m.group(1) == '-': factor = -1
            if m.group(3) in ('W','w'): factor = -1
            if m.group(11) != None:
              if m.group(11) in ('W','w'): factor = -1
            #Calculate decimal value
            dec = 0
            #Degrees
            dec = int(m.group(2))
            #Minutes
            if m.group(4) != None:
              minutes = m.group(5)
              if m.group(6) != None:
                minutes += m.group(6)
              dec += float(float(minutes) / 60.0)
            #Seconds
            if m.group(7) != None:
              seconds = m.group(8)
              if m.group(9) != None:
                seconds += m.group(9)
              dec += float(float(seconds) / 3600.0)
            dec *= factor
            return str(dec)
          else:
            return "0"
        else: return "0"

    def gps_dec2dms(self,gps_type,value):
        """
        Convert GPS DECIMAL value to DMS (degree-minute-second) STANDARD FORMAT
        """
        value = float(value)
        d     = value
        if d < 0: d *= -1 #Remove minus sign
        #Degrees
        rest  = d - int(d)#Fraction
        d     = int(d)    #Integer
        #Minutes
        m     = 60 * rest
        rest  = m - int(m)#Fraction
        m     = int(m)    #Integer
        if m < 10: m = "0"+str(m)
        else: m = str(m)
        #Seconds
        s     = round(60 * rest)
        if s < 10: s = "0"+str(s)
        else: s = str(s)
        if gps_type == 'latitude':
          if value > 0:
            return "".join([str(d),'N',m,"'",s,'"'])
          else:
            return "".join([str(d),'S',m,"'",s,'"'])
        elif gps_type == 'longitude':
          if value > 0:
            return "".join([str(d),'E',m,"'",s,'"'])
          else:
            return "".join([str(d),'W',m,"'",s,'"'])

    def removeHTML(self,string):
        import re
        return re.sub(r'<[^>]*>','',string)
        
    def ConvertStrUnicode(self, valor):
        retorno = '';
        if isinstance(valor, (int, float)):
            return str(valor)
            
        if isinstance(valor, bytes):
            retorno = valor.decode("utf8")
        else:
            retorno = str(valor)
        
        return retorno

class DefDict (dict):
    """
    Default Empty Dictionary
    """
    def __getitem__(self, item):
        try:
            item = dict.__getitem__(self, item)
        except KeyError:
            item = ""
        return item
