#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#python imports
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
#from dbgp.client import brk

class Getdata(object):

    #brk(host="localhost", port=9000)        
    #Configs
    g = General()
    index_url = g.get_config('index_url')
    list_page = urljoin(index_url, 'py/%s.list.py')
    
    opt_html = '\n\t<option value=""></option>'
    opt_html_selected = '\n\t<option selected="selected" value=""></option>'
    opt_selected = 'selected="selected"'
    opt_checked = 'checked="checked"'
    page_parts = {'top':'', 'submenu':'', 'hidden_forms':''}
    num_items = 1
    hierarchy = []
    dic_positions = {}
    
    global report_index_field
    
    def __init__(self, cookie_value, form):

        self.cookie_value = cookie_value

        #Logging
        self.logger = Logging.getLogger("getdata")
        self.d = self.logger.debug

        #Load Session
        self.session = Session()
        self.session.load(cookie_value)

        self.l = LocationBuilder(self.cookie_value)

        #Make form a class attribute
        self.form = form
        self.fields_definition = {}
        
        #check feedback parameter
        if 'feedback' in self.session.data and self.session.data['feedback']:
            self.feedback_value = self.session.data['feedback']
            self.session.data['feedback'] = 0
            self.session.save()
        else:
            self.feedback_value = 0

        #check id parameter
        if form.getvalue('id'):
            id = form.getvalue('id')
        else:
            id = ''

        #check row parameter
        if form.getvalue('row'):
            row = form.getvalue('row')
        else:
            row = ''

        #Define Database
        self.dbconnection = dbConnection(cookie_value)
        self.execute = self.dbconnection.execute
        self.fetch = self.dbconnection.fetch

        #Define Data Dict
        data = {}
        data['id'] = id
        data['id_user'] = self.session.data['id_user']
        data['id_coll'] = self.session.data['id_coll']
        data['id_lang'] = self.session.data['id_lang'] #id for label_lang
        data['action'] = ''
        data['back_where'] = 'detail'
        data['message'] = ''
        data['row'] = row
        self.data = data

        #Misc
        self._inst_option_list = None
        self.data_langs = self.session.data['data_langs']
		
    def ConvertStrUnicode(self, valor):
        retorno = '';
        if isinstance(valor, (int, float)):
            return str(valor)
            
        if (isinstance(valor, str) == False):
            retorno = str(valor).decode("utf8")
        else:
            retorno = valor
        
        return retorno	

    def get_stripped(self, field):
        return "REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(%s, '<b>', ''), '<i>', ''), '</b>', ''), '</i>', ''), '  ', ' ')" % (field)

    def format_date(self,action,field):
        '''
        Formats SQL date format (YYYY-mm-dd) to current locale date format
        '''
        if field: #field is a datetime.date object
            from time import strftime,strptime
            if action == 'edit':
              if self.session.data['date_input_mask'] is not None and self.session.data['date_input_mask'] != "": date_format = self.session.data['date_input_mask']
              else: date_format = self.g.get_config('date_input_mask')
            else: #view
              if self.session.data['date_output_mask'] is not None and self.session.data['date_output_mask'] != "": date_format = self.session.data['date_output_mask']
              else: date_format = self.g.get_config('date_output_mask')
            #If we can't find date_format attribute in config.xml then use a default date format
            if date_format is None:
                date_format = '%d/%m/%Y'
            return strftime(date_format,field.timetuple() )
        else: return ''

    def preferences(self, id_lang,allow_default=True):
        '''
        Create preferences' option list (currently only language labels)
        '''
        self.execute('get_all_from_table',{'table':'lang'})
        langs = self.fetch('all')
        languages = ""
        if allow_default:
          languages += "<option "
          if (id_lang == 'default'): languages += "selected='selected' "
          languages += "value='default'>%s</option>\n" % _("System Default")
        for lang in langs:
            languages += "\t<option "
            if (lang['id_lang'] == id_lang): languages += "selected='selected'"
            languages += " value='%s'>%s</option>\n" % (lang['code'],lang['lang'])
        return languages

    def usingDefaultLabel(self):
        '''
        Read SQLite database in order to know whether user is using
        the system default label or not
        '''
        db = dbConnection()
        db.execute('get_user_label',{'id_user':self.data['id_user']})
        label = db.fetch('one')
        if (label):
            return False
        else:
            return True

    def get(self, who, action):
                
        '''
        Get content according to given parameters:
        who = 'species', 'strains', 'doc', 'ref', 'people' or 'institutions'
        action = 'view' or 'edit' or 'new'
        '''

        #Logging
        self.logger.debug("Getting %s.%s" % (who, action))
        
        #Define specific submenu
        #brk(host="localhost", port=9000)
        
        if action in ('edit', 'new'):
            self.page_parts['submenu'] = self.g.read_html('submenu.form')
            if self.session.data['date_input_mask'] is not None: date_format = self.session.data['date_input_mask']
            else: date_format = self.g.get_config('date_input_mask')
            #If we can't find date_format attribute in config.xml then use a default date format
            if date_format is None or date_format == '':
                date_format = '%d/%m/%Y'
            self.data['date_format'] = date_format
            self.data['data_langs'] = ','.join("%s" % (list(k.keys())[0]) for k in self.data_langs)
            date_format = date_format.replace('%','%%') #avoid letting Python to decode string
            if (who != "people"):
                validate = 'href="javascript:validate(\''+who+'\',\''+date_format+'\')"'
            else:
                validate = 'href="javascript: if (!validateContact()) validate(\''+who+'\',\''+date_format+'\');"'
            self.page_parts['submenu'] = self.page_parts['submenu'].replace('href=""', validate)
        elif action == 'view':
            if self.data['id']:
                self.page_parts['submenu'] = self.g.read_html('submenu.detail')
                #brk(host="localhost", port=9000)
                self.page_parts['hidden_forms'] = self.g.read_html('hidden_forms.detail')
                if (who == 'strains'):
                    self.page_parts['submenu'] = self.page_parts['submenu'].replace("document.getElementById('edit').submit();", "document.getElementById('saveas').value = '0';document.getElementById('edit').submit();")
                    self.page_parts['submenu'] = "<a id=\"saveas_link\" href=\"javascript:document.getElementById('saveas').value = '1';document.getElementById('edit').action = setActiveTab(document.getElementById('edit').action);document.getElementById('edit').submit();\"><img src='../img/record_saveas.png' title=\"%(label_SaveAs)s\" alt=\"%(label_SaveAs)s\"></a>" + self.page_parts['submenu']
                #Security
                #If user does not have permission to delete then don't show the "delete" button
                allow_delete = self.g.get_area_permission(self.cookie_value, self.session, who, 'allow_delete')                
                if self.g.isManager(self.session.data['roles']): #Administrator or Manager
                  allow_delete = 'y'
                if allow_delete != 'y':
                  import re
                  self.page_parts['submenu'] = re.sub('<a id="action_delete" href="javascript:if\(confirm.*?/a>',"",self.page_parts['submenu'])
                #If user does not have permission to edit then don't show the "edit button"                
                allow_edit = self.g.get_item_permission(self.cookie_value, self.session, who, self.data['id'])
                if self.g.isManager(self.session.data['roles']): #Administrator or Manager
                  allow_edit = 'w'
                if allow_edit != 'w':
                  import re
                  self.page_parts['submenu'] = re.sub('<a id="action_edit" href="javascript:document.getElementById\(\'(edit)\'.*?/a>','',self.page_parts['submenu'])
                #If user does not have permission to create new then don't show the "new button"
                allow_create = self.g.get_area_permission(self.cookie_value, self.session, who, 'allow_create')
                if self.g.isManager(self.session.data['roles']): #Administrator or Manager
                  allow_create = 'y'
                if allow_create != 'y':
                  import re
                  self.page_parts['submenu'] = re.sub('<a id="action_new" href="[.]/%\(who\)s[.]new[.]py".*?/a>',"",self.page_parts['submenu'])
                  if who == 'strains': #then don't show the "save as button" too
                    self.page_parts['submenu'] = re.sub('<a id="saveas_link" href="javascript:document.getElementById\(\'(saveas)\'.*?/a>','',self.page_parts['submenu'])
            else:
                print(self.g.redirect(self.list_page % who))

        if who in ('docpopup','refpopup'):
            self.page_parts['top'] = ''
            self.page_parts['hidden_forms'] = ''
            self.page_parts['submenu'] = ''

        #Return specific area
        if who == 'species': return self.species(action)
        elif who == 'strains': return self.strains(action)
        elif who in ('doc','docpopup'): return self.doc(action)
        elif who in ('ref','refpopup'): return self.ref(action)
        elif who == 'institutions': return self.inst(action)
        elif who == 'people': return self.people(action)
        elif who == 'distribution': return self.distribution(action)
        elif who == 'preservation': return self.preservation(action)
        elif who == 'reports': return self.report(action)
        elif who == 'stockmovement': return self.stockmovement(action)
        elif who == 'container': return self.container(action)

    def species_list(self, action, id_species, notnull=False):
        """
        Generate a select/menu of the Species.
        'id_species' is used to set the default value
        'notnull' is used to include blank value or not
        """
        #Use default field order
        self.data['field_order'] = 'taxongroup'
        #Disable paging
        self.data['paging'] = ' ' #Attention: '' is converted to NULL in SQL
        self.data['condition'] = ' ' #Attention: '' is converted to NULL in SQL
        self.data['id_coll'] = self.session.data['id_coll']
        self.data['id_subcoll'] = self.session.data['id_subcoll']
        if self.g.isManager(self.session.data['roles']): #Administrator or Manager
          self.execute('get_species_list', self.data, raw_mode = True)
        else:
          roles = str(self.session.data['roles']).replace("L","")
          roles = roles.replace("[","(")
          roles = roles.replace("]",")")
          self.data['roles_list'] = roles
          self.execute('get_species_list_restrict', self.data,raw_mode = True)
        species_list = self.fetch('all')
        if notnull:
            if action == 'new': species_menu = '\n\t<option selected="selected" value="" group=""></option>'
            else: species_menu = ''
        else:
            if action == 'new': species_menu = '\n\t<option selected="selected" value="" group=""></option>'
            else: species_menu = '\n\t<option value="" group=""></option>'
        #List sorting
        species_list = sorted(species_list, lambda x, y: cmp(Lists.spe_fullname(x, use_author=False), Lists.spe_fullname(y, use_author=False)))
        for species in species_list:
            species_menu += ('\n\t<option %%s value="%s" group="%s">%s</option>'
                            % (species['id_species'], species['id_taxon_group'], Lists.spe_fullname(species, use_author=False).replace("%","%%") ) )
            if species['id_species'] == id_species:
              species_menu = species_menu % self.opt_selected
            else:
              species_menu = species_menu.replace("%s","")
        return species_menu

    def species(self,action):
        '''
        Species == Taxa
        '''
        data = self.data
        data['action'] = action
        data['ambient_risk_langs'] = ""
        data['comments_langs'] = ""
        data['groups_table'] = ""
        data['url_next'] = "<a href='javascript:Proximo(\"species.detail.py?id=%(id)s&row=%(row)s\")'>"
        data['url_prev'] = "<a href='javascript:Anterior(\"species.detail.py?id=%(id)s&row=%(row)s\")'>"
        data['close_link_prev'] = '</a>'
        data['close_link_next'] = '</a>'
        data['img_prev']= ''
        data['img_next']= ''

        if action == 'view': pass
        elif action == 'edit':
            data['title'] = _('Species Edit')
            data['next_action'] = 'update'
        elif action == 'new':
            data['title'] = _('Species New')
            data['next_action'] = 'insert'
            data['back_where'] = 'list'

        data['row_number'] = self.data['row']

        if (action == 'view' and 'row' in self.form):

            #Verify field_order is changed
            if 'field_order' in self.form:
                self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'species', self.form['field_order'].value)

            #Get field and mode for order list
            field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'species')

            stripped_sciname = self.get_stripped("sciname_no_auth")

            if field == 'species':
                field = stripped_sciname + " " + mode
            elif field == 'taxongroup':
                field = 'taxon_group %s' % mode
            else:
                field = field + ' ' + mode

            #Define field_order with mode
            self.data['field_order'] = field

            if (data['row'] == '0'):
                data['paging'] = ' LIMIT %s,2' % data['row']
            else:
                data['paging'] = ' LIMIT %s,3' % str(int(self.data['row']) - 1)

            data['id_lang'] = self.session.data['id_lang']
            data['id_coll'] = self.session.data['id_coll']
            data['id_subcoll'] = self.session.data['id_subcoll']

            #Filter
            filter = ''
            if ('filter' in self.form):
                filter = str(self.form['filter'].value).strip()
                filter = self.ConvertStrUnicode(filter).encode("utf-8")

                #Save filter on session
                self.session.data['filter_species'] = filter
                self.session.save()
            elif ('filter_species' in self.session.data):
                filter = self.session.data['filter_species']
                filter = self.ConvertStrUnicode(filter).encode("utf-8")

            if (filter != ''):
                words = [x for x in filter.split(" ") if x != '']
                self.data['condition']= []
                for word in words:
                    #0x25 == '%'
                    #self.data['condition'].append("AND (tgl.taxon_group LIKE x'25" + word.encode("hex") + "25' OR sp.genus LIKE x'25" + word.encode("hex") + "25' OR sp.subgenus LIKE REPLACE(REPLACE(x'25" + word.encode("hex") + "25', '(', ''), ')', '') OR sp.species LIKE x'25" + word.encode("hex") + "25' OR sub.subdiv LIKE x'25" + word.encode("hex") + "25' OR sp.infra_name LIKE x'25" + word.encode("hex") + "25' OR sp.hazard_group LIKE x'25" + word.encode("hex") + "25') ")
                    self.data['condition'].append(
                                                  "AND (tgl.taxon_group LIKE x'25" + word.encode("hex") + "25' " +
                                                  "OR " + stripped_sciname + " LIKE x'25" + word.encode("hex") + "25' " +
                                                  "OR sp.hazard_group LIKE x'25" + word.encode("hex") + "25') ")
                self.data['condition']= "".join(self.data['condition'])
            else:
                self.data['condition'] = ' '

            #Execute again for rows count
            if self.g.isManager(self.session.data['roles']): #Administrator or Manager
                self.execute('get_species_ids', self.data, True)
            else:
                roles = str(self.session.data['roles']).replace("L","")
                roles = roles.replace("[","(")
                roles = roles.replace("]",")")
                self.data['roles_list'] = roles
                self.execute('get_species_ids_restrict', self.data,raw_mode = True)

            list_species = list(self.fetch('all'))

            i=0
            for specie in list_species:

                if (data['row'] == '0'):
                    if (i == 0):
                        data['img_prev'] = ''
                        data['url_prev'] = ''
                        data['close_link_prev'] = ''
                    else:
                        next_pagination = {}
                        next_pagination['id'] = specie['id_species']
                        next_pagination['row'] = str(int(data['row']) + 1)
                        data['img_next'] = '<img title="'+ _("Next") +'" src="../img/next.gif" border="0">'

                        data['url_next'] = data['url_next'] % next_pagination
                else:
                    if (i == 0):
                        prev_pagination = {}
                        prev_pagination['id'] = specie['id_species']
                        prev_pagination['row'] = str(int(data['row']) - 1)
                        data['img_prev'] = '<img title="'+ _("Previous") +'" src="../img/prev.gif" border="0">'

                        data['url_prev'] = data['url_prev'] % prev_pagination
                    elif (i == 2):
                        next_pagination = {}
                        next_pagination['id'] = specie['id_species']
                        next_pagination['row'] = str(int(data['row']) + 1)
                        data['img_next'] = '<img title="'+ _("Next") +'" src="../img/next.gif" border="0">'

                        data['url_next'] = data['url_next'] % next_pagination

                i = i + 1

            if ((i == 2) and (data['row'] != '0')) or (i < 2 and data['row'] == '0'):
                data['url_next'] = ''
                data['close_link_next'] = ''
                data['img_next'] = ''

        else:
            data['url_next'] = ''
            data['close_link_next'] = ''
            data['img_next'] = ''

            data['img_prev'] = ''
            data['url_prev'] = ''
            data['close_link_prev'] = ''

        is_first = True
        for lang in self.data_langs:
            one_lang = list(lang.keys())[0]
            data['data_lang'] = list(lang.values())[0]
            #Species Data
            self.execute('get_species_data', data)
            species_parts = self.fetch('columns')
            self.logger.debug("species_parts: %s", str(species_parts))
            num_fields = 14

            if len(species_parts) < num_fields:
                species_parts =  DefDict()

            #Alternative State
            data2 = data.copy()
            data2['id'] = species_parts['id_alt_states']

            self.execute('get_species_data', data2)
            fields = self.fetch('columns')
            self.logger.debug("fields: %s", str(fields))
            if len(fields) == num_fields:
                alt_state = Lists.spe_fullname(fields, use_author=False)
            else:
                alt_state = ''

            self.logger.debug("alt state %s", alt_state)

            if is_first:
                data['id_taxon_group'] = species_parts['id_taxon_group']
                data['taxon_group'] = species_parts['taxon_group']
                data['hi_tax'] = species_parts['hi_tax']
                data['sciname'] = species_parts['sciname']
                data['sciname_no_auth'] = species_parts['sciname_no_auth']
                data['synonym'] = species_parts['synonym'] #TextLink
                data['hazard_group'] = species_parts['hazard_group']
                data['hazard_group_ref'] = species_parts['hazard_group_ref'] #TextLink
                #Hide alt_state and alt_state_type field if taxon-group is not one of "fungi" or "yeast"
                if str(species_parts['id_taxon_group']) in ("2","3"):
                  data['alt_state'] = alt_state
                else:
                  data['alt_state'] = "<script language='javascript'>function hideAltState() {document.getElementById('tb_alt_state').style.display='none';}"
                  data['alt_state'] += "addEvent(window, 'load', hideAltState);</script>"
                data['alt_state_type'] = species_parts['alt_state_type']

                #Get hyperlink from data['author']
                textLinkFactoryAuthor = TextLinkFactory(self.cookie_value, self.session.data['id_lang'], data['data_lang'])
                data['message'] = '%s<br /><span class="species"><b>%s</b></span><br />' % (data['taxon_group'], data['sciname'])
                #Security info
                #permissions = self.g.get_permissions(self.cookie_value, 'species', data)

            data['ambient_risk_%s' %one_lang] = species_parts['ambient_risk'] #TextLink
            data['comments_%s' %one_lang] = species_parts['comments'] #TextLink

            if action == 'view':
                self.logger.debug("View")

                textLinksSpeciesMulti = TextLinkFactory(self.cookie_value, self.session.data['id_lang'], data['data_lang'])

                textLinksSpeciesMulti['ambient_risk_%s' %one_lang] = species_parts['ambient_risk'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"")
                textLinksSpeciesMulti['comments_%s' %one_lang] = species_parts['comments'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"")

                #changes textlink to html link
                textLinksSpeciesMulti.fillData(data)
                data['ambient_risk_langs'] += ''' %s: %s<br />
                ''' %("<span class='label_color'>"+one_lang+"</span>", data['ambient_risk_%s' %one_lang])
                data['comments_langs'] += ''' %s: %s<br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['comments_%s' %one_lang])

            else:
                data['ambient_risk_tabs'] = self.generateLanguageTabs('ambient_risk')
                data['comments_tabs'] = self.generateLanguageTabs('comments')

                classtyle = 'block' #change

                data['ambient_risk_langs'] += '''<span class='%s' id='ambient_risk_field_%s'>
                    <textarea id="ambient_risk_%s" name="ambient_risk_%s" class="mceEditor" cols="" rows="">%s</textarea>
                </span>
                ''' %(classtyle, one_lang, one_lang, one_lang, data['ambient_risk_%s' %one_lang])

                data['comments_langs'] += '''<span class='%s' id='comments_field_%s' >
                    <textarea id="comments_%s" name="comments_%s" class="mceEditor" cols="" rows="">%s</textarea>
                </span>
                ''' %(classtyle, one_lang, one_lang, one_lang, data['comments_%s' %one_lang])

                #Load scientific name builder
                from .sciname import SciNameBuilder
                sciname_builder = SciNameBuilder(self.cookie_value)
                id_sciname = species_parts['id_sciname']
                data['id_sciname'] = id_sciname

                self.dbconnection.execute('get_sciname_hierarchy', { 'id_sciname': id_sciname })
                sciname_hierarchy = {}

                for row in self.dbconnection.fetch('all'):
                    sciname_hierarchy[row['id_hierarchy']] = row

                self.logger.debug("Building species")
                self.logger.debug("sciname_hierarchy: %s" % (sciname_hierarchy))
                self.data['sciname_builder'] = sciname_builder.html(self.session.data['id_subcoll'], self.session.data['id_lang'], id_sciname, data['id_taxon_group'], sciname_hierarchy)

            is_first = False

        #Security Tab
        #permissions = self.g.get_permissions(self.cookie_value, 'species', data)
        self.g.security_tab(self.cookie_value, action, data, 'species')

        #Alternative State Type
        if action == 'view':
            if species_parts['alt_state_type'] == 'ana': data['alt_state_type'] = _('Anamorfic')
            elif species_parts['alt_state_type'] == 'teleo': data['alt_state_type'] = _('Teleomorfic')
            textLinksSpecies = TextLinkFactory(self.cookie_value, self.session.data['id_lang'], data['id_lang'])
            textLinksSpecies.update({
                'taxon_ref'       :species_parts['taxon_ref'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\""),
                'synonym'         :species_parts['synonym'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\""),
                'hazard_group_ref':species_parts['hazard_group_ref'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\""),
            })
            textLinksSpecies.fillData(data)

        if action in ('edit','new'):
            #Taxon_ref
            data['taxon_ref'] = species_parts['taxon_ref']

            #Taxon_groups
            tgroups = ''
            self.execute('get_possible_taxon_groups',{'id_subcoll': self.session.data['id_subcoll'], 'id_lang': self.session.data['id_lang']})
            taxon_groups = self.fetch('all')
            for taxon_group in taxon_groups:
                tgroups += '\n\t<option %s value="'+str(taxon_group['id_taxon_group'])+'">'+taxon_group['taxon_group']+'</option>'
                if taxon_group['id_taxon_group'] == data['id_taxon_group']:
                    tgroups = tgroups % self.opt_selected
                else:
                    tgroups = tgroups % ''
            data['taxon_group'] = tgroups

            #Subdivisions -- THIS NO LOGER APPLIES
            #self.execute('get_all_from_table',{'table':'spe_subdiv'})
            #subdivisions = self.fetch('all')
            #List sorting
            #subdivisions = sorted(subdivisions, lambda x, y: cmp(x['subdiv'], y['subdiv']))
            #subdiv_html = ''
            #for subdiv in subdivisions:
            #    subdiv_html += '\n\t<option %%s value="%s">%s</option>' %(subdiv['id_subdiv'], subdiv['subdiv'])
            #    if subdiv['subdiv'] == data['subdiv']:
            #        subdiv_html = subdiv_html % self.opt_selected
            #    else:
            #        subdiv_html = subdiv_html % ''
            #data['subdiv'] = subdiv_html

            #Hazard_groups
            self.execute('get_field_type',{'table':'species','field':'hazard_group'})
            hgroups = self.fetch('columns')
            hgroups = hgroups['Type']
            hgroups = findall('\'.*?\'',hgroups)
            if action == 'new': hgroup_html = self.opt_html_selected
            else: hgroup_html = self.opt_html
            hgroups.sort()
            for hgroup in hgroups:
                hgroup = hgroup.replace('\'','')
                hgroup_html += '\n\t<option %s value="'+hgroup+'">'+hgroup+'</option>'
                if hgroup == data['hazard_group']: hgroup_html = hgroup_html % self.opt_selected
                else: hgroup_html = hgroup_html % ''
            data['hazard_group'] = hgroup_html

            #Name Qualifier
            ##not defined

            #Alternative State
            data['id_alt_states'] = species_parts['id_alt_states']

            #Alternative State Type
            output =  '<option value="ana" %%s>%s</option>' %_("Anamorfic")
            output += '<option value="teleo"  %%s>%s</option>' %_("Teleomorfic")
            if data['alt_state_type'] == 'ana': output = output % (self.opt_selected, '')
            elif data['alt_state_type'] == 'teleo': output = output % ('', self.opt_selected)
            data['alt_state_type'] = output

            #Make js data
            if (action == 'edit'): id_specie = data['id']
            else: id_specie = -1
            data['js_alternate_states'] = self.get_possible_alternate_states(id_specie)

        return data

    def strains(self,action):
        #brk(host="localhost", port=9000)
        data = self.data
        data['action'] = action
        data['coll_host_name_langs'] = ''
        data['coll_substratum_langs'] = ''
        data['coll_comments_langs'] = ''
        data['iso_isolation_from_langs'] = ''
        data['iso_method_langs'] = ''
        data['ident_method_langs'] = ''
        data['cul_medium_langs'] = ''
        data['cul_oxy_req_langs'] = ''
        data['cul_incub_time_langs'] = ''
        data['cul_comments_langs'] = ''
        data['pro_properties_langs'] = ''
        data['pro_applications_langs'] = ''
        data['pro_urls_langs'] = ''
        data['cha_ogm_comments_langs'] = ''
        data['cha_biorisk_comments_langs'] = ''
        data['cha_restrictions_langs'] = ''
        data['cha_pictures_langs'] = ''
        data['cha_urls_langs'] = ''
        data['cha_catalogue_langs'] = ''
        data['groups_table'] = ''
        data['pro_properties_langs'] = ''
        data['pro_applications_langs'] = ''
        data['pro_urls_langs'] = ''
        data['url_next'] = "<a href='javascript:Proximo(\"strains.detail.py?id=%(id)s&row=%(row)s\")'>"
        data['url_prev'] = "<a href='javascript:Anterior(\"strains.detail.py?id=%(id)s&row=%(row)s\")'>"
        data['close_link_prev'] = '</a>'
        data['close_link_next'] = '</a>'
        data['img_prev']= ""
        data['img_next']= ""

        if action == 'edit':
            if (self.form['saveas'].value == '0'):
                data['next_action'] = 'update'
            else:
                data['next_action'] = 'insert'
        elif action == 'new':
            data['next_action'] = 'insert'
            data['back_where'] = 'list'

        data['current_acronym'] = self.session.data['coll_name']

        data['row_number'] = self.data['row']

        if (action == 'view' and 'row' in self.form):

            #Verify field_order is changed
            if 'field_order' in self.form:
                self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'strains', self.form['field_order'].value)

            #Get field and mode for order list
            field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'strains')

            stripped_sciname = self.get_stripped("sciname")

            if field == 'species':
                field = stripped_sciname + ' ' + mode
            elif field == 'code':
                field = "CAST(RIGHT(INSERT(%s, 1, 0, '000000000000000000000000000000'), 30) AS CHAR) %s" % (field, mode)
            else:
                field = field + ' ' + mode

            #Define field_order with mode
            self.data['field_order'] = field

            if (data['row'] == '0'):
                data['paging'] = ' LIMIT %s,2' % data['row']
            else:
                data['paging'] = ' LIMIT %s,3' % str(int(self.data['row']) - 1)

            data['id_lang'] = self.session.data['id_lang']
            data['id_coll'] = self.session.data['id_coll']
            data['id_subcoll'] = self.session.data['id_subcoll']

            filter = ''
            if ('filter_strains' in self.session.data):
                data['filter_strains'] = self.session.data['filter_strains']

            if ('filter' in self.form):
                filter = str(self.form['filter'].value).strip()
                filter = self.ConvertStrUnicode(filter).encode("utf-8")

                #Save filter on session
                self.session.data['filter_strains'] = filter
                self.session.save()
            elif ('filter_strains' in self.session.data):
                filter = self.session.data['filter_strains']
                filter = self.ConvertStrUnicode(filter).encode("utf-8")

            if (filter != ''):
                words = [x for x in filter.split(" ") if x != '']
                self.data['condition']= []

                #Show inactive strains
                if (self.session.data['show_str_inactives'] == 0):
                    self.data['condition'].append("AND (status <> 'inactive')")

                for word in words:
                    #0x25 == '%'
                    self.data['condition'].append(
                                                  "AND (st.code LIKE x'25" + word.encode("hex") + "25' " +
                                                  "OR st.internal_code LIKE x'25" + word.encode("hex") + "25' " +
                                                  "OR " + stripped_sciname + " LIKE x'25" + word.encode("hex") + "25' " +
                                                  "OR ty.type LIKE x'25" + word.encode("hex") + "25' " +
                                                  "OR st.infra_complement LIKE x'25" + word.encode("hex") + "25') ")
                self.data['condition']= "".join(self.data['condition'])
            else:
                if (self.session.data['show_str_inactives'] == 0):
                    self.data['condition'] = "AND (status <> 'inactive')"
                else:
                    self.data['condition'] = ' '

            #Execute again for rows count
            if self.g.isManager(self.session.data['roles']): #Administrator or Manager
                self.execute('get_strain_ids', self.data, True)
            else:
                roles = str(self.session.data['roles']).replace("L","")
                roles = roles.replace("[","(")
                roles = roles.replace("]",")")
                self.data['roles_list'] = roles
                self.execute('get_strain_ids_restrict', self.data,raw_mode = True)


            list_strains = list(self.fetch('all'))

            i=0
            for strain in list_strains:

                if (data['row'] == '0'):
                    if (i == 0):
                        data['img_prev'] = ''
                        data['url_prev'] = ''
                        data['close_link_prev'] = ''
                    else:
                        next_pagination = {}
                        next_pagination['id'] = strain['id_strain']
                        next_pagination['row'] = str(int(data['row']) + 1)
                        data['img_next'] = '<img title="'+ _("Next") +'" src="../img/next.gif" border="0">'

                        data['url_next'] = data['url_next'] % next_pagination
                else:
                    if (i == 0):
                        prev_pagination = {}
                        prev_pagination['id'] = strain['id_strain']
                        prev_pagination['row'] = str(int(data['row']) - 1)
                        data['img_prev'] = '<img title="'+ _("Previous") +'" src="../img/prev.gif" border="0">'

                        data['url_prev'] = data['url_prev'] % prev_pagination
                    elif (i == 2):
                        next_pagination = {}
                        next_pagination['id'] = strain['id_strain']
                        next_pagination['row'] = str(int(data['row']) + 1)
                        data['img_next'] = '<img title="'+ _("Next") +'" src="../img/next.gif" border="0">'

                        data['url_next'] = data['url_next'] % next_pagination

                i = i + 1

            if ((i == 2) and (data['row'] != '0')) or (i < 2 and data['row'] == '0'):
                data['url_next'] = ''
                data['close_link_next'] = ''
                data['img_next'] = ''

        else:
            data['url_next'] = ''
            data['close_link_next'] = ''
            data['img_next'] = ''

            data['img_prev'] = ''
            data['url_prev'] = ''
            data['close_link_prev'] = ''

        is_first = True
        for lang in self.data_langs:            
            one_lang = list(lang.keys())[0]
            data['data_lang'] = list(lang.values())[0]

            #General Data
            self.execute('get_str_general_data', data)
            general = self.fetch('columns')
            self.logger.debug("get_str_general_data: %s" % (general))
            num_fields = 15
            if len(general) < num_fields:
                general = DefDict()

            #Deposit Data
            self.execute('get_str_deposit_data', data)
            deposit = self.fetch('columns')
            num_fields = 17
            if len(deposit) < num_fields:
                 deposit = DefDict()

            #Collection Event Data
            self.execute('get_str_coll_event_data', data)
            coll_event = self.fetch('columns')
            num_fields = 37
            if len(coll_event) < num_fields:
                 coll_event = DefDict()
            #join code_clinic_form+description
            if coll_event['code'] and coll_event['clinical_form']:
                clinic_form = '%s - %s' % (coll_event['code'], coll_event['clinical_form'])
            else:
                clinic_form = '%s%s' % (coll_event['code'], coll_event['clinical_form'])

            #Isolation Data
            self.execute('get_str_isolation_data', data)
            isolation = self.fetch('columns')
            num_fields = 7
            if len(isolation) < num_fields:
                isolation = DefDict()

            #Identification Data
            self.execute('get_str_identification_data', data)
            identification = self.fetch('columns')
            num_fields = 11
            if len(identification) < num_fields:
                identification = DefDict()

            #Culture Data
            self.execute('get_str_culture_data', data)
            culture = self.fetch('columns')
            num_fields = 6
            if len(culture) < num_fields:
                culture = DefDict()

            #Charac Data
            self.execute('get_str_characs_data', data)
            charac = self.fetch('columns')
            num_fields = 13
            if len(charac) < num_fields:
                 charac = DefDict()
            #Seting OGM Name
            ogm_type = charac['ogm']
            if charac['ogm'] == '0':
                 ogm_label = _('Unknown')
            elif charac['ogm'] == '1':
                 ogm_label = _('Group I')
            elif charac['ogm'] == '2':
                 ogm_label = _('Group II')
            else:
                 ogm_label = ''

            #Properties Data
            self.execute('get_str_properties_data', data)
            prop = self.fetch('columns')
            num_fields = 3
            if len(prop) < num_fields:
                 prop = DefDict()

            self.execute('get_sciname_parts_data', { 'id_lang': '1', 'id_sciname': general['id_sciname'], 'id_taxon_group': general['taxon_group'] } )
            parts_dict_aux = self.fetch('all')

            parts_dict = general.copy()
            for row in parts_dict_aux:
                parts_dict[row['rank'].lower()] = row['value']

            self.logger.debug(parts_dict)

            if is_first:
                #General
                if (action == 'edit' and self.form['saveas'].value == '1'):
                    data['code'] = ""
                    data['status'] = ""
                else:
                    data['code'] = general['code']

                data['numeric_code'] = general['numeric_code']
                data['division'] = general['division']

                data['internal_code'] = general['internal_code']
                data['id_species'] = general['id_species']
                data['sciname'] = general['sciname']
                data['hi_tax'] = general['hi_tax']
                #Prepare link to external dictionary as well
                self.logger.debug("data: %s" % (data))
                data['species'] = Lists.spe_fullname(parts_dict,data,self.session.data['label_lang_code'])
                data['spe_taxon_group'] = general['taxon_group']

                data['id_type'] = general['id_type']
                if (general['is_ogm']):
                  data['is_ogm'] = _("Yes")
                  data['is_ogm_check'] = "checked='checked'"
                else:
                  data['is_ogm'] = _("No")
                  data['is_ogm_check'] = ""
                data['infra_complement'] = general['infra_complement']
                if (general['go_catalog']):
                  data['label_go_catalog'] = _("This strain goes to catalog")
                  data['is_go_catalog_check'] = "checked='checked'"
                else:
                  data['label_go_catalog'] = ''
                  data['is_go_catalog_check'] = ""
                data['type'] = general['type']
                data['status'] = general['status'].capitalize()
                if action == 'view':
                    if data['status'] == 'Active': data['status'] = _("Active")
                    elif data['status'] == 'Inactive': data['status'] = _("Inactive")
                    elif data['status'] == 'Pending' : data['status'] = _("Pending")
                data['history'] = general['history'].replace("<a","<a class=\"tlink\"")
                data['extra_codes'] = general['extra_codes'].replace("<a","<a class=\"tlink\"")
                data['general_comments'] = general['comments'].replace("<a","<a class=\"tlink\"")
                data['message'] = '<b>%s</b><br /><span class="species">%s</span><br />%s' % (data['code'], data['species'], '')
                #data['message'] %= ('<a href="http://names.cria.org.br/index?%(sp_dictionary)s" target="_blank" ><img src="../img/sp.png" /></a> ' % data)
                #Deposit
                data['dep_id_person'] = deposit['id_person']
                data['dep_person'] = deposit['name']
                data['dep_id_institution'] = deposit['id_institution']
                data['dep_institution'] = deposit['name_institution']
                data['dep_genus'] = deposit['genus'].replace('"','&quot;').replace("'","&#39;")
                data['dep_species'] = deposit['species'].replace('"','&quot;').replace("'","&#39;")
                data['dep_classification'] = deposit['classification'].replace('"','&quot;').replace("'","&#39;")
                data['dep_infra_name'] = deposit['infra_name'].replace('"','&quot;').replace("'","&#39;")
                data['dep_infra_complement'] = deposit['infra_complement'].replace('"','&quot;').replace("'","&#39;")
                data['dep_date'] = self.format_date(action,deposit['date'])
                data['dep_id_reason'] = deposit['id_dep_reason']
                data['dep_reason'] = deposit['dep_reason']
                data['dep_preserv_method'] = deposit['preserve_method'].replace("<a","<a class=\"tlink\"")
                data['dep_form'] = deposit['form'].replace('"','&quot;').replace("'","&#39;")
                data['dep_aut_date'] = self.format_date(action, deposit['aut_date'])
                data['dep_aut_id_person'] = deposit['aut_id_person']
                data['dep_aut_person'] = deposit['aut_person']
                data['dep_aut_result'] = deposit['aut_result'] #TextLink
                data['dep_comments'] = deposit['comments'].replace("<a","<a class=\"tlink\"")

                #Collection Event
                data['coll_id_person'] = coll_event['id_person']
                data['coll_person'] = coll_event['name']
                data['coll_id_institution'] = coll_event['id_institution']
                data['coll_institution'] = coll_event['name_institution']
                data['coll_date'] = self.format_date(action,coll_event['date'])
                data['coll_id_country'] = coll_event['id_country']
                data['coll_id_state'] = coll_event['id_state']
                if coll_event['country_code'] != '': data['coll_country'] = coll_event['country'] + ' ('+coll_event['country_code']+')'
                else: data['coll_country'] = coll_event['country']
                if coll_event['state_code'] != '' : data['coll_state'] = coll_event['state'] + ' ('+coll_event['state_code']+')'
                else: data['coll_state'] = coll_event['state']
                data['coll_id_city'] = coll_event['id_city']
                data['coll_city'] = coll_event['city']
                data['coll_place'] = coll_event['place'].replace("<a","<a class=\"tlink\"")
                #Adjust Gps_precision format
                gpsPres = str(coll_event['gps_precision'])
                if gpsPres != '':
                    while len(gpsPres) < 5:
                        gpsPres = '0' + gpsPres
                data['coll_gps_precision'] = gpsPres
                data['coll_id_gps_datum'] = coll_event['id_gps_datum']
                data['coll_gps_datum'] = coll_event['gps_datum']
                data['coll_gps_comments'] = coll_event['gps_comments'].replace("<a","<a class=\"tlink\"")
                data['coll_host_genus'] = coll_event['host_genus'].replace('"','&quot;').replace("'","&#39;")
                data['coll_host_species'] = coll_event['host_species'].replace('"','&quot;').replace("'","&#39;")
                data['coll_host_classification'] = coll_event['host_classification'].replace('"','&quot;').replace("'","&#39;")
                data['coll_host_infra_name'] = coll_event['host_infra_name'].replace('"','&quot;').replace("'","&#39;")
                data['coll_host_infra_complement'] = coll_event['host_infra_complement'].replace('"','&quot;').replace("'","&#39;")
                data['coll_global_code'] = coll_event['global_code']
                data['coll_id_clinical_form'] = coll_event['id_clinical_form']
                data['coll_clinical_form'] = clinic_form
                data['coll_hiv'] = coll_event['hiv']

                if (str(data['spe_taxon_group']) != "5"):
                    data['hide_div'] = '<script language="javascript" type="text/javascript">document.getElementById("specific_for_protozoa").style.display = "none";</script>'

                #Security info
                #permissions = self.g.get_permissions(self.cookie_value, 'strains', data)

            data['coll_host_name_%s' %one_lang] = coll_event['host_name'] #TextLink
            data['coll_substratum_%s' %one_lang] = coll_event['substratum'] #TextLink
            data['coll_comments_%s' %one_lang] = coll_event['comments'] #TextLink

            data['iso_isolation_from_%s' %one_lang] = isolation['iso_isolation_from'] #TextLink
            data['iso_method_%s' %one_lang] = isolation['iso_method'] #TextLink

            data['ident_method_%s' %one_lang] = identification['ident_method'] #TextLink

            data['pro_properties_%s' %one_lang] = prop['properties'] #TextLink
            data['pro_applications_%s' %one_lang] = prop['applications'] #TextLink
            data['pro_urls_%s' %one_lang] = prop['urls'] #TextLink

            if action == 'view':
                if is_first:
                  #Format GPS
                  #Latitude
                  if coll_event['gps_latitude_mode'] == 'dms':
                    data['coll_gps_latitude'] = '<span class="uppercase">'+coll_event['gps_latitude_dms'] + ' ('+str(coll_event['gps_latitude']).strip('0.')+')'+'</span>'
                  elif coll_event['gps_latitude_mode'] == 'decimal': #decimal
                    data['coll_gps_latitude'] = '<span class="uppercase">'+str(coll_event['gps_latitude']).strip('0.') + ' ('+coll_event['gps_latitude_dms']+')'+'</span>'
                  else:
                    data['coll_gps_latitude'] = ''
                  #Longitude
                  if coll_event['gps_longitude_mode'] == 'dms':
                    data['coll_gps_longitude'] = '<span class="uppercase">'+coll_event['gps_longitude_dms'] + ' ('+str(coll_event['gps_longitude']).strip('0.')+')'+'</span>'
                  elif coll_event['gps_longitude_mode'] == 'decimal': #decimal
                    data['coll_gps_longitude'] = '<span class="uppercase">'+str(coll_event['gps_longitude']).strip('0.') + ' ('+coll_event['gps_longitude_dms']+')'+'</span>'
                  else:
                    data['coll_gps_longitude'] = ''

                textLinksStrainMulti = TextLinkFactory(self.cookie_value, self.session.data['id_lang'], data['data_lang'])

                textLinksStrainMulti['coll_host_name_%s' %one_lang] = coll_event['host_name'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"")
                textLinksStrainMulti['coll_substratum_%s' %one_lang] = coll_event['substratum'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"")
                textLinksStrainMulti['coll_comments_%s' %one_lang] = coll_event['comments'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"")

                textLinksStrainMulti.fillData(data)

                data['coll_host_name_langs'] += '''%s: %s<br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['coll_host_name_%s'%one_lang])
                data['coll_substratum_langs'] += '''%s: %s<br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['coll_substratum_%s'%one_lang])
                data['coll_comments_langs'] += '''%s: %s<br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['coll_comments_%s'%one_lang])
            else:
                if is_first:
                  #Format GPS
                  #Latitude
                  if coll_event['gps_latitude_mode'] == 'dms':
                    data['coll_gps_latitude'] = coll_event['gps_latitude_dms'].replace('"','&quot;')
                  else: #decimal
                    data['coll_gps_latitude'] = coll_event['gps_latitude']
                  #Longitude
                  if coll_event['gps_longitude_mode'] == 'dms':
                    data['coll_gps_longitude'] = coll_event['gps_longitude_dms'].replace('"','&quot;')
                  else: #decimal
                    data['coll_gps_longitude'] = coll_event['gps_longitude']

                data['coll_host_name_tabs'] = self.generateLanguageTabs('coll_host_name')
                data['coll_substratum_tabs'] = self.generateLanguageTabs('coll_substratum')
                data['coll_comments_tabs'] = self.generateLanguageTabs('coll_comments')

                classtyle = 'block' #change

                data['coll_host_name_langs'] += '''<span class='%s' id='coll_host_name_field_%s' >
                    <textarea name="coll_host_name_%s" id="coll_host_name_%s" class="mceEditor" cols="" rows="">%s</textarea>
                </span>
                ''' %(classtyle, one_lang, one_lang, one_lang, data['coll_host_name_%s' %one_lang])

                data['coll_substratum_langs'] += '''<span class='%s' id='coll_substratum_field_%s' >
                    <textarea name="coll_substratum_%s" id="coll_substratum_%s" class="mceEditor" cols="" rows="">%s</textarea>
                </span>
                '''%(classtyle, one_lang, one_lang, one_lang, data['coll_substratum_%s' %one_lang])

                data['coll_comments_langs'] += '''<span class='%s' id='coll_comments_field_%s' >
                    <textarea name="coll_comments_%s" id="coll_comments_%s" class="mceEditor" cols="" rows="">%s</textarea>
                </span>
                '''%(classtyle, one_lang, one_lang, one_lang, data['coll_comments_%s' %one_lang])

            #Isolation
            if is_first:
                data['iso_id_person'] = isolation['id_person']
                data['iso_person'] = isolation['name']
                data['iso_id_institution'] = isolation['id_institution']
                data['iso_institution'] = isolation['name_institution']
                data['iso_date'] = self.format_date(action,isolation['date'])
                data['iso_comments'] = isolation['comments'] #TextLink

            if action == 'view':
                textLinksStrainMulti = TextLinkFactory(self.cookie_value, self.session.data['id_lang'], data['data_lang'])

                textLinksStrainMulti['iso_isolation_from_%s' %one_lang] = isolation['iso_isolation_from'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"")
                textLinksStrainMulti['iso_method_%s' %one_lang] = isolation['iso_method'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"")

                textLinksStrainMulti.fillData(data)

                data['iso_isolation_from_langs'] += '''%s: %s<br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['iso_isolation_from_%s'%one_lang])

                data['iso_method_langs'] += '''%s: %s<br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['iso_method_%s'%one_lang])
            else:
                data['iso_isolation_from_tabs'] = self.generateLanguageTabs('iso_isolation_from')
                data['iso_method_tabs'] = self.generateLanguageTabs('iso_method')

                classtyle = 'block' #change

                data['iso_isolation_from_langs'] += '''<span class='%s' id='iso_isolation_from_field_%s' >
                    <textarea name="iso_isolation_from_%s" id="iso_isolation_from_%s" class="mceEditor" cols="" rows="">%s</textarea>
                </span>
                '''%(classtyle, one_lang, one_lang, one_lang, data['iso_isolation_from_%s' %one_lang])

                data['iso_method_langs'] += '''<span class='%s' id='iso_method_field_%s' >
                    <textarea name="iso_method_%s" id="iso_method_%s" class="mceEditor" cols="" rows="">%s</textarea>
                </span>
                '''%(classtyle, one_lang, one_lang, one_lang, data['iso_method_%s' %one_lang])

            #Identification
            if is_first:
                data['ident_date'] = self.format_date(action,identification['date'])
                data['ident_id_person'] = identification['id_person']
                data['ident_person'] = identification['name']
                data['ident_id_institution'] = identification['id_institution']
                data['ident_institution'] = identification['name_institution']
                data['ident_genus'] = identification['genus'].replace('"','&quot;').replace("'","&#39;")
                data['ident_species'] = identification['species'].replace('"','&quot;').replace("'","&#39;")
                data['ident_classification'] = identification['classification'].replace('"','&quot;').replace("'","&#39;")
                data['ident_infra_name'] = identification['infra_name'].replace('"','&quot;').replace("'","&#39;")
                data['ident_infra_complement'] = identification['infra_complement'].replace('"','&quot;').replace("'","&#39;")
                data['ident_comments'] = identification['comments'] #TextLink

            if action == 'view':
                textLinksStrainMulti = TextLinkFactory(self.cookie_value, self.session.data['id_lang'], data['data_lang'])

                textLinksStrainMulti['ident_method_%s' % one_lang] = identification['ident_method'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"")

                textLinksStrainMulti.fillData(data)

                data['ident_method_langs'] += '''%s: %s<br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['ident_method_%s'%one_lang])
            else:
                data['ident_method_tabs'] = self.generateLanguageTabs('ident_method')

                classtyle = 'block'

                data['ident_method_langs'] += '''<span class='%s' id='ident_method_field_%s' >
                    <textarea name="ident_method_%s" id="ident_method_%s" class="mceEditor" cols="" rows="">%s</textarea>
                </span>
                '''%(classtyle, one_lang, one_lang, one_lang, data['ident_method_%s' % one_lang])

            #Culture
            if is_first:
                data['cul_temp'] = culture['temp'].replace('"','&quot;').replace("'","&#39;")
                data['cul_ph'] = culture['ph'].replace('"','&quot;').replace("'","&#39;")

            data['cul_medium_%s' %one_lang] = culture['medium'] #TextLink
            data['cul_incub_time_%s' %one_lang] = culture['incub_time'].replace('"','&quot;').replace("'","&#39;")
            data['cul_oxy_req_%s' %one_lang] = culture['oxy_req'].replace('"','&quot;').replace("'","&#39;")
            data['cul_comments_%s' %one_lang] = culture['comments'] #TextLink

            if action == 'view':
                textLinksStrainMulti = TextLinkFactory(self.cookie_value, self.session.data['id_lang'], data['data_lang'])

                textLinksStrainMulti['cul_medium_%s' %one_lang] = culture['medium'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"")
                textLinksStrainMulti['cul_incub_time_%s' %one_lang] = culture['incub_time'].replace("%","%%")
                textLinksStrainMulti['cul_oxy_req_%s' %one_lang] = culture['oxy_req'].replace("%","%%")
                textLinksStrainMulti['cul_comments_%s' %one_lang] = culture['comments'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"")

                textLinksStrainMulti.fillData(data)

                data['cul_medium_langs'] += '''%s: %s<br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['cul_medium_%s' %one_lang])
                data['cul_incub_time_langs'] += '''%s: %s <br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['cul_incub_time_%s' %one_lang])
                data['cul_oxy_req_langs'] += '''%s: %s <br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['cul_oxy_req_%s' %one_lang])
                data['cul_comments_langs'] += '''%s: %s <br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['cul_comments_%s' %one_lang])
            else:
                data['cul_medium_tabs'] = self.generateLanguageTabs('cul_medium')
                data['cul_incub_time_tabs'] = self.generateLanguageTabs('cul_incub_time')
                data['cul_oxy_req_tabs'] = self.generateLanguageTabs('cul_oxy_req')
                data['cul_comments_tabs'] = self.generateLanguageTabs('cul_comments')

                classtyle = 'block' #change

                data['cul_medium_langs'] += '''<span class='%s' id='cul_medium_field_%s' >
                    <textarea name="cul_medium_%s" id="cul_medium_%s" class="mceEditor" cols="" rows="">%s</textarea>
                </span>
                ''' %(classtyle, one_lang, one_lang, one_lang, data['cul_medium_%s' %one_lang])

                data['cul_incub_time_langs'] += '''<span class='%s' id='cul_incub_time_field_%s' >
                    <input name="cul_incub_time_%s" id="cul_incub_time_%s" type="text" maxlength="50" value="%s" /><br />
                </span>
                '''%(classtyle, one_lang, one_lang, one_lang, data['cul_incub_time_%s' %one_lang])

                data['cul_oxy_req_langs'] += '''<span class='%s' id='cul_oxy_req_field_%s' >
                    <input name="cul_oxy_req_%s" id="cul_oxy_req_%s" type="text" maxlength="50" value="%s" /><br />
                </span>
                '''%(classtyle, one_lang, one_lang, one_lang, data['cul_oxy_req_%s' %one_lang])

                data['cul_comments_langs'] += '''<span class='%s' id='cul_comments_field_%s' >
                    <textarea name="cul_comments_%s" id="cul_comments_%s" class="mceEditor" cols="" rows="">%s</textarea>
                </span>
                '''%(classtyle, one_lang, one_lang, one_lang, data['cul_comments_%s' %one_lang])

            if is_first:
                #Characteristics
                data['cha_biochemical'] = charac['biochemical'] #TextLink
                data['cha_immunologic'] = charac['immunologic'] #TextLink
                data['cha_morphologic'] = charac['morphologic'] #TextLink
                data['cha_molecular'] = charac['molecular'] #TextLink
                data['cha_pathogenic'] = charac['pathogenic'] #TextLink
                data['cha_genotypic'] = charac['genotypic'] #TextLink
                data['cha_ogm'] = ogm_type
                data['cha_ogm_label'] = ogm_label

            data['cha_ogm_comments_%s'%one_lang] = charac['ogm_comments'] #TextLink
            data['cha_biorisk_comments_%s'%one_lang] = charac['biorisk_comments'] #TextLink
            data['cha_restrictions_%s'%one_lang] = charac['restrictions'] #TextLink
            data['cha_pictures_%s'%one_lang] = charac['pictures'] #TextLink
            data['cha_urls_%s'%one_lang] = charac['urls'] #TextLink
            data['cha_catalogue_%s'%one_lang] = charac['catalogue_notes'] #TextLink

            if action == 'view':

                textLinksStrainMulti = TextLinkFactory(self.cookie_value, self.session.data['id_lang'], data['data_lang'])

                textLinksStrainMulti['cha_ogm_comments_%s'%one_lang] = charac['ogm_comments'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"") #TextLink
                textLinksStrainMulti['cha_biorisk_comments_%s'%one_lang] = charac['biorisk_comments'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"") #TextLink
                textLinksStrainMulti['cha_restrictions_%s'%one_lang] = charac['restrictions'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"") #TextLink
                textLinksStrainMulti['cha_pictures_%s'%one_lang] = charac['pictures'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"") #TextLink
                textLinksStrainMulti['cha_urls_%s'%one_lang] = charac['urls'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"") #TextLink
                textLinksStrainMulti['cha_catalogue_%s'%one_lang] = charac['catalogue_notes'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"") #TextLink

                textLinksStrainMulti.fillData(data)

                data['cha_ogm_comments_langs'] += '''%s: %s<br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['cha_ogm_comments_%s'%one_lang])
                data['cha_biorisk_comments_langs'] += '''%s: %s<br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['cha_biorisk_comments_%s'%one_lang])
                data['cha_restrictions_langs'] += '''%s: %s<br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['cha_restrictions_%s'%one_lang])
                data['cha_pictures_langs'] += '''%s: %s<br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['cha_pictures_%s'%one_lang])
                data['cha_urls_langs'] += '''%s: %s<br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['cha_urls_%s'%one_lang])
                data['cha_catalogue_langs'] += '''%s: %s<br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['cha_catalogue_%s'%one_lang])

            else:
                data['cha_ogm_comments_tabs'] = self.generateLanguageTabs('cha_ogm_comments')
                data['cha_biorisk_comments_tabs'] = self.generateLanguageTabs('cha_biorisk_comments')
                data['cha_restrictions_tabs'] = self.generateLanguageTabs('cha_restrictions')
                data['cha_pictures_tabs'] = self.generateLanguageTabs('cha_pictures')
                data['cha_urls_tabs'] = self.generateLanguageTabs('cha_urls')
                data['cha_catalogue_tabs'] = self.generateLanguageTabs('cha_catalogue')

                classtyle = 'block' #change

                data['cha_ogm_comments_langs'] += '''<span class='%s' id='cha_ogm_comments_field_%s' >
                    <textarea name="cha_ogm_comments_%s" id="cha_ogm_comments_%s" class="mceEditor" cols="" rows="">%s</textarea>
                </span>
                '''%(classtyle, one_lang, one_lang, one_lang, data['cha_ogm_comments_%s' %one_lang])

                data['cha_biorisk_comments_langs'] += '''<span class='%s' id='cha_biorisk_comments_field_%s' >
                    <textarea name="cha_biorisk_comments_%s" id="cha_biorisk_comments_%s" class="mceEditor" cols="" rows="">%s</textarea>
                </span>
                '''%(classtyle, one_lang, one_lang, one_lang, data['cha_biorisk_comments_%s' %one_lang])

                data['cha_restrictions_langs'] += '''<span class='%s' id='cha_restrictions_field_%s' >
                    <textarea name="cha_restrictions_%s" id="cha_restrictions_%s" class="mceEditor" cols="" rows="">%s</textarea>
                </span>
                '''%(classtyle, one_lang, one_lang, one_lang, data['cha_restrictions_%s' %one_lang])

                data['cha_pictures_langs'] += '''<span class='%s' id='cha_pictures_field_%s' >
                    <textarea name="cha_pictures_%s" id="cha_pictures_%s" class="mceEditor" cols="" rows="">%s</textarea>
                </span>
                '''%(classtyle, one_lang, one_lang, one_lang, data['cha_pictures_%s' %one_lang])

                data['cha_urls_langs'] += '''<span class='%s' id='cha_urls_field_%s' >
                    <textarea name="cha_urls_%s" id="cha_urls_%s" class="mceEditor" cols="" rows="">%s</textarea>
                </span>
                '''%(classtyle, one_lang, one_lang, one_lang, data['cha_urls_%s' %one_lang])

                data['cha_catalogue_langs'] += '''<span class='%s' id='cha_catalogue_field_%s' >
                    <textarea name="cha_catalogue_%s" id="cha_catalogue_%s" class="mceEditor" cols="" rows="">%s</textarea>
                </span>
                '''%(classtyle, one_lang, one_lang, one_lang, data['cha_catalogue_%s' %one_lang])

            #Properties
            data['pro_properties_%s'%one_lang] = prop['properties'] #TextLink
            data['pro_applications_%s'%one_lang] = prop['applications'] #TextLink
            data['pro_urls_%s'%one_lang] = prop['urls'] #TextLink

            if action == 'view':
                textLinksStrainMulti = TextLinkFactory(self.cookie_value, self.session.data['id_lang'], data['data_lang'])

                textLinksStrainMulti['pro_properties_%s' %one_lang] = prop['properties'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"")
                textLinksStrainMulti['pro_applications_%s' %one_lang] = prop['applications'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"")
                textLinksStrainMulti['pro_urls_%s' %one_lang] = prop['urls'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"")

                textLinksStrainMulti.fillData(data)

                data['pro_properties_langs'] += '''%s: %s<br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['pro_properties_%s'%one_lang])
                data['pro_applications_langs'] += '''%s: %s<br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['pro_applications_%s'%one_lang])
                data['pro_urls_langs'] += '''%s: %s<br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['pro_urls_%s'%one_lang])
            else:
                data['pro_properties_tabs'] = self.generateLanguageTabs('pro_properties')
                data['pro_applications_tabs'] = self.generateLanguageTabs('pro_applications')
                data['pro_urls_tabs'] = self.generateLanguageTabs('pro_urls')

                classtyle = 'block' #change

                data['pro_properties_langs'] += '''<span class='%s' id='pro_properties_field_%s' >
                    <textarea name="pro_properties_%s" id="pro_properties_%s" class="mceEditor" cols="" rows="">%s</textarea>
                </span>
                '''%(classtyle, one_lang, one_lang, one_lang, data['pro_properties_%s' %one_lang])

                data['pro_applications_langs'] += '''<span class='%s' id='pro_applications_field_%s' >
                    <textarea name="pro_applications_%s" id="pro_applications_%s" class="mceEditor" cols="" rows="">%s</textarea>
                </span>
                '''%(classtyle, one_lang, one_lang, one_lang, data['pro_applications_%s' %one_lang])

                data['pro_urls_langs'] += '''<span class='%s' id='pro_urls_field_%s' >
                    <textarea name="pro_urls_%s" id="pro_urls_%s" class="mceEditor" cols="" rows="">%s</textarea>
                </span>
                '''%(classtyle, one_lang, one_lang, one_lang, data['pro_urls_%s' %one_lang])

            is_first = False

        #Security Tab
        self.g.security_tab(self.cookie_value, action, data, 'strains')

        if action in ('edit','new'):
            #Species
            data['species'] = self.species_list(action, data['id_species'], True)

            #Strain Type
            self.execute('get_str_type_subcoll', data)
            types = self.fetch('all')
            type_menu = []
            if action == 'new': type_menu.append(self.opt_html_selected)
            else: type_menu.append(self.opt_html)
            for s_type in types:
                if s_type['id_type'] == data['id_type']:
                  type_menu.append('\n\t<option %s value="%s">%s</option>' % (self.opt_selected, s_type['id_type'], s_type['type']))
                else:
                  type_menu.append('\n\t<option value="%s">%s</option>' % (s_type['id_type'], s_type['type']))
            data['type'] = "".join(type_menu)

            #Strain Division
            from .strain_formatter import StrainFormatter
            s = StrainFormatter(self.cookie_value)
            data['division'] = s.division_select_options(self.session.data['id_subcoll'], general['id_division'])

            #Strain status
            self.execute('get_field_type',{'table':'strain','field':'status'})
            column_descriptions = self.fetch('columns')
            status_list = column_descriptions['Type']
            status_list = status_list[6:-2].split("','")
            tstatus = ''
            status_list.sort()
            for status in status_list:
                #Translate status
                status_translated = ''
                if status == 'active': status_translated = _("Active")
                elif status == 'inactive': status_translated = _("Inactive")
                elif status == 'pending': status_translated = _("Pending")
                else: status_translated = str(status).capitalize()
                tstatus += '\n\t<option %s value="'+status+'">'+status_translated+'</option>'
                if str(status) == str(data['status'].lower()): tstatus = tstatus % self.opt_selected
                else: tstatus = tstatus % ''
            data['status'] = tstatus

            #Person
            self.execute('get_person')
            people = self.fetch('all')
            if action == 'new':
                people_menu_1 = [self.opt_html_selected]
                people_menu_2 = [self.opt_html_selected]
                people_menu_3 = [self.opt_html_selected]
                people_menu_4 = [self.opt_html_selected]
                people_menu_5 = [self.opt_html_selected]
            else:
                people_menu_1 = [self.opt_html]
                people_menu_2 = [self.opt_html]
                people_menu_3 = [self.opt_html]
                people_menu_4 = [self.opt_html]
                people_menu_5 = [self.opt_html]

            for person in people:
                if person['id_person'] == data['dep_id_person']:
                    people_menu_1.append('\n\t<option %s value="%s">%s</option>' % (self.opt_selected, person['id_person'], person['name']))
                else:
                    people_menu_1.append('\n\t<option value="%s">%s</option>' % (person['id_person'], person['name']))
                if person['id_person'] == data['coll_id_person']:
                    people_menu_2.append('\n\t<option %s value="%s">%s</option>' % (self.opt_selected, person['id_person'], person['name']))
                else:
                    people_menu_2.append('\n\t<option value="%s">%s</option>' % (person['id_person'], person['name']))
                if person['id_person'] == data['iso_id_person']:
                    people_menu_3.append('\n\t<option %s value="%s">%s</option>' % (self.opt_selected, person['id_person'], person['name']))
                else:
                    people_menu_3.append('\n\t<option value="%s">%s</option>' % (person['id_person'], person['name']))
                if person['id_person'] == data['dep_aut_id_person']:
                    people_menu_4.append('\n\t<option %s value="%s">%s</option>' % (self.opt_selected, person['id_person'], person['name']))
                else:
                    people_menu_4.append('\n\t<option value="%s">%s</option>' % (person['id_person'], person['name']))
                if person['id_person'] == data['ident_id_person']:
                    people_menu_5.append('\n\t<option %s value="%s">%s</option>' % (self.opt_selected, person['id_person'], person['name']))
                else:
                    people_menu_5.append('\n\t<option value="%s">%s</option>' % (person['id_person'], person['name']))

            data['dep_person'] = "".join(people_menu_1)
            data['coll_person'] = "".join(people_menu_2)
            data['iso_person'] = "".join(people_menu_3)
            data['dep_aut_person'] = "".join(people_menu_4)
            data['ident_person'] = "".join(people_menu_5)

            #Institution
            data['dep_institution'] = self.get_inst_option_list (data['dep_id_institution'])
            data['coll_institution'] = self.get_inst_option_list (data['coll_id_institution'])
            data['iso_institution'] = self.get_inst_option_list (data['iso_id_institution'])
            data['ident_institution'] = self.get_inst_option_list (data['ident_id_institution'])

            #Deposit Reason
            self.execute('get_str_dep_reason_subcoll', data)
            reasons = self.fetch('all')
            reason_menu = []
            if action == 'new':
                reason_menu.append(self.opt_html_selected)
            else:
                reason_menu.append(self.opt_html)
            for reason in reasons:
                if reason['id_dep_reason'] == data['dep_id_reason']:
                  reason_menu.append('\n\t<option %s value="%s">%s</option>' % (self.opt_selected, reason['id_dep_reason'], reason['dep_reason']))
                else:
                  reason_menu.append('\n\t<option value="%s">%s</option>' % (reason['id_dep_reason'], reason['dep_reason']))
            data['dep_reason'] = "".join(reason_menu)

            #Countries, States and Cities
            self.execute('get_country', data)
            countries = self.fetch('all')
            countries_menu = []
            if action == 'new': countries_menu.append(self.opt_html_selected)
            else: countries_menu.append(self.opt_html)
            #Check whether country-state-city (csc.js) javascript file exists
            from os import path
            js_csc = path.join(self.g.get_config("root_dir"),self.g.get_config("js_dir"),"csc_%s.js" % self.session.data['db_name'])
            if (path.exists(js_csc)):
              for country in countries:
                  countries_menu.append('\n\t<option value="%s">%s</option>' % (country['id_country'], country['country']+" ("+country['code']+")"))
              data['coll_country'] = "".join(countries_menu)
              f = open(js_csc, 'r')
              data['js_country_state_city'] = f.read()
              f.close()
            else:
              js_country_state = [] #Javascript array
              js_state_city = [] #Javascript array
              for country in countries:
                  countries_menu.append('\n\t<option value="%s">%s</option>' % (country['id_country'], country['country']+" ("+country['code']+")"))
                  #Get states from this country in order to create dynamic javascript
                  self.execute('get_country_states',country)
                  states = self.fetch('all')
                  js_country_state.append("country_state["+str(country['id_country'])+"]={\"name\":\""+country['country']+" ("+country['code']+")"+"\"")
                  for state in states:
                      js_country_state.append(","+str(state['id_state'])+":\""+state['state']+" ("+state['code']+")\"")
                      #Get cities from this state in order to create dynamic javascript
                      self.execute('get_state_cities',state)
                      cities = self.fetch('all')
                      #Create JS array using Python's List Comprehension
                      js_state_city.append("state_city["+str(state['id_state'])+"]={" + ",".join([str(city['id_city'])+":\""+city['city']+"\"" for city in cities]) + "};\n\t")
                  js_country_state.append("};\n\t")
              data['coll_country'] = "".join(countries_menu)
              #Fix unusual case when a state has no cities...
              js_state_city = "".join(js_state_city).replace("{}","null");
              #Add dynamic javascript to data dictionary
              data['js_country_state_city'] = "".join(js_country_state) + js_state_city
              ###########################################
              # Save csc.js file to improve performance #
              ###########################################
              f = open(js_csc, 'w')
              f.write(data['js_country_state_city'].encode('utf8'))
              f.close()

            #If we are on edit mode, make some adjustments
            #Country
            if (data['coll_id_country']):
                data['js_data_country'] = str(data['coll_id_country'])
            else:
                data['js_data_country'] = '0'
            #State
            if (data['coll_id_state']):
                data['js_data_state'] = str(data['coll_id_state'])
                self.execute('get_state_name',data)
                states = self.fetch('all')
                states = states[0]
                data['selected_coll_state'] = states['state']+' ('+states['code']+')'
            else:
                data['js_data_state'] = '0'
                data['selected_coll_state'] = ''
            #City
            if (data['coll_id_city']):
                data['js_data_city'] = str(data['coll_id_city'])
                self.execute('get_city_name',data)
                data['selected_coll_city'] = self.dbconnection.fetch('one')
            else:
                data['js_data_city'] = '0'
                data['selected_coll_city'] = ''

            #GPS Datums
            self.execute('get_str_gps_datum')
            datums = self.fetch('all')
            datums_menu = []
            if action == 'new': datums_menu.append(self.opt_html_selected)
            else: datums_menu.append(self.opt_html)
            for datum in datums:
                if datum['id_gps_datum'] == data['coll_id_gps_datum']:
                  datums_menu.append('\n\t<option %s value="%s">%s</option>' % (self.opt_selected, datum['id_gps_datum'], datum['gps_datum']))
                else:
                  datums_menu.append('\n\t<option value="%s">%s</option>' % (datum['id_gps_datum'], datum['gps_datum']))
            data['coll_gps_datum'] = "".join(datums_menu)

            #Clinic Form
            self.execute('get_str_clinical_form', data)
            clinics = self.fetch('all')
            clinics_menu = []
            if action == 'new': clinics_menu.append(self.opt_html_selected)
            else: clinics_menu.append(self.opt_html)
            for clinic in clinics:
                if clinic['id_clinical_form'] == data['coll_id_clinical_form']:
                  clinics_menu.append('\n\t<option %s value="%s">%s</option>' % (self.opt_selected,clinic['id_clinical_form'], clinic['clinical_form']))
                else:
                  clinics_menu.append('\n\t<option value="%s">%s</option>' % (clinic['id_clinical_form'], clinic['clinical_form']))
            data['coll_clinical_form'] = "".join(clinics_menu)

            #OGM
            self.execute('get_field_type',{'table':'str_characs','field':'ogm'})
            ogm_options = self.fetch('columns')['Type']
            ogm_options = findall('\'.*?\'', ogm_options)
            #if action == 'new': ogm_menu = self.opt_html_selected
            #else: ogm_menu = self.opt_html
            ogm_menu = ''
            for ogm in ogm_options:
                ogm = ogm.replace("\'","")
                if ogm == "0":
                    ogm_label = ''
                elif ogm == "1":
                    ogm_label = _('Group I')
                elif ogm == "2":
                    ogm_label = _('Group II')
                else:
                    ogm_label = '' #For Empty Database
                ogm_menu += '\n\t<option %s value="%s"> %s </option>'
                if ogm == data['cha_ogm']:
                    ogm_menu = ogm_menu % (self.opt_selected, ogm, ogm_label)
                else: ogm_menu = ogm_menu % ('', ogm, ogm_label)
            data['cha_ogm'] = ogm_menu

            #HIV
            hiv_html = '''<input name="coll_hiv" id="hiv_unknown" class="radio" type="radio" value="" %%s /><label for="hiv_unknown">%s</label>
                          <input name="coll_hiv" id="hiv_yes" class="radio" type="radio" value="yes" %%s /><label for="hiv_yes">%s</label>
                          <input name="coll_hiv" id="hiv_no" class="radio" type="radio" value="no"  %%s /><label for="hiv_no">%s</label>''' % (_("Not Determined"), _("Yes"), _("No") )
            if data['coll_hiv'] == 'yes':
                hiv_html = hiv_html % ('', self.opt_checked, '')
            elif data['coll_hiv'] == 'no':
                hiv_html = hiv_html % ('', '', self.opt_checked)
            elif not data['coll_hiv']:
                hiv_html = hiv_html % (self.opt_checked, '', '')
            data['coll_hiv'] = hiv_html
        elif action in 'view':
            textLinksStrain = TextLinkFactory(self.cookie_value, self.session.data['id_lang'], data['data_lang'])
            textLinksStrain.update({
                'dep_preserv_method': deposit['preserve_method'].replace("%","%%"),
                'dep_aut_result'    : deposit['aut_result'].replace("%","%%"),
                'cha_biochemical'   : charac['biochemical'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\""),
                'cha_immunologic'   : charac['immunologic'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\""),
                'cha_morphologic'   : charac['morphologic'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\""),
                'cha_molecular'     : charac['molecular'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\""),
                'cha_pathogenic'    : charac['pathogenic'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\""),
                'cha_genotypic'     : charac['genotypic'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\""),
                'dep_species'       : deposit['species'].replace("%","%%"),
                'iso_comments'      : isolation['comments'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\""),
                'iso_isolation_from': isolation['iso_isolation_from'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\""),
                'iso_method'        : isolation['iso_method'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\""),
                'ident_method'      : identification['ident_method'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\""),
                'ident_comments'    : identification['comments'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\""),
                'pro_properties'    : prop['properties'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\""),
                'pro_applications'  : prop['applications'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\""),
                'pro_urls'          : prop['urls'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"")
            })
            #changes textlink to html link
            textLinksStrain.fillData(data)
            #Translate coll_hiv chosen option
            if data['coll_hiv'] == 'yes':
              data['coll_hiv'] = _("Yes")
            elif data['coll_hiv'] == 'no':
              data['coll_hiv'] = _("No")
            else:
              data['coll_hiv'] = _("Not Determined")

        if action in ('edit','new'):
            from .strain_formatter import StrainFormatter
            s = StrainFormatter(self.cookie_value)
            data['js_strain_format'] = s.division_javascript_options(self.session.data['id_subcoll'])

        if action in ('edit','view','new'):
            data['js_data_lot_exist'] = self.verify_lot_exist(data['id'])

        if action in ('view',):
            data['coll_host_species'] = Lists.spe_name(data['coll_host_species'])
            data['ident_species'] = Lists.spe_name(data['ident_species'])
            data['dep_species'] = Lists.spe_name(data['dep_species'])

        return data

    def strainStock(self, data):
        #Stock counting
        table_stock = []
                

        if "type" in self.form and self.form["type"].value == "other":
            self.execute('get_strain_stock_minimum',{'id_lang':self.session.data['id_lang'], 'id_subcoll':self.session.data['id_subcoll'], 'id_strain':data['id_strain']})
            methods = self.fetch('all')

            #Data exist
            if len(methods) > 0:

                table_stock.append("\n\t<table class='stock_main_table'>")

                for method in methods:
                    if method["quantity"] == 0:
                        method["quantity"] = ""

                    self.execute('get_stock_lot',{'id_preservation_method':method['id_preservation_method'], 'id_strain':data['id_strain']})
                    lots = self.fetch('all')

                    table_stock.append("\n\t\t<tr>")

                    table_stock.append("\n\t\t\t<td class='stock_method'>%s (" % method["method"])
                    table_stock.append("%s: %s, " % (_("in stock"), method["in_stock"]))
                    table_stock.append("""%s: <input id='stock_minimum_%s' class='stock_minimum' type='text' value='%s' onkeyup='numberOnly(this);' onblur='fillStockJson();' />"""
                                       % (_("minimum stock"), method["id_preservation_method"], method["quantity"]))
                    table_stock.append(")</td>")

                    table_stock.append("\n\t\t</tr>")
                    table_stock.append("\n\t\t<tr>")
                    table_stock.append("\n\t\t\t<td>")

                    if lots:
                        table_lot = []
                        table_lot.append("\n\t\t\t\t<table class='stock_data_table'>")
                        table_lot.append("\n\t\t\t\t\t<tr>")
                        table_lot.append("\n\t\t\t\t\t\t<th class='stock_header_lot'>%s</th>" % _("Lot"))
                        table_lot.append("\n\t\t\t\t\t\t<th class='stock_header_stock'>%s</th>" % _("Stock"))
                        table_lot.append("\n\t\t\t\t\t\t<th class='stock_header_unit'>%s</th>" % _("Unit"))
                        table_lot.append("\n\t\t\t\t\t\t<th class='stock_header_location'>%s</th>" % _("Location"))
                        table_lot.append("\n\t\t\t\t\t\t<th class='stock_header_minimum_stock'>%s</th>" % _("Minimum Stock"))
                        table_lot.append("\n\t\t\t\t\t</tr>")

                        for lot in lots:
                            if (int(lot["stock_minimum"]) > 0 and int(lot["stock"]) <= int(lot["stock_minimum"])): style = "class='stock_less_than_minimum'"
                            else: style = ""

                            stock_positions = []
                            self.execute('get_available_locations', { 'id_strain': data['id_strain'], 'id_lot': lot['id_lot'] })
                            positions = self.fetch('all')

                            for p in positions:
                                stock_positions.append(
                                    self.l.get_incomplete_location(p['id_container_hierarchy'], p['row'], p['col'], None, p['available_qt']))

                            table_lot.append("\n\t\t\t\t\t<tr %s>" % style)
                            table_lot.append("\n\t\t\t\t\t\t<td>%s</td>" % lot["name"])
                            table_lot.append("\n\t\t\t\t\t\t<td>%s</td>" % lot["stock"])
                            table_lot.append("\n\t\t\t\t\t\t<td>%s</td>" % method["unit_measure"])
                            table_lot.append("\n\t\t\t\t\t\t<td>%s</td>" % '<br />'.join(stock_positions))
                            table_lot.append("\n\t\t\t\t\t\t<td>%s</td>" % lot["stock_minimum"])
                            table_lot.append("\n\t\t\t\t\t</tr>")

                        table_lot.append("\n\t\t\t\t</table>")

                        table_stock.append("".join(table_lot))
                        table_stock.append("\n\t\t\t</td>")
                        table_stock.append("\n\t\t</tr>")

                table_stock.append("\n\t</table>")

                data["stock_data"] = "".join(table_stock)
        else: # stock detail
            self.execute('get_strain_stock_minimum',{'id_lang':self.session.data['id_lang'], 'id_subcoll':self.session.data['id_subcoll'], 'id_strain':data['id_strain']})
            methods = self.fetch('all')

            #Data exist
            if len(methods) > 0:

                table_stock.append("\n\t<table class='stock_main_table'>")

                for method in methods:
                    if (not method["quantity"] and not method["in_stock"]):
                        continue

                    table_stock.append("\n\t\t<tr>")
                    if method["in_stock"] and method["quantity"]:
                        if method["in_stock"] <= method["quantity"]:
                            css = "stock_method_less_than_minimum"
                        else:
                            css = "stock_method"
                        table_stock.append("\n\t\t\t<td class='%s'>%s (" % (css, method["method"]))
                        table_stock.append("%s: %s, %s: %s" % (_("in stock"), method["in_stock"], _("minimum stock"), method["quantity"]))
                        table_stock.append(")</td>")
                    elif method["in_stock"]:
                        table_stock.append("\n\t\t\t<td class='stock_method'>%s (" % method["method"])
                        table_stock.append("%s: %s" % (_("in stock"), method["in_stock"]))
                        table_stock.append(")</td>")
                    elif method["quantity"]:
                        table_stock.append("\n\t\t\t<td class='stock_method_less_than_minimum'>%s (" % method["method"])
                        table_stock.append("%s: %s, %s: %s" % (_("in stock"), method["in_stock"], _("minimum stock"), method["quantity"]))
                        table_stock.append(")</td>")

                    table_stock.append("\n\t\t</tr>")
                    table_stock.append("\n\t\t<tr>")
                    table_stock.append("\n\t\t\t<td>")

                    if method["in_stock"]:
                        table_lot = []
                        table_lot.append("\n\t\t\t\t<table class='stock_data_table'>")
                        table_lot.append("\n\t\t\t\t\t<tr>")
                        table_lot.append("\n\t\t\t\t\t\t<th class='stock_header_lot'>%s</th>" % _("Lot"))
                        table_lot.append("\n\t\t\t\t\t\t<th class='stock_header_stock'>%s</th>" % _("Stock"))
                        table_lot.append("\n\t\t\t\t\t\t<th class='stock_header_unit'>%s</th>" % _("Unit"))
                        table_lot.append("\n\t\t\t\t\t\t<th class='stock_header_location'>%s</th>" % _("Location"))
                        table_lot.append("\n\t\t\t\t\t\t<th class='stock_header_minimum_stock'>%s</th>" % _("Minimum Stock"))
                        table_lot.append("\n\t\t\t\t\t</tr>")

                        self.execute('get_stock_lot',{'id_preservation_method':method['id_preservation_method'], 'id_strain':data['id_strain']})
                        lots = self.fetch('all')

                        for lot in lots:
                            if (int(lot["stock_minimum"]) > 0 and int(lot["stock"]) <= int(lot["stock_minimum"])): style = "class='stock_less_than_minimum'"
                            else: style = ""

                            stock_positions = []
                            self.execute('get_available_locations', { 'id_strain': data['id_strain'], 'id_lot': lot['id_lot'] })
                            positions = self.fetch('all')

                            for p in positions:
                                stock_positions.append(
                                    self.l.get_incomplete_location(p['id_container_hierarchy'], p['row'], p['col'], None, p['available_qt']))

                            table_lot.append("\n\t\t\t\t\t<tr %s>" % style)
                            table_lot.append("\n\t\t\t\t\t\t<td>%s</td>" % lot["name"])
                            table_lot.append("\n\t\t\t\t\t\t<td>%s</td>" % lot["stock"])
                            table_lot.append("\n\t\t\t\t\t\t<td>%s</td>" % method["unit_measure"])
                            table_lot.append("\n\t\t\t\t\t\t<td>%s</td>" % '<br />'.join(stock_positions))
                            table_lot.append("\n\t\t\t\t\t\t<td>%s</td>" % lot["stock_minimum"])
                            table_lot.append("\n\t\t\t\t\t</tr>")

                        table_lot.append("\n\t\t\t\t</table>")

                        table_stock.append("".join(table_lot))
                        table_stock.append("\n\t\t\t</td>")
                        table_stock.append("\n\t\t</tr>")

                table_stock.append("\n\t</table>")

                data["stock_data"] = "".join(table_stock)
            else:
                data["stock_data"] = "<br /><center>%s</center>" % _("There are no Lot Numbers for this Strain.")

    def doc(self,action):
        data = self.data
        data['action'] = action
        data['title_langs'] = ''
        data['description_langs'] = ''
        data['file_name_langs'] = ''
        data['new_file_langs'] = ''
        data['groups_table'] = ''
        data['content_test_category'] = ''
        data['id_subcoll'] = self.session.data['id_subcoll']
        data['url_next'] = "<a href='javascript:Proximo(\"doc.detail.py?id=%(id)s&row=%(row)s\")'>"
        data['url_prev'] = "<a href='javascript:Anterior(\"doc.detail.py?id=%(id)s&row=%(row)s\")'>"
        data['close_link_prev'] = '</a>'
        data['close_link_next'] = '</a>'
        data['img_prev']= ''
        data['img_next']= ''
        data['js_data'] = ''

        if action == 'view': pass
        elif action == 'edit':
            data['next_action'] = 'update'
        elif action == 'new':
            data['next_action'] = 'insert'
            data['back_where'] = 'list'

        data['row_number'] = self.data['row']

        if (action == 'view' and 'row' in self.form):
            #Verify field_order is changed
            if 'field_order' in self.form:
                self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'doc', self.form['field_order'].value)

            #Get field and mode for order list
            field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'doc')

            #Define field_order with mode
            self.data['field_order'] = field + ' ' + mode

            if (data['row'] == '0'):
                data['paging'] = ' LIMIT %s,2' % data['row']
            else:
                data['paging'] = ' LIMIT %s,3' % str(int(self.data['row']) - 1)

            data['id_lang'] = self.session.data['id_lang']
            data['id_coll'] = self.session.data['id_coll']
            data['id_subcoll'] = self.session.data['id_subcoll']

            #Filter
            filter = ''
            if ('filter' in self.form):
                filter = str(self.form['filter'].value).strip()
                filter = self.ConvertStrUnicode(filter).encode("utf-8")

                #Save filter on session
                self.session.data['filter_docs'] = filter
                self.session.save()
            elif ('filter_docs' in self.session.data):
                filter = self.session.data['filter_docs']
                filter = self.ConvertStrUnicode(filter).encode("utf-8")

            if (filter != ''):
                words = [x for x in filter.split(" ") if x != '']
                self.data['condition']= []
                for word in words:
                    #0x25 == '%'
                    self.data['condition'].append("AND (q.qualifier LIKE x'25" + word.encode("hex") + "25' OR doc.code LIKE x'25" + word.encode("hex") + "25' OR t.title LIKE x'25" + word.encode("hex") + "25') ")
                self.data['condition']= "".join(self.data['condition'])
            else:
                self.data['condition'] = ' '

            #Execute again for rows count
            if self.g.isManager(self.session.data['roles']): #Administrator or Manager
              self.execute('get_doc_ids', self.data, True)
            else:
              roles = str(self.session.data['roles']).replace("L","")
              roles = roles.replace("[","(")
              roles = roles.replace("]",")")
              self.data['roles_list'] = roles
              self.execute('get_doc_ids_restrict', self.data,raw_mode = True)

            list_doc = self.fetch('all')
            i=0
            for doc in list_doc:

                if (data['row'] == '0'):
                    if (i == 0):
                        data['img_prev'] = ''
                        data['url_prev'] = ''
                        data['close_link_prev'] = ''
                    else:
                        next_pagination = {}
                        next_pagination['id'] = doc['id_doc']
                        next_pagination['row'] = str(int(data['row']) + 1)
                        data['img_next'] = '<img title="'+ _("Next") +'" src="../img/next.gif" border="0">'

                        data['url_next'] = data['url_next'] % next_pagination
                else:
                    if (i == 0):
                        prev_pagination = {}
                        prev_pagination['id'] = doc['id_doc']
                        prev_pagination['row'] = str(int(data['row']) - 1)
                        data['img_prev'] = '<img title="'+ _("Previous") +'" src="../img/prev.gif" border="0">'

                        data['url_prev'] = data['url_prev'] % prev_pagination
                    elif (i == 2):
                        next_pagination = {}
                        next_pagination['id'] = doc['id_doc']
                        next_pagination['row'] = str(int(data['row']) + 1)
                        data['img_next'] = '<img title="'+ _("Next") +'" src="../img/next.gif" border="0">'

                        data['url_next'] = data['url_next'] % next_pagination

                i = i + 1

            if ((i == 2) and (data['row'] != '0')) or (i < 2 and data['row'] == '0'):
                data['url_next'] = ''
                data['close_link_next'] = ''
                data['img_next'] = ''

        else:
            data['url_next'] = ''
            data['close_link_next'] = ''
            data['img_next'] = ''

            data['img_prev'] = ''
            data['url_prev'] = ''
            data['close_link_prev'] = ''


        is_first = True
        for lang in self.data_langs:
            one_lang = list(lang.keys())[0]
            data['data_lang'] = list(lang.values())[0]
            self.execute('get_doc_data', data)
            docs = self.fetch('columns')
            num_fields = 6
            if len(docs) < num_fields:
                docs = DefDict()

            if is_first:
                data['code'] = docs['code']
                data['id_qualifier'] = docs['id_qualifier']
                data['qualifier'] = docs['qualifier']
                if('go_catalog' in docs):
                    if (docs['go_catalog']):
                        data['label_go_catalog'] = _("This document goes to catalog")
                        data['is_go_catalog_check'] = "checked='checked'"
                    else:
                        data['label_go_catalog'] = ''
                        data['is_go_catalog_check'] = ""
                if data['code']: data['message'] = '%s: %s' % (data['qualifier'], data['code'])

                #Security info
                #permissions = self.g.get_permissions(self.cookie_value, 'doc', data)

            data['title_%s' %one_lang] = docs['title'].replace('"','&quot;').replace("'","&#39;")
            data['description_%s'%one_lang] = docs['description'].replace("<a","<a class=\"tlink\"")
            data['file_name_%s' %one_lang] = docs['file_name']


            if data['file_name_%s'% one_lang]:
                data['download_%s'% one_lang] = (' [<a href="./doc.download.py?%s&%s&%s&%s" class="tlink">%s</a>]'
                                            % (
                                                urlencode({'file_name_%s' % one_lang: data['file_name_%s' % one_lang].encode('utf8')}),
                                                urlencode({'id': data['id']}),
                                                urlencode({'code': one_lang}),
                                                urlencode({'id_lang': list(lang.values())[0]}),
                                                _("download")
                                               )
                                            )
            else:
                data['download_%s'%one_lang] = ''

            if action == 'view':
                data['title_langs'] += '''%s: %s<br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['title_%s' %one_lang])
                data['description_langs'] += '''%s: %s<br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['description_%s' %one_lang])
                data['file_name_langs'] += '''%s: %s %s<br />
                '''%("<span class='label_color'>"+one_lang+"</span>", data['file_name_%s' %one_lang], data['download_%s'%one_lang])
                if data['id_qualifier'] == 5:
                  data['content_test_category'] = '<p><label>%s</label><br />%s</p>' % (_("Category"),docs['category'])

            else:
                #Get available categories for "test" qualifier
                test_groups = []
                self.execute('get_test_group_subcoll', {'id_lang':self.session.data['id_lang'],'id_subcoll':self.session.data['id_subcoll']})
                tests = self.fetch('all')
                for test in tests:
                  chosen_opt = ''
                  if test['id_test_group'] == docs['id_category']: chosen_opt = "selected='selected'"
                  test_groups.append('\n\t<option %s value="%s">%s</option>' % (chosen_opt,test['id_test_group'],test['category']))
                data['test_category'] = ''.join(test_groups)
                data['title_tabs'] = self.generateLanguageTabs('title')
                data['description_tabs'] = self.generateLanguageTabs('description')
                data['file_name_tabs'] = self.generateLanguageTabs('file_name')
                data['new_file_tabs'] = "<br />"#self.generateLanguageTabs('new_file')

                classtyle = 'block' #change

                data['title_langs'] += '''<span class='%s' id='title_field_%s' >
                <input onblur="isEmptyMulti('title',false)" name="title_%s" id="title_%s" class="doctitle" type="text" maxlength="100" value="%s" /><br />
                </span>
                ''' %(classtyle, one_lang, one_lang, one_lang, data['title_%s' %one_lang])

                data['description_langs'] += '''<span class='%s' id='description_field_%s' >
                <textarea name="description_%s" id="description_%s" class="mceEditor" cols="" rows="">%s</textarea>
                </span>
                ''' %(classtyle, one_lang, one_lang, one_lang, data['description_%s' %one_lang])

                data['file_name_langs'] += '''<span class='%s' id='file_name_field_%s' >
                <input name="file_name_%s" id="file_name_%s" type="text" value="%s" disabled="disabled" /><br />
                <span class="hidden"><input name="file_%s" type="hidden" value="%s" /></span>
                </span>
                '''%(classtyle, one_lang, one_lang, one_lang, data['file_name_%s' %one_lang], one_lang, data['file_name_%s' %one_lang] )

                data['new_file_langs'] += '''<span class='%s' id='new_file_field_%s' >
                    <input name="new_file_%s" id="new_file_%s" type="file" />
                    <br />
                </span>
                ''' %(classtyle, one_lang, one_lang, one_lang)
            is_first = False
        #Security Tab
        self.g.security_tab(self.cookie_value, action, data, 'doc')
        
        if action in ('edit','new'):
            #Qualifier
            self.execute('get_all_from_table',{'table':'doc_qualifier'})
            qualifiers = self.fetch('all')
            #List sorting
            qualifiers = sorted(qualifiers, lambda x, y: cmp(x['qualifier'], y['qualifier']))
            if action == 'new': qualifier_menu = self.opt_html_selected
            else: qualifier_menu = ''
            for qualifier in qualifiers:
                qualifier_menu += '\n\t<option %%s value="%s">%s</option>' % (qualifier['id_qualifier'],qualifier['qualifier'])
                if qualifier['id_qualifier'] == data['id_qualifier']:
                    qualifier_menu = qualifier_menu % self.opt_selected
                else:
                    qualifier_menu = qualifier_menu % ''
            data['qualifier'] = qualifier_menu
            if data['id_qualifier'] is not None and data['id_qualifier'] != 5:
              data['display_test_category'] = 'none'
            else:
              data['display_test_category'] = 'block'
            del qualifiers, qualifier_menu

        if action in ('edit'):
            data['code_Documents_disabled'] = " disabled='True' "
            if data['id_qualifier'] == 4: # Type of document: Meio
                # Need to check preservation dependency
                self.execute('get_doc_dependency_with_preservation', {'id':data['id']})
                if self.fetch('all'):
                    data['js_data'] += 'qualifier_blocked = true;'
                    data['js_data'] += 'qualifier_title = "%s";' % _("This document qualifier cannot be modified because it is been used by a preservation.")
                else:
                    data['js_data'] += 'qualifier_blocked = false;'
            elif data['id_qualifier'] == 5: # Type of document: Teste
                # Need to check quality control dependency
                self.execute('get_doc_dependency_with_quality_control', {'id':data['id']})
                if self.fetch('all'):
                    data['js_data'] += 'qualifier_blocked = true;'
                    data['js_data'] += 'qualifier_title = "%s";' % _("This document qualifier cannot be modified because it is been used by a quality control.")
                else:
                    data['js_data'] += 'qualifier_blocked = false;'

        if action in ('new'):
            data['js_data'] += 'qualifier_blocked = false;'
            data['code_Documents_disabled'] = ""

        return data

    def ref(self, action):
        data = self.data
        data['action'] = action
        data['comments_langs'] = ''
        data['groups_table'] = ""
        data['url_next'] = "<a href='javascript:Proximo(\"ref.detail.py?id=%(id)s&row=%(row)s\")'>"
        data['url_prev'] = "<a href='javascript:Anterior(\"ref.detail.py?id=%(id)s&row=%(row)s\")'>"
        data['close_link_prev'] = '</a>'
        data['close_link_next'] = '</a>'
        data['img_prev']= ''
        data['img_next']= ''

        if action == 'view': pass
        elif action == 'edit':
            data['next_action'] = 'update'
        elif action == 'new':
            data['next_action'] = 'insert'
            data['back_where'] = 'list'

        data['row_number'] = self.data['row']

        if (action == 'view' and 'row' in self.form):
            #Verify field_order is changed
            if 'field_order' in self.form:
                self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'ref', self.form['field_order'].value)

            #Get field and mode for order list
            field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'ref')

            if field == 'code':
                field = 'id_ref %s' % mode
            else:
                field = field + ' ' + mode

            #Define field_order with mode
            self.data['field_order'] = field

            if (data['row'] == '0'):
                data['paging'] = ' LIMIT %s,2' % data['row']
            else:
                data['paging'] = ' LIMIT %s,3' % str(int(self.data['row']) - 1)

            data['id_lang'] = self.session.data['id_lang']
            data['id_coll'] = self.session.data['id_coll']
            data['id_subcoll'] = self.session.data['id_subcoll']

            #Filter
            filter = ''
            if ('filter' in self.form):
                filter = str(self.form['filter'].value).strip()
                filter = self.ConvertStrUnicode(filter).encode("utf-8")

                #Save filter on session
                self.session.data['filter_refs'] = filter
                self.session.save()
            elif ('filter_refs' in self.session.data):
                filter = self.session.data['filter_refs']
                filter = self.ConvertStrUnicode(filter).encode("utf-8")

            if (filter != ''):
                words = [x for x in filter.split(" ") if x != '']
                self.data['condition']= []
                for word in words:
                    #0x25 == '%'
                    self.data['condition'].append("AND (ref.id_ref LIKE x'25" + word.encode("hex") + "25' OR ref.author LIKE x'25" + word.encode("hex") + "25' OR ref.title LIKE x'25" + word.encode("hex") + "25' OR ref.year LIKE x'25" + word.encode("hex") + "25') ")
                self.data['condition']= "".join(self.data['condition'])
            else:
                self.data['condition'] = ' '

            if self.g.isManager(self.session.data['roles']): #Administrator or Manager
                self.execute('get_ref_ids', self.data, True)
            else:
                roles = str(self.session.data['roles']).replace("L","")
                roles = roles.replace("[","(")
                roles = roles.replace("]",")")
                self.data['roles_list'] = roles
                self.execute('get_ref_ids_restrict',self.data,raw_mode = True)
            list_ref = self.fetch('all')

            i=0
            for ref in list_ref:

                if (data['row'] == '0'):
                    if (i == 0):
                        data['img_prev'] = ''
                        data['url_prev'] = ''
                        data['close_link_prev'] = ''
                    else:
                        next_pagination = {}
                        next_pagination['id'] = ref['id_ref']
                        next_pagination['row'] = str(int(data['row']) + 1)
                        data['img_next'] = '<img title="'+ _("Next") +'" src="../img/next.gif" border="0">'

                        data['url_next'] = data['url_next'] % next_pagination
                else:
                    if (i == 0):
                        prev_pagination = {}
                        prev_pagination['id'] = ref['id_ref']
                        prev_pagination['row'] = str(int(data['row']) - 1)
                        data['img_prev'] = '<img title="'+ _("Previous") +'" src="../img/prev.gif" border="0">'

                        data['url_prev'] = data['url_prev'] % prev_pagination
                    elif (i == 2):
                        next_pagination = {}
                        next_pagination['id'] = ref['id_ref']
                        next_pagination['row'] = str(int(data['row']) + 1)
                        data['img_next'] = '<img title="'+ _("Next") +'" src="../img/next.gif" border="0">'

                        data['url_next'] = data['url_next'] % next_pagination

                i = i + 1

            if ((i == 2) and (data['row'] != '0')) or (i < 2 and data['row'] == '0'):
                data['url_next'] = ''
                data['close_link_next'] = ''
                data['img_next'] = ''

        else:
            data['url_next'] = ''
            data['close_link_next'] = ''
            data['img_next'] = ''

            data['img_prev'] = ''
            data['url_prev'] = ''
            data['close_link_prev'] = ''

        is_first = True
        for lang in self.data_langs:
            one_lang = list(lang.keys())[0]
            data['data_lang'] = list(lang.values())[0]
            self.execute('get_ref_data', data)
            refs = self.fetch('columns')
            num_fields = 5
            if len(refs) < num_fields:
                refs = DefDict()

            if is_first:
                data['title'] = refs['title'].replace('"','&quot;').replace("'","&#39;")
                data['author'] = refs['author'].replace('"','&quot;').replace("'","&#39;")
                data['year'] = refs['year'].replace('"','&quot;').replace("'","&#39;")
                data['url'] = refs['url'].replace("<a","<a class=\"tlink\"")
                data['message'] = '[%s] <b>%s</b> %s' % (data['id'], data['title'], data['author'])

                if('go_catalog' in refs):
                    if (refs['go_catalog']):
                        data['label_go_catalog'] = _("This reference goes to catalog")
                        data['is_go_catalog_check'] = "checked='checked'"
                    else:
                        data['label_go_catalog'] = ''
                        data['is_go_catalog_check'] = ""

                #Security info
                #permissions = self.g.get_permissions(self.cookie_value, 'ref', data)

            data['comments_%s' %one_lang] = refs['comments']

            if action == 'view':
                data['comments_langs'] += '''%s: %s<br />
                ''' %("<span class='label_color'>"+one_lang+"</span>", data['comments_%s' %one_lang].replace("<a","<a class=\"tlink\""))
            else:
                data['comments_tabs'] = self.generateLanguageTabs('comments')

                classtyle = 'block'

                data['comments_langs'] += '''<span class='%s' id='comments_field_%s' >
                    <textarea name="comments_%s" id="comments_%s" class="mceEditor" cols="" rows="">%s</textarea>
                </span>''' %(classtyle, one_lang, one_lang, one_lang, data['comments_%s' %one_lang])
            is_first = False

        #Security Tab
        self.g.security_tab(self.cookie_value, action, data, 'ref')
        return data

    def people(self, action):
        data = self.data
        data['action'] = action
        data['comments_langs'] = ''
        data['groups_table'] = ""
        data['url_next'] = "<a href='javascript:Proximo(\"people.detail.py?id=%(id)s&row=%(row)s\")'>"
        data['url_prev'] = "<a href='javascript:Anterior(\"people.detail.py?id=%(id)s&row=%(row)s\")'>"
        data['close_link_prev'] = '</a>'
        data['close_link_next'] = '</a>'
        data['img_prev']= ''
        data['img_next']= ''

        if action == 'view': pass
        elif action == 'edit':
            data['next_action'] = 'update'
        elif action == 'new':
            data['next_action'] = 'insert'
            data['back_where'] = 'list'

        data['row_number'] = self.data['row']

        if (action == 'view' and 'row' in self.form):
            #Verify field_order is changed
            if 'field_order' in self.form:
                self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'people', self.form['field_order'].value)

            #Get field and mode for order list
            field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'people')

            #Verify field_order for special order
            if field == 'institution':
                isInstitution = True
                field = 'name'
            else:
                isInstitution = False

            #Define field_order with mode
            self.data['field_order'] = field + ' ' + mode

            if (data['row'] == '0'):
                data['paging'] = ' LIMIT %s,2' % data['row']
            else:
                data['paging'] = ' LIMIT %s,3' % str(int(self.data['row']) - 1)

            data['id_lang'] = self.session.data['id_lang']
            data['id_coll'] = self.session.data['id_coll']
            data['id_subcoll'] = self.session.data['id_subcoll']

            #Filter
            filter = ''
            if ('filter' in self.form):
                filter = str(self.form['filter'].value).strip()
                filter = self.ConvertStrUnicode(filter).encode("utf-8")

                #Save filter on session
                self.session.data['filter_people'] = filter
                self.session.save()
            elif ('filter_people' in self.session.data):
                filter = self.session.data['filter_people']
                filter = self.ConvertStrUnicode(filter).encode("utf-8")

            if (filter != ''):
                words = [x for x in filter.split(" ") if x != '']

                self.data['condition'] = []
                for word in words:
                    #0x25 == '%'
                    if self.g.isManager(self.session.data['roles']): #Administrator or Manager
                        self.data['condition'].append("AND (p.name LIKE x'25" + word.encode("hex") + "25' OR p.nickname LIKE REPLACE(REPLACE(x'25" + word.encode("hex") + "25', '(', ''), ')', '') OR ((SELECT COUNT(institution.id_institution) FROM institution INNER JOIN contact_relations ON (institution.id_institution = contact_relations.id_institution) WHERE contact_relations.id_person = p.id_person AND (institution.complement LIKE x'25" + word.encode("hex") + "25' OR institution.nickname LIKE x'25" + word.encode("hex") + "25')) > 0)) ")
                    else:
                        self.data['condition'].append("AND (p.name LIKE x'25" + word.encode("hex") + "25' OR p.nickname LIKE REPLACE(REPLACE(x'25" + word.encode("hex") + "25', '(', ''), ')', '') OR ((SELECT COUNT(institution.id_institution) FROM institution INNER JOIN contact_relations ON (institution.id_institution = contact_relations.id_institution) WHERE contact_relations.id_person = p.id_person AND (institution.complement LIKE x'25" + word.encode("hex") + "25' OR institution.nickname LIKE x'25" + word.encode("hex") + "25')) > 0)) ")
                self.data['condition']= "".join(self.data['condition'])
            else:
                self.data['condition'] = ' '

            if self.g.isManager(self.session.data['roles']): #Administrator or Manager
               self.execute('get_person_ids', self.data, True)
            else:
                roles = str(self.session.data['roles']).replace("L","")
                roles = roles.replace("[","(")
                roles = roles.replace("]",")")
                self.data['roles_list'] = roles
                self.execute('get_person_ids_restrict',self.data,raw_mode = True)
            list_people = self.fetch('all')

            i=0
            for person in list_people:

                if (data['row'] == '0'):
                    if (i == 0):
                        data['img_prev'] = ''
                        data['url_prev'] = ''
                        data['close_link_prev'] = ''
                    else:
                        next_pagination = {}
                        next_pagination['id'] = person['id_person']
                        next_pagination['row'] = str(int(data['row']) + 1)
                        data['img_next'] = '<img title="'+ _("Next") +'" src="../img/next.gif" border="0">'

                        data['url_next'] = data['url_next'] % next_pagination
                else:
                    if (i == 0):
                        prev_pagination = {}
                        prev_pagination['id'] = person['id_person']
                        prev_pagination['row'] = str(int(data['row']) - 1)
                        data['img_prev'] = '<img title="'+ _("Previous") +'" src="../img/prev.gif" border="0">'

                        data['url_prev'] = data['url_prev'] % prev_pagination
                    elif (i == 2):
                        next_pagination = {}
                        next_pagination['id'] = person['id_person']
                        next_pagination['row'] = str(int(data['row']) + 1)
                        data['img_next'] = '<img title="'+ _("Next") +'" src="../img/next.gif" border="0">'

                        data['url_next'] = data['url_next'] % next_pagination

                i = i + 1

            if ((i == 2) and (data['row'] != '0')) or (i < 2 and data['row'] == '0'):
                data['url_next'] = ''
                data['close_link_next'] = ''
                data['img_next'] = ''

        else:
            data['url_next'] = ''
            data['close_link_next'] = ''
            data['img_next'] = ''

            data['img_prev'] = ''
            data['url_prev'] = ''
            data['close_link_prev'] = ''

        is_first = True
        for lang in self.data_langs:
            one_lang = list(lang.keys())[0]
            data['data_lang'] = list(lang.values())[0]
            #SELECT name, nickname, address, phone, email, comments
            self.execute('get_person_data', data)
            person = self.fetch('columns')
            num_fields = 6
            if len(person) < num_fields:
                person = DefDict()

            #Person Data
            if is_first:
                data['name'] = person['name'].replace('"','&quot;').replace("'","&#39;")
                data['nickname'] = person['nickname'].replace('"','&quot;').replace("'","&#39;")
                data['address']= person['address'].replace("<a","<a class=\"tlink\"")
                data['phone']= person['phone'].replace("<a","<a class=\"tlink\"")
                data['email']= person['email']
                data['people_contacts'] = self.people_contacts(action)
                data['message'] = '<b>%s</b><br />%s' % (data['nickname'], data['name'])

                if('go_catalog' in person):
                    if (person['go_catalog']):
                        data['label_go_catalog'] = _("This people goes to catalog")
                        data['is_go_catalog_check'] = "checked='checked'"
                    else:
                        data['label_go_catalog'] = ''
                        data['is_go_catalog_check'] = ""

                #Security info
                #permissions = self.g.get_permissions(self.cookie_value, 'people', data)

            data['comments_%s' %one_lang]= person['comments']

            if action == 'view':
                data['comments_langs'] += '''
                    %s: %s<br />
                ''' %("<span class='label_color'>"+one_lang+"</span>", data['comments_%s' %one_lang].replace("<a","<a class=\"tlink\""))
                data['email']= "<a href='mailto:"+person['email']+"' class='tlink'>"+person['email']+"</a>"
            else:
                data['comments_tabs'] = self.generateLanguageTabs('comments')

                classtyle = 'block' #change

                data['comments_langs'] += '''<span class='%s' id='comments_field_%s' >
                    <textarea name="comments_%s" id="comments_%s" class="mceEditor" cols="" rows="">%s</textarea>
                </span>
                ''' %(classtyle, one_lang, one_lang, one_lang, data['comments_%s' %one_lang])
            is_first = False

        #Security Tab
        self.g.security_tab(self.cookie_value, action, data, 'people')
        return data

    def people_contacts (self, action):
        #SELECT id_institution, i.complement, i.nickname, cr.contact, cr.department, cr.email
        self.execute ("get_person_contact_relations", self.data)
        contacts = self.fetch("all")
        trows = [];
        #in konqueror 3.4, a bug prevents the links inside the scrolling div to work
        #properly  One can comment the widget of choice at will, for the same
        #functionality. I __need__ the widget "button" to be easily available for testing.
        # JS

        widget = '<input type="button" onclick="%s" id="%s" class="button" style="display: %s" value="%s" />'
        #widget = '<a onclick="%s" id="%s" style="display: %s">%s</a> '
        if action == "view":
            if not contacts: return ""
            for  contact in contacts:
                #institution, complement, nickname, contact, department, email
                institution = contact["complement"]
                if contact["nickname"]: institution += " (%s)" % contact["nickname"]
                if contact["contact"]: institution += ' [%s]' % _('contact')
                institution_link = '<a href="institutions.detail.py?id=%s">%s</a>' %\
                                   (str(contact["institution"]), institution)
                trows.append ("""<tr>
                                  \t\t<td>%s</td>
                                  \t\t<td>%s</td>
                                  \t\t<td>%s</td>
                                  </tr>\n"""
                % (institution_link, contact["department"], "<a href='mailto:"+contact["email"]+"' class='tlink'>"+contact["email"]+"</a>"))
            html = ("""<table id="people_contacts" cellspacing="10">
                        \t<tr>
                        \t\t<th>%s</th>
                        \t\t<th>%s</th>
                        \t\t<th>%s</th>
                        \t</tr>
                        %s
                        </table>
                    """
            % (_("Institution"), _("Department"), _("E-mail"),
                 "".join(trows)))
            return html
        elif action in ("edit", "new"):
            counter = 0

            select_institution = '<select class="select_inst" id="ins_select_inst" name="ins_select_inst">%s</select>\n' % (self.get_inst_option_list())
            check_contact =  '<input type="checkbox" id="ins_check_contact" name="ins_check_contact" class="checkbox" value="YES"/>'
            text_dep =  '<input type="text" id="ins_text_dep" name="ins_text_dep" class="text" maxlength="80" value=""/>\n'
            text_email =  '<input type="text" id="ins_text_email" name="ins_text_email" class="text" maxlength="100" value=""/>\n'

            #widget = '<input type="button" onclick="%s" id="insert_row" class="new_contact_button" value="%s" />' % ("javascript:insert_contact(_last_ct_index, true)", _("Insert"))
            widget = '<img src="../img/insert.png" onclick="%s" title="%s" class="insert_contact" style="cursor: pointer;"/>' % ("javascript:insert_contact(_last_ct_index, true)", _("Insert"))


            html = """<table width="670px" id="people_contacts" cellspacing="4">
                        \t<tr>
                        \t\t<th>%s</th>
                        \t\t<th style="width:10px">%s</th>
                        \t\t<th>%s</th>
                        \t\t<th>%s</th>
                        \t\t<th></th>
                        \t</tr>
                        \t<tr>
                        \t\t<td>%s</td>
                        \t\t<td style="width:10px">%s</td>
                        \t\t<td>%s</td>
                        \t\t<td>%s</td>
                        \t\t<td align="right">%s</td>
                        \t</tr></table>
                    """ % (_("Institution"), _("Contact"), _("Department"), _("E-mail"),
                           select_institution, check_contact, text_dep, text_email, widget)

            #for contact in contacts:
            for contact in []:
                counter += 1

        self.execute ("get_institution")
        institutions_data = self.fetch("all")
        #inst_ids = [int(el['id_institution']) for el in institutions_data]
        #inst_names = [el['name'].encode("utf-8") for el in institutions_data]
        #inst_nicks = [el['nickname'].encode("utf-8") for el in institutions_data]

        def js_list (key, mapping = None):
            if not mapping:
                mapping = contacts
            ret_list = []
            for contact in mapping:
                if isinstance(contact[key], str):
                    ret_list.append(self.g.escape_quote (contact[key]))
                else:
                    ret_list.append(str(contact[key]).decode('utf-8'))
            return "[%s]" % ", ".join(["'%s'" % element for element in ret_list])
            #return str([str(contact[key]) for contact in contacts])

        inst_ids = [int(el['id_institution']) for el in institutions_data]
        inst_names = js_list ('name', institutions_data)
        inst_nicks = js_list ('nickname', institutions_data)
        javascript = ("""
                        <script type="text/javascript">
                        var _last_ct_index = %s;
                        var _inst_ids = %s;
                        var _inst_names = %s;
                        var _inst_nicks = %s;

                        var _cont_inst_ids = %s;
                        var _cont_inst_names = %s;
                        var _cont_inst_nicks = %s;
                        var _cont_contact = %s;
                        var _cont_department = %s;
                        var _cont_email = %s;

                        build_contact_list();
                        </script>""" % (counter, str(inst_ids), inst_names, inst_nicks,
                        js_list("institution"), js_list ("complement"), js_list("nickname"),
                        js_list("contact"), js_list("department"), js_list("email")

                        ))
        return html + javascript

    def get_inst_option_list(self, id_sel_institution = None):
        #caches the query for institutions, as it may be retrieved several times
        #in a single script run:
        none_sel = "-1"
        if self._inst_option_list is None:
            self.execute ("get_institution")
            #(id_institution, complement)
            institutions = self.fetch('all')

            self._inst_selected_dict = {none_sel: ""}
            opt_string = """<option value="%s" %s >%s</option>"""
            inst_options = [opt_string % ("", "%%(%s)s" % none_sel, "---")]
            if len(institutions):
                for inst in institutions:
                    #creates html <option> tag string, leaving space for marking
                    #the selected option based on id_institution later
                    inst_options.append (opt_string % (inst['id_institution'],
                                         "%%(%d)s" % inst['id_institution'],
                                         inst['nickname'].replace("%","%%") + ' - ' + inst['name'].replace("%","%%") ))
                    self._inst_selected_dict[str(inst['id_institution'])] = ""
            self._inst_option_list  = "\n\t".join(inst_options)
        # "0" might be a valid institution id
        if id_sel_institution in (None, "", -1):
            id_sel_institution = none_sel
        self._inst_selected_dict [str(id_sel_institution)] = self.opt_selected
        inst_option_list = self._inst_option_list % self._inst_selected_dict
        self._inst_selected_dict [str(id_sel_institution)] = None
        return inst_option_list


    def inst(self, action):
        data = self.data
        data['action'] = action
        data['comments_langs'] = ''
        data['groups_table'] = ""
        data['url_next'] = "<a href='javascript:Proximo(\"institutions.detail.py?id=%(id)s&row=%(row)s\")'>"
        data['url_prev'] = "<a href='javascript:Anterior(\"institutions.detail.py?id=%(id)s&row=%(row)s\")'>"
        data['close_link_prev'] = '</a>'
        data['close_link_next'] = '</a>'
        data['img_prev']= ''
        data['img_next']= ''

        if action == 'view': pass
        elif action == 'edit':
            data['next_action'] = 'update'
        elif action == 'new':
            data['next_action'] = 'insert'
            data['back_where'] = 'list'

        data['row_number'] = self.data['row']

        if (action == 'view' and 'row' in self.form):
            #Verify field_order is changed
            if 'field_order' in self.form:
                self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'inst', self.form['field_order'].value)

            #Get field and mode for order list
            field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'inst')

            field = field + ' ' + mode

            #Define field_order with mode
            self.data['field_order'] = field

            if (data['row'] == '0'):
                data['paging'] = ' LIMIT %s,2' % data['row']
            else:
                data['paging'] = ' LIMIT %s,3' % str(int(self.data['row']) - 1)

            data['id_lang'] = self.session.data['id_lang']
            data['id_coll'] = self.session.data['id_coll']
            data['id_subcoll'] = self.session.data['id_subcoll']

            #Filter
            filter = ''
            if ('filter' in self.form):
                filter = str(self.form['filter'].value).strip()
                filter = self.ConvertStrUnicode(filter).encode("utf-8")

                #Save filter on session
                self.session.data['filter_insts'] = filter
                self.session.save()
            elif ('filter_insts' in self.session.data):
                filter = self.session.data['filter_insts']
                filter = self.ConvertStrUnicode(filter).encode("utf-8")

            if (filter != ''):
                words = [x for x in filter.split(" ") if x != '']
                self.data['condition']= []
                for word in words:
                    #0x25 == '%'
                    if self.g.isManager(self.session.data['roles']): #Administrator or Manager:
                        self.data['condition'].append("AND (nickname LIKE x'25" + word.encode("hex") + "25' OR name LIKE x'25" + word.encode("hex") + "25' OR complement LIKE x'25" + word.encode("hex") + "25') ")
                    else:
                        self.data['condition'].append("AND (nickname LIKE x'25" + word.encode("hex") + "25' OR name LIKE x'25" + word.encode("hex") + "25' OR complement LIKE x'25" + word.encode("hex") + "25') ")
                self.data['condition']= "".join(self.data['condition'])
            else:
                self.data['condition'] = ' '

            if self.g.isManager(self.session.data['roles']): #Administrator or Manager
                self.execute('get_inst_ids', self.data, True)
            else:
                roles = str(self.session.data['roles']).replace("L","")
                roles = roles.replace("[","(")
                roles = roles.replace("]",")")
                self.data['roles_list'] = roles
                self.execute('get_inst_ids_restrict',self.data,raw_mode = True)
            list_inst = self.fetch('all')

            i=0
            for inst in list_inst:

                if (data['row'] == '0'):
                    if (i == 0):
                        data['img_prev'] = ''
                        data['url_prev'] = ''
                        data['close_link_prev'] = ''
                    else:
                        next_pagination = {}
                        next_pagination['id'] = inst['id_institution']
                        next_pagination['row'] = str(int(data['row']) + 1)
                        data['img_next'] = '<img title="'+ _("Next") +'" src="../img/next.gif" border="0">'

                        data['url_next'] = data['url_next'] % next_pagination
                else:
                    if (i == 0):
                        prev_pagination = {}
                        prev_pagination['id'] = inst['id_institution']
                        prev_pagination['row'] = str(int(data['row']) - 1)
                        data['img_prev'] = '<img title="'+ _("Previous") +'" src="../img/prev.gif" border="0">'

                        data['url_prev'] = data['url_prev'] % prev_pagination
                    elif (i == 2):
                        next_pagination = {}
                        next_pagination['id'] = inst['id_institution']
                        next_pagination['row'] = str(int(data['row']) + 1)
                        data['img_next'] = '<img title="'+ _("Next") +'" src="../img/next.gif" border="0">'

                        data['url_next'] = data['url_next'] % next_pagination

                i = i + 1

            if ((i == 2) and (data['row'] != '0')) or (i < 2 and data['row'] == '0'):
                data['url_next'] = ''
                data['close_link_next'] = ''
                data['img_next'] = ''

        else:
            data['url_next'] = ''
            data['close_link_next'] = ''
            data['img_next'] = ''

            data['img_prev'] = ''
            data['url_prev'] = ''
            data['close_link_prev'] = ''


        is_first = True
        for lang in self.data_langs:
            one_lang = list(lang.keys())[0]
            data['data_lang'] = list(lang.values())[0]

            self.execute('get_inst_data', data)
            inst_data = self.fetch('columns')
            num_fields = 11
            if len(inst_data) < num_fields:
                inst_data = DefDict()

            if is_first:
                data['code1'] = inst_data['code1'].replace('"','&quot;').replace("'","&#39;")
                data['code2'] = inst_data['code2'].replace('"','&quot;').replace("'","&#39;")
                data['code3'] = inst_data['code3'].replace('"','&quot;').replace("'","&#39;")
                data['complement'] = inst_data['complement'].replace('"','&quot;').replace("'","&#39;")
                data['nickname'] = inst_data['nickname'].replace('"','&quot;').replace("'","&#39;")
                data['name'] = inst_data['name'].replace('"','&quot;').replace("'","&#39;")
                data['address'] = inst_data['address'].replace("<a","<a class=\"tlink\"")
                data['phone'] = inst_data['phone'].replace("<a","<a class=\"tlink\"")
                data['email'] = inst_data['email']
                data['website'] = inst_data['website']
                data['message'] = '<b>%s</b><br />%s<br />' % (data['nickname'], data['name'])

                if('go_catalog' in inst_data):
                    if (inst_data['go_catalog']):
                        data['label_go_catalog'] = _("This institution goes to catalog")
                        data['is_go_catalog_check'] = "checked='checked'"
                    else:
                        data['label_go_catalog'] = ''
                        data['is_go_catalog_check'] = ""

                #Security info
                #permissions = self.g.get_permissions(self.cookie_value, 'institutions', data)

            data['comments_%s' %one_lang] = inst_data['comments']
            if action == 'view':
                data['comments_langs'] += '''%s: %s<br />
                ''' %("<span class='label_color'>"+one_lang+"</span>", data['comments_%s' %one_lang].replace("<a","<a class=\"tlink\""))
                data['email'] = "<a class='tlink' href='mailto:"+inst_data['email']+"'>"+inst_data['email']+"</a>"
                #If there is no protocol indicated, presume it to be "http"
                if inst_data['website'] != None and (inst_data['website'].find("://") == -1):
                  website_href = "http://"+inst_data['website']
                else:
                  website_href = inst_data['website']
                data['website'] = "<a class='tlink' target='_blank' href='"+website_href+"'>"+inst_data['website']+"</a>"
            else:
                data['comments_tabs'] = self.generateLanguageTabs('comments')

                classtyle = 'block' #change

                data['comments_langs'] += '''<span class='%s' id='comments_field_%s' >
                    <textarea name="comments_%s" id="comments_%s" class="mceEditor" cols="" rows="">%s</textarea>
                    </span>
                ''' %(classtyle, one_lang, one_lang, one_lang, data['comments_%s' %one_lang])

            is_first = False

        #Security Tab
        self.g.security_tab(self.cookie_value, action, data, 'institutions')
        return data

    def get_users_select(self, id_user=None):
        '''
        Display all available users in a <select> where: <option value="id_user">"name"</option>
        '''
        db = dbConnection()
        db.execute('get_all_users')
        users = db.fetch('all')
        #List sorting
        users = sorted(users, lambda x, y: cmp(x['name'].lower(), y['name'].lower()))
        users_opt = []
        for user in users:
            if user['id_user'] == id_user:
                users_opt.append('\n\t<option value="%s" selected="selected">%s</option>' % (user['id_user'],user['name']))
            else:
                users_opt.append('\n\t<option value="%s">%s</option>' % (user['id_user'],user['name']))
        return ''.join(users_opt)

    def get_username(self, id_user):
        db = dbConnection()
        db.execute('get_user_name', {'id_user':id_user})
        return db.fetch('one')

    def get_person_name(self, id_person):
        self.execute('get_one_person', {'id':id_person})
        return self.fetch('one')

    def get_inst_select(self, id_inst=None):
        '''
        Display all available clients (institutions) in a <select> where <option value="id_inst">"name"</option>
        '''
        self.execute('get_inst')
        institutions = self.fetch('all')
        inst_opt = []

        for inst in institutions:
            if inst['id_institution'] == id_inst:
                inst_opt.append('\n\t<option value="%s" selected="selected">%s</option>' % (inst['id_institution'],inst['name']))
            else:
                inst_opt.append('\n\t<option value="%s">%s</option>' % (inst['id_institution'],inst['name']))
        return ''.join(inst_opt)

    def get_person_select(self, id_person=None):
        '''
        Display all available clients (people) in a <select> where: <option value="id_person">"name"</option>
        '''
        self.execute('get_person')
        people = self.fetch('all')
        person_opt = []
        person_opt.append('\n\t<option value="">---</option>')
        for person in people:
            self.execute('get_person_contact_relations', {'id':person['id_person']})
            contacts = self.fetch('all')
            inst_list = []
            for contact in contacts:
                inst_list.append(str(contact['institution']))
            if len(inst_list) == 0:
                selected = ""
                if person['id_person'] == id_person: selected = 'selected="selected"'
                person_opt.append('\n\t<option value="%s" %s inst="-1">%s</option>' % (person['id_person'],selected,person['name']))
            elif person['id_person'] == id_person:
                person_opt.append('\n\t<option value="%s" inst="%s" selected="selected">%s</option>' % (person['id_person'],"|".join(inst_list),person['name']))
            else:
                person_opt.append('\n\t<option value="%s" inst="%s">%s</option>' % (person['id_person'],"|".join(inst_list),person['name']))
        return ''.join(person_opt)

    def get_preservation_method(self,id_method='', id_methods = []):
        '''
        Display all available preservation methods in a <select> where: <option value="id_preservation_method">"method"</option>
        '''
        self.execute('get_preservation_method_subcoll',{'id_lang':self.session.data['id_lang'],'id_subcoll':self.session.data['id_subcoll']})
        methods = self.fetch('all')
        #List sorting
        methods = sorted(methods, lambda x, y: cmp(x['method'].lower(), y['method'].lower()))
        method_opt = []
        for method in methods:
            selected = ''
            if method['id_preservation_method'] == id_method or method['id_preservation_method'] in id_methods:
                selected = "selected='selected'"
            method_opt.append('\n\t<option %s value="%s" unit="%s">%s</option>' % (selected, method['id_preservation_method'], method['unit_measure'], method['method']))
        return ''.join(method_opt)

    def get_documents(self,id_qualifier):
        '''
        Display all available documents of specified qualifier in a <select> where: <option value="id_doc">"title"</option>
        '''
        self.execute('get_doc_by_qualifier',{'id_lang':self.session.data['id_lang'],'id_coll':self.session.data['id_coll'],'id_qualifier':id_qualifier})
        docs = self.fetch('all')
        doc_opt = []
        doc_opt.append('\n\t<option value=""> </option>')
        for doc in docs:
          doc_opt.append('\n\t<option value="%s">%s</option>' % (doc['id_doc'],doc['title']))
        return ''.join(doc_opt)

    def get_strains_select(self,id_strain=''):
        '''
        Display all available strains in a <select> where:
        <option value="id_strain">"acronym" "code" - "taxon"</option>
        '''
        #on unused fields - keep one space (' ') in order to differ empty string from None Type
        
        if (id_strain == ''):
            condition = ' AND status <> \'inactive\''
        else:
            condition = ' AND (status <> \'inactive\' OR st.id_strain = %s)' % str(id_strain)
            
        #raise condition
        
        self.execute('get_strain_list_order_code', {'id_lang':self.session.data['id_lang'],'id_coll':self.session.data['id_coll'],'id_subcoll':self.session.data['id_subcoll'],'paging':' ','condition':condition,'field_order':'st.id_strain'}, True)
        strains = self.fetch('all')
        strain_opt = []
        for strain in strains:
          strain_full = ''
          strain_full += strain['code'] + ' - ' + Lists.spe_fullname(strain, use_infracomplement=True)

          selected = ''
          if strain['id_strain'] == id_strain:
              selected = "selected='selected'"

          strain_opt.append('\n\t<option %s value="%s">%s</option>' % (selected, strain['id_strain'],strain_full))

        return ''.join(strain_opt)

    def get_lot_select(self,id_lot=''):
        '''
        Display all available lots in a <select> where:
        <option value="id_lot">"name"</option>
        '''
        #Subcollection filtering
        self.data['id_subcoll'] = self.session.data['id_subcoll']

        self.execute('get_all_lot_gt_zero', self.data)
        lots = self.fetch('all')

        lot_opt = []
        for lot in lots:
          selected = ''
          if lot['id_lot'] == id_lot:
            selected = "selected='selected'"
          lot_opt.append('\n\t<option %s value="%s">%s</option>' % (selected, lot['id_lot'], lot['name']))
        return "".join(lot_opt)

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

    def distribution(self, action):
        data = self.data
        data['action'] = action
        data['title_langs'] = ''
        data['comments_langs'] = ''
        data['groups_table'] = ""
        data['url_next'] = "<a href='javascript:Proximo(\"distribution.detail.py?id=%(id)s&row=%(row)s\")'>"
        data['url_prev'] = "<a href='javascript:Anterior(\"distribution.detail.py?id=%(id)s&row=%(row)s\")'>"
        data['close_link_prev'] = '</a>'
        data['close_link_next'] = '</a>'
        data['img_prev']= ''
        data['img_next']= ''
        data['js_distribution_data'] = 'distribution_data = null;'

        if action == 'view': pass
        elif action == 'edit':
            data['next_action'] = 'update'
        elif action == 'new':
            data['next_action'] = 'insert'
            data['back_where'] = 'list'

        data['row_number'] = self.data['row']

        if (action == 'view' and 'row' in self.form):
            stripped_sciname = self.get_stripped("sciname_no_auth")

            #Verify field_order is changed
            if 'field_order' in self.form:
                self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'distribution', self.form['field_order'].value)

            isInstitution = False;

            #Get field and mode for order list
            field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'distribution')

            if field == 'lot_name':
                field = 'l.name %s' % mode
            elif field == 'species':
                field = stripped_sciname + " " + mode
            elif field == 'institution':
                isInstitution = True;
                field = 'i.name %s' % mode
            else:
                field = field + ' ' + mode


            #Define field_order with mode
            self.data['field_order'] = field

            if (data['row'] == '0'):
                data['paging'] = ' LIMIT %s,2' % data['row']
            else:
                data['paging'] = ' LIMIT %s,3' % str(int(self.data['row']) - 1)

            data['id_lang'] = self.session.data['id_lang']
            data['id_coll'] = self.session.data['id_coll']
            data['id_subcoll'] = self.session.data['id_subcoll']

            #Filter
            filter = ''
            if ('filter' in self.form):
                filter = str(self.form['filter'].value).strip()
                filter = self.ConvertStrUnicode(filter).encode("utf-8")

                #Save filter on session
                self.session.data['filter_distributions'] = filter
                self.session.save()
            elif ('filter_distributions' in self.session.data):
                filter = self.session.data['filter_distributions']
                filter = self.ConvertStrUnicode(filter).encode("utf-8")

            if (filter != ''):
                words = [x for x in filter.split(" ") if x != '']
                self.data['condition']= []
                for word in words:
                    #0x25 == '%'
                    self.data['condition'].append(
                            "AND (DATE_FORMAT(d.date,'" + self.get_dateformat('output') + "') LIKE x'25" + word.encode("hex") + "25' " +
                            "OR l.name LIKE x'25" + word.encode("hex") + "25' " +
                            "OR " + stripped_sciname + " LIKE x'25" + word.encode("hex") + "25' "
                            "OR dol.quantity = '" + word + "' OR i.name LIKE x'25" + word.encode("hex") + "25' OR p.name LIKE x'25" + word.encode("hex") + "25' " +
                            "OR st.infra_complement LIKE x'25" + word.encode("hex") + "25') ")
                self.data['condition']= "".join(self.data['condition'])
            else:
                self.data['condition'] = ' '

            #Execute again for rows count
            if self.g.isManager(self.session.data['roles']): #Administrator or Manager
              self.execute('get_distribution_ids', self.data, True)
            else:
              roles = str(self.session.data['roles']).replace("L","")
              roles = roles.replace("[","(")
              roles = roles.replace("]",")")
              self.data['roles_list'] = roles
              self.execute('get_distribution_ids_restrict', self.data,raw_mode = True)

            list_distribution = self.fetch('all')
            i=0
            for dsitribution in list_distribution:

                if (data['row'] == '0'):
                    if (i == 0):
                        data['img_prev'] = ''
                        data['url_prev'] = ''
                        data['close_link_prev'] = ''
                    else:
                        next_pagination = {}
                        next_pagination['id'] = dsitribution['id_distribution']
                        next_pagination['row'] = str(int(data['row']) + 1)
                        data['img_next'] = '<img title="'+ _("Next") +'" src="../img/next.gif" border="0">'

                        data['url_next'] = data['url_next'] % next_pagination
                else:
                    if (i == 0):
                        prev_pagination = {}
                        prev_pagination['id'] = dsitribution['id_distribution']
                        prev_pagination['row'] = str(int(data['row']) - 1)
                        data['img_prev'] = '<img title="'+ _("Previous") +'" src="../img/prev.gif" border="0">'

                        data['url_prev'] = data['url_prev'] % prev_pagination
                    elif (i == 2):
                        next_pagination = {}
                        next_pagination['id'] = dsitribution['id_distribution']
                        next_pagination['row'] = str(int(data['row']) + 1)
                        data['img_next'] = '<img title="'+ _("Next") +'" src="../img/next.gif" border="0">'

                        data['url_next'] = data['url_next'] % next_pagination

                i = i + 1

            if ((i == 2) and (data['row'] != '0')) or (i < 2 and data['row'] == '0'):
                data['url_next'] = ''
                data['close_link_next'] = ''
                data['img_next'] = ''

        else:
            data['url_next'] = ''
            data['close_link_next'] = ''
            data['img_next'] = ''

            data['img_prev'] = ''
            data['url_prev'] = ''
            data['close_link_prev'] = ''


        is_first = True
        for lang in self.data_langs:
            one_lang = list(lang.keys())[0]
            data['data_lang'] = list(lang.values())[0]
            self.execute('get_distribution_data', data)

            distributions = self.fetch('columns')

            num_fields = 10
            if len(distributions) < num_fields:
                distributions = DefDict()


            if is_first:
                data['id_coll'] = self.session.data['id_coll']
                data['id_subcoll'] = self.session.data['id_subcoll']
                data['distribution_date'] = self.format_date(action,distributions['date'])
                data['distribution_id_lot'] = distributions['id_lot']
                data['distribution_lot'] = self.get_lot_select(distributions['id_lot'])
                if data['distribution_lot'] == '' and action == 'new': #There are no Lots available yet
                    from . import exception
                    raise exception.SicolException("no_lots_available")
                data['distribution_lot_name'] = distributions['lot_name']
                data['distribution_id_strain'] = distributions['id_strain']
                data['distribution_strain'] = self.get_strains_select(distributions['id_strain'])
                if action != 'new':
                    data['distribution_strain_name'] = distributions['code'] + ' - ' + '<span class="species">' + Lists.spe_fullname(distributions, use_infracomplement=True) + '</span>'
                else:
                    data['distribution_strain_name'] = ''
                data['distribution_id_user'] = distributions['id_user']
                data['distribution_user'] = self.get_person_select(distributions['id_user'])
                data['distribution_user_name'] = self.get_person_name(distributions['id_user'])
                data['distribution_quantity'] = distributions.get('quantity', 0)

                from .location import LocationHelper
                location_helper = LocationHelper(action=action,model='distribution', data=data,cookie_value=self.cookie_value, decrease_stock_optional=True)

                if distributions['not_identified'] == 1:
                    data['location'] = location_helper.renderTag(not_identified=True)
                else:
                    data['location'] = location_helper.renderTag()

                data['distribution_id_institution'] = distributions['id_institution']
                data['distribution_institution'] = self.get_inst_select(distributions['id_institution'])
                data['distribution_institution_name'] = distributions['inst_name']
                if data['distribution_institution'] == '': #There are no Institutions available yet
                    from . import exception
                    raise exception.SicolException("no_inst_available")
                data['distribution_id_person'] = distributions['id_person']
                data['distribution_person'] = self.get_person_select(distributions['id_person'])
                data['distribution_person_name'] = distributions['person_name']

                previously_used_amp = {}
                if action == 'edit':
                    previously_used_amp[data['distribution_id_strain']] = {}
                    previously_used_amp[data['distribution_id_strain']][data['distribution_id_lot']] = {'used':int(data['distribution_quantity']),'prepared':0}

                    data['js_distribution_data'] = 'distribution_data = ["%s","%s"];' % (data['distribution_id_lot'],
                                                                                         data['distribution_lot_name'])

                data['js_global_lot_strain'] = self.get_lot_strain_ampoules(previously_used_amp=previously_used_amp, selected_id_lot=distributions['id_lot'])

                textLinksStrain = TextLinkFactory(self.cookie_value, self.session.data['id_lang'], data['data_lang'])
                textLinksStrain['distribution_reason'] = distributions['reason'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"")

                #changes textlink to html link
                textLinksStrain.fillData(data)

                #Show in Upper message square: date, strain, institution, person (if exists)
                person_name = ''
                if data['distribution_person_name'] != '---': person_name = data['distribution_person_name']
                data['message'] = '%s<br /><b>%s</b><br />%s<br />%s' % (data['distribution_date'], data['distribution_strain_name'], data['distribution_institution_name'], person_name)

                #Security info
                #permissions = self.g.get_permissions(self.cookie_value, 'distribution', data)

            is_first = False

        #Security Tab
        self.g.security_tab(self.cookie_value, action, data, 'distribution')
        return data

    def preservation(self, action):
        from .json import JsonBuilder
        self.logger.debug("PRESERVATION")
        data = self.data
        data['action'] = action
        data['title_langs'] = ''
        data['comments_langs'] = ''
        data['groups_table'] = ""
        data['id_coll'] = self.session.data['id_coll']
        data['id_subcoll'] = self.session.data['id_subcoll']
        data['url_next'] = "<a href='javascript:Proximo(\"preservation.detail.py?id=%(id)s&row=%(row)s\")'>"
        data['url_prev'] = "<a href='javascript:Anterior(\"preservation.detail.py?id=%(id)s&row=%(row)s\")'>"
        data['close_link_prev'] = '</a>'
        data['close_link_next'] = '</a>'
        data['img_prev']= ''
        data['img_next']= ''

        if action == 'view':
            data['display_origin_img'] = 'none'
        elif action == 'edit':
            data['next_action'] = 'update'
            data['display_origin_img'] = 'none'
        elif action == 'new':
            data['next_action'] = 'insert'
            data['back_where'] = 'list'
            data['display_origin_img'] = 'inline'

        data['row_number'] = self.data['row']

        if (action == 'view' and 'row' in self.form):
            #Verify field_order is changed
            if 'field_order' in self.form:
                self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'preservation', self.form['field_order'].value)

            isTaxon = False;

            #Get field and mode for order list
            field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'preservation')

            if field == 'lot_name':
                field = 'l.name %s' % mode
            elif field == 'species':
                stripped_sciname = self.get_stripped("sciname_no_auth")
                field = "l.name ASC, Code " + mode + ", " +  stripped_sciname + " " + mode
            elif field == 'date':
                field = 'date %s, l.name ' % mode
            elif field == 'method':
                field = 'pml.method %s, l.name, date ' % mode
            elif field == 'stock_minimum':
                field = 'l.name, stock_minimum %s, date' % mode
            elif field == 'stock':
                field = 'l.name, stock %s , date ' % mode
            else:
                field = "l.name, date, " + field + ' ' + mode

            #Define field_order with mode
            self.data['field_order'] = field

            #raise str(field)

            if (data['row'] == '0'):
                data['paging'] = ' LIMIT %s,2' % data['row']
            else:
                data['paging'] = ' LIMIT %s,3' % str(int(self.data['row']) - 1)

            data['id_lang'] = self.session.data['id_lang']
            data['id_coll'] = self.session.data['id_coll']
            data['id_subcoll'] = self.session.data['id_subcoll']

            stripped_sciname = self.get_stripped("sciname_no_auth")

            #Filter
            filter = ''
            if ('filter' in self.form):
                filter = str(self.form['filter'].value).strip()
                filter = self.ConvertStrUnicode(filter).encode("utf-8")

                #Save filter on session
                self.session.data['filter_preservations'] = filter
                self.session.save()
            elif ('filter_preservations' in self.session.data):
                filter = self.session.data['filter_preservations']
                filter = self.ConvertStrUnicode(filter).encode("utf-8")

            if (filter != ''):
                words = [x for x in filter.split(" ") if x != '']
                self.data['condition']= []
                for word in words:
                    #0x25 == '%'
                    self.data['condition'].append(
                            "AND (DATE_FORMAT(p.date,'" + self.get_dateformat('output') + "') LIKE x'25" + word.encode("hex") + "25' " +
                            "OR l.name LIKE x'25" + word.encode("hex") + "25' " +
                            "OR ((SELECT COUNT(preservation.id_preservation) " +
                            "FROM preservation " +
                            "INNER JOIN preservation_strain USING (id_preservation) " +
                            "INNER JOIN strain USING (id_strain) " +
                            "INNER JOIN species USING (id_species) " +
                            "WHERE preservation.id_preservation = p.id_preservation " +
                            "AND ('" + self.session.data['subcoll_code'] + "' LIKE x'25" + word.encode("hex") + "25' " +
                            "OR strain.code LIKE x'25" + word.encode("hex") + "25' " +
                            "OR " + stripped_sciname + " LIKE x'25" + word.encode("hex") + "25')) > 0) "
                            "OR pml.method LIKE x'25" + word.encode("hex") + "25' " +
                            "OR st.infra_complement LIKE x'25" + word.encode("hex") + "25') ")
                self.data['condition']= "".join(self.data['condition'])
            else:
                self.data['condition'] = ' '

            #Execute again for rows count
            if self.g.isManager(self.session.data['roles']): #Administrator or Manager
              self.execute('get_preservation_ids', self.data, True)
            else:
              roles = str(self.session.data['roles']).replace("L","")
              roles = roles.replace("[","(")
              roles = roles.replace("]",")")
              self.data['roles_list'] = roles
              self.execute('get_preservation_ids_restrict', self.data,raw_mode = True)
            list_preservation = self.fetch('all')

            i=0
            for preservation in list_preservation:

                if (data['row'] == '0'):
                    if (i == 0):
                        data['img_prev'] = ''
                        data['url_prev'] = ''
                        data['close_link_prev'] = ''
                    else:
                        next_pagination = {}
                        next_pagination['id'] = preservation['id_preservation']
                        next_pagination['row'] = str(int(data['row']) + 1)
                        data['img_next'] = '<img title="'+ _("Next") +'" src="../img/next.gif" border="0">'

                        data['url_next'] = data['url_next'] % next_pagination
                else:
                    if (i == 0):
                        prev_pagination = {}
                        prev_pagination['id'] = preservation['id_preservation']
                        prev_pagination['row'] = str(int(data['row']) - 1)
                        data['img_prev'] = '<img title="'+ _("Previous") +'" src="../img/prev.gif" border="0">'

                        data['url_prev'] = data['url_prev'] % prev_pagination
                    elif (i == 2):
                        next_pagination = {}
                        next_pagination['id'] = preservation['id_preservation']
                        next_pagination['row'] = str(int(data['row']) + 1)
                        data['img_next'] = '<img title="'+ _("Next") +'" src="../img/next.gif" border="0">'

                        data['url_next'] = data['url_next'] % next_pagination

                i = i + 1

            if ((i == 2) and (data['row'] != '0')) or (i < 2 and data['row'] == '0'):
                data['url_next'] = ''
                data['close_link_next'] = ''
                data['img_next'] = ''

        else:
            data['url_next'] = ''
            data['close_link_next'] = ''
            data['img_next'] = ''

            data['img_prev'] = ''
            data['url_prev'] = ''
            data['close_link_prev'] = ''


        #Get Main Data
        self.execute('get_preservation_data',data)
        preservation = self.fetch('columns')

        # marks all the strains that are reused on other
        # preservation, distribution or CQ
        not_identified_strains = []
        if 'id_lot' in preservation:
            self.logger.debug('^-^ %s ' % preservation['id_lot'])
            self.execute('get_lot_usage_information', { 'id_lot': preservation['id_lot'] }, force_debug=False)
            reused_strains = []
            rows = self.fetch('all')
            for row in rows:
              if not row['id_strain'] in reused_strains:
                  reused_strains.append(row['id_strain'])

            self.execute('get_preservation_lot_usage_information_identified', { 'id_lot': preservation['id_lot'] }, force_debug=False)
            rows = self.fetch('all')
            for row in rows:
              if not row['id_strain'] in reused_strains:
                  reused_strains.append(row['id_strain'])

            self.execute('get_preservation_lot_usage_information_all', { 'id_lot': preservation['id_lot'] })
            rows = self.fetch('all')
            for row in rows:
                if not row['id_strain'] in not_identified_strains:
                    not_identified_strains.append(row['id_strain'])

            self.execute('get_distribution_lot_usage_information_all', { 'id_lot': preservation['id_lot'] })
            rows = self.fetch('all')
            for row in rows:
                if not row['id_strain'] in not_identified_strains:
                    not_identified_strains.append(row['id_strain'])

            self.execute('get_quality_lot_usage_information_all', { 'id_lot': preservation['id_lot'] })
            rows = self.fetch('all')
            for row in rows:
                if not row['id_strain'] in not_identified_strains:
                    not_identified_strains.append(row['id_strain'])

            self.execute('get_movement_lot_usage_information_all', { 'id_lot': preservation['id_lot'] })
            rows = self.fetch('all')
            for row in rows:
                if not row['id_strain'] in reused_strains:
                    reused_strains.append(row['id_strain'])

        num_fields = 7
        if len(preservation) < num_fields:
            preservation = DefDict()

        #Get GLOBAL COUNTER
        self.execute('get_preservation_strain_count',data)
        global_counter = int(self.fetch('one')) + 1

        #Get Main Data
        data['date'] = self.format_date(action,preservation['date'])
        data['username'] = self.get_person_name(preservation['id_user'])
        data['lot_number'] = preservation['lot_name']
        data['main_lot_id'] = preservation['id_lot']
        data['used_method'] = preservation['used_method']
        data['data_lang'] = list(self.data_langs[0].values())[0]
        data['info'] = preservation['info']
        if action == 'view':
            textLinksStrain = TextLinkFactory(self.cookie_value, self.session.data['id_lang'], data['data_lang'])
            textLinksStrain.update({
                'info'   : data['info'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"")
            })
            #changes textlink to html link
            textLinksStrain.fillData(data)
        #Get Used Method
        data['preservation_method'] = self.get_preservation_method(preservation['id_method'])
        #Get all people available to be a responsible technician
        data['preservation_user'] = self.get_person_select(preservation['id_user'])
        #Set preservation_types
        data['display_origin_name'] = 'block'
        data['display_origin_lot'] = 'none'
        data['display_origin_lot_ampoules'] = 'none'


        #Get purity state
        output = '<select name="preservation_purity" id="preservation_purity">'
        output += '<option value="ok" selected="selected" >%s</option>' % _("OK")
        output += '<option value="contaminated">%s</option>' % _("Contaminated")
        output += '</select>'
        data['preservation_purity'] = output
        #Get Preservation Type
        output = '<select name="preservation_type" id="preservation_type">'
        output += '<option value="none" selected="selected" ></option>'
        output += '<option value="spore" %%s >%s</option>' % _("Preservation by Spores")
        output += '<option value="block" %%s >%s</option>' % _("Preservation by Blocks")
        output += '</select>'
        data['preservation_type'] = output
        #Get culture medium
        data['preservation_culture_medium'] = self.get_documents(4) #4 = doc_qualifier == 'Medium'
        #Get Available Strains
        data['preservation_strain'] = self.get_strains_select()
        #Input hidden
        data['old_combination'] = []
        #Start-up Javascript
        data['js_data'] = []
        if not_identified_strains:
            data['js_data'].append(' not_identified_strains = ' + JsonBuilder.dump(not_identified_strains) + ';')
        else:
            data['js_data'].append(' not_identified_strains = null ;')

        previously_used_amp = {}
        #Upper content
        data['message'] = '%s - <b>Lote %s</b><br />%s' % (data['date'], preservation['lot_name'], preservation['used_method'])

        #Get Data for each Strain
        self.execute('get_preservation_strain_data',data,force_debug=False)
        preservation_strain = self.fetch('all') #26 fields

        #Security tab
        self.g.security_tab(self.cookie_value, action, data, 'preservation')

        invalid_lots = {}
        from .labels import label_dict
        strain_data = []
        aux_dict = {}

        if (global_counter == 1):
            data['js_data'].append(' reused_strains = null; ')

        for i in range(1,global_counter):
            j = i - 1 #index for manipulation of "preservation_strain" dictionary
            aux_dict = preservation_strain[j]

            if action == 'view':
                self.logger.debug("#AUX_DICT#")
                self.logger.debug(aux_dict)

                #Label Translation
                aux_dict.update(label_dict)
                aux_dict['i'] = i
                self.logger.debug('*** aux_dict')
                self.logger.debug(aux_dict['id_strain'])
                self.logger.debug(data['main_lot_id'])
                amp_data = {'id_strain': aux_dict['id_strain'], 'id_lot': data['main_lot_id']}
                self.execute('get_preservation_strain_prepared_ampoules', amp_data, force_debug=False)
                aux_dict['prepared'] = self.fetch('one')
                #Fill used e prepared with unit of measure
                aux_dict['preservation_prepared'] = _("Number of Prepared %s") % preservation['unit_measure']
                #Species full name
                aux_dict['species_fullname'] = Lists.spe_fullname(aux_dict, use_infracomplement=True).replace("%","%%")
                aux_dict['strain_fullname'] = aux_dict['code'] + ' - ' + '<span class="species">' + aux_dict['species_fullname'] + '</span>'
                if aux_dict['origin_type'] == 'original': #Show Original Culture's name
                    aux_dict['origin_name'] = aux_dict['origin']
                    aux_dict['origin'] = _("Original Culture")
                    aux_dict['origin_info'] = '''
                        <p class="cols_3">
                            <label>%(label_Preservation_Strain_Origin)s :</label> %(origin)s
                        </p>
                        <p class="cols_3">
                            <label>%(label_Preservation_General_Strain_Code)s :</label> %(origin_name)s
                        </p>
                        <p class="cols_3">
                            &nbsp;
                        </p>
                    ''' % aux_dict
                elif aux_dict['origin_type'] == 'lot': #Show Lot Number and Amount Used
                    aux_dict['preservation_used'] = _("Number of Used %s") % aux_dict['unit_measure']
                    aux_dict['origin'] = _("Lot Number")
                    if aux_dict['not_identified']: # Not identified origin
                        aux_dict['origin_pos'] = _("Not identified")
                    else:
                        aux_dict['origin_pos'] = self.l.get_location(aux_dict['id_container'], aux_dict['id_origin_container_hierarchy'], aux_dict['origin_row'], aux_dict['origin_col'], quantity=aux_dict['origin_quantity'])
                    self.logger.debug("Origin: %s" % aux_dict['origin_pos'])
                    aux_dict['origin_info'] = '''
                        <p class="cols_3">
                            <label>%(label_Preservation_Strain_Origin)s :</label> %(origin)s
                        </p>
                        <p class="cols_3">
                            <label>%(label_Preservation_General_Origin_Lot_Number)s :</label> %(lot_name)s
                        </p>
                        <p class="cols_3" style='white-space:nowrap;'>
                            <label>%(label_Preservation_Strain_Origin_Position)s :</label> %(origin_pos)s
                        </p>
                    ''' % aux_dict

                if aux_dict['purity'] == 'y':
                    aux_dict['purity'] = _("Ok")
                else:
                    aux_dict['purity'] = "<b class='red_info'>" + _("Contaminated") + "</b>"
                #Counting
                if aux_dict['counting_na'] == 'y':
                    aux_dict['does_counting_apply'] = ' ('+_("Does not apply")+')'
                elif aux_dict['counting_na'] == 'n':
                    aux_dict['does_counting_apply'] = ''
                #Create link to DOC referencing CULTURE MEDIUM
                aux_dict['culture_medium'] = """<a href='javascript:popWinOpen("./docpopup.detail.py?id=%s",760,400,"%s");' class=\"tlink\" >%s</a>""" % (aux_dict['id_doc'], _("Culture Medium") ,aux_dict['culture_medium'])
                if aux_dict['preservation_type'] == 'block':
                    aux_dict['preservation_type'] = _("By Blocks")
                elif aux_dict['preservation_type'] == 'spore':
                    aux_dict['preservation_type'] = _("By Spores")
                elif aux_dict['preservation_type'] == 'none':
                    aux_dict['preservation_type'] = _("Does not apply")
                temp = ''
                aux_dict['stock_pos'] = "<br/>" + aux_dict['stock_pos'].replace("\n", "<br/>")
                #self.execute('get_current_locations', { 'id_lot': preservation['id_lot'], 'id_strain': aux_dict['id_strain'] })
                #aux_dict['current_locations'] =
                #tinyMCE & TextLink
                textLinksStrain = TextLinkFactory(self.cookie_value, self.session.data['id_lang'], data['data_lang'])
                textLinksStrain.update({
                    'macro'     : aux_dict['macro'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\""),
                    'micro'     : aux_dict['micro'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\""),
                    'result'    : aux_dict['result'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\""),
                    'obs'       : aux_dict['obs'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"")
                })
                #changes textlink to html link
                textLinksStrain.fillData(aux_dict)
                #Get Data for THIS Strain
                strain_data.append('''
                <div id="strain_%(i)s">

                    <p>
                        <a class="a_pointer" onclick="return MaximizeMinimize(this,'innerstrain_');" ><img title='%(label_Preservation_Strain_Maximize)s' src='../img/maximize.gif' border='0' /></a>
                        <label>%(label_Preservation_Strain_Strain)s :</label> %(strain_fullname)s</p>
                    </p>

                    <div id='innerstrain_%(i)s' style='display:none'>
                    <fieldset class='preserv_fieldset'><legend>%(label_Preservation_Strain_Origin_Fieldset)s</legend>
                           %(origin_info)s
                       <p class='cols_3' style='clear:both'>
                           <label>%(preservation_prepared)s:</label> %(prepared)s
                        </p>
                        <p class='cols_3'>
                            <label>%(label_Preservation_Strain_Stock_Position)s :</label> %(stock_pos)s
                        </p>
                        <p class='cols_3'>
                            <label>%(label_Preservation_Strain_Stock_Limit)s :</label> %(stock_minimum)s
                        </p>
                    </fieldset>
                    <fieldset class='preserv_fieldset'><legend>%(label_Preservation_Strain_Culture_Conditions)s</legend>
                        <p class='cols_3'>
                            <label>%(label_Preservation_Strain_Culture_Medium)s : </label> %(culture_medium)s
                        </p>
                        <p class='cols_3'>
                            <label>%(label_Preservation_Strain_Temperature)s :</label> %(temp)s
                        </p>
                        <p class='cols_3'>
                            <label>%(label_Preservation_Strain_Incubation_Time)s :</label> %(incub_time)s
                        </p>
                    </fieldset>
                    <fieldset class='preserv_fieldset'><legend>%(label_Preservation_General_Preservation_Method_Fieldset)s</legend>
                        <p class='cols_3'>
                            <label>%(label_Preservation_Strain_Cryoprotector)s :</label> %(cryo)s
                        </p>
                        <p class='cols_3'>
                            <label>%(label_Preservation_Strain_Type)s :</label> %(preservation_type)s
                        </p>
                    </fieldset>
                    <fieldset class='preserv_fieldset'><legend>%(label_Preservation_Strain_Purity_Fieldset)s</legend>
                        <p class='cols_3'>
                            <label>%(label_Preservation_Strain_Purity)s :</label> %(purity)s
                        </p>
                        <p class='cols_3'>
                            <label>%(label_Preservation_Strain_Counting)s :</label> %(counting)s %(does_counting_apply)s
                        </p>
                    </fieldset>
                        <p>
                            <label>%(label_Preservation_Strain_Macro_Characs)s :</label> %(macro)s
                        </p>
                        <p>
                            <label>%(label_Preservation_Strain_Micro_Characs)s :</label> %(micro)s
                        </p>
                        <p>
                            <label>%(label_Preservation_Strain_Result)s :</label> %(result)s
                        </p>
                        <p>
                            <label>%(label_Preservation_Strain_Obs)s :</label> %(obs)s
                        </p>
                    </div>
                </div>
                <br />
                <hr />''' % aux_dict)

            else: #edit,recover
                id_lot_aux = aux_dict["id_lot"]
                if str(id_lot_aux) == '': id_lot_aux = 0
                data['old_combination'].append("%s-%s" % (aux_dict['id_strain'],id_lot_aux))
                invalid_lots[int(aux_dict['id_strain'])] = []
                #Ignore own Lot ID
                invalid_lots[int(aux_dict['id_strain'])].append(int(data['main_lot_id']))
                self.get_invalid_lots(invalid_lots,int(aux_dict['id_strain']),int(data['main_lot_id']))
                #raise str(data['main_lot_id'])
                #raise str(invalid_lots)
                all_info = []
                aux_data = ''
                #.replace('"','&quot;').replace("'","&#39;")
                aux_data += '\tstrain_info[%s] = {' % i
                all_info.append("'strain':'"+str(aux_dict["id_strain"])+"'")
                all_info.append("'code':'"+str(aux_dict["code"])+"'")
                all_info.append("'sciname_no_auth':'"+str(Lists.strip_ml_tags(aux_dict["sciname_no_auth"]))+"'")
                all_info.append("'prepared':'"+str(aux_dict["prepared"]).replace("'","\\'")+"'")
                all_info.append("'origin_type':'"+aux_dict["origin_type"]+"'")
                if aux_dict["origin_type"] == "original": #Show Original Culture's name
                    all_info.append("'origin_info':'"+aux_dict["origin"].replace("'","\\'")+"'")
                elif aux_dict["origin_type"] == "lot": #Show Lot Number and Amount Used
                    #self.logger.debugObj('aux_dict: %s', aux_dict)
                    all_info.append("'used':'"+str(aux_dict["used"]).replace("'","\\'")+"'")
                    all_info.append("'id_lot':'"+str(aux_dict["id_lot"])+"'")
                    all_info.append("'lot_name':'"+str(aux_dict["lot_name"])+"'")
                    all_info.append("'origin_location':'%(id_origin_container_hierarchy)s_%(origin_row)s_%(origin_col)s_%(origin_quantity)s'" % aux_dict)
                    if aux_dict['not_identified']:
                        all_info.append("'origin_container_id':''")
                        all_info.append("'origin_location_text':'%s'" % _("Not identified"))
                    else:
                        all_info.append("'origin_container_id':%s" % aux_dict['id_container'])
                        all_info.append("'origin_location_text':'%s'" %
                            self.l.get_incomplete_location(aux_dict['id_origin_container_hierarchy'], aux_dict['origin_row'], aux_dict['origin_col'], quantity=aux_dict['origin_quantity']))
                    #Update info about previously used ampoules for this lot-strain combination
                    if aux_dict["id_strain"] not in previously_used_amp:
                        previously_used_amp[aux_dict["id_strain"]] = {}
                    if aux_dict["id_lot"] not in previously_used_amp[aux_dict["id_strain"]]:
                        previously_used_amp[aux_dict["id_strain"]][aux_dict["id_lot"]] = {'used':0,'prepared':0}
                    previously_used_amp[aux_dict["id_strain"]][aux_dict["id_lot"]]["used"] = aux_dict["used"]
                if aux_dict["id_strain"] not in previously_used_amp:
                    previously_used_amp[aux_dict["id_strain"]] = {}
                if data["main_lot_id"] not in previously_used_amp[aux_dict["id_strain"]]:
                    previously_used_amp[aux_dict["id_strain"]][data["main_lot_id"]] = {'used':0,'prepared':0}
                previously_used_amp[aux_dict["id_strain"]][data["main_lot_id"]]["prepared"] = aux_dict["prepared"]

                self.d('stock_pos(aux_dict): %s' % aux_dict['stock_pos'])
                self.d(aux_dict['stock_pos'])

                all_info.append("'stock_pos_str':'"+aux_dict["stock_pos"].replace("'","\\'").replace("\n", "\\n").replace("\r", "")+"'")

                temp_sp = []
                self.d(' --=========-- ')
                for sp in aux_dict['stock_pos'].split("\n"):
                    self.d(sp)
                    if sp:
                        sp = sp.replace("\r", "")
                        temp_sp.append("'%s': '%s'" % (sp, sp))

                all_info.append("'stock_pos': {%s}" % ', '.join(temp_sp))

                self.d('all_info: %s' % all_info)

                #self.logger.debug("*** id_lot: %(id_lot)s, id_strain: %(id_strain)s" % { 'id_lot': preservation['id_lot'], 'id_strain': aux_dict['id_strain'] })
                self.execute('get_lot_strain_location', { 'id_lot': preservation['id_lot'], 'id_strain': aux_dict['id_strain'] })
                rows = self.fetch('all')
                for row in rows:
                    tr = {}
                    tr['row'] = LocationBuilder.get_label(row['ini_row'], row['row'])
                    tr['col'] = LocationBuilder.get_label(row['ini_col'], row['col'])
                    row['location'] = row['pattern'] % tr
                all_info.append("'current_locations': '" + JsonBuilder.dump(rows) + "'")
                all_info.append("'stock_minimum':'"+str(aux_dict["stock_minimum"])+"'")
                all_info.append("'culture_medium':'"+str(aux_dict["id_doc"])+"'")
                all_info.append("'temp':'"+aux_dict["temp"].replace("'","\\'")+"'")
                all_info.append("'incub_time':'"+aux_dict["incub_time"].replace("'","\\'")+"'")
                all_info.append("'cryo':'"+aux_dict["cryo"].replace("'","\\'")+"'")
                all_info.append("'preservation_type':'"+aux_dict["preservation_type"]+"'")
                all_info.append("'purity':'"+aux_dict["purity"]+"'")
                all_info.append("'counting':'"+aux_dict["counting"].replace("'","\\'")+"'")
                all_info.append("'counting_na':'"+aux_dict["counting_na"]+"'")
                all_info.append("'macro':'"+aux_dict["macro"].replace("'","\\'")+"'")
                all_info.append("'micro':'"+aux_dict["micro"].replace("'","\\'")+"'")
                all_info.append("'result':'"+aux_dict["result"].replace("'","\\'")+"'")
                all_info.append("'obs':'"+aux_dict["obs"].replace("'","\\'")+"'")
                aux_data += ",".join(all_info)
                aux_data += '}; reused_strains = ' + JsonBuilder.dump(reused_strains) + ';'
                data['js_data'].append(aux_data)
                data['hdn_reused_strain'] = JsonBuilder.dump(reused_strains)


        data['old_combination'] = ",".join(data['old_combination'])
        #Get possible origins. #<span> needed to fix IE-only bug
        output = '<select name="preservation_origin" id="preservation_origin" onchange="changedOrigin(this)">'
        output += '<option value="original" selected="selected">%s</option>' % _("Original Culture")
        #Create Global Javascript Variable to control ampoules stock within each lot-strain combination
        if 'id_lot' not in aux_dict:
            aux_dict['id_lot'] = 0
        data['js_global_lot_strain'] = self.get_lot_strain_ampoules(invalid_lots=invalid_lots,previously_used_amp=previously_used_amp,selected_id_lot=aux_dict["id_lot"])
        if data['js_global_lot_strain'] == 'global_strain_lot = null;': #special case: this is the first lot inserted
            output += '</select>'
        else:
            output += '<option value="lot">%s</option>' % _("Lot")
            output += '</select>'
        data['preservation_origin'] = output
        #Finalize start-up javascript
        data['js_data'] = "\n".join(data['js_data'])
        data['preservation_strains_data'] = ''.join(strain_data)

        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        self.logger.debug(pp.pformat(data))

        return data

    def generateLanguageTabs(self, label):
        tabs_html = ' &nbsp; <span class="fieldstab" >'
        is_first = True
        for lang in self.data_langs:
            one_lang = list(lang.keys())[0]
            tab_style = 'inactive'
            if is_first:
                tab_style = 'active'
            tabs_html += '''
                <a id='%s_tab_%s'class='%s' href='javascript:changeLanguageTab(\"%s\", \"%s\");'>%s</a>&nbsp;
            '''%(label, one_lang, tab_style, label, one_lang, one_lang)
            is_first = False
        tabs_html += '</span>'
        return tabs_html

    def get_invalid_lots(self,invalid_lots,id_strain,id_current_lot):
        '''
        RECURSIVE FUNCTION
        Fill up dictionary with an array of Invalid Lots IDs
        dict invalid_lots - dictionary to be filled up
        int id_strain - Strain ID
        int id_current_lot - Current Lot's ID
        '''
        #Grab children
        self.execute('get_preservation_strain_descendants',{'id_strain':id_strain,'id_lot':id_current_lot})
        children = self.dbconnection.fetch('all')
        for child in children:
            #Visit them first
            child_id_lot = int(child['p_id_lot'])
            self.get_invalid_lots(invalid_lots,id_strain,child_id_lot)
            #Add Lot ID to invalid_lots dictionary
            invalid_lots[id_strain].append(child_id_lot)
        return

    def get_lot_strain_ampoules(self,chosen_strain=0,previously_used_amp={},invalid_lots={},selected_id_lot=0):
        '''
        Create Javascript Global Variable with the amount of ampoules per Lot-Strain combination
        int chosen_strain - Filter dictionary to only show data about chosen strain (id)
        dict previously_used_amp - Dictionary with info about amount of ampoules originally used
        int main_lot_id - ID of current editing lot (0 if new/unknown lot)
        '''
        str_js = 'global_strain_lot = {'
        if selected_id_lot == '':
            selected_id_lot = 0
        self.execute('get_lot_strain_ampoules_combo',{'id_lot':selected_id_lot, 'id_lang':self.session.data['id_lang']})
        lsac = self.fetch('all') #lsac = lot-strain-ampoule-combo
        last_strain = 0
        js = []
        aux_js = []
        for lsa in lsac:
            #Filter by chosen strain id (if id != 0)
            if chosen_strain != 0 and last_strain == chosen_strain and lsa['id_strain'] != chosen_strain:
                break
            if chosen_strain != 0 and lsa['id_strain'] != chosen_strain:
                continue
            if lsa['id_strain'] != last_strain:
                if last_strain != 0:
                    js.append(str(last_strain) + ':{' + ",".join(aux_js) + '}')
                    aux_js = []
                last_strain = lsa['id_strain']
            used_amp = 0
            prepared_amp = 0
            #Add "previously used amount of ampoules" if exists
            if previously_used_amp != {}:
                if lsa['id_strain'] in previously_used_amp:
                    if lsa['id_lot'] in previously_used_amp[lsa['id_strain']]:
                        used_amp = previously_used_amp[lsa['id_strain']][lsa['id_lot']]['used']
                        prepared_amp = previously_used_amp[lsa['id_strain']][lsa['id_lot']]['prepared']
            #Ignore invalid lots
            if invalid_lots == {} or (int(lsa['id_strain']) not in invalid_lots) or ( int(lsa['id_lot']) not in invalid_lots[int(lsa['id_strain'])] ):
                aux_js.append('%d:{"name":"%s","ampoules":%d,"used":%d,"prepared":%d,"unit_measure":"%s"}' % (lsa['id_lot'],lsa['name'],lsa['stock'],used_amp,prepared_amp,lsa['unit_measure']))
        if last_strain != 0:
            js.append(str(last_strain) + ':{' + ",".join(aux_js) + '}')
        #Finalize dictionary
        str_js += ",".join(js) + '};'
        if len(js) > 0:
            return str_js
        else:
            return 'global_strain_lot = null;'

    def possible_members(self):
        '''
        Create possible members' global array
        '''
        db = dbConnection()
        db.execute('get_all_users')
        members = db.fetch('all')
        group_members = '<script type="text/javascript">var _grouparray_possible_members = new Array();\n'
        for member in members:
            group_members += "_grouparray_possible_members[_grouparray_possible_members.length] = new Array('%s','%s');\n" % (member['name'],member['id_user'])
        group_members += "</script>"
        return group_members

    def possible_data_langs(self,global_var_name=''):
        '''
        Create possible data_langs' global array
        '''
        self.execute('get_possible_data_langs')
        data_langs = self.fetch('rows')
        data_languages = '<script type="text/javascript">var _%sarray_possible_data_langs = new Array();\n' % global_var_name
        for data_lang in data_langs:
            data_languages += "_%sarray_possible_data_langs[_%sarray_possible_data_langs.length] = '%s';\n" % (global_var_name,global_var_name,data_lang)
        data_languages += "</script>"
        return data_languages

    def possible_combo_values(self,combo_name,id_lang):
        '''
        Create possible combo values' global array
        '''
        if combo_name == 'taxon_group':
          self.execute('get_taxon_groups', {'id_lang':id_lang})
          taxon_groups = self.fetch('all')
          js_taxon_groups = '<script type="text/javascript">var _array_possible_taxon_groups = new Array();\n'
          for taxon_group in taxon_groups:
              js_taxon_groups += "_array_possible_taxon_groups[_array_possible_taxon_groups.length] = new Array('%s','%s','%s');\n" % (taxon_group['taxon_group'], taxon_group['id_taxon_group'], taxon_group['has_hierarchy'])
          js_taxon_groups += "</script>"
          return js_taxon_groups
        elif combo_name == 'str_type':
          self.execute('get_str_type', {'id_lang':id_lang})
          str_types = self.fetch('all')
          js_str_types = '<script type="text/javascript">var _array_possible_str_types = new Array();\n'
          for str_type in str_types:
              js_str_types += "_array_possible_str_types[_array_possible_str_types.length] = new Array('%s','%s');\n" % (str_type['type'],str_type['id_type'])
          js_str_types += "</script>"
          return js_str_types
        elif combo_name == 'dep_reason':
          self.execute('get_str_dep_reason', {'id_lang':id_lang})
          dep_reasons = self.fetch('all')
          js_dep_reasons = '<script type="text/javascript">var _array_possible_dep_reasons = new Array();\n'
          for dep_reason in dep_reasons:
              js_dep_reasons += "_array_possible_dep_reasons[_array_possible_dep_reasons.length] = new Array('%s','%s');\n" % (dep_reason['dep_reason'],dep_reason['id_dep_reason'])
          js_dep_reasons += "</script>"
          return js_dep_reasons
        elif combo_name == 'preservation_method':
          self.execute('get_preservation_method', {'id_lang':id_lang})
          preservation_methods = self.fetch('all')
          js_preservation_methods = '<script type="text/javascript">var _array_possible_preservation_methods = new Array();\n'
          for preservation_method in preservation_methods:
              js_preservation_methods += "_array_possible_preservation_methods[_array_possible_preservation_methods.length] = new Array('%s','%s');\n" % (preservation_method['method'],preservation_method['id_preservation_method'])
          js_preservation_methods += "</script>"
          return js_preservation_methods
        elif combo_name == 'test_group':
          self.execute('get_test_group', {'id_lang':id_lang})
          test_groups = self.fetch('all')
          js_test_groups = '<script type="text/javascript">var _array_possible_test_groups = new Array();\n'
          for test_group in test_groups:
              js_test_groups += "_array_possible_test_groups[_array_possible_test_groups.length] = new Array('%s','%s');\n" % (test_group['category'],test_group['id_test_group'])
          js_test_groups += "</script>"
          return js_test_groups

    def data_lang_list(self):
        '''
        Get all available data langs in database
        '''
        self.execute('get_all_from_table',{'table':'lang'})
        langs = self.fetch('all')
        return langs

    def possible_start_pages(self):
        '''
        Get all possible start pages
        '''
        self.execute('get_possible_start_pages')
        start_pages = self.fetch('all')
        current_start_page = self.g.get_config('start_page')
        opt = []
        for page in start_pages:
          selected = ''
          pg = page['name']+'.list'
          if pg == current_start_page:
            selected = "selected='selected'"
          opt.append("<option %s value='%s'>%s</option>" % (selected,pg,page['description']))
        return "\n".join(opt)

    def group_members(self, role_id):
        '''
        Create group members' string
        '''
        db = dbConnection()
        self.execute('get_group_members', {'id_role':role_id})
        members = self.fetch('all')
        group_members = []
        for member in members:
            #Get user name from his ID
            db.execute('get_user_name',{'id_user':member['id_user']})
            group_members.append(str(db.fetch('one').encode('utf8')) + "," + str(member['id_user']))
        group_members = ";".join(group_members)
        return group_members.decode('utf8')

    def subcoll_data_langs(self, id_subcoll):
        '''
        Create Subcollection Languages string
        '''
        db = dbConnection()
        db.execute('get_subcoll_data_langs', {'id_subcoll':id_subcoll})
        subcoll_data_langs = db.fetch('all')
        subcoll_data_languages = []
        for subcoll_data_lang in subcoll_data_langs:
            subcoll_data_languages.append(subcoll_data_lang['data_lang'])
        subcoll_data_languages = "'" + ",".join(subcoll_data_languages) + "'"
        return subcoll_data_languages

    def subcoll_combo_config(self, id_subcoll,combo_name):
        '''
        Create Subcollection Combo Configuration string
        '''
        if combo_name == "taxon_group":
            self.execute('get_subcoll_combo_taxon_group', {'id_subcoll':id_subcoll})
        elif combo_name == 'str_type':
          self.execute('get_subcoll_combo_str_type', {'id_subcoll':id_subcoll})
        elif combo_name == 'dep_reason':
          self.execute('get_subcoll_combo_dep_reason', {'id_subcoll':id_subcoll})
        elif combo_name == 'preservation_method':
          self.execute('get_subcoll_combo_preservation_method', {'id_subcoll':id_subcoll})
        elif combo_name == 'test_group':
          self.execute('get_subcoll_combo_test_group', {'id_subcoll':id_subcoll})
        elements = self.fetch('rows')
        vector = []
        for el in elements:
          vector.append(str(el))
        return str("'" + ",".join(vector) + "'")

    def user_roles(self,id_user):
        '''
        Return a comma separated list of user groups
        '''
        self.execute('get_user_roles_names',{'id_user':id_user})
        user_roles = self.fetch('rows')
        return ", ".join(user_roles)

    def get_available_docs(self,id_lang,id_coll,roles):
        if self.g.isManager(roles): #Administrator or Manager
          self.execute('get_doc_list', {'id_lang':id_lang,'id_coll':id_coll,'field_order':'code','paging':' ','condition':' '},raw_mode = True)
        else:
          roles = str(self.session.data['roles']).replace("L","")
          roles = roles.replace("[","(")
          roles = roles.replace("]",")")
          self.execute('get_doc_list_restrict',{'id_lang':id_lang,'id_coll':id_coll,'field_order':'code','roles_list':roles,'paging':' ','condition':' '},raw_mode = True)
        docs = self.fetch('all')
        sel_doc = []
        for one_doc in docs:
          if one_doc['title'] == '': #Get first title found by id_lang (usually English)
            self.execute('get_first_doc_title_found',{'id_doc':one_doc['id_doc']})
            one_doc['title'] = self.fetch('one')
          if one_doc['title'] == '':
              one_doc['title'] = str(one_doc['code'])
          else:
              one_doc['title'] = '%s - %s' % (str(one_doc['code']), one_doc['title'])

          sel_doc.append("<option value='%s' qualifier='%s'>%s</option>" % (one_doc['code'],one_doc['qualifier'],one_doc['title']) )
        return "<br />\n".join(sel_doc)

    def get_available_refs(self,id_lang,id_coll,roles):
        if self.g.isManager(roles): #Administrator or Manager
          self.execute('get_ref_list', {'id_lang':id_lang,'id_coll':id_coll,'field_order':'id_ref','paging':' ','condition':' '},raw_mode = True)
        else:
          roles = str(self.session.data['roles']).replace("L","")
          roles = roles.replace("[","(")
          roles = roles.replace("]",")")
          self.execute('get_ref_list_restrict',{'id_lang':id_lang,'id_coll':id_coll,'field_order':'id_ref','roles_list':roles,'paging':' ','condition':' '},raw_mode = True)
        refs = self.fetch('all')
        sel_ref = []

        for one_ref in refs:
          #if one_ref['title'] == '': #Get first title found by id_lang (usually English)
            #self.execute('get_first_ref_title_found',{'id_ref':one_ref['id_ref']})
            #one_ref['title'] = self.fetch('one')
          if one_ref['title'] == '':
              one_ref['title'] = str(one_ref['id_ref'])
          else:
              one_ref['title'] = '%s - %s' % (str(one_ref['id_ref']), one_ref['title'])

          sel_ref.append("<option value='%s'>%s</option>" % (one_ref['id_ref'],self.g.removeHTML(one_ref['title'])) )
        return "<br />\n".join(sel_ref)

    def get_doc_qualifiers(self):
        self.execute('get_doc_qualifiers')
        qualifiers = self.fetch('rows')
        q_doc = []
        for one_q in qualifiers:
          q_doc.append("<option value='%s'>%s</option>" % (one_q,one_q) )
        return "<br />\n".join(q_doc)

    @classmethod
    def user_lines_per_page(self,id_user):
        '''
        Return how many lines are shown per page (used in list paging)
        '''
        db = dbConnection()
        db.execute('get_user_lines_per_page',{'id_user':id_user})
        return db.fetch('one')

    @classmethod
    def user_max_num_pages(self,id_user):
        '''
        Return how numbers pages are shown in pagination (used in list paging)
        '''
        db = dbConnection()
        db.execute('get_user_max_num_pages',{'id_user':id_user})
        return db.fetch('one')

    @classmethod
    def user_show_str_inactives(self,id_user,html=False):
        '''
        Return if the users wants to see strains inactives
        '''
        db = dbConnection()
        db.execute('get_user_show_str_inactives',{'id_user':id_user})
        show_str_inactives = db.fetch('one')

        if (html):
            if (show_str_inactives):
                return "checked"
            else:
                return ""
        else:
            return show_str_inactives

    def get_possible_alternate_states(self, id_specie):
        self.execute('get_possible_alternate_states', {'id_coll':self.session.data['id_coll'],'id_subcoll':self.session.data['id_subcoll']})
        species_list = self.fetch('all')
        alternate_states = []
        alternate_states.append("var alternate_states = new Array();\n")
        #List sorting
        species_list = sorted(species_list, lambda x, y: cmp(Lists.spe_fullname(x), Lists.spe_fullname(y)))
        for species in species_list:
            if (str(id_specie) != str(species['id_species'])):
                alternate_states.append("alternate_states[alternate_states.length] = ")
                alternate_states.append("['%s', '%s', '%s'];" % (species['taxongroup'], species['id_species'], Lists.spe_fullname(species, apply_font_style = False, use_author=False).replace("%","%%")))
        return "".join(alternate_states)

    def verify_lot_exist(self, id_strain):
        '''
        Verify if there is any lot related to the strain 'id_strain'
        '''
        self.execute('verify_lot_exist', {'id_strain':id_strain})
        return self.fetch('one')

    def container(self, action):
        #brk(host="localhost", port=9000)
        
        data = self.data
        data['id_subcoll'] = self.session.data['id_subcoll']
        data['action'] = action
        data['url_next'] = "<a href='javascript:Proximo(\"container.detail.py?id=%(id)s&row=%(row)s\")'>"
        data['url_prev'] = "<a href='javascript:Anterior(\"container.detail.py?id=%(id)s&row=%(row)s\")'>"
        data['close_link_prev'] = '</a>'
        data['close_link_next'] = '</a>'
        data['img_prev']= ''
        data['img_next']= ''

        if action == 'view': pass
        elif action == 'edit':
            data['next_action'] = 'update'
        elif action == 'new':
            data['next_action'] = 'insert'
            data['back_where'] = 'list'
            data['form_action'] = '<input type="hidden" name="form_action" value="new">'

        if (action == 'view' and 'row' in self.form):
            #Verify field_order is changed
            if 'field_order' in self.form:
                self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'container', self.form['field_order'].value)
    
            #Get field and mode for order list
            field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'container')
            
            #Define field_order with mode
            field = field + ' ' + mode
            self.data['field_order'] = field
            
            if (data['row'] == '0'):
                data['paging'] = ' LIMIT %s,2' % data['row']
            else:
                data['paging'] = ' LIMIT %s,3' % str(int(self.data['row']) - 1)
                
            data['id_lang'] = self.session.data['id_lang']
            data['id_subcoll'] = self.session.data['id_subcoll']
            
            self.execute('get_container_ids', self.data, True)
            list_containers = self.fetch('all')
            
            i=0
            for container in list_containers:
                if (data['row'] == '0'):
                    if (i == 0):
                        data['img_prev'] = ''
                        data['url_prev'] = ''
                        data['close_link_prev'] = ''
                    else:
                        next_pagination = {}
                        next_pagination['id'] = container['id_container']
                        next_pagination['row'] = str(int(data['row']) + 1)
                        data['img_next'] = '<img title="'+ _("Next") +'" src="../img/next.gif" border="0">'

                        data['url_next'] = data['url_next'] % next_pagination
                else:
                    if (i == 0):
                        prev_pagination = {}
                        prev_pagination['id'] = container['id_container']
                        prev_pagination['row'] = str(int(data['row']) - 1)
                        data['img_prev'] = '<img title="'+ _("Previous") +'" src="../img/prev.gif" border="0">'

                        data['url_prev'] = data['url_prev'] % prev_pagination
                    elif (i == 2):
                        next_pagination = {}
                        next_pagination['id'] = container['id_container']
                        next_pagination['row'] = str(int(data['row']) + 1)
                        data['img_next'] = '<img title="'+ _("Next") +'" src="../img/next.gif" border="0">'

                        data['url_next'] = data['url_next'] % next_pagination

                i = i + 1

            if ((i == 2) and (data['row'] != '0')) or (i < 2 and data['row'] == '0'):
                data['url_next'] = ''
                data['close_link_next'] = ''
                data['img_next'] = ''
        else:
            data['url_next'] = ''
            data['close_link_next'] = ''
            data['img_next'] = ''
            data['img_prev'] = ''
            data['url_prev'] = ''
            data['close_link_prev'] = ''        

        if (action in ('edit', 'view')):
            self.execute('get_container_data', data)
            container = self.fetch('columns')

            self.execute('get_container_preservation_methods', {'id_container':data['id'], 'id_lang':data['id_lang']})
            methods = self.fetch('all')
   
            if action == 'edit':
                id_methods = []
                for method in methods:
                    id_methods.append(method['id_preservation_method'])
                data['preservation_method'] = self.get_preservation_method(id_methods=id_methods)            
                
                self.execute('get_used_container', self.data)
                used_times = len(self.fetch('rows'))
                
                if used_times > 0:
                    data['abbreviation_disabled'] = 'disabled="disabled"'
                    data['method_disabled'] = 'disabled="disabled"'
                    data['form_action'] = '<input type="hidden" name="form_action" value="partial_edit">'
                    data['javascript_include'] = 'form.container.edit.js'
                else:
                    data['form_action'] = '<input type="hidden" name="form_action" value="full_edit">'
                    data['javascript_include'] = 'form.container.new.js'

            else:
                data['preservation_methods'] = ', '.join([method['method'] for method in methods])

            data['abbreviation'] = container['abbreviation']
            data['description'] = container['description']
            data['message'] = '<b>%s</b><br /><span class="reports">%s</span><br />' % (data['abbreviation'], data['description'])

            if action == 'view' or used_times:
                data['container_hierarchy'] = self._get_container_hierarchy(data['id'])
                data['container_hierarchy_edit'] = ''
            elif action == 'edit':
                data['container_hierarchy'] = ''                
                data['container_hierarchy_edit'] = self.mount_container_hierarchy_edit(data['id'])
        else:
            data['onclick_new'] = 'onclick="return newContainer();"'
            data['onclick_remove'] = 'onclick="return removeContainer(this);"'
            data['preservation_method'] = self.get_preservation_method()
        return data

    def _get_container_hierarchy(self, id_container):
        hierarchy_html = '<ul><li><a href="#">&nbsp;</a>%s</li></ul>'
        self.execute('get_container_top_hierarchy', {'id_container': id_container})
        parents = self.fetch('all')
        if len(parents) == 0:
            return _("Structure not defined.")
        hierarchy = []
        
        for parent in parents:
            hierarchy.append(self._create_node(parent['id_container_hierarchy']))
        return hierarchy_html % "".join(hierarchy)
    
    def _create_node(self, id_container_hierarchy):
        node_template = '''
        <ul>
            <li class="jstree-open" rel="folder">
                <a>%s</a>
                %s
            </li>
        </ul>'''
        self.execute('get_container_hierarchy_data', {'id_container_hierarchy': id_container_hierarchy})
        container = self.fetch('columns')
        node_description = _("Abbreviation") + ": <b>" + container['abbreviation'] + "</b> - " + _("Description") + ": <b>" + container['description'] + "</b> "

        # Get all the childrens of this container hierarchy node
        self.execute('get_container_hierarchy', {'id_parent': id_container_hierarchy})
        childrens = self.fetch('all')

        #brk("localhost", 9000)
        children_nodes = []
        if len(childrens) > 0:
            for child in childrens:
                children_nodes.append(self._create_node(child['id_container_hierarchy']))
        else:
            self.execute('get_location_data', {'id_container_hierarchy': id_container_hierarchy})
            location = self.fetch('columns')
            node_description += " - " + _("Rows") + ": <b>%s</b> - "
            node_description += _("Cols") + ": <b>%s</b> - "
            node_description += _("Ini row") + ": <b>%s</b> - "
            node_description += _("Ini col") + ": <b>%s</b> - "
            node_description += _("Pattern") + ": <b>%s</b> "
            node_description = node_description % (location['rows'], location['cols'], location['ini_row'], location['ini_col'], location['pattern'].replace("%(row)s", "<>").replace("%(col)s", "[]"))

        node_returned = node_template % (node_description, "".join(children_nodes))
        return node_returned

    def mount_container_hierarchy_edit(self, id_container):
        hierarchy_html = "<script language='javascript'>function load_data_container() {\n"
        self.execute('get_container_top_hierarchy', {'id_container': id_container})
        parents = self.fetch('all')
        

        self.create_node_edit(parents)
        return hierarchy_html + "".join(self.hierarchy) + "}; \n setTimeout(load_data_container, 500);</script>"
    
        
    def create_node_edit(self, parents = None):
        #brk("localhost", 9000)
        for parent in parents:                        
                            
            if (len(self.dic_positions) > 0 and parent['id_parent'] in self.dic_positions):
                atual = self.dic_positions[parent['id_parent']]
                self.hierarchy.append("$('#demo').jstree('select_one', 'Child_" + str(atual) + "');\n$('#add_folder').click();\n")
            else:
                self.hierarchy.append("$('#demo').jstree('select_one', 'Child_0');\n$('#add_folder').click();\n")
                atual = 1
            
            self.dic_positions[parent['id_container_hierarchy']] = self.num_items
            
            #Number actual of Nodes
            self.num_items += 1
           
            # Get all the childrens of this container hierarchy node
            self.execute('get_container_hierarchy', {'id_parent': parent['id_container_hierarchy']})
            childrens = self.fetch('all')
    
            # Get location data for this container hierarchy node
            self.execute('get_location_data', {'id_container_hierarchy': parent['id_container_hierarchy']})
            location = self.fetch('columns')        
            children_nodes = []
            
            if len(childrens) > 0:
                self.hierarchy.append("$('#Node_" + str(self.num_items) + "abbreviation').val('" + parent['abbreviation'] + "');\n")
                self.hierarchy.append("$('#Node_" + str(self.num_items) + "description').val('" + parent['description'] + "');\n")
                self.create_node_edit(childrens)
            else:
                self.hierarchy.append("$('#Node_" + str(self.num_items) + "abbreviation').val('" + parent['abbreviation'] + "');\n")
                self.hierarchy.append("$('#Node_" + str(self.num_items) + "description').val('" + parent['description'] + "');\n")
                if ('rows' in location):
                    self.hierarchy.append("$('#Node_" + str(self.num_items) + "rows').val('" + str(location['rows']) + "');\n")
                    self.hierarchy.append("$('#Node_" + str(self.num_items) + "cols').val('" + str(location['cols']) + "');\n")
                    self.hierarchy.append("$('#Node_" + str(self.num_items) + "ini_row').val('" + str(location['ini_row']) + "');\n")
                    self.hierarchy.append("$('#Node_" + str(self.num_items) + "ini_col').val('" + str(location['ini_col']) + "');\n")
                    self.hierarchy.append("$('#Node_" + str(self.num_items) + "pattern').val('" + (self.ConvertStrUnicode(location['pattern'])).replace("%(row)s", "<>").replace("%(col)s", "[]") + "');\n")                

    def xml2dict(self, dom):
        dict_xml = {}
        select_fields = []
        order_fields = []
        group_fields = []
        
        total_fields = ''        
        
        #select fields
        select = dom.getElementsByTagName('select')               
        if select.length > 0:
            for node in select[0].getElementsByTagName('field'):                
                select_fields.append(str(node.attributes['name'].value))
        
        #group fields
        group = dom.getElementsByTagName('group')
        if group.length > 0:
            for node in group[0].getElementsByTagName('field'):                
                group_fields.append(str(node.attributes['name'].value))
        
        #order fields
        order = dom.getElementsByTagName('order')
        if order.length > 0:
            for node in order[0].getElementsByTagName('field'):                
                order_fields.append(str(node.attributes['name'].value))
        
        #total fields
        total = dom.getElementsByTagName('total')
        if total.length > 0:
            for node in total[0].getElementsByTagName('field'):
                dict_xml['total'] = {'name': str(node.attributes['name'].value), 'function': node.attributes['function'].value }
                
        #brk('localhost', 9000)
        dict_xml['filters'] = []
        #filters
        filters = dom.getElementsByTagName('filters')[0]
        for node in filters.childNodes:
            if (node.nodeType == node.ELEMENT_NODE) and (node.hasAttribute('field')):
                dict_xml['filters'].append(self.get_xmldata(node))

        dict_xml['select'] = select_fields
        dict_xml['order'] = order_fields
        dict_xml['group'] = group_fields

        format = dom.getElementsByTagName('format')[0]
        self.get_report_format(format, dict_xml)               
        
        if (format.attributes['type'].value == 'custom'):
            
            import base64
            
            dict_xml['templates'] = {}
            dict_xml['templates']['main'] = {}
            #custom template
            main = dom.getElementsByTagName('main')[0]
            self.get_custom_template(main, dict_xml)
            
            dict_xml['templates']['group'] = {}        
            custom_group = dom.getElementsByTagName('groups')[0]
            for node in custom_group.childNodes:
                if (node.nodeType == node.ELEMENT_NODE) and (node.hasAttribute('name')):
                    dic_tmp = {node.attributes['name'].value: ''}
                    
                    dict_xml['templates']['group'][node.attributes['name'].value] = {'header':'', 'footer':''}
                    if (node.getElementsByTagName('header')[0].firstChild != None):
                        dict_xml['templates']['group'][node.attributes['name'].value]['header'] = base64.b64encode(node.getElementsByTagName('header')[0].firstChild.data.strip().replace("[_new_line_]", '\r\n').replace("[_tab_]", "\t").encode("utf-8"))
                    if (node.getElementsByTagName('footer')[0].firstChild != None):
                        dict_xml['templates']['group'][node.attributes['name'].value]['footer'] = base64.b64encode(node.getElementsByTagName('footer')[0].firstChild.data.strip().replace("[_new_line_]", '\r\n').replace("[_tab_]", "\t").encode("utf-8"))
        
        return  dict_xml    
   
    def get_custom_template(self, main, dict_xml):
        
        import base64
        
        if len(main.getElementsByTagName('header')) > 0:
            if main.getElementsByTagName('header')[0].firstChild != None:                
                dict_xml['templates']['main']['header'] = base64.b64encode(main.getElementsByTagName('header')[0].firstChild.data.strip().replace("[_new_line_]", '\r\n').replace("[_tab_]", "\t").encode("utf-8"))
            else:
                dict_xml['templates']['main']['header'] = ""
        
        if len(main.getElementsByTagName('footer')) > 0:
            if main.getElementsByTagName('footer')[0].firstChild != None:
                dict_xml['templates']['main']['footer'] = base64.b64encode(main.getElementsByTagName('footer')[0].firstChild.data.strip().replace("[_new_line_]", '\r\n').replace("[_tab_]", "\t").encode("utf-8"))
            else:
                dict_xml['templates']['main']['footer'] = ""
                
        if len(main.getElementsByTagName('css')) > 0:
            if main.getElementsByTagName('css')[0].firstChild != None:                
                dict_xml['templates']['main']['css'] = base64.b64encode(main.getElementsByTagName('css')[0].firstChild.data.replace("[_new_line_]", '\r\n').replace("[_tab_]", "\t").encode("utf-8"))
            else:
                dict_xml['templates']['main']['css'] = ""         
             
        if len(main.getElementsByTagName('data')) > 0:
            if main.getElementsByTagName('data')[0].firstChild != None:
                dict_xml['templates']['main']['data'] = base64.b64encode(main.getElementsByTagName('data')[0].firstChild.data.strip().replace("[_new_line_]", '\r\n').replace("[_tab_]", "\t").encode("utf-8"))
            else:
                dict_xml['templates']['main']['data'] = ""
        
    def get_report_format(self, node, dict_tmp):
        
        if (node.hasAttribute('type')):
            dict_tmp['format'] = node.attributes['type'].value
        
        if (node.hasAttribute('header_position')):
            dict_tmp['header_position'] = node.attributes['header_position'].value
        
        if (node.hasAttribute('append_subcoll_templates')):
            dict_tmp['append_subcoll_templates'] = node.attributes['append_subcoll_templates'].value
        
        if (node.hasAttribute('separator')):
            dict_tmp['separator'] = node.attributes['separator'].value
            
        if (node.hasAttribute('header')):
            dict_tmp['header'] = node.attributes['header'].value

        if (node.hasAttribute('chart_type')):
            dict_tmp['chart_type'] = node.attributes['chart_type'].value
        
  
    def get_filters(self, filterList):
        lista = []
        for node in filterList:
            if node.childNodes.length > 0:
                self.get_filters(node.childNodes)
                if (node.nodeType == 1) and (node.hasAttribute('field')):
                    lista.append(self.get_xmldata(node))
            else:
                if (node.nodeType == 1 and node.hasAttribute('field')):
                    lista.append(self.get_xmldata(node))    
    
    def get_xmldata(self, node):
        dict_tmp = {'field':'', 'value':'', 'condition':'' , 'connector':'', 'user_defined': '', 'field_lookup': '', 'childs': []}
        if (node.hasAttribute('field')):
            dict_tmp['field'] = node.attributes['field'].value
        
        if (node.hasAttribute('condition')):
            dict_tmp['condition'] = node.attributes['condition'].value
        
        if (node.hasAttribute('value')):
            import base64
            dict_tmp['value'] = base64.b64encode(self.ConvertStrUnicode(node.attributes['value'].value).encode('utf-8'))
        
        if (node.hasAttribute('connector')):
            dict_tmp['connector'] = node.attributes['connector'].value
        
        if (node.hasAttribute('user_defined')):
            dict_tmp['user_defined'] = node.attributes['user_defined'].value
            
        if (node.hasAttribute('field_lookup')):
            dict_tmp['field_lookup'] = node.attributes['field_lookup'].value
        
        for child in node.childNodes:
            dict_tmp['childs'].append(self.get_xmldata(child))
            
        return dict_tmp
    
    def report(self,action):
        #brk("localhost",9000)
        data = self.data
        data['action'] = action
        data['description'] = ''
        data['type_name'] = ''
        data['select'] = ''
        data['order'] = ''
        data['condition'] = ''
        data['group'] = ''
        data['total'] = ''
        data['id_subcoll'] = self.session.data['id_subcoll']
        data['url_next'] = "<a href='javascript:Proximo(\"reports.detail.py?id=%(id)s&row=%(row)s\")'>"
        data['url_prev'] = "<a href='javascript:Anterior(\"reports.detail.py?id=%(id)s&row=%(row)s\")'>"
        data['close_link_prev'] = '</a>'
        data['close_link_next'] = '</a>'
        data['img_prev']= ''
        data['img_next']= ''
        data['js_data'] = ''

        if action == 'view': pass
        elif action == 'edit':
            data['next_action'] = 'update'
        elif action == 'new':
            data['next_action'] = 'insert'
            data['back_where'] = 'list'
        
        if (self.data['row'] != ''):
            data['row_number'] = self.data['row']
        else:
            data['row_number'] = '0'        
        
        if (action == 'view'):
            #Verify field_order is changed
            if 'field_order' in self.form:
                self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'doc', self.form['field_order'].value)

            #Get field and mode for order list
            field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'doc')

            #Define field_order with mode
            self.data['field_order'] = field + ' ' + mode

            if (data['row_number'] == '0'):
                data['paging'] = ' LIMIT %s,2' % data['row_number']
            else:
                data['paging'] = ' LIMIT %s,3' % str(int(data['row_number']) - 1)

            data['id_lang'] = self.session.data['id_lang']
            data['id_coll'] = self.session.data['id_coll']
            data['id_subcoll'] = self.session.data['id_subcoll']

            #Filter
            filter = ''
            if ('filter' in self.form):
                filter = str(self.form['filter'].value).strip()
    
                #Save filter on session
                self.session.data['filter_reports'] = filter
                self.session.save()
            elif ('filter_reports' in self.session.data):
                filter = self.session.data['filter_reports']

            if ('filter' in self.form):
                filter = str(self.form['filter'].value).strip()

                #Save filter on session
                self.session.data['filter_reports'] = filter
                self.session.save()
            elif ('filter_reports' in self.session.data):
                filter = self.session.data['filter_reports']
    
            self.data['condition'] = []            
            if (filter != ''):
                words = [x for x in filter.split(" ") if x != '']    
                
                for word in words:
                    #0x25 == '%'
                    self.data['condition'].append(
                                                  " AND (replang.type LIKE x'25" + word.encode("hex") + "25' " +
                                                  " OR rep.description LIKE x'25" + word.encode("hex") + "25') ")
                self.data['condition']= "".join(self.data['condition'])
            else:
                self.data['condition'] = ' '

            #Verify field_order is changed
            if 'field_order' in self.form:
                self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'reports', self.form['field_order'].value)

            #Get field and mode for order list
            field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'reports')
            
            #Define field_order with mode
            self.data['field_order'] = field + ' ' + mode

            #Execute again for rows count
            if 2 in self.session.data['roles']: #Administrator
              self.execute('get_report_ids', self.data, True)
            else:
              roles = str(self.session.data['roles']).replace("L","")
              roles = roles.replace("[","(")
              roles = roles.replace("]",")")
              self.data['roles_list'] = roles
              self.execute('get_reports_ids_restrict', self.data,raw_mode = True)

            list_report = self.fetch('all')
            i=0
            for report in list_report:

                if (data['row_number'] == '0'):
                    if (i == 0):
                        data['img_prev'] = ''
                        data['url_prev'] = ''
                        data['close_link_prev'] = ''
                    else:
                        next_pagination = {}
                        next_pagination['id'] = report['id_report']
                        next_pagination['row'] = str(int(data['row_number']) + 1)
                        data['img_next'] = '<img title="'+ _("Next") +'" src="../img/next.gif" border="0">'

                        data['url_next'] = data['url_next'] % next_pagination
                else:
                    if (i == 0):
                        prev_pagination = {}
                        prev_pagination['id'] = report['id_report']
                        prev_pagination['row'] = str(int(data['row_number']) - 1)
                        data['img_prev'] = '<img title="'+ _("Previous") +'" src="../img/prev.gif" border="0">'

                        data['url_prev'] = data['url_prev'] % prev_pagination
                    elif (i == 2):
                        next_pagination = {}
                        next_pagination['id'] = report['id_report']
                        next_pagination['row'] = str(int(data['row_number']) + 1)
                        data['img_next'] = '<img title="'+ _("Next") +'" src="../img/next.gif" border="0">'

                        data['url_next'] = data['url_next'] % next_pagination

                i += 1

            if ((i == 2) and (data['row_number'] != '0')) or (i < 2 and data['row_number'] == '0'):
                data['url_next'] = ''
                data['close_link_next'] = ''
                data['img_next'] = ''

        else:
            data['url_next'] = ''
            data['close_link_next'] = ''
            data['img_next'] = ''

            data['img_prev'] = ''
            data['url_prev'] = ''
            data['close_link_prev'] = ''

        is_first = True        
        for lang in self.data_langs:
            one_lang = list(lang.keys())[0]
            data['data_lang'] = list(lang.values())[0]
            data['id_report'] = self.form['id'].value            
            self.execute('get_report_data', data, True)
            reports = self.fetch('columns')
            num_fields = 2
            if len(reports) < num_fields:
                reports = DefDict()
            
            if is_first:               
                data['description'] = reports['description']
                data['type_name'] = reports['type']
                data['xml'] = reports['definition']
                self.data['type'] = reports['id_report_type']
                
                from xml.dom.minidom import parse, parseString

                #brk(host="localhost", port=9000)
                dom = parseString(data['xml'].encode("utf8").replace('\r\n',"[_new_line_]").replace("\t","[_tab_]"))
                
                from .labels import label_dict
                from .reports import Reports
                Rep = Reports(self.form, self.cookie_value)
                Rep.get_fields_definition(reports['id_report_type'] )                
                xml_dict = self.xml2dict(dom)
                if len(xml_dict['select']) > 0:
                    data['select'] = '<p><label>' + label_dict['label_Rep_General_Select'] + '</label><br />'
                    for x in xml_dict['select']:
                        data['select'] += label_dict[Rep.fields_definition[str(x)]['label']] + '<br />'
                    data['select'] += '</p>'
                    
                if len(xml_dict['order']) > 0:
                    data['order'] += '<p><label>' + label_dict['label_Rep_General_Order'] + '</label><br />'
                    for x in xml_dict['order']:
                        data['order'] += label_dict[Rep.fields_definition[str(x)]['label']] + '<br />'
                    data['order'] += '</p>'
                    
                if len(xml_dict['group']) > 0:
                    data['group'] += '<p><label>' + label_dict['label_Rep_General_Group'] + '</label><br />'
                    for x in xml_dict['group']:
                        data['group'] += label_dict[Rep.fields_definition[str(x)]['label']] + '<br />'
                    data['order'] += '</p>'
                    
                if 'total' in xml_dict:
                    data['total'] += '<p><label>' + label_dict['label_Rep_General_Totalizer'] + '</label><br />'
                    data['total'] += label_dict[Rep.fields_definition[str(xml_dict['total']['name'])]['label']]
                    data['total'] += '</p>'

                self.report_index_field = 0
                
                
                from .reports import Reports
                from .labels import label_dict
                from .label_values_reports import label_values_dict
                from .label_values_reports import values_dict
                
                z = Reports(self.form, self.cookie_value)
                z.get_fields_definition(reports['id_report_type'])
                self.fields_definition = z.fields_definition
                self.order_keys = z.order_keys
                                                
                data['arrayFields'] = []
                data['arrayFieldsValues'] = []
                data['arrayFieldsDef'] = "{"                
                data['arrayTypes'] = []
                data['lang_code'] = self.session.data['label_lang_code']
                
                for key in self.order_keys:
                    data['arrayFieldsValues'].append(str(key))
                    data['arrayFields'].append(str(label_dict[self.fields_definition[key]['label']].encode("utf8")))
                    data['arrayFieldsDef'] += key + ": '" + str(self.fields_definition[key]['data_type'].encode("utf8")) +"', "
                
                data['arrayFieldsDef'] = data['arrayFieldsDef'][0:len(data['arrayFieldsDef'])-2] + "}";                    
               
                data['arrayConnectors'] = ['AND','OR']
                
                data['arrayTypes'].append('Fixed')
                data['arrayTypes'].append('Variable')
                data['arrayTypes'].append('Field')
                
                data['enum_label_values'] = str(label_values_dict).replace(": u'",": '")
                data['enum_values'] = str(values_dict).replace(": u'",": '")

                self.scripts = ''
                #brk(host="localhost", port=9000)
                if len(xml_dict['filters']) > 0:
                    data['filter'] = '<br /><p><label>' + label_dict['label_Rep_General_Filter'] + '</label><br />'
                    data['filter'] += self.mount_filter(xml_dict['filters'])
                    data['filter'] += '</p>'      
      
                data['finalIndex'] = self.report_index_field
                data["xml_dict"] = xml_dict
                data["id_report"] = self.form['id'].value
               
                data['report_format'] = self.mount_format(xml_dict, label_dict)                
                
                data['languages'] = self.preferences(self.session.data['id_lang'], False)
                data['scripts_report'] = self.scripts
                is_first = False
        
        data['message'] = '<b>%s</b><br /><span class="reports">%s</span><br />' % (data['description'], data['type_name'])
        
        #Security Tab
        self.g.security_tab(self.cookie_value, action, data, 'reports')
        return data
    
    def mount_format(self, xml_dict, label_dict):
        
        return_value = label_dict["label_Rep_" + str(xml_dict['format']).lower()] + "<br />"
        
        if xml_dict['format'] == 'default':
            #default html options
            return_value += "<br /><label for='id_header' id='label_id_header'>" + label_dict['label_Rep_Header'] + "</label><br />"
            return_value += "<select name='options_header' id='options_header'>"
            return_value += "<option value='internal'>" + label_dict['label_Rep_Internal'] + "</option>"
            return_value += "<option value='external'>" + label_dict['label_Rep_External'] + "</option>"
            return_value += "<option value='none'>" + label_dict['label_Rep_None'] + "</option>"
            return_value += "</select>"
            
            return_value += "<script language='javascript'>"            
            #set value for option_header
            return_value += "$('#options_header').val('" + xml_dict['header_position'] + "');"
            return_value += "</script>"
            
        elif xml_dict['format'] == 'csv':

            return_value += "<br /><label for='id_with_header' id='label_with_header'>" + label_dict['label_Rep_Header'] + "</label>"
            return_value += "&nbsp;&nbsp;&nbsp;&nbsp;"
            return_value += "<label for='id_label_separator' id='label_separator'>" + label_dict['label_Rep_Separator'] + "</label><br />"
            return_value += "<input type='checkbox' id='with_header' name='with_header' class='cols_5_checkbox'>"
            return_value += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
            return_value += "<input type='text' id='separator' name='separator' class='csv_textbox' maxlength=1><br />"
            
            return_value += "<script language='javascript'>"                
            #set value for with_header and separator
            if xml_dict['header']:
                return_value += "$('#with_header').attr('checked','checked');"
            return_value += "$('#separator').val('" + xml_dict['separator'] + "');"            
            return_value += "</script>"
            
        elif xml_dict['format'] == 'chart':
            return_value += "<br /><label for='id_chart_type' id='label_chart_type'>" + label_dict['label_Rep_chart_type'] + "</label><br />"
            return_value += "<select name='options_chart_type' id='options_chart_type' style='width=auto;'>"
            return_value += "<option value='bar'>" + label_dict['label_Rep_Bar'] + '</option>'
            return_value += "<option value='pie'>" + label_dict['label_Rep_Pie'] + '</option>'
            return_value += "<option value='line'>" + label_dict['label_Rep_Line'] + '</option>'
            return_value += "<option value='column'>" + label_dict['label_Rep_Column'] + '</option>'
            return_value += "</select>"
            
            return_value += "<script language='javascript'>"                
            #set value for options_chart_type
            return_value += "$('#options_chart_type').val('" + xml_dict['chart_type'] + "');"
            return_value += "</script>"

        return return_value
    
    def mount_filter(self, lista_filter):
        from .labels import label_dict
        
        retorno = ''
        if len(lista_filter) > 0:
            retorno+= "<div id='filterDiv_0'>"         
            
            for item in lista_filter:            
                if str(item["user_defined"]) == 'True':                    
                    name_field = "field='" + item['field'] + "'"
                    name_condition = "condition='" + item['condition'] + "'"
                    self.report_index_field += 1
                    
                    allowBlank = "allowBlank='yes'"                    
                    if (len(item['childs']) > 0):
                        allowBlank = "allowBlank='no'"

                    retorno += "<div style='Padding:1px;'>" + label_dict["label_Rep_connector_" + str(item['connector']).lower()]  + " (" + label_dict[self.fields_definition[str(item['field'])]['label']] + " " + label_dict["label_Rep_" + str(item['condition']).lower()]
                    
                    if (str(self.fields_definition[item['field']]['data_type']) != 'enum'):
                        retorno += " <input " + allowBlank + " type='text' name='value_" + str(self.report_index_field) + "' id='value_" + str(self.report_index_field) + "' " + name_field + " " + name_condition + " />"
                        if str(item['condition']).lower() == 'in' or str(item['condition']).lower() == 'not_in':                        
                            self.scripts += "validateField(" + str(self.report_index_field) + ", window.event, '" + item['field'] + "', true);"
                        else:
                            self.scripts += "validateField(" + str(self.report_index_field) + ", window.event, '" + item['field'] + "');"
                    else:
                        retorno += " <select " + allowBlank + " name='value_" + str(self.report_index_field) + "' id='value_" + str(self.report_index_field) + "' style='width:auto;' " + name_field + " " + name_condition + " /></select>"
                        
                        self.scripts += "validateField(" + str(self.report_index_field) + ", window.event, '" + item['field'] + "');"
                        self.scripts += "dropDownItems('value_" + str(self.report_index_field) + "'," + str(self.report_index_field) + ",'" + item['field'] + "');"
                else:
                    retorno += "<div style='Padding:1px;'>"
                    if item['field_lookup'] != '':
                        retorno += label_dict["label_Rep_connector_" + str(item['connector']).lower()]  + ' (' + label_dict[self.fields_definition[str(item['field'])]['label']] + ' ' + label_dict["label_Rep_" + str(item['condition']).lower()] + ' <b>' + label_dict[self.fields_definition[str(item['field_lookup'])]['label']] + '</b>'
                    else:
                        import base64
                        retorno += label_dict["label_Rep_connector_" + str(item['connector']).lower()] + ' (' + label_dict[self.fields_definition[str(item['field'])]['label']] + ' ' + label_dict["label_Rep_" + str(item['condition']).lower()] + ' <b>' + self.ConvertStrUnicode(base64.b64decode(item['value'])) + '</b>'
                
                if len(item['childs']) > 0 :
                    retorno += self.mount_filter(item['childs']) + " )"
                else:
                    retorno += ") </div>"
                    
            retorno+= "</div>"

        return retorno
    
    def stockmovement(self, action):
        data = self.data
        data['id_subcoll'] = self.session.data['id_subcoll']
        data['action'] = action
        data['url_next'] = "<a href='javascript:Proximo(\"stockmovement.detail.py?id=%(id)s&row=%(row)s\")'>"
        data['url_prev'] = "<a href='javascript:Anterior(\"stockmovement.detail.py?id=%(id)s&row=%(row)s\")'>"
        data['close_link_prev'] = '</a>'
        data['close_link_next'] = '</a>'
        data['img_prev']= ''
        data['img_next']= ''

        if action == 'view': pass
        elif action == 'edit':
            data['next_action'] = 'update'
        elif action == 'new':
            data['next_action'] = 'insert'
            data['back_where'] = 'list'

        data['row_number'] = self.data['row']
        
        if (action == 'view' and 'row' in self.form):
            #Verify field_order is changed
            if 'field_order' in self.form:
                self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'stockmovement', self.form['field_order'].value)
    
            #Get field and mode for order list
            field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'stockmovement')
            
            #Define field_order with mode
            field = field + ' ' + mode
            self.data['field_order'] = field
            
            if (data['row'] == '0'):
                data['paging'] = ' LIMIT %s,2' % data['row']
            else:
                data['paging'] = ' LIMIT %s,3' % str(int(self.data['row']) - 1)
                
            data['id_lang'] = self.session.data['id_lang']
            data['id_subcoll'] = self.session.data['id_subcoll']
            
            self.execute('get_stock_movement_ids', self.data, True)
            list_stock_movements = self.fetch('all')
          
            i=0
            for stock_movement in list_stock_movements:
                if (data['row'] == '0'):
                    if (i == 0):
                        data['img_prev'] = ''
                        data['url_prev'] = ''
                        data['close_link_prev'] = ''
                    else:
                        next_pagination = {}
                        next_pagination['id'] = stock_movement['id_stock_movement']
                        next_pagination['row'] = str(int(data['row']) + 1)
                        data['img_next'] = '<img title="'+ _("Next") +'" src="../img/next.gif" border="0">'

                        data['url_next'] = data['url_next'] % next_pagination
                else:
                    if (i == 0):
                        prev_pagination = {}
                        prev_pagination['id'] = stock_movement['id_stock_movement']
                        prev_pagination['row'] = str(int(data['row']) - 1)
                        data['img_prev'] = '<img title="'+ _("Previous") +'" src="../img/prev.gif" border="0">'

                        data['url_prev'] = data['url_prev'] % prev_pagination
                    elif (i == 2):
                        next_pagination = {}
                        next_pagination['id'] = stock_movement['id_stock_movement']
                        next_pagination['row'] = str(int(data['row']) + 1)
                        data['img_next'] = '<img title="'+ _("Next") +'" src="../img/next.gif" border="0">'

                        data['url_next'] = data['url_next'] % next_pagination

                i = i + 1

            if ((i == 2) and (data['row'] != '0')) or (i < 2 and data['row'] == '0'):
                data['url_next'] = ''
                data['close_link_next'] = ''
                data['img_next'] = ''
        else:
            data['url_next'] = ''
            data['close_link_next'] = ''
            data['img_next'] = ''
            data['img_prev'] = ''
            data['url_prev'] = ''
            data['close_link_prev'] = ''        
        
        positions_data = []
        
        if (action in ('edit', 'view')):
            self.execute('get_stock_movement_data', data)
            stock_movement = self.fetch('columns')
            data['date'] = self.format_date(action, stock_movement['date'])
            data['description'] = stock_movement['description']
            
            data['message'] = '<strong>%s</strong><br />%s' % (self.format_date("view", stock_movement['date']), data['description'][0:180])
            
            self.execute('get_stock_movement_location_data', data)
            locations = self.fetch('all')            
            
            if (action == 'edit'):
                data['preservation_method'] = self.get_preservation_method(stock_movement['id_preservation_method'])
                data['disabled'] = '_disabled'
                data['method_disabled'] = 'disabled="disabled"'
                
                positions_data.append("<script type='text/javascript'>")
                positions_data.append("positions_info = new Array();")
                
                for location in locations:
                    origin_location = str(location["id_container_hierarchy_from"]) + "_" + str(location["row_from"]) + "_" + str(location["col_from"])               
                    origin_location_text = self.l.get_incomplete_location(location['id_container_hierarchy_from'], location['row_from'], location['col_from'], None, -1)
                    
                    if location['id_container_hierarchy_to'] != "":
                        destination_location = str(location["id_container_hierarchy_to"]) + "_" + str(location["row_to"]) + "_" + str(location["col_to"])
                        destination_location_text = self.l.get_incomplete_location(location['id_container_hierarchy_to'], location['row_to'], location['col_to'], None, -1)
                    else:
                        destination_location = ""
                        destination_location_text = ""
                    
                    positions_data.append("positions_info[positions_info.length] = {'origin_location': '" + origin_location + "', 'origin_location_text': '" + origin_location_text + "', 'destination_location': '" + destination_location + "', 'destination_location_text': '" + destination_location_text + "'};")
                
                positions_data.append("</script>")
            else:
                data['preservation_method'] = stock_movement['method']
                
                positions_data.append("<table class='table_locations' style='width: 550px;'>")
                positions_data.append("<thead>")
                positions_data.append("<th>%s</th>" % _("Stock Movement From"))
                positions_data.append("<th>%s</th>" % _("Stock Movement To"))
                positions_data.append("</thead>")
                positions_data.append("<tbody>")
                
                for location in locations:
                    origin_location_text = self.l.get_incomplete_location(location['id_container_hierarchy_from'], location['row_from'], location['col_from'], None, -1)
                    
                    if location['id_container_hierarchy_to'] != "":
                        destination_location_text = self.l.get_incomplete_location(location['id_container_hierarchy_to'], location['row_to'], location['col_to'], None, -1)
                    else:
                        destination_location_text = _("(Discard)")
                
                    positions_data.append("<tr>")
                    positions_data.append("<td>%s</td>" % origin_location_text)
                    positions_data.append("<td>%s</td>" % destination_location_text)
                    positions_data.append("<tr>")
                
                positions_data.append("</tbody>")
                positions_data.append("</table>")            
        else:
            data['onclick_new'] = 'onclick="return newStockMovement();"'
            data['onclick_remove'] = 'onclick="return removeStockMovement(this);"'
            data['preservation_method'] = self.get_preservation_method()            
            positions_data.append("<script type='text/javascript'>")
            positions_data.append("positions_info = new Array();")
            positions_data.append("</script>")
            
        data['positions_data'] = "\n".join(positions_data)
        
        return data
    
    def ConvertStrUnicode(self, valor):
        retorno = '';
        if isinstance(valor, (int, float)):
            return str(valor)
            
        if (isinstance(valor, str) == False):
            retorno = str(valor).decode("utf8")
        else:
            retorno = valor
        
        return retorno
