#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

from .session import Session
from .cookie import Cookie
from .general import General
from .dbconnection import dbConnection
from .loghelper import Logging
from .json import JsonBuilder

# Import translation function
try:
    from .i18n import I18n
    # Create a temporary instance to initialize the global _
    _temp_i18n = I18n()
    from builtins import _
except (ImportError, AttributeError):
    # Fallback if translation is not available
    def _(text):
        return text

class SciNameBuilder(object):
    g = General()

    def __init__(self, cookie_value, dbconnection = None):
        #Cookies
        self.cookie_value = cookie_value
        
        #Logging
        self.logger = Logging.getLogger("sciname")

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

    def check_existing(self, hi_tax, sciname,id_subcoll, id_sciname=None):
        if not hi_tax:
            hi_tax = ''
        
        if id_sciname is not None:
            id_sciname = str(id_sciname)
        
        # Escapar caracteres especiais e garantir que os valores sejam strings válidas
        if sciname is None:
            sciname = ''
        if hi_tax is None:
            hi_tax = ''
            
        # Limpar e validar os dados de entrada
        sciname = str(sciname).strip()
        hi_tax = str(hi_tax).strip()
        
        # Criar o valor composto de forma segura
        compound_value = '%s|%s' % (hi_tax, sciname)
        sciname_data = {'compound_hitax_sciname': compound_value, 'id_subcoll':id_subcoll, 'id_sciname':id_sciname }
        
        self.logger.debug("Checking for existing sciname with compound value: %s" % compound_value)
        
        try:
            self.execute('check_sciname', sciname_data)
            result = self.fetch('one')
            current_id_sciname = str(result) if result is not None else None
            self.logger.debug("current id: %s" % (current_id_sciname))
            
            self.logger.debug("sciname_data leo: %s" % (sciname_data))

        except Exception as e:
            self.logger.error("Error in check_existing: %s" % str(e))
            self.logger.error("compound_value: %s" % compound_value)
            return False
        
        # if nothing was returned from the database, there isn't such sciname
        if not current_id_sciname or current_id_sciname == 'None':
            self.logger.debug("not found - False")
            return False
        
        # if a specific id was passed, it only "exists" if it's another sciname
        # or in other words, if the id of the existing item is different from the
        # one we are probably updating
        if id_sciname is not None:
            self.logger.debug("found: %s <> %s = %s" % (id_sciname, current_id_sciname, id_sciname != current_id_sciname))
            return id_sciname != current_id_sciname
        
        # if id_sciname was not passed and there is such a sciname on the datbase,
        # we consider it exists 
        self.logger.debug("found: True")
        return True         
        
    def update(self, id_subcoll, id_lang, id_sciname, form):
        hi_tax = form.getvalue('higher_taxa_html') or ''
        sciname = form.getvalue('sciname_html') or ''
        if self.check_existing(hi_tax, sciname, id_subcoll, id_sciname):
            from . import exception
            raise exception.SicolException (_("Another taxa with that Higher Taxa and Scientific Name combination already exists."))

        sciname_data = { 
            'id_sciname': id_sciname, 
            'hi_tax': hi_tax, 
            'sciname': sciname, 
            'sciname_no_auth': form.getvalue('sciname_no_auth') or ''
        }
        self.execute('update_sciname', sciname_data)
        
        self.execute('delete_sciname_hierarchy', {'id_sciname': id_sciname})
        self.insert_hierarchy(id_subcoll, id_lang, id_sciname, form)
        
    def insert(self, id_subcoll, id_lang, form):
        hi_tax = form.getvalue('higher_taxa_html') or ''
        sciname = form.getvalue('sciname_html') or ''
        if self.check_existing(hi_tax, sciname, id_subcoll, 0):
            from . import exception
            raise exception.SicolException (_("Another taxa with that Higher Taxa and Scientific Name combination already exists."))

        self.logger.debug('form: %s' % (str(form)))

        #isolates id_taxon_group
        id_taxon_group = form.getvalue('taxon_group')
        self.logger.debug('id_taxon_group: %s' % (id_taxon_group))

        #creates the sciname record
        sciname_data = { 
            'hi_tax': form.getvalue('higher_taxa_html') or '', 
            'sciname': form.getvalue('sciname_html') or '', 
            'sciname_no_auth': form.getvalue('sciname_no_auth') or ''
        }
        self.logger.debug('sciname_data: %s' % (str(sciname_data)))
        
        self.execute('insert_sciname', sciname_data)
        self.execute('last_insert_id')
        id_sciname = self.fetch('one')
        self.logger.debug('id_sciname: %s' % (str(id_sciname)))
        
        self.insert_hierarchy(id_subcoll, id_lang, id_sciname, form)
            
        return id_sciname
    
    def insert_hierarchy(self, id_subcoll, id_lang, id_sciname, form):
        #retrieves all scientific name fields for this subcoll and language
        id_taxon_group = form.getvalue('taxon_group')
        rows = self.getfields(id_subcoll, id_lang, id_taxon_group)
        for row in rows:
            row['type_prefix'] = ('sci', 'hi')[row['hi_tax']]
            key_value = '%(type_prefix)s_value_%(id_taxon_group)s_%(seq)s' % row
            key_author = '%(type_prefix)s_author_%(id_taxon_group)s_%(seq)s' % row
            key_hierarchy = '%(type_prefix)s_hierarchy_%(id_taxon_group)s_%(seq)s' % row
            self.logger.debug('keys: v:[%s] a:[%s] h:[%s]' % (key_value, key_author, key_hierarchy))
            
            value = form.getvalue(key_value)
            author = form.getvalue(key_author)
            id_hierarchy = form.getvalue(key_hierarchy)
            self.logger.debug('values: v:[%s] a:[%s] h:[%s]' % (value, author, id_hierarchy))

            if value:
                sciname_detail_data = { 
                    'id_sciname': id_sciname, 
                    'id_hierarchy': id_hierarchy,
                    'value' : value,
                    'author' : author
                }
                
                self.execute('insert_sciname_hierarchy', sciname_detail_data)
        
    def html(self, id_subcoll, id_lang, id_sciname, id_taxon_group = None, sciname_hierarchy = None):
        from .labels import label_dict
        dict = {}
        
        #retrieves all scientific name fields for this subcoll and language
        rows = self.getfields(id_subcoll, id_lang)

        #this is the template of items for one taxon group
        html_template = '''
                <div id='sciname_builder_%(id_taxon_group)s' class='%(css_class)s'>
                <p>
                <table>
                    <tbody>
                    <tr>
                        <td>
                            <fieldset>
                                <legend>%%(label_Species_General_Higher_Taxa)s</legend>
                                <p><table>%(higher_taxa)s</table></p>
                            </fieldset>
                        </td>
                        <td>
                            <fieldset>
                                <legend>%%(label_Species_General_Scientific_Name)s</legend>
                                <p><table>%(sciname)s</table></p>
                            </fieldset>
                        </td>
                    </tr>
                    </tbody>
                </table>
                </p>
                </div>'''
            
        #this is the template for each field, the author is optional
        html_detail = '''
            <tr>
                <td><p><label id="label_%(type_prefix)s_value_%(id_taxon_group)s_%(seq)s">%(rank)s</label></p></td>
                <td>
                    <input name='%(type_prefix)s_value_%(id_taxon_group)s_%(seq)s' id='%(type_prefix)s_value_%(id_taxon_group)s_%(seq)s' class='sci_name' value='%(value)s' %(onblur)s onchange='applySciName();'>
                    <input type='hidden' name='%(type_prefix)s_hierarchy_%(id_taxon_group)s_%(seq)s' value='%(id_hierarchy)s'> 
                </td>
                %(author_html)s
            </tr>'''
        
        #when field has author, this template is added to the field template
        html_author_detail = '''
             <td><p><label if="label_%(type_prefix)s_author_%(id_taxon_group)s_%(seq)s">%(label_Species_General_Author)s</label></p></td>
            <td><input name='%(type_prefix)s_author_%(id_taxon_group)s_%(seq)s' id='%(type_prefix)s_author_%(id_taxon_group)s_%(seq)s' class='sci_author' value='%(author)s' onchange='applySciName();'></td>'''
                

        #complete html holder
        html_body = []
        #holds the json variable that will represent all fields
        js_data = {}
        
        #helper html chunks
        hitax_html = []
        sciname_html = []
        
        #holds the current taxon group for level breaking (below)
        current_taxon_group = None
        
        #previous row
        prev_row = {}
        
        #for each field found on the database
        for row in rows:
            
            # check if new taxon_group
            if not current_taxon_group or current_taxon_group != row['id_taxon_group']:
                self.add_sciname_block(dict, html_template, html_body, hitax_html, sciname_html, current_taxon_group, prev_row, id_taxon_group)

                # reset variables
                hitax_html = []
                sciname_html = []
                current_taxon_group = row['id_taxon_group']

            
            #prefixes differ for high_taxa and sciname for handling correctly on client-side
            row['type_prefix'] = ['sci', 'hi'][row['hi_tax']]
            
            #if sciname_hierarchy was passed, we fill the fields with saved values
            id_hierarchy = row['id_hierarchy']
            if sciname_hierarchy and id_taxon_group and id_hierarchy in sciname_hierarchy and current_taxon_group == id_taxon_group:
                this_dict = sciname_hierarchy[id_hierarchy] 
                row['value'] = this_dict['value']
                row['author'] = this_dict['author']
            else: 
                row['value'] = '' 
                row['author'] = ''

            #helper dict of attributes to be added to the field
            helper_dict = row.copy()
            helper_dict['author_html'] = ''
            
            if (row['required'] == 1):
                helper_dict['onblur'] = "onblur='isEmpty(this, null);'"               
                helper_dict['rank'] += ' *'
            else:
                helper_dict['onblur'] = ""               
            
            #adds author_html to the field html
            if (row['has_author'] == 1):
                complete_dict = helper_dict.copy()
                complete_dict.update(label_dict)
                helper_dict['author_html'] = html_author_detail % complete_dict  
                
            #appends on the correct html chunk
            if row['hi_tax'] == 1:
                #higher taxa fieldset group
                hitax_html.append(html_detail % helper_dict)
            else:
                #scientific name fieldset group
                sciname_html.append(html_detail % helper_dict)

            #variables for being used as key on js_data dict
            taxon_group = row['id_taxon_group']
            seq = row['seq']
            
            #if the dict doesn't have this taxon_group yet, add it
            if taxon_group not in js_data:
                js_data[taxon_group] = {}
                
            #if the dict doesn't have this seq on this taxon_group yet, add it
            if seq not in js_data[taxon_group]:
                js_data[taxon_group][seq] = {}
                
            #add the field to the correct taxon_group and seq
            js_data[taxon_group][seq] = row
            
            #saves previous row for filling the template correctly
            prev_row = row.copy()

        #last iteration of the loop
        self.add_sciname_block(dict, html_template, html_body, hitax_html, sciname_html, current_taxon_group, row, id_taxon_group)

        #creates a json variable from the dictionary
        js = JsonBuilder.createJson(js_data)
        
        #assembles final HTML block to be rendered 
        html = "\n".join(html_body) % label_dict

        #transfer the javascript and the html to the html template file
        if isinstance(js, bytes):
            js = js.decode('utf-8')
        if isinstance(html, bytes):
            html = html.decode('utf-8')

        # Garantir que o template seja string
        template_content = self.g.read_html('sciname.form')
        if isinstance(template_content, bytes):
            template_content = template_content.decode('utf-8')

        template = template_content % { 
            'sciname_builder_js': js, 
            'sciname_builder_html': html 
        }
        
        #and returns it
        return template

    def getfields(self, id_subcoll, id_lang, id_taxon_group = None):
        #sciname data
        data = { 'id_subcoll': id_subcoll, 'id_lang': id_lang, 'taxon_group': ' ' }

        if id_taxon_group:
            data['taxon_group'] = 'AND id_taxon_group=%s' % (id_taxon_group)
            
        #retrieves all scientific name fields for this subcoll and language
        self.execute('get_sciname_builder_fields', data, raw_mode=True)
        return self.fetch('all')

    def add_sciname_block(self, dict, html_template, html_body, hitax_html, sciname_html, current_taxon_group, field, id_taxon_group = None):
        if current_taxon_group:
            #when loading the page, if has loaded data, we'll display the sciname builder 
            #for that taxon group by default
            dict['css_class'] = 'sciname_builder'
            if id_taxon_group and id_taxon_group == current_taxon_group:
                dict['css_class'] = 'sciname_builder_current'

            dict['id_taxon_group'] = field['id_taxon_group']
            dict['higher_taxa'] = "\n".join(hitax_html)
            dict['sciname'] = "\n".join(sciname_html)
            self.logger.debug("Append [%s]\n<= [%s]" % (html_template, dict))
            html_body.append(html_template % dict)
