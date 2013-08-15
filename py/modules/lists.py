#!/usr/bin/env python
#-*- coding: utf-8 -*-

#python imports
from sys import exit
#from dbgp.client import brk

#project imports
from session import Session
from dbconnection import dbConnection
from general import General
import math
from os import environ

class Lists(object):

    g = General()
    page_parts = {}
    page_parts['top'] = g.read_html('default.top.list')
    page_parts['submenu'] = g.read_html('submenu.list')
    session = None

    def __init__(self, form=None, cookie_value=''):
        #brk(host="localhost", port=9000)
    
        self.cookie_value = cookie_value
        if cookie_value:
            #Load Session
            self.session = Session()
            self.session.load(cookie_value)

            #check feedback parameter
            if self.session.data.has_key('feedback') and self.session.data['feedback']:
                self.feedback_value = self.session.data['feedback']
                self.session.data['feedback'] = 0
                self.session.save()
            else:
                self.feedback_value = 0

            #Define Data Dict
            data = {}
            data['id_lang'] = self.session.data['id_lang'] #id for label_lang
            data['id_coll'] = self.session.data['id_coll']
            data['id_subcoll'] = self.session.data['id_subcoll']

            #Define form
            self.form = form

            self.data = data

            #Define Database
            self.dbconnection = dbConnection(cookie_value)
            self.execute = self.dbconnection.execute
            self.fetch = self.dbconnection.fetch
            self.getrowscount = self.dbconnection.getrows

            #Define global variables
            self.html = ''
            self.foothtml = ''
            self.indent_size = '\n' + ' '*12 #\t*6

            #Define global image ordering variables
            self.order_img = ''
            self.img = ''
            self.img_path_up = '../img/order_up.png'
            self.img_path_down = '../img/order_down.png'
			
    def ConvertStrUnicode(self, valor):
        retorno = '';
        if isinstance(valor, (int, long, float)):
            return str(valor)
            
        if (isinstance(valor, unicode) == False):
            retorno = str(valor).decode("utf8")
        else:
            retorno = valor
        
        return retorno

    def get(self, who):
        html = {'message':'', 'data':'', 'datafoot':'', 'current_page':1, 'text_filter':''}

        if who == 'species': html['data'], html['datafoot'], html['current_page'], html['text_filter'] = self.species()
        elif who == 'strains': html['data'], html['datafoot'], html['current_page'], html['text_filter'] = self.strains()
        elif who == 'doc': html['data'], html['datafoot'], html['current_page'], html['text_filter'] = self.doc()
        elif who == 'reports': html['data'], html['datafoot'], html['current_page'], html['text_filter'] = self.reports()
        elif who == 'ref': html['data'], html['datafoot'], html['current_page'], html['text_filter'] = self.ref()
        elif who == 'people': html['data'], html['datafoot'], html['current_page'], html['text_filter'] = self.people()
        elif who == 'institutions': html['data'], html['datafoot'], html['current_page'], html['text_filter'] = self.inst()
        elif who == 'preservation': html['data'], html['datafoot'], html['current_page'], html['text_filter'] = self.preservation()
        elif who == 'distribution': html['data'], html['datafoot'], html['current_page'], html['text_filter'] = self.distribution()
        elif who == 'stockmovement': html['data'], html['datafoot'], html['current_page'], html['text_filter'] = self.stockmovement()
        elif who == 'container': html['data'], html['datafoot'], html['current_page'], html['text_filter'] = self.container()
        html['text_filter'] = html['text_filter'].replace('"','&quot;').replace("'","&#39;")
        return html

    @classmethod
    def spe_fullname(cls, parts_dict,data=[],lang_code='',apply_font_style=True,use_author=False,use_infracomplement=False):
        """
        Composes full name for Species.
        'parts_dict' parameter must be a dictionary with the following fields:
        genus, subgenus, species, subdiv and infra_name
        External link: "genus=g&species=s&subspecies=s&lang=en" where
        "genus" is mandatory and "lang" is always a two-letter language code
        """

        from loghelper import Logging

        if parts_dict.has_key('sciname'):
            if use_author:
                ret = parts_dict['sciname']
            else:
                ret = parts_dict['sciname_no_auth']

            if ret and not apply_font_style:
                ret = Lists.strip_ml_tags(ret)

            if use_infracomplement:
                ret = "%s %s" % (ret, parts_dict['infra_complement'])

            if data != []:
                parts = parts_dict.copy()
                if not parts.has_key('species'):
                    parts['species'] = ''
                if not parts.has_key('subspecies'):
                    parts['subspecies'] = ''

                data['sp_dictionary'] = "genus=%(genus)s&species=%(species)s&subspecies=%(subspecies)s&lang=%%s" % parts
                data['sp_dictionary'] = data['sp_dictionary'] % lang_code[:2]

            return ret

        if data != []:
            data['sp_dictionary'] = ''
        if not parts_dict:
            return ""
        parts = parts_dict.copy ()
        if data != []:
            data['sp_dictionary'] = "genus=%(genus)s&species=%(species)s&subspecies=%(infra_name)s&lang=%%s" % parts
            data['sp_dictionary'] = data['sp_dictionary'] % lang_code[:2]

        if (apply_font_style):
            #Not Italic for Specie = "sp."
            if parts['species'] == 'sp.':
                parts['species'] = ('<span class="sp_ponto">%s</span>'
                                     % parts['species'])

        #insert parenthesis for subgenus
        if parts['subgenus'] and parts['subgenus'] != ' ': parts['subgenus'] = '(%s)' % parts['subgenus']

        if (apply_font_style):
            if parts['subdiv'] != '' and parts['subdiv'][-1] == '.':
              parts['subdiv'] = '<span class="sp_ponto">%s</span>' % parts['subdiv']

        if (use_infracomplement):
            species = "%(genus)s %(subgenus)s %(species)s %(subdiv)s %(infra_name)s %(infra_complement)s" % parts
        else:
            species = "%(genus)s %(subgenus)s %(species)s %(subdiv)s %(infra_name)s" % parts

        return species

    @classmethod
    def strip_ml_tags(cls, in_text):
        """Description: Removes all HTML/XML-like tags from the input text.
        Inputs: s --> string of text
        Outputs: text string without the tags

        # doctest unit testing framework

        >>> test_text = "Keep this Text <remove><me /> KEEP </remove> 123"
        >>> strip_ml_tags(test_text)
        'Keep this Text  KEEP  123'
        """
        # convert in_text to a mutable object (e.g. list)
        s_list = list(in_text)
        i,j = 0,0

        while i < len(s_list):
            # iterate until a left-angle bracket is found
            if s_list[i] == '<':
                while s_list[i] != '>':
                    # pop everything from the the left-angle bracket until the right-angle bracket
                    s_list.pop(i)

                # pops the right-angle bracket, too
                s_list.pop(i)
            else:
                i=i+1

        # convert the list back into text
        join_char=''
        return join_char.join(s_list)

    @classmethod
    def spe_name(cls, specie):
        """
        Returns specie name with special html style if it name ends with dot (.)
        """
        specie = specie.strip()
        if len(specie) and specie.endswith('.'):
            return '<span class="sp_ponto">%s</span>' % specie
        else:
            return specie

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

    def get_stripped(self, field):
        return "REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(%s, '<b>', ''), '<i>', ''), '</b>', ''), '</i>', ''), '  ', ' ')" % (field)

    def species(self):
        html = '%s<tr class="%s" onclick="location=\'./species.detail.py?id=%s&row=%s\'">\
                  %s  <td class="code">%s</td>\
                  %s  <td class="species">%s</td>\
                  %s  <td class="type">%s</td>\
                  %s</tr>'

        stripped_sciname = self.get_stripped("sciname_no_auth")

        #Filter
        filter = ''
        if (self.form.has_key('filter')):
            filter = str(self.form['filter'].value).strip()
            filter = self.ConvertStrUnicode(filter).encode("utf-8")

            #Save filter on session
            self.session.data['filter_species'] = filter
            self.session.save()
        elif (self.session.data.has_key('filter_species')):
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

        #Verify field_order is changed
        if self.form.has_key('field_order'):
            self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'species', self.form['field_order'].value)

        #Get field and mode for order list
        field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'species')

        #Creating order image

        #Define if order is Asc, or Desc
        if mode == "ASC":
          self.img="<img class='order' src='"+self.img_path_up+"'/>"
        else:
          self.img="<img class='order' src='"+self.img_path_down+"'/>"

        #define what img in HTML must be changed
        self.order_img = "img_" + field

        if field == 'species':
            field = stripped_sciname + " " + mode
        elif field == 'taxongroup':
            field = 'taxon_group %s' % mode
        else:
            field = field + ' ' + mode

        #Define field_order with mode
        self.data['field_order'] = field

        #Disable paging
        self.data['paging'] = ';'

        #Execute again for rows count
        if self.g.isManager(self.session.data['roles']): #Administrator or Manager
          self.execute('get_species_list', self.data, True)
        else:
          roles = str(self.session.data['roles']).replace("L","")
          roles = roles.replace("[","(")
          roles = roles.replace("]",")")
          self.data['roles_list'] = roles
          self.execute('get_species_list_restrict', self.data,raw_mode = True)

        #Define totalpages
        totalpages = int(math.ceil(float(self.getrowscount())/self.session.data['lines_per_page']))

        #Verify page
        page = 1
        if self.form.has_key('page'):
            page = int(self.form['page'].value)
            if page <= 0: page = 1
            elif page > totalpages: page = totalpages

            #Save filter on session
            self.session.data['page_species'] = page
            self.session.save()
        elif (self.session.data.has_key('page_species')):
            if (self.form.has_key('filter')):
                #Save filter on session
                self.session.data['page_species'] = page
                self.session.save()
            else:
                page = int(self.session.data['page_species'])

        #Enable paging
        if (totalpages > 1):
          self.data['paging'] = 'LIMIT ' + str((page - 1) * self.session.data['lines_per_page']) + ',' + str(self.session.data['lines_per_page']) + ';'

        #SELECT id_species, taxon_group, genus, subgenus, species, subdiv, infra_name, hazard_group
        if self.g.isManager(self.session.data['roles']): #Administrator or Manager
          self.execute('get_species_list', self.data, True)
        else:
          roles = str(self.session.data['roles']).replace("L","")
          roles = roles.replace("[","(")
          roles = roles.replace("]",")")
          self.data['roles_list'] = roles
          self.execute('get_species_list_restrict', self.data, raw_mode = True)

        list_species = self.fetch('all')

        i = 0

        for species in list_species:

            #Hazard Group
            if not species['hazard_group']:
                species['hazard_group'] = '-'

            #Species FullName
            species_name = species['sciname_no_auth']

            #Class of row
            if ((i % 2) == 0): css_class = "row1"
            else: css_class = "row2"

            #Absolute Row for the navigator of detail's page
            absolute_row = i + ((self.session.data['lines_per_page']) * (page - 1))

            #Output
            self.html += html % (self.indent_size, css_class, str(species['id_species']), absolute_row,
                                 self.indent_size, species['taxongroup'],
                                 self.indent_size, species_name,
                                 self.indent_size, species['hazard_group'],
                                 self.indent_size)
            i += 1

        #Security
        #If user does not have permission to create then don't show the "new" button
        allow_create = self.g.get_area_permission(self.cookie_value, self.session, 'species', 'allow_create')
        if self.g.isManager(self.session.data['roles']):
	  allow_create = 'y'
        if allow_create != 'y':
          import re
          self.page_parts['submenu'] = re.sub('<a id="action_new" href="[.]/%\(who\)s[.]new[.]py".*?/a>',"",self.page_parts['submenu'])

        return self.html, self.get_foothtml(3, page, self.session.data['max_num_pages'], totalpages, '.' + environ['SCRIPT_NAME'][environ['SCRIPT_NAME'].rindex('/'):] + '?page=%s'), page, filter.decode('utf8')
    
    def strains(self):
        html = '%s<tr class="%s" onclick="location=\'./strains.detail.py?id=%s&row=%s\'" style="white-space:nowrap; %s">\
                  %s  <td class="code">%s</td>\
                  %s  <td class="species">%s</td>\
                  %s  <td class="internal_code">%s</td>\
                  %s  <td class="type">%s</td>\
                  %s</tr>'

        stripped_sciname = self.get_stripped("sciname")

        #Filter
        filter = ''
        if (self.form.has_key('filter')):
            filter = str(self.form['filter'].value).strip()
            filter = self.ConvertStrUnicode(filter).encode("utf-8")

            #Save filter on session
            self.session.data['filter_strains'] = filter
            self.session.save()
        elif (self.session.data.has_key('filter_strains')):
            filter = self.session.data['filter_strains']
            filter = self.ConvertStrUnicode(filter).encode("utf-8")

        filter_temp = filter

        if (filter_temp != ''):
            words = [x for x in filter_temp.split(" ") if x != '']
            self.data['condition']= []
            aux_condition = []

            #Show inactive strains
            if (self.session.data['show_str_inactives'] == 0):
                aux_condition.append("AND (status <> 'inactive') ")

            for word in words:
                #0x25 == '%'
                aux_condition.append(
                                        "AND (st.code LIKE x'25" + word.encode("hex") + "25' " +
                                        "OR st.internal_code LIKE x'25" + word.encode("hex") + "25' " +
                                        "OR " + stripped_sciname + " LIKE x'25" + word.encode("hex") + "25' " +
                                        "OR ty.type LIKE x'25" + word.encode("hex") + "25' " +
                                        "OR st.infra_complement LIKE x'25" + word.encode("hex") + "25') ")
            self.data['condition']= "".join(aux_condition)
        else:
            if (self.session.data['show_str_inactives'] == 0):
                self.data['condition'] = "AND (status <> 'inactive')"
            else:
                self.data['condition'] = ' '

        #raise self.data['condition']
        #Verify field_order is changed
        if self.form.has_key('field_order'):
            self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'strains', self.form['field_order'].value)

        #Get field and mode for order list
        field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'strains')

        #Creating order image

        #Define if order is Asc, or Desc
        if mode == "ASC":
          self.img="<img class='order' src='"+self.img_path_up+"'/>"
        else:
          self.img="<img class='order' src='"+self.img_path_down+"'/>"

        #define what img in HTML must be changed
        self.order_img = "img_" + field

        if field == 'species':
            field = stripped_sciname + ' ' + mode
        elif field == 'code':
            field = "%s %s" % (field, mode)
        else:
            field = field + ' ' + mode

        #Define field_order with mode
        self.data['field_order'] = field

        #Disable paging
        self.data['paging'] = ';'

        #Execute again for rows count
        if self.g.isManager(self.session.data['roles']): #Administrator or Manager
          self.execute('get_strain_list', self.data, True)
        else:
          roles = str(self.session.data['roles']).replace("L","")
          roles = roles.replace("[","(")
          roles = roles.replace("]",")")
          self.data['roles_list'] = roles
          self.execute('get_strain_list_restrict', self.data,raw_mode = True)

        #Define totalpages
        totalpages = int(math.ceil(float(self.getrowscount())/self.session.data['lines_per_page']))

        #Verify page
        page = 1
        if self.form.has_key('page'):
            page = int(self.form['page'].value)
            if page <= 0: page = 1
            elif page > totalpages: page = totalpages

            #Save filter on session
            self.session.data['page_strains'] = page
            self.session.save()
        elif (self.session.data.has_key('page_strains')):
            if (self.form.has_key('filter')):
                #Save filter on session
                self.session.data['page_strains'] = page
                self.session.save()
            else:
                page = int(self.session.data['page_strains'])


        #Enable paging
        if (totalpages > 1):
          self.data['paging'] = 'LIMIT ' + str((page - 1) * self.session.data['lines_per_page']) + ',' + str(self.session.data['lines_per_page']) + ';'

        #SELECT id_strain, code, genus, subgenus, species, subdiv, infra_name, type
        if self.g.isManager(self.session.data['roles']): #Administrator or Manager
          self.execute('get_strain_list', self.data, True)
        else:
          roles = str(self.session.data['roles']).replace("L","")
          roles = roles.replace("[","(")
          roles = roles.replace("]",")")
          self.data['roles_list'] = roles
          self.execute('get_strain_list_restrict', self.data,raw_mode = True)
        list_strains = list(self.fetch('all'))

        i = 0

        for strain in list_strains:
            #Species FullName
            species = Lists.spe_fullname(strain, use_infracomplement=True)

            #Strain Type
            if not strain['type']:
                strain['type'] = '-'

            #Origin Code,
            if not strain['internal_code']:
                strain['internal_code'] = '-'

            code = strain['code']

            #if status active color black, else color gray
            style_tr = ''
            if strain['status'] != 'inactive':
                style_tr = 'color:#000';
            else:
                style_tr = 'color:#A2A2A2'

            from labels import label_dict
            has_critical = False
            critical_stock_html = []
            #Check critical stock for this strain by preservation method
            self.execute('get_strain_critical_stock_preservation_method', {'id_strain':strain['id_strain'],'id_lang':self.session.data['id_lang'],'id_subcoll':self.session.data['id_subcoll']})
            all_lots = self.fetch('all')
            if all_lots:
                critical_stock_html += ['<table class=''popup_table'' width=''100%%'' cellpadding=2 cellspacing=2 border=0><tr class=''popup_table'' font-weight: bold;''><th class=''popup_table'' width=''131px''>%(label_Strains_Stock_Preservation_Method)s</th><th class=''popup_table'' width=''90px''>%(label_Strains_Stock_Minimum)s</th><th class=''popup_table'' width=''90px''>%(label_Strains_Stock_In_Stock)s</th></tr>' % label_dict]
                has_critical = True
            for one_lot in all_lots:
                critical_stock_html.append('<tr class=''popup_table''><td class=''popup_table''>%s</td><td class=''popup_table'' style=''text-align: right''>%s</td><td class=''popup_table'' style=''text-align: right''>%s</td></tr>' % (one_lot['method'], one_lot['quantity'], one_lot['in_stock']))
            if all_lots:
                critical_stock_html.append('</table>')

            #Check critical stock for this strain
            self.execute('get_strain_critical_stock', {'id':strain['id_strain']})
            all_lots = self.fetch('all')
            if all_lots:
                critical_stock_html += ['<table class=''popup_table'' width=''100%%'' cellpadding=2 cellspacing=2 border=0><tr class=''popup_table'' font-weight: bold;''><th class=''popup_table'' width=''131px''>%(label_Strains_Stock_Lot_Number)s</th><th class=''popup_table'' width=''90px''>%(label_Strains_Stock_Minimum)s</th><th class=''popup_table'' width=''90px''>%(label_Strains_Stock_In_Stock)s</th></tr>' % label_dict]
                has_critical = True
            for one_lot in all_lots:
                critical_stock_html.append('<tr class=''popup_table''><td class=''popup_table''>%s</td><td class=''popup_table'' style=''text-align: right''>%s</td><td class=''popup_table'' style=''text-align: right''>%s</td></tr>' % (one_lot['lot_name'], one_lot['stock_minimum'], one_lot['stock']))
            if all_lots:
                critical_stock_html.append('</table>')

            if has_critical:
                html_id = str(strain['id_strain'])
                image_onclick = "criticalPopup(event, '%s', '%s', '%s', '%s', '%s');" % (
                    "img" + html_id,
                    "div" + html_id,
                    _("Critical stock levels") + ":",
                    "".join(critical_stock_html),
                    'general'
                )
                img_title = _("There are items with critical stock levels. Click for details.")
                critical_image = '''
                    <img id="%s" src="../img/exclamation.png" onClick="%s; return true;" style="cursor: pointer" title="%s" alt="%s">
                    <input type='hidden' id='%s' value=''>
                    <div id="%s" class="critical_popup" onClick='closePopup(event, \"%s\");'></div>
                ''' % ("img" + html_id, image_onclick, img_title, img_title, "save_div" + html_id, "div" + html_id, "div" + html_id)
                code = "%s %s" % (code, critical_image)

            #Class of row
            if ((i % 2) == 0): css_class = "row1"
            else: css_class = "row2"

            #Absolute Row for the navigator of detail's page
            absolute_row = i + ((self.session.data['lines_per_page']) * (page - 1))

            #Output
            self.html += html % (self.indent_size, css_class, str(strain['id_strain']), absolute_row, style_tr,
                                 self.indent_size, code,
                                 self.indent_size, species,
                                 self.indent_size, strain['internal_code'],
                                 self.indent_size, strain['type'],
                                 self.indent_size)
            i += 1

        #Security
        #If user does not have permission to create then don't show the "new" button
        allow_create = self.g.get_area_permission(self.cookie_value, self.session, 'strains', 'allow_create')
        if self.g.isManager(self.session.data['roles']):
	  allow_create = 'y'
        if allow_create != 'y':
          import re
          self.page_parts['submenu'] = re.sub('<a id="action_new" href="[.]/%\(who\)s[.]new[.]py".*?/a>',"",self.page_parts['submenu'])

        return self.html, self.get_foothtml(4, page, self.session.data['max_num_pages'], totalpages, '.' + environ['SCRIPT_NAME'][environ['SCRIPT_NAME'].rindex('/'):] + '?page=%s'), page, filter.decode('utf8')

    def doc(self):
        html = '%s<tr class="%s" onclick="location=\'./doc.detail.py?id=%s&row=%s\'">\
                  %s  <td class="qualifier">%s</td>\
                  %s  <td class="code">%s</td>\
                  %s  <td class="title">%s</td>\
                  %s</tr>'

        #Filter
        filter = ''
        if (self.form.has_key('filter')):
            filter = str(self.form['filter'].value).strip()
            filter = self.ConvertStrUnicode(filter).encode("utf-8")

            #Save filter on session
            self.session.data['filter_docs'] = filter
            self.session.save()
        elif (self.session.data.has_key('filter_docs')):
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

        #Verify field_order is changed
        if self.form.has_key('field_order'):
            self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'doc', self.form['field_order'].value)

        #Get field and mode for order list
        field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'doc')

        #Creating order image

        #Define if order is Asc, or Desc
        if mode == "ASC":
          self.img="<img class='order' src='"+self.img_path_up+"'/>"
        else:
          self.img="<img class='order' src='"+self.img_path_down+"'/>"

        #define what img in HTML must be changed
        self.order_img = "img_" + field

        #Define field_order with mode
        self.data['field_order'] = field + ' ' + mode

        #Disable paging
        self.data['paging'] = ';'

        #Execute again for rows count
        if self.g.isManager(self.session.data['roles']): #Administrator or Manager
          self.execute('get_doc_list', self.data, True)
        else:
          roles = str(self.session.data['roles']).replace("L","")
          roles = roles.replace("[","(")
          roles = roles.replace("]",")")
          self.data['roles_list'] = roles
          self.execute('get_doc_list_restrict', self.data,raw_mode = True)

        #Define totalpages
        totalpages = int(math.ceil(float(self.getrowscount())/self.session.data['lines_per_page']))

        #Verify page
        page = 1
        if self.form.has_key('page'):
            page = int(self.form['page'].value)
            if page <= 0: page = 1
            elif page > totalpages: page = totalpages

            #Save filter on session
            self.session.data['page_docs'] = page
            self.session.save()
        elif (self.session.data.has_key('page_docs')):
            if (self.form.has_key('filter')):
                #Save filter on session
                self.session.data['page_docs'] = page
                self.session.save()
            else:
                page = int(self.session.data['page_docs'])

        #Enable paging
        if (totalpages > 1):
          self.data['paging'] = 'LIMIT ' + str((page - 1) * self.session.data['lines_per_page']) + ',' + str(self.session.data['lines_per_page']) + ';'

        #SELECT id_doc, qualifier, code, title
        if self.g.isManager(self.session.data['roles']): #Administrator or Manager
          self.execute('get_doc_list', self.data, True)
        else:
          roles = str(self.session.data['roles']).replace("L","")
          roles = roles.replace("[","(")
          roles = roles.replace("]",")")
          self.data['roles_list'] = roles
          self.execute('get_doc_list_restrict',self.data,raw_mode = True)
        list_doc = self.fetch('all')

        i = 0

        for doc in list_doc:
            if doc['title'] == '': #Get first title found by id_lang (usually English)
              self.execute('get_first_doc_title_found',{'id_doc':doc['id_doc']})
              doc['title'] = self.fetch('one')

            #Class of row
            if ((i % 2) == 0): css_class = "row1"
            else: css_class = "row2"

            #Absolute Row for the navigator of detail's page
            absolute_row = i + ((self.session.data['lines_per_page']) * (page - 1))

            #Output
            self.html += html % (self.indent_size, css_class, str(doc['id_doc']), absolute_row,
                                 self.indent_size, doc['qualifier'],
                                 self.indent_size, doc['code'],
                                 self.indent_size, doc['title'],
                                 self.indent_size)
            i += 1

        #Security
        #If user does not have permission to create then don't show the "new" button
        allow_create = self.g.get_area_permission(self.cookie_value, self.session, 'doc', 'allow_create')
        if self.g.isManager(self.session.data['roles']):
	  allow_create = 'y'
        if allow_create != 'y':
          import re
          self.page_parts['submenu'] = re.sub('<a id="action_new" href="[.]/%\(who\)s[.]new[.]py".*?/a>',"",self.page_parts['submenu'])

        return self.html, self.get_foothtml(3, page, self.session.data['max_num_pages'], totalpages, '.' + environ['SCRIPT_NAME'][environ['SCRIPT_NAME'].rindex('/'):] + '?page=%s'), page, filter.decode('utf8')

    def ref(self):
        html = '%s<tr class="%s" onclick="location=\'./ref.detail.py?id=%s&row=%s\'">\
                  %s  <td class="code">%s</td>\
                  %s  <td class="author">%s</td>\
                  %s  <td class="title">%s</td>\
                  %s  <td class="year">%s</td>\
                  %s</tr>'

        #Filter
        filter = ''
        if (self.form.has_key('filter')):
            filter = str(self.form['filter'].value).strip()
            filter = self.ConvertStrUnicode(filter).encode("utf-8")

            #Save filter on session
            self.session.data['filter_refs'] = filter
            self.session.save()
        elif (self.session.data.has_key('filter_refs')):
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

        #Verify field_order is changed
        if self.form.has_key('field_order'):
            self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'ref', self.form['field_order'].value)

        #Get field and mode for order list
        field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'ref')

        #Creating order image

        #Define if order is Asc, or Desc
        if mode == "ASC":
          self.img="<img class='order' src='"+self.img_path_up+"'/>"
        else:
          self.img="<img class='order' src='"+self.img_path_down+"'/>"

        #define what img in HTML must be changed
        self.order_img = "img_" + field

        if field == 'code':
            field = 'id_ref %s' % mode
        else:
            field = field + ' ' + mode

        #Define field_order with mode
        self.data['field_order'] = field

        #Disable paging
        self.data['paging'] = ';'

        #Execute again for rows count
        if self.g.isManager(self.session.data['roles']): #Administrator or Manager
          self.execute('get_ref_list', self.data, True)
        else:
          roles = str(self.session.data['roles']).replace("L","")
          roles = roles.replace("[","(")
          roles = roles.replace("]",")")
          self.data['roles_list'] = roles
          self.execute('get_ref_list_restrict', self.data,raw_mode = True)

        #Define totalpages
        totalpages = int(math.ceil(float(self.getrowscount())/self.session.data['lines_per_page']))

        #Verify page
        page = 1
        if self.form.has_key('page'):
            page = int(self.form['page'].value)
            if page <= 0: page = 1
            elif page > totalpages: page = totalpages

            #Save filter on session
            self.session.data['page_refs'] = page
            self.session.save()
        elif (self.session.data.has_key('page_refs')):
            if (self.form.has_key('filter')):
                #Save filter on session
                self.session.data['page_refs'] = page
                self.session.save()
            else:
                page = int(self.session.data['page_refs'])

        #Enable paging
        if (totalpages > 1):
          self.data['paging'] = 'LIMIT ' + str((page - 1) * self.session.data['lines_per_page']) + ',' + str(self.session.data['lines_per_page']) + ';'

        #SELECT id_ref, author, title, year
        if self.g.isManager(self.session.data['roles']): #Administrator or Manager
          self.execute('get_ref_list', self.data, True)
        else:
          roles = str(self.session.data['roles']).replace("L","")
          roles = roles.replace("[","(")
          roles = roles.replace("]",")")
          self.data['roles_list'] = roles
          self.execute('get_ref_list_restrict',self.data,raw_mode = True)
        list_ref = self.fetch('all')
        i = 0

        for ref in list_ref:
            #if ref['title'] == '': #Get first title found by id_lang (usually English)
              #self.execute('get_first_ref_title_found',{'id_ref':ref['id_ref']})
              #ref['title'] = self.fetch('one')

            #Class of row

            if ((i % 2) == 0): css_class = "row1"
            else: css_class = "row2"

            #Absolute Row for the navigator of detail's page
            absolute_row = i + ((self.session.data['lines_per_page']) * (page - 1))

            #Output
            self.html += html % (self.indent_size, css_class, str(ref['id_ref']), absolute_row,
                                 self.indent_size, str(ref['id_ref']),
                                 self.indent_size, ref['author'],
                                 self.indent_size, ref['title'],
                                 self.indent_size, ref['year'],
                                 self.indent_size)
            i += 1

        #Security
        #If user does not have permission to create then don't show the "new" button
        allow_create = self.g.get_area_permission(self.cookie_value, self.session, 'ref', 'allow_create')
        if self.g.isManager(self.session.data['roles']):
	  allow_create = 'y'
        if allow_create != 'y':
          import re
          self.page_parts['submenu'] = re.sub('<a id="action_new" href="[.]/%\(who\)s[.]new[.]py".*?/a>',"",self.page_parts['submenu'])

        return self.html, self.get_foothtml(4, page, self.session.data['max_num_pages'], totalpages, '.' + environ['SCRIPT_NAME'][environ['SCRIPT_NAME'].rindex('/'):] + '?page=%s'), page, filter.decode('utf8')

    def people(self):
        html = '%s<tr class="%s" onclick="location=\'./people.detail.py?id=%s&row=%s\'">\
                %s  <td class="name">%s</td>\
                %s  <td class="institution">%s</td>\
                %s</tr>'

        #Filter
        filter = ''
        if (self.form.has_key('filter')):
            filter = str(self.form['filter'].value).strip()
            filter = self.ConvertStrUnicode(filter).encode("utf-8")

            #Save filter on session
            self.session.data['filter_people'] = filter
            self.session.save()
        elif (self.session.data.has_key('filter_people')):
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

        #Verify field_order is changed
        if self.form.has_key('field_order'):
            self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'people', self.form['field_order'].value)

        #Get field and mode for order list
        field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'people')

        #Creating order image

        #Define if order is Asc, or Desc
        if mode == "ASC":
          self.img="<img class='order' src='"+self.img_path_up+"'/>"
        else:
          self.img="<img class='order' src='"+self.img_path_down+"'/>"

        #define what img in HTML must be changed
        self.order_img = "img_" + field

        #Verify field_order for special order
        if field == 'institution':
            isInstitution = True
            field = 'name'
        else:
            isInstitution = False

        #Define field_order with mode
        self.data['field_order'] = field + ' ' + mode

        #Disable paging
        self.data['paging'] = ';'

        #Execute again for rows count
        if self.g.isManager(self.session.data['roles']): #Administrator or Manager
          self.execute('get_person_list', self.data, True)
        else:
          roles = str(self.session.data['roles']).replace("L","")
          roles = roles.replace("[","(")
          roles = roles.replace("]",")")
          self.data['roles_list'] = roles
          self.execute('get_person_list_restrict', self.data,raw_mode = True)

        #Define totalpages
        totalpages = int(math.ceil(float(self.getrowscount())/self.session.data['lines_per_page']))

        #Verify page
        page = 1
        if self.form.has_key('page'):
            page = int(self.form['page'].value)
            if page <= 0: page = 1
            elif page > totalpages: page = totalpages

            #Save filter on session
            self.session.data['page_people'] = page
            self.session.save()
        elif (self.session.data.has_key('page_people')):
            if (self.form.has_key('filter')):
                #Save filter on session
                self.session.data['page_people'] = page
                self.session.save()
            else:
                page = int(self.session.data['page_people'])

        #Enable paging
        if (totalpages > 1):
          self.data['paging'] = 'LIMIT ' + str((page - 1) * self.session.data['lines_per_page']) + ',' + str(self.session.data['lines_per_page']) + ';'

        #SELECT id_person, name, nickname
        if self.g.isManager(self.session.data['roles']): #Administrator or Manager
          self.execute('get_person_list', self.data, True)
        else:
          roles = str(self.session.data['roles']).replace("L","")
          roles = roles.replace("[","(")
          roles = roles.replace("]",")")
          self.data['roles_list'] = roles
          self.execute('get_person_list_restrict',self.data,raw_mode = True)
        list_people = self.fetch('all')
        list_people2 = list()

        for person in list_people:
            #Name + Nickname
            if person['nickname']:
                person['name'] += ' (%s)' % person['nickname']

            #SELECT id_institution, complement, nickname, contact, department, email
            self.execute ("get_person_contact_relations", {'id':person['id_person']})
            list_inst = self.fetch("all")
            institutions = []
            for inst in list_inst:
                str_inst = inst['complement']
                if inst['nickname']:
                    str_inst += " (%s)" % inst['nickname']
                if inst['contact']:
                    str_inst += " [%s]" % _('contact');
                institutions.append(str_inst)
            institutions.sort()
            person['institution'] = "<br />".join(institutions)

            list_people2.append(person)

        #If order is institution use ins_people_cmp
        if isInstitution:
            if self.data['field_order'][-3:] == 'ASC':
                list_people2.sort(self.ins_people_cmp)
            elif self.data['field_order'][-4:] == 'DESC':
                list_people2.sort(cmp=self.ins_people_cmp, reverse=True)

        i = 0

        #Output
        for person in list_people2:

            #Class of row
            if ((i % 2) == 0): css_class = "row1"
            else: css_class = "row2"

            #Absolute Row for the navigator of detail's page
            absolute_row = i + ((self.session.data['lines_per_page']) * (page - 1))

            self.html += html % (self.indent_size, css_class, str(person['id_person']), absolute_row,
                                 self.indent_size, person['name'],
                                 self.indent_size, person['institution'],
                                 self.indent_size)
            i += 1

        #Security
        #If user does not have permission to create then don't show the "new" button
        allow_create = self.g.get_area_permission(self.cookie_value, self.session, 'people', 'allow_create')
        if self.g.isManager(self.session.data['roles']):
	  allow_create = 'y'
        if allow_create != 'y':
          import re
          self.page_parts['submenu'] = re.sub('<a id="action_new" href="[.]/%\(who\)s[.]new[.]py".*?/a>',"",self.page_parts['submenu'])

        return self.html, self.get_foothtml(3, page, self.session.data['max_num_pages'], totalpages, '.' + environ['SCRIPT_NAME'][environ['SCRIPT_NAME'].rindex('/'):] + '?page=%s'), page, filter.decode('utf8')

    def inst(self):
        #Output
        html = '%s<tr class="%s" onclick="location=\'./institutions.detail.py?id=%s&row=%s\'">\
                %s  <td class="nickname">%s</td>\
                %s  <td class="name">%s</td>\
                %s  <td class="complement">%s</td>\
                %s</tr>'

        #Filter
        filter = ''
        if (self.form.has_key('filter')):
            filter = str(self.form['filter'].value).strip()
            filter = self.ConvertStrUnicode(filter).encode("utf-8")

            #Save filter on session
            self.session.data['filter_insts'] = filter
            self.session.save()
        elif (self.session.data.has_key('filter_insts')):
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

        #Verify field_order is changed
        if self.form.has_key('field_order'):
            self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'inst', self.form['field_order'].value)

        #Get field and mode for order list
        field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'inst')

        #Creating order image

        #Define if order is Asc, or Desc
        if mode == "ASC":
          self.img="<img class='order' src='"+self.img_path_up+"'/>"
        else:
          self.img="<img class='order' src='"+self.img_path_down+"'/>"

        #define what img in HTML must be changed
        self.order_img = "img_" + field

        field = field + ' ' + mode

        #Define field_order with mode
        self.data['field_order'] = field

        #Disable paging
        self.data['paging'] = ';'

        #Execute again for rows count
        if self.g.isManager(self.session.data['roles']): #Administrator or Manager
          self.execute('get_inst_list', self.data, True)
        else:
          roles = str(self.session.data['roles']).replace("L","")
          roles = roles.replace("[","(")
          roles = roles.replace("]",")")
          self.data['roles_list'] = roles
          self.execute('get_inst_list_restrict', self.data,raw_mode = True)

        #Define totalpages
        totalpages = int(math.ceil(float(self.getrowscount())/self.session.data['lines_per_page']))

        #Verify page
        page = 1
        if self.form.has_key('page'):
            page = int(self.form['page'].value)
            if page <= 0: page = 1
            elif page > totalpages: page = totalpages
            #Save filter on session
            self.session.data['page_insts'] = page
            self.session.save()

        elif (self.session.data.has_key('page_insts')):
            if (self.form.has_key('filter')):
                #Save filter on session
                self.session.data['page_insts'] = page
                self.session.save()
            else:
                page = int(self.session.data['page_insts'])

        #Enable paging
        if (totalpages > 1):
          self.data['paging'] = 'LIMIT ' + str((page - 1) * self.session.data['lines_per_page']) + ',' + str(self.session.data['lines_per_page']) + ';'

        #SELECT id_institution, complement, nickname, name
        if self.g.isManager(self.session.data['roles']): #Administrator or Manager
          self.execute('get_inst_list', self.data, True)
        else:
          roles = str(self.session.data['roles']).replace("L","")
          roles = roles.replace("[","(")
          roles = roles.replace("]",")")
          self.data['roles_list'] = roles
          self.execute('get_inst_list_restrict',self.data,raw_mode = True)
        list_inst = self.fetch('all')

        i = 0

        for inst in list_inst:
            complement = inst['complement']

            #Class of row
            if ((i % 2) == 0): css_class = "row1"
            else: css_class = "row2"

            #Absolute Row for the navigator of detail's page
            absolute_row = i + ((self.session.data['lines_per_page']) * (page - 1))

            #Output
            self.html += html % (self.indent_size, css_class, str(inst['id_institution']), absolute_row,
                                 self.indent_size, inst['nickname'],
                                 self.indent_size, inst['name'],
                                 self.indent_size, complement,
                                 self.indent_size)
            i += 1

        #Security
        #If user does not have permission to create then don't show the "new" button
        allow_create = self.g.get_area_permission(self.cookie_value, self.session, 'institutions', 'allow_create')
        if self.g.isManager(self.session.data['roles']):
	  allow_create = 'y'
        if allow_create != 'y':
          import re
          self.page_parts['submenu'] = re.sub('<a id="action_new" href="[.]/%\(who\)s[.]new[.]py".*?/a>',"",self.page_parts['submenu'])

        return self.html, self.get_foothtml(3, page, self.session.data['max_num_pages'], totalpages, '.' + environ['SCRIPT_NAME'][environ['SCRIPT_NAME'].rindex('/'):] + '?page=%s'), page, filter.decode('utf8')

    def preservation(self):
        html = '%s<tr class="%s" onclick="location=\'./preservation.detail.py?id=%s&row=%s\'">\
                  %s  <td class="date">%s</td>\
                  %s  <td class="lot">%s</td>\
                  %s  <td class="method">%s</td>\
                  %s  <td class="strain">%s</td>\
                  %s  <td class="stock">%s</td>\
                  %s  <td class="instock">%s</td>\
                %s</tr>'

        stripped_sciname = self.get_stripped("sciname_no_auth")

        #Filter
        filter = ''
        if (self.form.has_key('filter')):
            filter = str(self.form['filter'].value).strip()
            filter = self.ConvertStrUnicode(filter).encode("utf-8")

            #Save filter on session
            self.session.data['filter_preservations'] = filter
            self.session.save()
        elif (self.session.data.has_key('filter_preservations')):
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

        #Verify field_order is changed
        if self.form.has_key('field_order'):
            self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'preservation', self.form['field_order'].value)

        isTaxon = False;

        #Get field and mode for order list
        field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'preservation')

        #Creating order image

        #Define if order is Asc, or Desc
        if mode == "ASC":
          self.img="<img class='order' src='"+self.img_path_up+"'/>"
        else:
          self.img="<img class='order' src='"+self.img_path_down+"'/>"

        #define what img in HTML must be changed
        self.order_img = "img_" + field

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

        #raise str(field)

        #Define field_order with mode
        #self.data['field_order'] = field
        self.data['field_order'] = field

        #Disable paging
        self.data['paging'] = ';'

        #Execute again for rows count
        if self.g.isManager(self.session.data['roles']): #Administrator or Manager
          self.execute('get_preservation_list', self.data, True)
        else:
          roles = str(self.session.data['roles']).replace("L","")
          roles = roles.replace("[","(")
          roles = roles.replace("]",")")
          self.data['roles_list'] = roles
          self.execute('get_preservation_list_restrict', self.data,raw_mode = True)

        #Define totalpages
        totalpages = int(math.ceil(float(self.getrowscount())/self.session.data['lines_per_page']))

        #Verify page
        page = 1
        if self.form.has_key('page'):
            page = int(self.form['page'].value)
            if page <= 0: page = 1
            elif page > totalpages: page = totalpages

            #Save filter on session
            self.session.data['page_preservations'] = page
            self.session.save()
        elif (self.session.data.has_key('page_preservations')):
            if (self.form.has_key('filter')):
                #Save filter on session
                self.session.data['page_preservations'] = page
                self.session.save()
            else:
                page = int(self.session.data['page_preservations'])

        #Enable paging
        if (totalpages > 1):
          self.data['paging'] = 'LIMIT ' + str((page - 1) * self.session.data['lines_per_page']) + ',' + str(self.session.data['lines_per_page']) + ';'

        #Subcollection filtering
        self.data['id_subcoll'] = self.session.data['id_subcoll']

        #SELECT
        if self.g.isManager(self.session.data['roles']): #Administrator or Manager
          self.execute('get_preservation_list', self.data, True)
        else:
          roles = str(self.session.data['roles']).replace("L","")
          roles = roles.replace("[","(")
          roles = roles.replace("]",")")
          self.data['roles_list'] = roles
          self.execute('get_preservation_list_restrict',self.data,raw_mode = True)
        preservations = self.fetch('all')

        #Put all strains together in one field
        previous_id = 0
        strain_list = []

        for preservation in preservations:
            stock_css_class = ""
            if (preservation["in_stock"] <= preservation["stock_minimum"]):
                stock_css_class = "red"

            #Not Italic for Species = "sp."
            #if preservation['species'] == 'sp.':
            #    preservation['species'] = '<span class="sp_ponto">%s</span>' % preservation['species']
            if preservation['id_preservation'] != previous_id:
                previous_id = preservation['id_preservation']
                strain_list.append(preservation)
                strain_list[-1]['strain'] = '<span class="' + stock_css_class + '">' + preservation['code'] + ' - ' + '<span class="species">' + Lists.spe_fullname(preservation, use_infracomplement=True) + '</span>' + '</span>'
                strain_list[-1]['stock_minimum'] = '<span class="' + stock_css_class + '">' + str(preservation['stock_minimum']) + '</span>'
                strain_list[-1]['in_stock'] = '<span class="' + stock_css_class + '">' + str(preservation['in_stock']) + '</span>'
            else:
                strain_list[-1]['strain'] += '<br />'+'<span class="' + stock_css_class + '">' + preservation['code'] + ' - ' + '<span class="species">'  + Lists.spe_fullname(preservation, use_infracomplement=True) + '</span>' + '</span>'
                strain_list[-1]['stock_minimum'] += '<br />'+'<span class="' + stock_css_class + '">' + str(preservation['stock_minimum']) + '</span>'
                strain_list[-1]['in_stock'] += '<br />'+'<span class="' + stock_css_class + '">' + str(preservation['in_stock']) + '</span>'

        #If order is taxon use preserv_strain_cmp
        if isTaxon:
            if self.data['field_order'][-3:] == 'ASC':
                strain_list.sort(self.preserv_strain_cmp)
            elif self.data['field_order'][-4:] == 'DESC':
                strain_list.sort(cmp=self.preserv_strain_cmp, reverse=True)

        i = 0

        for preservation in strain_list:
            #Class of row
            if ((i % 2) == 0): css_class = "row1"
            else: css_class = "row2"

            #Absolute Row for the navigator of detail's page
            absolute_row = i + ((self.session.data['lines_per_page']) * (page - 1))

            #Output
            self.html += html % (self.indent_size, css_class, preservation['id_preservation'], absolute_row,
                                 self.indent_size, self.format_date('view',preservation['date']),
                                 self.indent_size, preservation['lot_name'],
                                 self.indent_size, preservation['method'],
                                 self.indent_size, preservation['strain'],
                                 self.indent_size, preservation['stock_minimum'],
                                 self.indent_size, preservation['in_stock'],
                                 self.indent_size)
            i += 1

        #Security
        #If user does not have permission to create then don't show the "new" button
        allow_create = self.g.get_area_permission(self.cookie_value, self.session, 'preservation', 'allow_create')
        if self.g.isManager(self.session.data['roles']):
	  allow_create = 'y'
        if allow_create != 'y':
          import re
          self.page_parts['submenu'] = re.sub('<a id="action_new" href="[.]/%\(who\)s[.]new[.]py".*?/a>',"",self.page_parts['submenu'])

        return self.html, self.get_foothtml(6, page, self.session.data['max_num_pages'], totalpages, '.' + environ['SCRIPT_NAME'][environ['SCRIPT_NAME'].rindex('/'):] + '?page=%s'), page, filter.decode('utf8')

    def distribution(self):
        html = '%s<tr class="%s" onclick="location=\'./distribution.detail.py?id=%s&row=%s\'">\
                  %s  <td class="date">%s</td>\
                  %s  <td class="lot">%s</td>\
                  %s  <td class="strain">%s</td>\
                  %s  <td class="quantity">%s</td>\
                  %s  <td class="institution">%s</td>\
                %s</tr>'

        stripped_sciname = self.get_stripped("sciname_no_auth")

        #Filter
        filter = ''
        if (self.form.has_key('filter')):
            filter = str(self.form['filter'].value).strip()
            filter = self.ConvertStrUnicode(filter).encode("utf-8")

            #Save filter on session
            self.session.data['filter_distributions'] = filter
            self.session.save()
        elif (self.session.data.has_key('filter_distributions')):
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
                        "OR st.code LIKE x'25" + word.encode("hex") + "25' " +
                        "OR " + stripped_sciname + " LIKE x'25" + word.encode("hex") + "25' "
                        "OR dol.quantity = x'" + word.encode("hex") + "' OR i.name LIKE x'25" + word.encode("hex") + "25' OR p.name LIKE x'25" + word.encode("hex") + "25' " +
                        "OR st.infra_complement LIKE x'25" + word.encode("hex") + "25') ")
            self.data['condition']= "".join(self.data['condition'])
        else:
            self.data['condition'] = ' '

        #Verify field_order is changed
        if self.form.has_key('field_order'):
            self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'distribution', self.form['field_order'].value)

        isInstitution = False;

        #Get field and mode for order list
        field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'distribution')

        #Creating order image

        #Define if order is Asc, or Desc
        if mode == "ASC":
          self.img="<img class='order' src='"+self.img_path_up+"'/>"
        else:
          self.img="<img class='order' src='"+self.img_path_down+"'/>"

        #define what img in HTML must be changed
        self.order_img = "img_" + field

        if field == 'lot_name':
            field = 'l.name %s' % mode
        elif field == 'species':
            field = 'st.code ' + mode + ', ' + stripped_sciname + ' ' + mode
        elif field == 'institution':
            isInstitution = True;
            field = 'i.name %s' % mode
        else:
            field = field + ' ' + mode

        #Define field_order with mode
        self.data['field_order'] = field

        #Subcollection filtering
        self.data['id_subcoll'] = self.session.data['id_subcoll']

        #Disable paging
        self.data['paging'] = ';'

        #Execute again for rows count
        if self.g.isManager(self.session.data['roles']): #Administrator or Manager
          self.execute('get_distribution_list', self.data, True)
        else:
          roles = str(self.session.data['roles']).replace("L","")
          roles = roles.replace("[","(")
          roles = roles.replace("]",")")
          self.data['roles_list'] = roles
          self.execute('get_distribution_list_restrict', self.data,raw_mode = True)
        #Define totalpages
        totalpages = int(math.ceil(float(self.getrowscount())/self.session.data['lines_per_page']))

        #Verify page
        page = 1
        if self.form.has_key('page'):
            page = int(self.form['page'].value)
            if page <= 0: page = 1
            elif page > totalpages: page = totalpages

            #Save filter on session
            self.session.data['page_distributions'] = page
            self.session.save()
        elif (self.session.data.has_key('page_distributions')):
            if (self.form.has_key('filter')):
                #Save filter on session
                self.session.data['page_distributions'] = page
                self.session.save()
            else:
                page = int(self.session.data['page_distributions'])

        #Enable paging
        if (totalpages > 1):
          self.data['paging'] = 'LIMIT ' + str((page - 1) * self.session.data['lines_per_page']) + ',' + str(self.session.data['lines_per_page']) + ';'

        #SELECT id_ref, author, title, year
        if self.g.isManager(self.session.data['roles']): #Administrator or Manager
          self.execute('get_distribution_list', self.data, True)
        else:
          roles = str(self.session.data['roles']).replace("L","")
          roles = roles.replace("[","(")
          roles = roles.replace("]",")")
          self.data['roles_list'] = roles
          self.execute('get_distribution_list_restrict',self.data,raw_mode = True)
        distributions = self.fetch('all')
        distributions2 = []

        for distribution in distributions:

            #Not Italic for Specie = "sp."
            #if distribution['species'] == 'sp.':
            #    distribution['species'] = '<span class="sp_ponto">%s</span>' % distribution['species']

            #person name include in ()
            if distribution['person_name'] != '':
                distribution['institution'] = distribution['inst_name'] + "<br/>%s" % distribution['person_name']
            else:
                distribution['institution'] = distribution['inst_name']
            distribution['strain'] = distribution['code'] + ' - ' + Lists.spe_fullname(distribution, use_infracomplement=True)

            distributions2.append(distribution)

        #If order is institution use ins_people_cmp
        if isInstitution:
            if self.data['field_order'][-3:] == 'ASC':
                distributions2.sort(self.ins_people_cmp)
            elif self.data['field_order'][-4:] == 'DESC':
                distributions2.sort(cmp=self.ins_people_cmp, reverse=True)

        i = 0

        for distribution in distributions2:
            #Class of row
            if ((i % 2) == 0): css_class = "row1"
            else: css_class = "row2"

            #Absolute Row for the navigator of detail's page
            absolute_row = i + ((self.session.data['lines_per_page']) * (page - 1))

            if not int(distribution['sum_quantity']):
                distribution['sum_quantity'] = '-'

            #Output
            self.html += html % (self.indent_size, css_class, distribution['id_distribution'], absolute_row,
                                 self.indent_size, self.format_date('view',distribution['date']),
                                 self.indent_size, distribution['lot_name'],
                                 self.indent_size, distribution['strain'],
                                 self.indent_size, distribution['sum_quantity'],
                                 self.indent_size, distribution['institution'],
                                 self.indent_size)
            i += 1

        #Security
        #If user does not have permission to create then don't show the "new" button
        allow_create = self.g.get_area_permission(self.cookie_value, self.session, 'distribution', 'allow_create')
        if self.g.isManager(self.session.data['roles']):
	  allow_create = 'y'
        if allow_create != 'y':
          import re
          self.page_parts['submenu'] = re.sub('<a id="action_new" href="[.]/%\(who\)s[.]new[.]py".*?/a>',"",self.page_parts['submenu'])

        return self.html, self.get_foothtml(5, page, self.session.data['max_num_pages'], totalpages, '.' + environ['SCRIPT_NAME'][environ['SCRIPT_NAME'].rindex('/'):] + '?page=%s'), page, filter.decode('utf8')

    def reports(self):
        #brk(host="localhost", port=9000)
        html = '%s<tr class="%s" onclick="location=\'./reports.detail.py?id=%s&row=%s\'">\
                %s  <td class="type">%s</td>\
                %s  <td class="description">%s</td>\
                %s</tr>'

        #Filter
        filter = ''
        if (self.form.has_key('filter')):
            filter = str(self.form['filter'].value).strip()

            #Save filter on session
            self.session.data['filter_reports'] = filter
            self.session.save()
        elif (self.session.data.has_key('filter_reports')):
            filter = self.session.data['filter_reports']

        if (filter != ''):
            words = [x for x in filter.split(" ") if x != '']

            self.data['condition'] = []
            for word in words:
                #0x25 == '%'
                self.data['condition'].append(
                                              "AND (replang.type LIKE x'25" + word.encode("hex") + "25' " +
                                              "OR rep.description LIKE x'25" + word.encode("hex") + "25') ")
            self.data['condition']= "".join(self.data['condition'])
        else:
            self.data['condition'] = ' '

        #Verify field_order is changed
        if self.form.has_key('field_order'):
            self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'reports', self.form['field_order'].value)

        #Get field and mode for order list
        field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'reports')
        
        #Creating order image

        #Define if order is Asc, or Desc
        if mode == "ASC":
          self.img="<img class='order' src='"+self.img_path_up+"'/>"
        else:
          self.img="<img class='order' src='"+self.img_path_down+"'/>"

        #define what img in HTML must be changed
        self.order_img = "img_" + field

        #Define field_order with mode
        self.data['field_order'] = field + ' ' + mode

        #Disable paging
        self.data['paging'] = ';'

        #Execute again for rows count
        if 2 in self.session.data['roles']: #Administrator
          self.execute('get_report_list', self.data, True)
        else:
          roles = str(self.session.data['roles']).replace("L","")
          roles = roles.replace("[","(")
          roles = roles.replace("]",")")
          self.data['roles_list'] = roles
          self.execute('get_report_list_restrict', self.data,raw_mode = True)

        #Define totalpages
        totalpages = int(math.ceil(float(self.getrowscount())/self.session.data['lines_per_page']))

        #Verify page
        page = 1
        if self.form.has_key('page'):
            page = int(self.form['page'].value)
            if page <= 0: page = 1
            elif page > totalpages: page = totalpages

            #Save filter on session
            self.session.data['page_reports'] = page
            self.session.save()
        elif (self.session.data.has_key('page_reports')):
            if (self.form.has_key('filter')):
                #Save filter on session
                self.session.data['page_reports'] = page
                self.session.save()
            else:
                page = int(self.session.data['page_reports'])

        #Enable paging
        if (totalpages > 1):
          self.data['paging'] = 'LIMIT ' + str((page - 1) * self.session.data['lines_per_page']) + ',' + str(self.session.data['lines_per_page']) + ';'

        #SELECT type, description
        if 2 in self.session.data['roles']: #Administrator
          self.execute('get_report_list', self.data, True)
        else:
          roles = str(self.session.data['roles']).replace("L","")
          roles = roles.replace("[","(")
          roles = roles.replace("]",")")
          self.data['roles_list'] = roles
          self.execute('get_report_list_restrict',self.data,raw_mode = True)
        list_report = self.fetch('all')
        
        i = 0

        #Output
        for report in list_report:

            #Class of row
            if ((i % 2) == 0): css_class = "row1"
            else: css_class = "row2"

            #Absolute Row for the navigator of detail's page
            absolute_row = i + ((self.session.data['lines_per_page']) * (page - 1))

            self.html += html % (self.indent_size, css_class, str(report['id_report']), absolute_row,
                                 self.indent_size, report['type'],
                                 self.indent_size, report['description'],
                                 self.indent_size)
            i += 1

        #Security
        #If user does not have permission to create then don't show the "new" button	
        allow_create = self.g.get_area_permission(self.cookie_value, self.session, 'reports', 'allow_create')
        if self.g.isManager(self.session.data['roles']):
	  allow_create = 'y'
        if allow_create != 'y':
          import re
          self.page_parts['submenu'] = re.sub('<a id="action_new" href="[.]/%\(who\)s[.]new[.]py".*?/a>',"",self.page_parts['submenu'])          

        return self.html, self.get_foothtml(3, page, self.session.data['max_num_pages'], totalpages, '.' + environ['SCRIPT_NAME'][environ['SCRIPT_NAME'].rindex('/'):] + '?page=%s'), page, filter.decode('utf8')

    def get_foothtml(self, number_columns, current, max_numberpages, total, base_link):
        """Return html for the foot of the list"""

        if total == 1: #Don't show paging when there is only one page to look at
          return ''

        base_foot = '<tr>\
                       <td colspan="%(number_columns)s">\
                         <ul>\
                           %(li_html)s\
                         </ul>\
                       </td>\
                     </tr>'
        li_html = ''

        #Only numbers
        if total <= max_numberpages:
            for i in range(1, total + 1):
                if current == i:
                    li_html += '<li><a href="%(link_page)s" class="pageselected">%(page)s</a></li>' % {'link_page':base_link % i, 'page':i}
                else:
                    li_html += '<li><a href="%(link_page)s">%(page)s</a></li>' % {'link_page':base_link % i, 'page':i}
            return base_foot % {'number_columns':number_columns, 'li_html':li_html}
        #Numbers and special pages
        else:
            num_pages_left = ((max_numberpages-1)/2)
            num_pages_right = (max_numberpages/2)

            if ((current - num_pages_left) > 0) and ((current + num_pages_right < total)):
                if (current - num_pages_left != 1):
                    li_html += '<li class="specialpages"><a href="%s">&laquo;</a></li>' % base_link % 1
                for i in range(current - num_pages_left, current + num_pages_right + 1):
                    if current == i:
                        li_html += '<li><a href="%(link_page)s" class="pageselected">%(page)s</a></li>' % {'link_page':base_link % i, 'page':i}
                    else:
                        li_html += '<li><a href="%(link_page)s">%(page)s</a></li>' % {'link_page':base_link % i, 'page':i}
                li_html += '<li class="specialpages"><a href="%s">&raquo;</a></li>' % base_link % total
                return base_foot % {'number_columns':number_columns, 'li_html':li_html}
            elif ((current - num_pages_left) > 0) and ((current + num_pages_right >= total)):
                li_html += '<li class="specialpages"><a href="%s">&laquo;</a></li>' % base_link % 1
                for i in range(current - num_pages_left, total + 1):
                    if current == i:
                        li_html += '<li><a href="%(link_page)s" class="pageselected">%(page)s</a></li>' % {'link_page':base_link % i, 'page':i}
                    else:
                        li_html += '<li><a href="%(link_page)s">%(page)s</a></li>' % {'link_page':base_link % i, 'page':i}
                #li_html += '<li class="specialpages"><a href="%s">&raquo;</a></li>' % base_link % total
                return base_foot % {'number_columns':number_columns, 'li_html':li_html}
            #Per page, fill numbers and insert special pages
            elif current <= max_numberpages:
                #li_html += '<li class="specialpages"><a href="%s">&laquo;</a></li>' % base_link % 1
                for i in range(1, max_numberpages + 1):
                    if current == i:
                        li_html += '<li><a href="%(link_page)s" class="pageselected">%(page)s</a></li>' % {'link_page':base_link % i, 'page':i}
                    else:
                        li_html += '<li><a href="%(link_page)s">%(page)s</a></li>' % {'link_page':base_link % i, 'page':i}
                #li_html += '<li class="specialpages"><a href="%s">&hellip;</a></li>' % base_link % (max_numberpages + 1)
                li_html += '<li class="specialpages"><a href="%s">&raquo;</a></li>' % base_link % total
                return base_foot % {'number_columns':number_columns, 'li_html':li_html}
#            else:
#                #first_page_group = ((((current - 1) / max_numberpages) + 1) * max_numberpages) - max_numberpages + 1
#                #last_page_group = ((((current - 1) / max_numberpages) + 1) * max_numberpages)
#                first_page_group = current - ((max_numberpages-1)/2)
#                last_page_group = current + (max_numberpages/2)
#
#                #If is last group, hide others links next group
#                if total < last_page_group:
#                    last_page_group -= last_page_group - total
#
#                li_html += '<li class="specialpages"><a href="%s">&laquo;</a></li>' % base_link % 1
#                #li_html += '<li class="specialpages"><a href="%s">&hellip;</a></li>' % base_link % (first_page_group - 1)
#                for i in range(first_page_group, last_page_group + 1):
#                    if current == i:
#                        li_html += '<li><a href="%(link_page)s" class="pageselected">%(page)s</a></li>' % {'link_page':base_link % i, 'page':i}
#                    else:
#                        li_html += '<li><a href="%(link_page)s">%(page)s</a></li>' % {'link_page':base_link % i, 'page':i}
#                #If is not last group, show next group
#                if total > last_page_group:
#                    pass
#                    #li_html += '<li class="specialpages"><a href="%s">&hellip;</a></li>' % base_link % (last_page_group + 1)
#                li_html += '<li class="specialpages"><a href="%s">&raquo;</a></li>' % base_link % total
#                return base_foot % {'number_columns':number_columns, 'li_html':li_html}

    def ins_people_cmp(self, x, y):
        """Special order for people"""

        if x['institution'] > y['institution']:
            return 1
        if x['institution'] == y['institution']:
            return 0
        if x['institution'] < y['institution']:
            return -1

    def preserv_strain_cmp(self, x, y):
        """Special order for preservation"""

        if x['strain'] > y['strain']:
            return 1
        if x['strain'] == y['strain']:
            return 0
        if x['strain'] < y['strain']:
            return -1

    def code_strains_cmp(self, x, y):
        """Special order for strains"""

        a = x['code'].rjust(30, '0')
        b = y['code'].rjust(30, '0')

        if a > b:
            return 1
        if a == b:
            return 0
        if a < b:
            return -1
        
    
    def stockmovement(self):
        html = '%s<tr class="%s" onclick="location=\'./stockmovement.detail.py?id=%s&row=%s\'">\
                  %s  <td class="date">%s</td>\
                  %s  <td class="description">%s</td>\
                  %s  <td class="preservation_method">%s</td>\
                  %s</tr>'

        #Verify field_order is changed
        if self.form.has_key('field_order'):
            self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'stockmovement', self.form['field_order'].value)

        #Get field and mode for order list
        field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'stockmovement')

        #Creating order image
        #Define if order is Asc, or Desc
        if mode == "ASC":
          self.img="<img class='order' src='"+self.img_path_up+"'/>"
        else:
          self.img="<img class='order' src='"+self.img_path_down+"'/>"

        #define what img in HTML must be changed
        self.order_img = "img_" + field

        #Define field_order with mode
        field = field + ' ' + mode
        self.data['field_order'] = field

        #Disable paging
        self.data['paging'] = ';'

        #Execute again for rows count
        self.execute('get_stock_movement_list', self.data, True)

        #Define totalpages
        totalpages = int(math.ceil(float(self.getrowscount())/self.session.data['lines_per_page']))

        #Verify page
        page = 1
        if self.form.has_key('page'):
            page = int(self.form['page'].value)
            if page <= 0: page = 1
            elif page > totalpages: page = totalpages

            #Save filter on session
            self.session.data['page_stock_movement'] = page
            self.session.save()
        elif (self.session.data.has_key('page_stock_movement')):            
            page = int(self.session.data['page_stock_movement'])

        #Enable paging
        if (totalpages > 1):
          self.data['paging'] = 'LIMIT ' + str((page - 1) * self.session.data['lines_per_page']) + ',' + str(self.session.data['lines_per_page']) + ';'

        #SELECT id_stock_movement, date, description, method
        self.execute('get_stock_movement_list', self.data, True)
        list_stock_movement = self.fetch('all')

        for line, stock_movement in enumerate(list_stock_movement):
            #Class of row
            if ((line % 2) == 0): css_class = "row1"
            else: css_class = "row2"

            #Absolute Row for the navigator of detail's page
            absolute_row = line + ((self.session.data['lines_per_page']) * (page - 1))

            #Output
            self.html += html % (self.indent_size, css_class, str(stock_movement['id_stock_movement']), absolute_row,
                                 self.indent_size, self.format_date('view',stock_movement['date']),
                                 self.indent_size, stock_movement['description'],
                                 self.indent_size, stock_movement['method'],
                                 self.indent_size)

        return self.html, self.get_foothtml(3, page, self.session.data['max_num_pages'], totalpages, '.' + environ['SCRIPT_NAME'][environ['SCRIPT_NAME'].rindex('/'):] + '?page=%s'), page, ""


    def container(self):
        html = '%s<tr class="%s" onclick="location=\'./container.detail.py?id=%s&row=%s\'">\
                  %s  <td class="abbreviation">%s</td>\
                  %s  <td class="description">%s</td>\
                  %s  <td class="preservation_method">%s</td>\
                  %s</tr>'

        #Verify field_order is changed
        if self.form.has_key('field_order'):
            self.g.saveListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'container', self.form['field_order'].value)

        #Get field and mode for order list
        field, mode = self.g.getListOrder(self.session.data['id_user'], self.session.data['id_subcoll'], 'container')

        #Creating order image
        #Define if order is Asc, or Desc
        if mode == "ASC":
          self.img="<img class='order' src='"+self.img_path_up+"'/>"
        else:
          self.img="<img class='order' src='"+self.img_path_down+"'/>"

        #define what img in HTML must be changed
        self.order_img = "img_" + field

        #Define field_order with mode
        field = field + ' ' + mode
        self.data['field_order'] = field

        #Disable paging
        self.data['paging'] = ';'

        #Execute again for rows count
        self.execute('get_container_list', self.data, True)

        #Define totalpages
        totalpages = int(math.ceil(float(self.getrowscount())/self.session.data['lines_per_page']))

        #Verify page
        page = 1
        if self.form.has_key('page'):
            page = int(self.form['page'].value)
            if page <= 0: page = 1
            elif page > totalpages: page = totalpages

            #Save filter on session
            self.session.data['page_container'] = page
            self.session.save()
        elif (self.session.data.has_key('page_container')):            
            page = int(self.session.data['page_container'])

        #Enable paging
        if (totalpages > 1):
          self.data['paging'] = 'LIMIT ' + str((page - 1) * self.session.data['lines_per_page']) + ',' + str(self.session.data['lines_per_page']) + ';'

        self.execute('get_container_list', self.data, True)
        list_container = self.fetch('all')

        for line, container in enumerate(list_container):

            self.data['id_container'] = container['id_container']
            self.execute('get_container_preservation_methods', self.data, True)

            preservation_methods = []
            list_methods = self.fetch('all')
            for method in list_methods:
                preservation_methods.append(method['method'])

            #Class of row
            if ((line % 2) == 0): css_class = "row1"
            else: css_class = "row2"

            #Absolute Row for the navigator of detail's page
            absolute_row = line + ((self.session.data['lines_per_page']) * (page - 1))

            #Output
            self.html += html % (self.indent_size, css_class, str(container['id_container']), absolute_row,
                                 self.indent_size, container['abbreviation'],
                                 self.indent_size, container['description'],
                                 self.indent_size, ', '.join(preservation_methods),
                                 self.indent_size)

        return self.html, self.get_foothtml(3, page, self.session.data['max_num_pages'], totalpages, '.' + environ['SCRIPT_NAME'][environ['SCRIPT_NAME'].rindex('/'):] + '?page=%s'), page, ""
