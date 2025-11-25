#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from sys import exit,platform
from os import path
#from dbgp.client import brk

if platform == "win32": #Windows reads upload/download as Text instead of Binary...
    import msvcrt
    from os import O_BINARY
    msvcrt.setmode(0, O_BINARY) #stdin
    msvcrt.setmode(1, O_BINARY) #stdout

import cgitb; cgitb.enable()
#python imports
from cgi import FieldStorage
from urllib.parse import urljoin

#project imports
from .i18n import I18n
from . import exception
from .session import Session
from .cookie import Cookie
from .general import General, DefDict
from .dbconnection import dbConnection
from .loghelper import Logging

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

class Principal(object):
    i18n = I18n()
    g = General()

    # Configs
    root_dir = g.root_dir
    index_url = g.get_config('index_url')
    if not index_url:  # Fallback se index_url estiver vazio
        index_url = 'http://localhost/'
    http_header = g.get_config('http_header')
    js_line = g.get_config('javascript_line')
    css_line = g.get_config('css_line')

    # HTML Parts
    html_header = g.read_html('header')
    html_main = g.read_html('main')
    html_footer = g.read_html('footer')

    index = urljoin(index_url, 'index.html')
    start_page = './' + g.get_config('start_page') + '.py'

    def __init__(self):
        '''
        Class Constructor
        '''

        # Define Logging
        self.logger = Logging.getLogger("page_mount")
        self.d = self.logger.debug

        # Define Cookie
        self.cookie = Cookie()
        self.cookie_value = self.cookie.read('Sicol_Session')

        # Set Language according to user preference
        self.i18n = I18n(cookie_value=self.cookie_value)
        from .labels import label_dict
        self.label_dict = label_dict

        # Define Sqlite Connection
        self.dbconnection = dbConnection()
        self.execute = self.dbconnection.execute
        self.cursor = self.dbconnection.cursor
        self.fetch = self.dbconnection.fetch

        # Define others global vars
        self.form = FieldStorage()
        self.session = Session()
        self.data = DefDict()
        self.data.update({
                     'js': '',
                     'css': '',
                     'cookie': '',
                     'start_page': self.start_page,
                     'who': '',
                     'feedback_value': 0,
                    })
        self.set_version()
        self.process_data = {}
        self.page_parts = {}

    def set_version(self):
        '''
        Check SICol version to show on page title
        '''
        work_dir = path.join(self.root_dir, 'v???')
        from glob import glob
        versions = glob(work_dir)
        if versions:
            v = versions[0]
            self.data['version'] = v[-3:-2] + '.' + v[-2:-1] + '.' + v[-1:]
        else:
            self.data['version'] = "desconhecida"

    def clear_session_data(self):
        init_info = ('id_user','login','id_coll','coll_name','id_subcoll',
                     'subcoll_code','db_host','db_port','db_name','db_user',
                     'db_pwd','dbms')
        for info in init_info:
            try:
                del self.session.data[info]
            except KeyError:
                pass
        self.session.save()

    def fetch_data_langs(self, subcoll_id):
        '''
        Fetch all data_langs from database and return them ordered according
        to user-defined index of "sys_data_lang" table in SQLite
        '''
        self.logger.debug('entrando')
        data_lang = [] # use list so we can ORDER a sequence of dictionaries
        # langs ordered by user-defined index where the first one is the user current lang
        # Presume that all indexes are correctly ordered (no gaps allowed)
        self.execute('get_subcoll_data_langs', {'id_subcoll': subcoll_id})
        subcoll_langs = self.fetch('rows')
        if subcoll_langs == []:  # Then get info from config.xml
            subcoll_langs = self.g.get_config('data_lang').split(",")
            # remove spaces
            i = 0
            for subcoll_lang in subcoll_langs:
                subcoll_langs[i] = subcoll_lang.replace(' ','')
                i += 1
            del i

        # import commands
        # self.logger.debug("Whoami: %s", commands.getstatusoutput('whoami'))

        # Get all langs id and code
        self.session.save()
        self.logger.debug('metade')
        db = dbConnection(self.cookie_value)
        self.logger.debug('metade depois')
        db.execute('get_lang_id_and_code')
        langs = db.fetch('all')
        langs_id = {}
        for lang in langs:
            langs_id[lang['code']] = lang['id_lang']
        for subcoll_lang in subcoll_langs:
            data_lang.append({subcoll_lang: langs_id[subcoll_lang]})

        self.logger.debug('saindo')
        return data_lang

    def set_session_vars(self, id_coll=None, id_subcoll=None):
        '''
        Load content inside Session Cookie
        '''
        self.session.load(self.cookie_value)
        id_user = self.session.data['id_user']

        # Collection and Subcollection info
        if not (id_coll and id_subcoll):
            self.logger.debug('Problem zone 1: %s %s' % (id_coll, id_subcoll))
            # Collection Data
            self.execute('get_coll_data',{'id_user':id_user})
            coll_data = self.fetch('columns')
            self.logger.debug('coll_data: %s' % str(coll_data))
            self.session.data['id_coll'] = coll_data['id_coll']
            self.session.data['coll_name'] = coll_data['coll_name']
            # Subcollection Data
            self.execute('get_subcoll_data', {'id_user': id_user})
            subcoll_data = self.fetch('columns')
            self.logger.debug('subcoll_data: %s' % str(subcoll_data))
            self.session.data['id_subcoll'] = subcoll_data['id_subcoll']
            self.session.data['subcoll_code'] = subcoll_data['subcoll_code']
            del coll_data, subcoll_data
        else:
            # Collection Data
            self.session.data['id_coll'] = id_coll
            self.execute('get_coll_name', {'id_coll': id_coll})
            self.session.data['coll_name'] = self.fetch('one', 'coll_name')
            # Subcollection Data
            self.session.data['id_subcoll'] = id_subcoll
            self.execute('get_subcoll_code', {'id_coll': id_coll, 'id_subcoll': id_subcoll})
            self.session.data['subcoll_code'] = self.fetch('one', 'subcoll_code')
            del id_coll, id_subcoll  # below use only session data

        try:
            # Database info
            self.execute('get_db_info', {'id_coll': self.session.data['id_coll']})
            db_info = self.fetch('columns')
            self.logger.debug('db_info: %s' % str(db_info))
            self.session.data['id_base'] = db_info['id_base']
            self.session.data['db_host'] = db_info['host']
            self.session.data['db_port'] = db_info['port']
            self.session.data['db_name'] = db_info['dbname']
            self.session.data['db_user'] = db_info['user']
            self.session.data['db_pwd'] = db_info['pwd']
            self.session.data['dbms'] = db_info['dbms']

            # Get Preferences
            self.d('user_pref')
            user_pref = {'label_lang': None}  # It needed because return null-string if no values
            self.execute('get_user_preferences', {'id_user': id_user})
            user_pref.update(self.fetch('columns'))

            self.d('subcoll_pref')
            subcoll_pref = {'date_input_mask': None, 'date_output_mask': None, 'label_lang': None} #It needed because return null-string if no values
            self.execute('get_subcoll_preferences', {'id_subcoll': self.session.data['id_subcoll']})
            subcoll_pref.update(self.fetch('columns'))
            self.session.data.update(subcoll_pref)

            self.d('before data_langs')
            self.logger.debug(self.session.data['id_subcoll'])
            self.session.data['data_langs'] = self.fetch_data_langs(self.session.data['id_subcoll'])
            self.d('after data_langs')

            # Set Label Language
            self.d('set label lang')
            id_lang, code_lang = self.get_id_lang(user_pref['label_lang'], subcoll_pref['label_lang'])
            self.session.data['id_lang'] = id_lang
            self.session.data['label_lang_code'] = code_lang

            # Get user roles - user must have at least 1 role, from group "user"
            db = dbConnection(self.cookie_value)
            db.execute('get_all_user_roles', {'id_user': id_user})
            self.session.data['roles'] = db.fetch('rows')  # List of roles. E.g.:[1L,2L,3L...]

            # Get user preference of how many lines are shown for each page (used in paging)
            from .getdata import Getdata
            self.session.data['lines_per_page'] = Getdata.user_lines_per_page(self.session.data['id_user'])
            self.session.data['max_num_pages'] = Getdata.user_max_num_pages(self.session.data['id_user'])
            self.session.data['show_str_inactives'] = Getdata.user_show_str_inactives(self.session.data['id_user'])

            # Load user preference of how to order list fields
            self.g.loadListOrder(self.session.data['id_user'], self.session.data['id_subcoll'])

            # Save set data
            self.logger.debug("Returning from setting vars...")
            self.session.save()
        except Exception as e:
            import traceback
            self.logger.error('Error logging user in: %s', traceback.format_exc(e))
            raise e

    def get_label_code(self):
        lang_code = None
        if ("label_lang_code" in self.session.data):
            lang_code = self.session.data['label_lang_code']
#        if (self.session.data.has_key("id_user")):
#            self.execute('get_user_label',{'id_user':self.session.data['id_user']})
#            lang_code = self.fetch('one')
        if not lang_code:
            lang_code = self.g.get_config('label_lang')
        return lang_code

    def get_id_lang(self, user_lang=None, subcoll_lang=None):
        # Language used must obey the following order: user config -> subcoll config -> server config
        if user_lang:
            lang_code = user_lang
        elif subcoll_lang:
            lang_code = subcoll_lang
        else:
            lang_code = self.g.get_config('label_lang')
            if (len(lang_code) < 2) or (len(lang_code) > 4) or (not lang_code):
                from .i18n import _
                out = self.g.get_config('http_header')
                out += '\n\n%s <b>label_lang</b> %s' % (_("Invalid"), _("entry in config.xml."))
                out += '\n<br />%s' % _('Check field "code" of table "lang" in main database.')
                login_check = self.g.read_html('login_check')
                if isinstance(login_check, bytes):
                    login_check = login_check.decode('utf-8')
                out += login_check % -5
                print(out)
                exit(1)
        # self.dbConnection always contain a reference to the first sqlite database only.
        self.session.save()
        self.i18n.set_lang(lang_code)
        db = dbConnection(self.cookie_value)
        db.execute('get_lang_by_code', {'code': lang_code})
        return db.fetch('one'), lang_code

    def user_related_error(self, ex_error, page, category, js, css):
        '''
        Treat here all user-related errors. Show a user-friendly message

        Usage:
        import sys
        ex_error = sys.exc_info()[1].args[0]
        if isinstance(ex_error, bytes):
            ex_error = ex_error.decode('utf-8')
        user_related_error(ex_error)
        '''
        from . import exception
        exception.clear_exceptions()
        if (ex_error == 'column login is not unique'):
            ex_error = _("Login already exists!")
            str_error = '<div class="user_error">%s</div>' % ex_error
            css = ('main', 'default', 'default.detail', 'form.save')
            self.header_includes(page, category, js, css)
            self.data['page'] = self.g.read_html('form.save')
            self.data['error_info'] = str_error
        elif (ex_error == "no_lots_available"):
            ex_error = _("There are currently no lots available for distribution!") + "<br />\n" + _("Please insert a lot in the Preservation screen.")
            str_error = '<div class="user_error">%s</div>' % ex_error
            css = ('main', 'default', 'default.detail', 'form.save')
            self.header_includes(page, category, (), css)
            self.data['page'] = self.g.read_html('form.save')
            self.data['error_info'] = str_error
        elif (ex_error == "no_inst_available"):
            ex_error = _("There are currently no institutions available in the system!") + "<br />\n" + _("Please insert an institution.")
            str_error = '<div class="user_error">%s</div>' % ex_error
            css = ('main', 'default', 'default.detail','form.save')
            self.header_includes(page, category, (), css)
            self.data['page'] = self.g.read_html('form.save')
            self.data['error_info'] = str_error
        elif (ex_error.startswith("REDIRECT:")):
            # Handle para redirecionamento após salvar
            redirect_url = ex_error[9:]  # Remove "REDIRECT:" prefix
            print(self.g.redirect(redirect_url))
            exit()
        elif (ex_error.find("Timeout") != -1):
            ex_error = _("Generation Timeout") + ": " + "%.1f " % float(ex_error.split(":")[1]) + " seconds." + "<br />\n" + _("Please change the fields in your report or change the 'report_timeout' parameter in the config.xml file.")
            str_error = '<div class="user_error">%s</div>' % ex_error
            css = ('main', 'default', 'default.detail', 'form.save')
            self.header_includes(page, category, (), css)
            self.data['page'] = self.g.read_html('report.error')
            self.data['error_info'] = str_error

    def mount(self, page, category, js, css):
        # brk(host="localhost", port=9000)
        self.logger.debug(f"Mounting page {page} category [{category}] js [{js}] css [{css}]")
        self.checkup(page, category)
        if (page == 'logout'):  # delete session
            self.html_footer = ''
            self.session.delete()
            self.session.del_expired_sessions()
            # Go straight back to login screen
            print((self.g.redirect(self.index)))
        try:
            self.content_includes(page, category)
            self.header_includes(page, category, js, css)
        except exception.SicolException:
            import sys
            exc = sys.exc_info()[1]
            msg = exc
            if isinstance(msg, bytes):
                msg = msg.decode('utf-8', errors='replace')
            else:
                msg = str(msg)

            # Check if this is a redirect (success case) vs actual error
            if str(msg).startswith("REDIRECT:"):
                self.logger.debug("[page: %s] %s" % (page, msg))
            else:
                self.logger.error("[page: %s] %s" % (page, msg))
            # Error messages in sicol exception
            # are presented to the user when the final html is displayed
            if "page" not in self.data:
                self.data["page"] = ""
                ex_error = sys.exc_info()[1].args[0]
                if isinstance(ex_error, bytes):
                    ex_error = ex_error.decode('utf-8')
                else:
                    ex_error = str(ex_error)
                # User related error - show differently from developer generated error
                self.user_related_error(ex_error, page, category, js, css)

        # join data for output
        self.data.update(self.session.data)
        self.data.update(self.process_data)
        self.data.update(self.label_dict)

        # Format page_parts and insert in data
        for key in self.page_parts:
            template = self.page_parts[key]
            if isinstance(template, bytes):
                template = template.decode('utf-8')  # decode bytes to str
            self.page_parts[key] = template % self.data  # regular str formatting
        self.data.update(self.page_parts)
        self.page_show(page)

    def checkup(self, page, category):
        # test cookie and session
        if not (self.cookie_value and self.session.isvalid(self.cookie_value)):
            if (page == 'tests'):
                self.session.create()  # automatic save session
                self.data['cookie'] = self.cookie.send(self.session.data['id'])
            else:
                # without permission, go to index.py
                if (page.find("strains.quality") == -1):  # iframe
                    print((self.g.redirect(self.index)))
        else:
            self.session.load(self.cookie_value)
            # empty session cache
            if (category not in ('main', 'external')) and (page != 'subcollections'):
                self.clear_session_data()

            # test access violation without login
            if (category == 'main') or (page == 'subcollections'):
                try:
                    self.session.data['id_user']
                    self.session.data['login']
                except KeyError:
                    print((self.g.redirect(self.index)))

            # test access violation without a chosen subcollection
            if (category == 'main'):
                try:
                    self.session.data['id_coll']
                    self.session.data['id_subcoll']
                except KeyError:
                    print((self.g.redirect(self.index)))

    def check_feedback(self):
        # check feedback parameter
        if 'feedback' in self.session.data and self.session.data['feedback']:
            self.data['feedback_value'] = self.session.data['feedback']
            self.session.data['feedback'] = 0
            self.session.save()
        else:
            self.data['feedback_value'] = 0

    def get_template(self, page, area, action):
        '''
        Get HTML template according to given parameters and user permissions:
        action = "save" | "del" | "form" | "new" | "detail" | (others)
        area = 'species' | 'strains' | 'people' | 'institutions' | 'doc' | 'ref' | 'preservation' | 'distribution' | 'report'
        page = page type
        '''
        html_page = ''
        if action in ('save', 'del'):
            if action == 'del':
                allow_delete = self.g.get_area_permission(self.cookie_value, self.session, area, 'allow_delete')
                if self.g.isManager(self.session.data['roles']):  # Administrator or Manager
                    allow_delete = 'y'
                if allow_delete != 'y':
                    html_page = self.g.read_html('access.denied')
                else:
                    html_page = self.g.read_html('form.save')
            else:
                html_page = self.g.read_html('form.save')
        elif action in ('form', 'new'):
            # Check whether user has permission to create new items
            if action == 'new':
                allow_create = self.g.get_area_permission(self.cookie_value, self.session, area, 'allow_create')
                if self.g.isManager(self.session.data['roles']):  # Administrator or Manager
                    allow_create = 'y'
                if allow_create != 'y':
                    html_page = self.g.read_html('access.denied')
                else:
                    html_page = self.g.read_html(area + '.form')
            else:  # action == 'form', when user is editing item
                allow_edit = self.g.get_item_permission(self.cookie_value, self.session, area, self.form.getvalue('id'))
                if self.g.isManager(self.session.data['roles']):  # Administrator or Manager
                    allow_edit = 'w'
                if allow_edit != 'w':
                    html_page = self.g.read_html('access.denied')
                else:
                    html_page = self.g.read_html(area + '.form')
        else:
            if action == 'detail':
                # Check whether user has permission to see item details of chosen area
                allow_detail = self.g.get_item_permission(self.cookie_value, self.session, area, self.form.getvalue('id'))
                if self.g.isManager(self.session.data['roles']):  # Administrator or Manager
                    allow_detail = 'w'
                if allow_detail == '':  # no permission
                    html_page = self.g.read_html('access.denied')
                else:  # read or write permission
                    html_page = self.g.read_html(page)
            else:
                html_page = self.g.read_html(page)
        return html_page

    def content_includes(self, page, category):
        # brk(host="localhost", port=9000)
        html_page = ''
        process_data = ''
        # 'others' category pages
        if (category == 'others'):
            if page != 'login_check':
                # for not 'main' category, html_main is the proper page file
                self.html_main = self.g.read_html(page)
                if (page == 'login'):
                    self.html_footer = ''
                    # Generate i18n javascript file, if needed
                    from modules.js_translator import JS_Translator
                    js_tr = JS_Translator(self.cookie_value, self.i18n)
                    if (js_tr.needsUpdate()): js_tr.doUpdate()
                # from modules.page_mount import Principal
            if (page == 'subcollections'):
                # list subcollections to choose from
                if not ('coll' in self.form and 'subcoll' in self.form):
                    from .subcollections import Subcollections
                    subcollections = Subcollections(self.cookie_value)
                    redirect, html_page = subcollections.list()
                    del subcollections

                    if 'logout' in self.form:
                        keys_to_delete = []
                        for key in self.session.data:
                            # we need to delete from session the filter and
                            # the page where the user were
                            if key.startswith('filter_') or key.startswith('page_'):
                                keys_to_delete.append(key)

                        if keys_to_delete:
                            for key in keys_to_delete:
                                del self.session.data[key]
                            self.session.save()

                    if redirect:
                        print((self.g.redirect('./logout.py')))
                # update session for chosen subcollection
                else:
                    self.set_session_vars(self.form.getvalue('coll'), self.form.getvalue('subcoll'))
                    # Generate i18n javascript file, if needed
                    from modules.js_translator import JS_Translator
                    js_tr = JS_Translator(self.cookie_value, self.i18n)
                    if (js_tr.needsUpdate()):
                        js_tr.doUpdate()
                    print((self.g.redirect(self.start_page)))
            elif (page == 'login_check'):

                self.html_main = ''
                self.html_header = ''
                self.html_footer = ''

                self.session.load(self.cookie_value)

                from .login import Login
                login = Login(self.form)
                test = login.test(self.cookie_value)

                self.logger.debug("Test: %s" % (test))

                if (test in (1, 2)):
                    login_data = self.form.getvalue('user')
                    self.session.data['login'] = login_data
                    self.execute('get_user_data', {'login': login_data})
                    user_data = self.fetch('columns')
                    self.logger.debug('user_data: %s' % (str(user_data)))
                    self.session.data['id_user'] = user_data['id_user']
                    self.session.data['user_name'] = user_data['user_name']
                    self.session.save()
                    self.set_session_vars()
                    del user_data

                # return script to login message
                self.html_main = self.g.read_html(page) % test
                self.logger.debug("Returning: %s" % (self.html_main))
                del login, test

        # 'main' category pages
        elif (category == 'main'):
            if page == 'download':
                from .download import Download
                page = Download(self.form)
                print((page.doc()))
                exit(0)
            elif page.split('.')[0] == 'reports' and page.split('.')[1] in ('show', 'edit', 'new'):
                from .reports import Reports
                action = page.split('.')[1]
                page = Reports(self.form, self.cookie_value)

                if action == 'show':
                    try:
                        if 'xml_dict' in self.form:
                            dict_final = page.safe_eval_dict(self.form['xml_dict'].value)
                            report_format = dict_final.get('format', '').lower()

                            if report_format in ('csv', 'xml'):
                                page.show()
                                exit(0)

                        output = page.show()
                        self.html_main = output
                    except Exception as err:
                        raise exception.SicolException(str(err))

                    self.html_header = ""
                    self.html_footer = ""

                elif action == 'new':
                    # Security
                    # If user cannot create a new strain, he also cannot create a new strain from a previous one.
                    allow_create = self.g.get_area_permission(self.cookie_value, self.session, 'reports', 'allow_create')
                    if self.g.isManager(self.session.data['roles']):  # Administrator or Manager
                        allow_create = 'y'
                    if allow_create != 'y':
                        self.data['page'] = self.g.read_html('access.denied')
                        self.page_parts['submenu'] = ""
                    else:
                        dict = {}
                        dict = page.new()
                        self.process_data = dict['data']
                        self.data['page'] = self.g.read_html(dict['screen_name'])
                        self.page_parts['submenu'] = self.g.read_html('submenu.form')

                elif action == 'edit':
                    if ('id' in self.form):
                        id = self.form['id'].value
                    else:
                        id = self.session.data['new_report']['id']
                    allow_edit = self.g.get_item_permission(self.cookie_value, self.session, 'reports', id)
                    if self.g.isManager(self.session.data['roles']):  # Administrator or Manager
                        allow_edit = 'w'
                    if allow_edit == '' or allow_edit == 'r':  # no permission
                        self.data['page'] = self.g.read_html('access.denied')
                        self.page_parts['submenu'] = ""
                    else:
                        dict = {}
                        dict = page.edit()
                        self.process_data = dict['data']
                        self.data['page'] = self.g.read_html(dict['screen_name'])
                        self.page_parts['submenu'] = self.g.read_html('submenu.form')
                return

            elif page.split('.')[0] == 'reports' and page.split('.')[1] in ('list'):
                self.session.data['new_report'] = {}
                self.session.save()

            elif page == 'preferences':
                from .getdata import Getdata
                getdata = Getdata(self.cookie_value, self.form)
                if ('language' in self.form):
                    # Update user preferences in SQLite
                    chosen_label_lang = self.form['language'].value
                    if (chosen_label_lang == 'default'):  # Delete user preference and let him use the system's default settings
                        self.execute('delete_user_label', {'id_user': self.session.data['id_user']})
                        chosen_label_lang = ''
                    elif (getdata.usingDefaultLabel()): #Insert new
                        self.execute('insert_user_label', {'label_lang': chosen_label_lang, 'id_user': self.session.data['id_user']})
                    else: #Update only
                        self.execute('update_user_label', {'label_lang': chosen_label_lang, 'id_user': self.session.data['id_user']})

                    # Update user password, if he wants to
                    user_id = str(self.form['util_user_id'].value)
                    user_pwd = ''
                    if ('util_user_pwd' in self.form): #Empty fields are discarded automatically
                        user_pwd = str(self.form['util_user_pwd'].value)
                        try:
                            from hashlib import md5 as new_md5
                        except ImportError:
                            from hashlib import md5 as new_md5
                        user_pwd = new_md5(user_pwd.encode('utf-8')).hexdigest()
                        # Change User Password
                        self.execute('update_user_pwd_only', {'id_user': user_id,'pwd': user_pwd})

                    # Update user lines shown per page (used for paging)
                    user_lines_per_page = 50  # default value
                    if ('util_user_lines_per_page' in self.form):  # Empty fields are discarded automatically
                        user_lines_per_page = int(self.form['util_user_lines_per_page'].value)
                        if user_lines_per_page <= 0:
                            user_lines_per_page = 50  # default value
                        self.session.data['lines_per_page'] = user_lines_per_page
                    self.execute('update_user_lines_per_page', {'id_user': user_id,'lines_per_page': user_lines_per_page})

                    # Update user lines shown per page (used for paging)
                    user_max_num_pages = 5  # default value
                    if ('util_user_max_num_pages' in self.form):  # Empty fields are discarded automatically
                        user_max_num_pages = int(self.form['util_user_max_num_pages'].value)
                        if user_max_num_pages <= 0:
                            user_max_num_pages = 5  # default value
                        self.session.data['max_num_pages'] = user_max_num_pages
                    self.execute('update_user_max_num_pages', {'id_user': user_id,'max_num_pages': user_max_num_pages})

                    # Update user show strain inactives (used to show on list inactives strains)
                    user_show_str_inactives = 0 #default value
                    if ('util_user_show_str_inactives' in self.form):
                        user_show_str_inactives = int(self.form['util_user_show_str_inactives'].value)
                    self.session.data['show_str_inactives'] = user_show_str_inactives
                    self.execute('update_user_show_str_inactives', {'id_user': user_id,'show_str_inactives': user_show_str_inactives})


                    # Update session
                    self.session.data['id_lang'], self.session.data['label_lang_code'] = self.get_id_lang(chosen_label_lang)

                    # Warn user that operation was successful
                    self.session.data['feedback'] = 1

                    # Save set data
                    self.session.save()

                    # Generate i18n javascript file, if needed
                    from .js_translator import JS_Translator
                    js_tr = JS_Translator(self.cookie_value, self.i18n, chosen_label_lang)
                    if (js_tr.needsUpdate()): js_tr.doUpdate()

                    # Reload page to get effects from changes
                    print((self.g.redirect('./preferences.py')))
                    exit(0)

                self.check_feedback()

                # Update global variables
                self.data['page'] = self.g.read_html('preferences')

                # brk(host="localhost", port=9000)
                self.page_parts['submenu'] = self.g.read_html('submenu.save')

                # Show user roles (groups)
                self.data['usergroups'] = getdata.user_roles(self.session.data['id_user'])

                # Show user info
                self.data['userlines_per_page'] = Getdata.user_lines_per_page(self.session.data['id_user'])
                self.data['usermax_num_pages'] = Getdata.user_max_num_pages(self.session.data['id_user'])
                self.data['usershow_str_inactives'] = Getdata.user_show_str_inactives(self.session.data['id_user'], html=True)

                # Create Languages selection
                # Check whether user is using his own preference or the system's default
                if (getdata.usingDefaultLabel()):
                    self.data['languages'] = getdata.preferences('default')
                else:
                    self.data['languages'] = getdata.preferences(self.session.data['id_lang'])

                # Account tab
                self.data['iduser'] = self.session.data['id_user']
                self.data['username'] = self.session.data['user_name']
                self.data['userlogin'] = self.session.data['login']
                return

            elif page == 'location':
                from .location import LocationBuilder
                self.html_main = '%(page)s'
                self.data['page'] = self.g.read_html('location.form')
                location = LocationBuilder(self.cookie_value)
                self.data['debug'] = ''
                return

            elif page == 'configuration':
                from .configuration import Configuration
                utils = Configuration(self.cookie_value, self.form)
                if ('util_type' in self.form):  # User submitted data
                    utils.readForm()
                    # Read feedback value from saved session data
                    self.session.load(self.cookie_value)
                    self.check_feedback()
                # Load HTML template
                if (self.g.isAdmin(self.session.data['roles'])):  # Administrator
                    self.data['page'] = self.g.read_html('configuration')
                else:  # Non-Admin users are not allowed here
                    self.data['page'] = self.g.read_html('access.denied')
                    return
                # JAVASCRIPT Global Data
                utils.loadJSData(self.data)
                # Collections tab
                utils.loadCollTab(self.data)
                # SubCollections tab
                utils.loadSubCollTab(self.data)
                # Groups tab
                utils.loadGroupTab(self.data)
                # Combo tab
                utils.loadComboTab(self.data,self.session.data['id_lang'])
                # User tab
                utils.loadUserTab(self.data)
                # Database tab
                utils.loadDBTab(self.data)
                # Config.XML tab
                utils.loadConfigTab(self.data)
                # Division tab
                utils.loadDivisionTab(self.data)
                # Templates tab
                utils.loadReportTemplatesTab(self.data)
                return
            elif page == 'traceability':
                from .traceability import Traceability
                trace = Traceability(self.cookie_value, self.form)
                page_data = trace.render_page()
                self.data.update(page_data)
                return

            elif page == 'textlink':
                # Page = TinyMCE's Javascript PopUp for TextLink insertion
                from .getdata import Getdata
                getdata = Getdata(self.cookie_value, self.form)
                self.html_main = '%(page)s'
                self.data['page'] = self.g.read_html('textlink')
                # Get Document and Reference titles
                self.data['sel_doc'] = getdata.get_available_docs(
                    self.session.data['id_lang'],
                    self.session.data['id_coll'],
                    self.session.data['roles']
                )
                self.data['sel_ref'] = getdata.get_available_refs(
                    self.session.data['id_lang'],
                    self.session.data['id_coll'],
                    self.session.data['roles']
                )
                self.data['sel_qualifier_doc'] = getdata.get_doc_qualifiers()
                return

            elif page == 'fieldlink':
                # brk(host="localhost", port=9000)                
                # Page = TinyMCE's Javascript PopUp for FieldLink insertion

                from .reports import Reports
                page = Reports(self.form, self.cookie_value)

                page.fill_system_fieldlinks(self.data)

                self.html_main = '%(page)s'
                self.data['page'] = self.g.read_html('fieldlink')
                return



            # Getting which page we are dealing with
            self.data['who'] = who = page.split('.')[0]
            action = page.split('.')[1]

            self.logger.debug("Parsed: action %s for page %s" % (action, who))

            # Only Administrator and Manager can view utilites area
            if who in ('stockmovement'):
                if not (self.g.isManager(self.session.data['roles'])):  # Administrator or Manager
                    self.data['page'] = self.g.read_html('access.denied')
                    return

            # Get who_lang
            if who not in ('doc', 'docpopup', 'ref', 'refpopup', 'container'):
                self.data['who_lang'] = self.label_dict['menu_%s' % who.title()]
            elif who in ('doc', 'docpopup'):
                self.data['who_lang'] = self.label_dict['menu_Documents']
            elif who in ('ref', 'refpopup'):
                self.data['who_lang'] = self.label_dict['menu_References']
            elif who in ('container'):
                self.data['who_lang'] = self.label_dict['menu_Containers']

            # Getting Template Page
            if who in ('docpopup',):
                html_page = self.get_template(page, 'doc', action)
            elif who in ('refpopup',):
                html_page = self.get_template(page, 'ref', action)
            else:
                html_page = self.get_template(page, who, action)

            if who in ('docpopup', 'refpopup'):
                self.html_main = html_page
                self.html_footer = ''

            # Get LIST Data
            if action == 'list':
                from .lists import Lists
                lists = Lists(self.form, self.cookie_value)
                process_data = lists.get(who)
                self.page_parts = lists.page_parts
                self.data['feedback_value'] = lists.feedback_value
                self.data[lists.order_img] = lists.img
                del lists
            # Get Detail and Form Data
            elif action in ('detail', 'form', 'new'):
                from .getdata import Getdata
                getdata = Getdata(self.cookie_value, self.form)
                if action == 'detail':
                    process_data = getdata.get(who, 'view')
                elif action == 'form':
                    process_data = getdata.get(who, 'edit')
                    if process_data['next_action'] == 'insert':
                        # Security
                        # If user cannot create a new strain, he also cannot create a new strain from a previous one.
                        allow_create = self.g.get_area_permission(self.cookie_value, self.session, who, 'allow_create')
                        if self.g.isManager(self.session.data['roles']):  # Administrator or Manager
                            allow_create = 'y'
                        if allow_create != 'y':
                            html_page = self.g.read_html('access.denied')
                elif action == 'new':
                    allow_create = self.g.get_area_permission(self.cookie_value, self.session, who, 'allow_create')
                    if self.g.isManager(self.session.data['roles']):  # Administrator or Manager
                        allow_create = 'y'
                    if allow_create == 'y':
                        process_data = getdata.get(who, 'new')
                self.page_parts = getdata.page_parts
                self.data['feedback_value'] = getdata.feedback_value
                del getdata

            # Receiver Save Return
            elif action == 'save':
                from .form_save import Save
                save = Save(self.cookie_value, self.form)
                process_data = save.set(who)
                del save

            # Receiver Delete Return
            elif action == 'del':
                allow_delete = self.g.get_area_permission(self.cookie_value, self.session, who, 'allow_delete')
                if self.g.isManager(self.session.data['roles']):  # Administrator or Manager
                    allow_delete = 'y'
                if allow_delete == 'y':
                    from .form_del import Delete
                    delete = Delete(self.cookie_value, self.form)
                    process_data = delete.set(who)
                    del delete
        elif (category == 'external'):
            if not (self.cookie_value and self.session.isvalid(self.cookie_value)):
                self.html_main = "<script type='text/javascript'>window.parent.document.location = '%s';</script>" % self.index
                self.html_footer = ''
            else:
                if page == 'strains.quality.list':
                    from .quality import Quality
                    quality = Quality(page, self.cookie_value, self.form)
                    if (quality.hasItemPermission(self.form.getvalue('id'))):
                        quality = Quality(page, self.cookie_value, self.form)
                        quality.loadQualities(self.data)
                        self.html_main = self.data['quality_table']
                        self.html_footer = ''
                    else:
                        self.html_main = self.g.read_html('access.denied')
                if page == 'strains.quality.new' or page == 'strains.quality.edit':
                    from .quality import Quality
                    quality = Quality(page, self.cookie_value, self.form)
                    if (quality.hasItemPermission(self.form.getvalue('id_strain'))):
                        self.data['who'] = "strains.quality"
                        self.data['id_strain'] = str(self.form['id_strain'].value)
                        self.data['date_format'] = self.g.get_config('date_input_mask')
                        self.html_footer = ''
                        html_page = self.g.read_html('strains.quality.form')
                        if page == 'strains.quality.new':
                            self.data['action'] = 'insert'
                            self.data['quality_id_person'] = -1
                            self.data['quality_id_lot'] = -1
                            self.data['purity'] = quality.renderPurity()
                            quality.loadItems(self.data)
                        else:
                            self.data['action'] = 'update'
                            self.data['id_quality'] = str(self.form['id_quality'].value)
                            quality.loadQuality(self.data)
                            quality.loadItems(self.data)
                        self.html_main = html_page
                    else:
                        self.html_main = self.g.read_html('access.denied')
                if page == 'strains.quality.save':
                    from .quality import Quality
                    quality = Quality(page, self.cookie_value, self.form)
                    action = self.form.getvalue('next_action')
                    has_permission = True
                    if (action == 'insert' or action == 'update'):
                        if (not quality.hasItemPermission(self.form.getvalue('id_strain'))):
                            has_permission = False
                    else:  # delete
                        if (not quality.hasAreaPermission('allow_delete')):
                            has_permission = False
                    if (has_permission):
                        from .form_save import Save
                        save = Save(self.cookie_value, self.form)
                        process_data = save.strainQuality()
                        if ('error_info' in process_data):
                            self.html_main = self.g.read_html('form.save')
                        del save
                    else:
                        self.html_main = self.g.read_html('access.denied')
                if page == 'strains.stock.list':
                    # Check whether user has permission to see item details of chosen area
                    self.session.load(self.cookie_value)
                    allow_detail = self.g.get_item_permission(self.cookie_value, self.session, 'strains', self.form.getvalue('id'))
                    if self.g.isManager(self.session.data['roles']):  # Administrator or Manager
                        allow_detail = 'w'
                    if allow_detail == '':  # no permission
                        self.html_main = self.g.read_html('access.denied')
                    else:
                        self.data['who'] = "strains.stock"
                        self.data['id_strain'] = str(self.form['id'].value)
                        self.data['date_format'] = self.g.get_config('date_input_mask')
                        self.html_footer = ''
                        html_page = self.g.read_html('strains.stock.list')
                        from .getdata import Getdata
                        getdata = Getdata(self.cookie_value, self.form)
                        getdata.strainStock(self.data)
                        self.html_main = html_page

        # Update global variables
        self.data['page'] = html_page
        self.process_data = process_data

    def replace_externals(self, js, js_line, debug_mode=False):
        tinymce_path = 'external/tinymce/jscripts/tiny_mce/tiny_mce'

        jquery_path = 'external/jquery/jquery'
        jquery_boxy_path = 'external/jquery/jquery.boxy'
        jquery_tooltip_path = 'external/jquery/jquery.tooltip.min'
        jquery_select_path = 'external/jquery/jquery.selectboxes.min'

        jquery_ui_core = 'external/jquery/ui/jquery.ui.core'
        jquery_ui_widget = 'external/jquery/ui/jquery.ui.widget'
        jquery_ui_mouse = 'external/jquery/ui/jquery.ui.mouse'

        jquery_ui_sortable = 'external/jquery/ui/jquery.ui.sortable'

        json_path = 'external/json2'
        sprintf_path = 'external/sprintf'
        if js == 'ext.tinymce':
            self.data['js'] += js_line % tinymce_path
        elif js == 'ext.jquery':
            self.data['js'] += js_line % jquery_path
            self.data['js'] += js_line % jquery_boxy_path
            self.data['js'] += js_line % jquery_tooltip_path
            self.data['js'] += js_line % jquery_select_path
        elif js == 'ext.jquery.ui':
            self.data['js'] += js_line % jquery_ui_core
            self.data['js'] += js_line % jquery_ui_widget
            self.data['js'] += js_line % jquery_ui_mouse
        elif js == 'ext.jquery.ui.sortable':
            self.data['js'] += js_line % jquery_ui_sortable
        elif js == 'ext.json':
            self.data['js'] += js_line % json_path
        elif js == 'ext.sprintf':
            self.data['js'] += js_line % sprintf_path
        else:
            if debug_mode.lower() == 'true':
                js += '_src'
            self.data['js'] += js_line % js

    def header_includes(self, page, category, js, css):
        g = General()
        debug_mode = g.get_config("debug_mode")

        if debug_mode.lower() == 'true':
            self.data['js'] += self.js_line % 'general_src'
        else:
            self.data['js'] += self.js_line % 'general'

        # JavaScript Inclusions
        if js:
            js_line = '\n%s' % self.js_line
            js_lang_code = self.get_label_code()
            translation_js_path = 'js_i18n/translation_%s' % js_lang_code
            # one javascript file
            if isinstance(js, str):
                self.data['js'] += js_line % translation_js_path  # add js_translator file
                self.replace_externals(js, js_line, debug_mode)

            # many javascript files
            elif isinstance(js, tuple):
                self.data['js'] += js_line % translation_js_path  # add js_translator file
                for item in js:
                    self.replace_externals(item, js_line, debug_mode)
        else:
            js_line = self.js_line
            js_lang_code = self.get_label_code()
            translation_js_path = 'js_i18n/translation_%s' % js_lang_code
            self.data['js'] += js_line % translation_js_path  # add js_translator file
            """
                                <script src="../../jquery-1.5.1.js"></script>
                                <script src="../../ui/jquery.ui.core.js"></script>
                                <script src="../../ui/jquery.ui.widget.js"></script>
                                <script src="../../ui/jquery.ui.mouse.js"></script>
                                <script src="../../ui/jquery.ui.sortable.js"></script>
            """

        # CSS Inclusions
        css_line = '\n%s' % self.css_line
        if (category == 'main'):
            self.data['css'] += css_line % category
        if css:
            if isinstance(css, str):
                self.data['css'] += css_line % css
            elif isinstance(css, tuple):
                css_list = self.expand_css_list(css)
                for item in css_list:
                    self.data['css'] += css_line % item

    def expand_css_list(self, css_tuple):
        css_list = []
        for item in css_tuple:
            if item == 'location':
                css_list.extend( ('boxy', 'jquery.tooltip', 'location.default') )
            else:
                css_list.append(item)

        return css_list

    def page_show(self, page):
        # raise str(page)
        # Criar cópia do http_header para evitar modificar a variável de classe
        current_http_header = self.http_header
        
        # Complete the  http_header if Cookie exists
        if self.data['cookie']:
            current_http_header += '\n%(cookie)s'

        # Force all data to be UTF8 compatible - make them all of 'unicode' type
        if 'error_info' in self.data:
            try:
                self.data['error_info'] = str(self.data['error_info'])
                exception.clear_exceptions()
            except:
                pass

        for i in self.data:
            if type(self.data[i]) == str:
                try:
                    self.data[i] = self.data[i].decode('utf8')
                except:
                    pass

        # Join parts and show
        template = self.data['page']
        if isinstance(template, bytes):
            template = template.decode('utf-8')  # decode bytes to str
        self.data['page'] = (template % self.data)

        # Do not show the configuration button to ordinary users
        if 'roles' in self.session.data:
            if not self.g.isAdmin(self.session.data['roles']):
                # Garantir que html_main é string antes de concatenar
                if isinstance(self.html_main, bytes):
                    self.html_main = self.html_main.decode('utf-8')
                self.html_main += '<script type="text/javascript">if (document.getElementById("user_menu_admin")) document.getElementById("user_menu_admin").style.display="none";</script>'

        #Do not show the utilites button to ordinary users
        if 'roles' in self.session.data:
            if not self.g.isManager(self.session.data['roles']):
                # Garantir que html_main é string antes de concatenar
                if isinstance(self.html_main, bytes):
                    self.html_main = self.html_main.decode('utf-8')
                self.html_main += '<script type="text/javascript">if (document.getElementById("user_menu_utilities")) document.getElementById("user_menu_utilities").style.display="none";</script>'

        # Sempre enviar cabeçalhos HTTP primeiro
        formatted_header = current_http_header % self.data
        print(formatted_header)
        print()  # Linha em branco separando cabeçalhos do corpo

        # Monta o HTML sem reimprimir cabeçalho HTTP (enviado em index.py)
        html_header = self.html_header.decode('utf-8') if isinstance(self.html_header, bytes) else self.html_header
        html_main = self.html_main.decode('utf-8') if isinstance(self.html_main, bytes) else self.html_main
        html_footer = self.html_footer.decode('utf-8') if isinstance(self.html_footer, bytes) else self.html_footer
        full_page = "\n".join((
                    html_header,
                    exception.get_html(),
                    html_main,
                    html_footer
                ))

        try:
            # message,submenu
            full_page = full_page % self.data
        except KeyError as e:
            # create a SicolException, which properly formats our error:
            from .i18n import _
            exception.SicolException("%s: %s" % (_("KeyError when assembling final html"), e), 1, "%s\n<br />%s %s" % (str(e.args), _("Data"), self.data))
            full_page = "\n".join((
                    self.html_header,
                    exception.get_html(),
                    self.html_main,
                    self.html_footer
                ))
        except TypeError as e:
            # Programming error: missing key(s) in self.data dictionary
            import re
            from .i18n import _
            page_keys = re.compile(r"%\((.+?)\)", re.MULTILINE | re.DOTALL | re.IGNORECASE)
            page_keys = page_keys.findall(full_page)
            not_found = []
            for k in page_keys:
                if k not in list(self.data.keys()):
                    not_found.append(k)
            # create a SicolException, which properly formats our error:
            exception.clear_exceptions()
            self.html_header = re.sub(r'%\(.+?\)s', r'', self.html_header)
            exception.SicolException("<p>%s </p>\n%s: %s" % ("TypeError: " + str(e), _("Missing keys"), str(", ".join(not_found))))
            full_page = "\n".join((
                  self.html_header,
                  exception.get_html()
                  ))

        # Imprime o conteúdo HTML já em str, sem bytes prefixados
        print(full_page)
