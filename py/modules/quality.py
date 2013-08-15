#!/usr/bin/env python 
#-*- coding: utf-8 -*-

from session import Session
from general import General
from dbconnection import dbConnection
from getdata import Getdata
from textlinkfactory import TextLinkFactory
from location import LocationHelper
from loghelper import Logging
import re

class Quality(object):
    
    g = General()
    session = None

    def __init__(self, action, cookie_value='',form=None):
        if '.' in action:
            self.action = action.split('.')[-1]
        else:
            self.action = action
            
        self.cookie_value = cookie_value
        #Define Logging
        self.logger = Logging.getLogger("page_mount")
        self.d = self.logger.debug

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

        self.data_lang = self.session.data['data_langs'][0].values()[0]

        #Load GetData class
        self.getdata = Getdata(self.cookie_value, self.form)
        
    def loadQualities(self, data):
        if (self.form.has_key('id')):
            
            type = str(self.form['type'].value)
            
            quality_table = ["<body>"]
            
            quality_table.append("\n\t<table id='quality_table' class='data' cellspacing='0' cellpadding='0'>")
            
            if (type != 'detail'):
                quality_table.append("\n\t<tr>\n\t<td class='quality_cell'><a class='quality_link' href='strains.quality.new.py?id_strain=%s' target='_self'><img src='../img/record_add.png' title='%s' alt='%s'></a></td>\n\t<td class='quality_cell'></td></tr>" % (str(self.form['id'].value), _("New"), _("New")))
            
            self.db.execute('get_str_quality_data',{'id_strain':str(self.form['id'].value), 'id_lang':self.session.data['id_lang']})
            qualities = self.db.fetch('all')
            
            if len(qualities) > 0: 
                for quality in qualities:
                    
                    number_of_removed = _("Number of Used %s") % quality['unit_measure']
                    if int(quality['quantity']) == 0:
                        quality['quantity'] = '-'
                    
                    quality_row = []
                    quality_list = []
                    
                    user = self.getQualityUser(str(quality['id_user']))
                    
                    quality_row.append("\n\t<tr>\n\t<td class='quality_cell'><label>%s:</label> %s %s</td>\n\t<td class='quality_cell' valign='bottom'>%s</td>\n</tr>")
                    
                    quality_list.append("\n<ul>")
                    quality_list.append("\n\t<li><label>%s:</label> %s </li>" % (_("Responsible technician"), user))
                    quality_list.append("\n\t<li><label>%s:</label> %s [<label>%s:</label> %s]</li>" % (number_of_removed, str(quality['quantity']), _("Lot"), quality['lot']))
                    quality_list.append("<br/>")
                    
                    data['id'] = quality['id_quality']
                    self.logger.debug('data: %s', data)
                    if quality['not_identified'] == 1:
                        quality_list.append(self.renderLocation(data, not_identified=True))
                    else:
                        quality_list.append(self.renderLocation(data))
                    
                    quality_list.append("\n</ul>")
                    
                    quality_list.append(self.getQualityTests(quality['id_quality']))
                    
                    links = ""
                    if (type != 'detail'):
                        links = "<a class='quality_link' href='strains.quality.edit.py?id_strain=%s&id_quality=%s' target='_self'><img src='../img/record_edit.png' title='%s' alt='%s'></a>" % (str(self.form['id'].value), str(quality['id_quality']), _("EDIT"), _("EDIT"))
                        
                        #Security
                        #If user does not have permission to delete then don't show the "delete" button
                        allow_delete = self.g.get_area_permission(self.cookie_value, self.session, 'strains', 'allow_delete')
                        if self.g.isManager(self.session.data['roles']): #Administrator or Manager
                          allow_delete = 'y'
                        if allow_delete == 'y':
                            links += "&nbsp;&nbsp;<a class='quality_link' onclick='javascript: if(confirm(\"%s\")) deleteQuality(\"%s\",\"%s\");' target='_self'><img src='../img/record_delete.png' title='%s' alt='%s'></a>" % (_("Do you really want to delete this item?"), str(self.form['id'].value), str(quality['id_quality']), _("DELETE"), _("DELETE"))
                    
                    quality_row = "".join(quality_row)
                    quality_row = quality_row % (_("Date"), self.getdata.format_date('view', quality['date']), "".join(quality_list), links)
                    quality_table.append(quality_row)
            elif type == 'detail':
                quality_table.append("<tr><td><center>%s</center></td></tr>"  % _("There are no quality tests for this strain."))
                
            quality_table.append("\n</table>")
            quality_table.append("\n</body>")
            quality_table.append("\n<script type='text/javascript'>addEvent(window, 'load', resizeIframe);</script>")
            quality_table.append("\n<script type='text/javascript'>addEvent(window, 'load', enableLinks);</script>")
            quality_table.append("\n</html>")
            data['quality_table'] = quality_table = "".join(quality_table)
            
    def getQualityUser(self, id_user):
        self.db.execute('get_one_person',{'id':id_user})
        return self.db.fetch('one')
    
    def getQualityTests(self, id_quality):
        
        self.db.execute('get_str_quality_tests',{'id_lang':self.session.data['id_lang'],'id_quality':id_quality})
        tests = self.db.fetch('all')
        
        test_list = []
        
        for test in tests:
            textLinksStrain = TextLinkFactory(self.cookie_value, self.session.data['id_lang'], self.data_lang)
            textLinksStrain.update({
                'result'   : test['result'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"")
            })
            textLinksStrain.update({
                'comments'   : test['comments'].replace("%","%%").replace("&#160;", " ").replace("<a","<a class=\"tlink\"")
            })
            #changes textlink to html link
            textLinksStrain.fillData(test)
            
            #Purity
            if test['purity'] == 'y':
                test['purity'] = _("Ok")
            else:
                test['purity'] = "<b class='red_info'>" + _("Contaminated") + "</b>"
            #Counting
            if test['counting_not_apply'] == 'y':
                test['does_counting_apply'] = ' ('+_("Does not apply")+')'
            elif test['counting_not_apply'] == 'n':
                test['does_counting_apply'] = ''
            
            ufc_ml = ""            
            if (self.g.ConvertStrUnicode(test["counting"]) != ""):
                ufc_ml = "UFC/ml"
                
            #Changes counting notation
            regexp = r'(?P<bdot>\d+)(\.(?P<adot>\d*))+E(?P<exp>\d+)'
            repl = r'\g<bdot>,\g<adot>x10<sup>\g<exp></sup>'
            repl_adot_fail = r'\g<bdot>,0x10<sup>\g<exp></sup>'
            
            adot_test = re.match(regexp, self.g.ConvertStrUnicode(test["counting"]))
            if adot_test:
                if (len(adot_test.group('adot'))):
                    test["counting"] = adot_test.expand(repl)
                else:
                    test["counting"] = adot_test.expand(repl_adot_fail)
            
            test_list.append("<ul>")
            test_list.append(("<li><label>%s:</label> %s </li>" % (_("Used Test"), test['title'])))
            test_list.append(("<li><label>%s:</label> %s </li>" % (_("Purity"), test['purity'])))
            test_list.append(("<li><label>%s:</label> %s %s</li>" % (_("Counting"), test["counting"].replace("'","\\'") + " " + ufc_ml, test['does_counting_apply'])))
            test_list.append(("<li><label>%s:</label> %s </li>" % (_("Result"), test['result'])))
            test_list.append(("<li><label>%s:</label> %s </li>" % (_("Observations"), test['comments'])))
            test_list.append("</ul>")
        
        return "".join(test_list)

    def renderLocation(self, data, not_identified=False):
        self.logger.debug('action: %s' % self.action)
        from location import LocationHelper
        location_helper = LocationHelper(
            action=self.action,
            model='quality', 
            data=data,
            cookie_value=self.cookie_value,
            decrease_stock_optional=True,
            quantity_field='num_amp',
        )
        
        return location_helper.renderTag(not_identified)
    
    def loadItems(self, data):
        data['tec_resp'] = self.loadPossibleResponsibles(data['quality_id_person'])
        data['id_coll'] = self.session.data['id_coll']
        data['id_subcoll'] = self.session.data['id_subcoll']

        data['id'] = data['id_quality']
        if data['not_identified'] == 1:
            data['location'] = self.renderLocation(data, not_identified=True)
        else:
            data['location'] = self.renderLocation(data)
        
        #Create Global Javascript Variable to control ampoules stock within each lot-strain combination
        previously_used_amp = {}
        #Update info about previously used ampoules for this lot-strain combination
        try:
            previously_used_amp[int(data['id_strain'])][data['quality_id_lot']] = {'used':data["num_amp"],'prepared':0}
        except:
            previously_used_amp[int(data['id_strain'])] = {}
        previously_used_amp[int(data['id_strain'])][data['quality_id_lot']] = {'used':data["num_amp"],'prepared':0}
        
        data['js_global_lot_strain'] = self.getdata.get_lot_strain_ampoules(int(data['id_strain']), previously_used_amp=previously_used_amp,selected_id_lot=data['quality_id_lot'])
        data['quality_tests'] = self.loadPossibleTests()
        
    def loadQuality(self, data):
        self.db.execute('get_str_quality', {'id_quality':data['id_quality'], 'id_lang':self.session.data['id_lang']})
        quality = self.db.fetch('columns')
        data['date'] = self.getdata.format_date('view', quality['date'])
        data['quality_id_person'] = quality['id_user']
        data['num_amp'] = quality['quantity']
        data['quality_id_lot'] = quality['id_lot']
        data['not_identified'] = quality['not_identified']
        
        data['js_quality_data'] = 'quality_data = ["%s","%s"];' % (quality['id_lot'],
                                                                        quality['lot_name'])
        
        #Get purity state
        data['purity'] = self.renderPurity()
        
        #Get GLOBAL COUNTER
        self.db.execute('get_str_quality_tests_count',{'id_quality': data['id_quality']})
        global_counter = int(self.db.fetch('one')) + 1
        
        #Start-up Javascript
        data['js_data'] = []
        
        #Get Data for each Test
        self.db.execute('get_str_quality_tests', {'id_lang':self.session.data['id_lang'],'id_quality':data['id_quality']})
        quality_tests = self.db.fetch('all')
        
        for i in xrange(1,global_counter):
            j = i - 1 #index for manipulation of "quality_tests" dictionary
            aux_dict = quality_tests[j]
            
            all_info = []
            aux_data = ''
            
            aux_data += '\ttest_info[%s] = {' % i
            all_info.append("'id_test':'"+str(aux_dict["id_doc"])+"'")
            all_info.append("'purity':'"+aux_dict["purity"]+"'")
            all_info.append("'counting':'"+aux_dict["counting"].replace("'","\\'")+"'")
            all_info.append("'counting_not_apply':'"+aux_dict["counting_not_apply"]+"'")
            all_info.append("'result':'"+aux_dict["result"]+"'")
            all_info.append("'comments':'"+aux_dict["comments"]+"'")
            
            aux_data += ",".join(all_info)
            aux_data += '};'
            data['js_data'].append(aux_data)
        
        data['js_data'] = "\n".join(data['js_data'])
        return data
            
    def loadPossibleResponsibles(self, id_person):
        responsibles = ['\n\t<option value=''></option>']
        self.db.execute('get_person')
        people = self.db.fetch('all')
        for person in people:
            if person['id_person'] == id_person:
                responsibles.append('\n\t<option %s value="%s">%s</option>' % ('selected="selected"', person['id_person'], person['name']))
            else:
                responsibles.append('\n\t<option value="%s">%s</option>' % (person['id_person'], person['name']))
        return "".join(responsibles)
    
    def loadStrainLots(self, id_lot):
        strain_lots = ['\n\t<option value=''></option>']
        self.db.execute('get_strain_lots', {'id_strain':str(self.form['id_strain'].value), 'id_lang':self.session.data['id_lang']})
        lots = self.db.fetch('all')
        for lot in lots:
            if lot['id_lot'] == id_lot:
                strain_lots.append('\n\t<option %s value="%s" unit="%s">%s</option>' % ('selected="selected"', lot['id_lot'], lot['unit_measure'], lot['name']))
            else:
                strain_lots.append('\n\t<option value="%s" unit="%s">%s</option>' % (lot['id_lot'], lot['unit_measure'], lot['name']))
        return "".join(strain_lots)
    
    def loadPossibleTests(self):
        possible_tests = ['\n\t<option value=''></option>']
        self.db.execute('get_doc_by_qualifier', {'id_lang':self.session.data['id_lang'], 'id_coll': self.session.data['id_coll'], 'id_qualifier':5})
        tests = self.db.fetch('all')
        for test in tests:
            possible_tests.append('\n\t<option value="%s">%s</option>' % (test['id_doc'], test['title']))  
        return "".join(possible_tests)
    
    def renderPurity(self):
        #Get purity state
        output = '<select name="purity" id="purity" class="select_25">'
        output += '<option value="ok" selected="selected" >%s</option>' % _("OK")
        output += '<option value="contaminated">%s</option>' % _("Contaminated")
        output += '</select>'     
        return output
    
    def hasItemPermission(self, id_strain):
        allow = self.g.get_item_permission(self.cookie_value, self.session, 'strains', id_strain)
        if self.g.isManager(self.session.data['roles']): #Administrator or Manager
            allow = 'w'
        return allow == 'w'
    
    def hasAreaPermission(self, action):
        allow = self.g.get_area_permission(self.cookie_value, self.session, 'strains', action)
        if self.g.isManager(self.session.data['roles']): #Administrator or Manager
            allow = 'y'
        return allow == 'y'
            
