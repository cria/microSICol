#!/usr/bin/env python2
#-*- coding: utf-8 -*-

# Python imports
from time import strftime, strptime
import math

# Project imports
from dbconnection import dbConnection
from general import General
from getdata import Getdata
from log import Log
from loghelper import Logging
from os import environ
from session import Session
from labels_traceability import label_trace
from labels_traceability import label_values_dict
from labels_traceability import values_dict


class Traceability(object):
    IMG_PATH_UP = '../img/order_up.png'
    IMG_PATH_DOWN = '../img/order_down.png'
    TOTAL_TH_COLUMNS = 8

    GLUE = ' '
    CLEAR_FILTER = ' '

    g = General()
    session = None

    def __init__(self, cookie_value='', form=None):
        self.current_page = 1
        self.total_pages = 1

        self.cookie_value = cookie_value
        if self.cookie_value:
            # Load Session
            self.session = Session()
            self.session.load(self.cookie_value)

            # Define Data Dict
            data = {}
            data['id_lang'] = self.session.data['id_lang']  # id for label_lang
            data['id_coll'] = self.session.data['id_coll']
            data['id_subcoll'] = self.session.data['id_subcoll']
            # Non-Admin users are not allowed here
            data['page'] = self.g.read_html('access.denied')
            self.data = data

            self.form = form

            # Define log Database
            base_descr = self.build_base_descr(self.cookie_value)
            self.dbconnection_log = dbConnection(base_descr=base_descr)

            # Hack to always use raw_mode when executing
            def raw_execute_log(*args, **kwargs):
                kwargs['raw_mode'] = True
                return self.dbconnection_log.execute(*args, **kwargs)
            self.execute_log = raw_execute_log
            self.fetch_log = self.dbconnection_log.fetch

            # Define Database
            self.dbconnection = dbConnection(self.cookie_value)

            # Hack to always use raw_mode when executing
            def raw_execute(*args, **kwargs):
                kwargs['raw_mode'] = True
                return self.dbconnection.execute(*args, **kwargs)
            self.execute = raw_execute
            self.fetch = self.dbconnection.fetch

            # Define Logging
            self.logger = Logging.getLogger("traceability")
            self.l = Log(self.cookie_value, self.dbconnection_log)

            # Load GetData class
            self.getdata = Getdata(self.cookie_value, self.form)

    def check_permissions(self):
        if (self.g.isManager(self.session.data['roles'])):  # Admin or Manager
            self.data['page'] = self.g.read_html('traceability')

    def render_page(self):
        self.check_permissions()

        filters = self.get_filters(empty_too=True)
        self.data.update(filters)

        self.data['date_format'] = self.get_date_format()
        self.data['users_list_as_options'] = self.users_list_as_options(filters['user'])
        self.data['operations_list_as_options'] = self.operations_list_as_options(filters['operation'])
        self.data['fields_list_as_options'] = self.fields_list_as_options(filters['field'])
        self.data['log_rows'] = self.render_log_rows()
        self.data['log_pagination'] = self.get_log_pagination(
            self.TOTAL_TH_COLUMNS,
            self.current_page,
            self.session.data['max_num_pages'],
            self.total_pages,
            '.' + environ['SCRIPT_NAME'][environ['SCRIPT_NAME'].rindex('/'):] + '?page=%s')
        return self.data

    def render_log_rows(self):
        html_row = '<tr class="row%(row_class)s">\
                      <td class="date_time">%(date_time)s</td>\
                      <td class="user">%(user)s</td>\
                      <td class="operation">%(operation_label)s</td>\
                      <td class="record">%(id_entity)s</td>\
                      <td class="strain_code">%(code_entity)s</td>\
                      <td class="lot">%(lot)s</td>\
                      <td class="field">%(field_label)s</td>\
                      <td class="value">%(value)s</td>\
                    </tr>'

        query_data = self.get_query_data()
        self.execute_log('log_log_list', query_data)
        log_rows = self.fetch_log('all')

        # Build the html, row by row
        html_log_rows = []
        row_class = 1
        for row_data in log_rows:
            row_data['row_class'] = row_class

            row_data['date_time'] = self.format_date_time(row_data['date_time'])
            row_data['field_label'] = label_trace[str(row_data['field_label'])]
            row_data['operation_label'] = label_trace[str(row_data['operation_label'])]
                    
            if row_data['label_value_lookup']:                
                row_data['value'] = values_dict[label_values_dict[row_data['label_value_lookup']][str(row_data['value'])]]                

            elif row_data['mlang_value']:
                row_data['value'] = label_trace[str(row_data['value'])]

            elif row_data['mlang_table']:
                row_data['value'] = self.get_multilanguage_value(
                    table=row_data['mlang_table'],
                    field=row_data['mlang_field'],
                    key=row_data['mlang_key'],
                    value=row_data['value'])
                
            

            html_log_rows.append(html_row % row_data)

            if row_class == 1:
                row_class = 2
            else:
                row_class = 1

        return ''.join(html_log_rows)

    def get_query_data(self):
        filters = self.get_filters()

        condition_query = self.build_condition_query(filters)

        field_order = self.get_field_order()

        paging = self.build_limit_query_part(condition_query, field_order)

        query_data = {
            'condition': condition_query,
            'field_order': field_order,
            'paging': paging}

        return query_data

    def get_filters(self, empty_too=False):
        filters = {}

        fields_name = [
            'datetime_from', 'datetime_to', 'user', 'operation', 'record',
            'strain_code', 'lot', 'field', 'value']

        for field in fields_name:
            filter_session_key = 'traceability_%s' % field

            if environ['REQUEST_METHOD'] == 'GET':  # Retrieve from Session
                if filter_session_key in self.session.data:
                    filter_value = self.session.data[filter_session_key]
                else:
                    filter_value = ''
            elif environ['REQUEST_METHOD'] == 'POST':  # Retrieve from form
                if field in self.form:
                    filter_value = str(self.form[field].value).strip()
                else:
                    filter_value = ''

                # Save filter on session for later use
                self.session.data[filter_session_key] = filter_value
                self.session.save()

            if filter_value or empty_too:
                filters[field] = filter_value

        return filters

    def build_condition_query(self, filters):
        conditions = [self.GLUE]

        if 'datetime_from' not in filters:
            filters['datetime_from'] = None
        if 'datetime_to' not in filters:
            filters['datetime_to'] = None
        conditions.append(self.datetime_condition(
            filters['datetime_from'], filters['datetime_to']))

        if 'user' in filters:
            conditions.append(self.user_condition(filters['user']))
        if 'operation' in filters:
            conditions.append(self.operation_condition(filters['operation']))
        if 'record' in filters:
            conditions.append(self.record_condition(filters['record']))
        if 'strain_code' in filters:
            conditions.append(self.strain_code_condition(filters['strain_code']))
        if 'lot' in filters:
            conditions.append(self.lot_condition(filters['lot']))
        if 'field' in filters:
            conditions.append(self.field_condition(filters['field']))
        if 'value' in filters:
            conditions.append(self.value_condition(filters['value']))

        condition_query = self.GLUE.join(conditions)
        return condition_query

    def get_field_order(self):
        # Verify field_order is changed
        if 'field_order' in self.form:
            self.g.saveListOrder(
                self.session.data['id_user'],
                self.session.data['id_subcoll'],
                'traceability',
                self.form['field_order'].value)

        # Get field_order and mode for order list
        field_order, mode = self.g.getListOrder(
            self.session.data['id_user'],
            self.session.data['id_subcoll'],
            'traceability')

        # Define if order is Asc, or Desc
        order_img_template = '<img class="order" src="%s" />'
        if mode == 'ASC':
            order_img_html = order_img_template % self.IMG_PATH_UP
        else:
            order_img_html = order_img_template % self.IMG_PATH_DOWN

        self.data['img_%s' % field_order] = order_img_html

        return '%s %s' % (field_order, mode)

    def build_limit_query_part(self, condition_query, field_order):
        # Disable paging for row counting
        query_data = {
            'condition': condition_query,
            'field_order': field_order,
            'paging': self.GLUE}

        # Execute for rows count
        self.execute_log('log_log_list', query_data)

        # Calculate how many pages are
        lines = float(self.dbconnection_log.getrows())
        lines_per_page = int(self.session.data['lines_per_page'])
        total_pages = int(math.ceil(lines / lines_per_page))

        # Verify page
        page = 1
        if 'page' in self.form:
            page = int(self.form['page'].value)
            if page <= 0:
                page = 1
            elif page > total_pages:
                page = total_pages

            # Save filter on session
            self.session.data['page_traceability'] = page
            self.session.save()
        elif 'page_traceability' in self.session.data:
            if 'filter' in self.form:
                # Save filter on session
                self.session.data['page_traceability'] = page
                self.session.save()
            else:
                page = int(self.session.data['page_traceability'])

        # Enable paging
        limit_query = self.GLUE
        if (total_pages > 1):
            offset = (page - 1) * lines_per_page
            limit_query = 'LIMIT %s, %s' % (offset, lines_per_page)

        self.current_page = page
        self.total_pages = total_pages

        return limit_query

    def datetime_condition(self, start=None, end=None):
        if start is not None:
            start = strptime(start, self.get_date_format())
            start = strftime('%Y-%m-%d', start)
        if end is not None:
            end = strptime(end, self.get_date_format())
            end = strftime('%Y-%m-%d', end)

        if start is not None and end is not None:
            return "AND date_time BETWEEN '%s' AND '%s'" % (start, end)
        elif start is not None:
            return "AND date_time >= '%s'" % start
        elif end is not None:
            return "AND date_time <= '%s'" % end
        else:
            return ""

    def user_condition(self, filter_value):
        g = General()
        return "AND user LIKE '%%%s%%'" % g.ConvertStrUnicode(filter_value)

    def operation_condition(self, filter_value):
        return "AND id_log_operation = '%s'" % filter_value

    def record_condition(self, filter_value):
        return "AND id_entity LIKE '%%%s%%'" % filter_value

    def strain_code_condition(self, filter_value):
        g = General()
        return "AND code_entity LIKE '%%%s%%'" % g.ConvertStrUnicode(filter_value)
		
    def lot_condition(self, filter_value):
        g = General()
        return "AND lot LIKE '%%%s%%'" % g.ConvertStrUnicode(filter_value)

    def field_condition(self, filter_value):
        return "AND id_log_field = '%s'" % filter_value

    def value_condition(self, filter_value):
        g = General()
        return "AND value LIKE '%%%s%%'" % g.ConvertStrUnicode(filter_value)

    def users_list_as_options(self, selected_value):
        return self.anything_list_as_options(
            query_name='log_log_list_users',
            label_field='user',
            selected_value=selected_value)

    def operations_list_as_options(self, selected_value):
        return self.anything_list_as_options(
            query_name='log_log_list_operations',
            label_field='label',
            value_field='id_log_operation',
            selected_value=selected_value,
            translate=True)

    def fields_list_as_options(self, selected_value):
        return self.anything_list_as_options(
            query_name='log_log_list_fields',
            label_field='label',
            value_field='id_log_field',
            selected_value=selected_value,
            translate=True)

    def anything_list_as_options(
        self,
        query_name,
        label_field,
        value_field=None,
        selected_value=None,
        translate=False):

        g = General()

        option_template = '<option value="%s">%s</option>'
        selected_option_template = '<option value="%s" selected>%s</option>'

        if value_field is None:
            value_field = label_field

        self.execute_log(query_name)
        rows = self.fetch_log('all')

        if str(selected_value) == self.CLEAR_FILTER:
            empty_option = selected_option_template % (self.CLEAR_FILTER, '')
        else:
            empty_option = option_template % (self.CLEAR_FILTER, '')

        options = [empty_option]

        for row in rows:
            if g.ConvertStrUnicode(row[value_field]) == g.ConvertStrUnicode(selected_value):
                template = selected_option_template
            else:
                template = option_template

            if translate:
                options.append(
                    template % (row[value_field], label_trace[str(row[label_field])]))
            else:
                options.append(
                    template % (row[value_field], row[label_field]))

        return ''.join(options)

    def get_multilanguage_value(self, table=None, field=None, key=None, value=None):
        self.execute('log_log_mlang', {
            'table': table,
            'field': field,
            'key': key,
            'value': value,
            'id_lang': self.data['id_lang'], })
        multilanguage_value = self.fetch('one')
        return multilanguage_value

    def build_base_descr(self, cookie_value):
        # Grab the settings to connect to log database

        id_base = self.session.data['id_base']
        sqlite_connection = dbConnection()
        sqlite_connection.execute('get_all_dbs_log', {'id_base': id_base})
        base_log = sqlite_connection.fetch('columns')

        try:
            host = base_log['host']
            port = base_log['port']
            db_name = base_log['db_name']
            user = base_log['user']
            pwd = base_log['pwd']
            dbms = base_log['dbms_name']
        except KeyError:
            message = "There isn't log connection info for this database."
            raise Exception(message)

        base_descr = {
            'host': host,
            'port': port,
            'db_name': db_name,
            'user': user,
            'pwd': pwd,
            'dbms': dbms
        }

        return base_descr

    def get_date_format(self):
        ''' Get locale output date format. '''

        mask_key = 'date_output_mask'

        date_mask = self.validate_date_mask(self.session.data[mask_key])
        if date_mask:
            return date_mask

        date_mask = self.validate_date_mask(self.g.get_config(mask_key))
        if date_mask:
            return date_mask

        return '%d/%m/%Y'

    def validate_date_mask(self, date_mask):
        ''' Validate if a date mask has a value that we should look at. '''

        if date_mask is not None and date_mask != "":
            return date_mask
        return False

    def get_date_time_format(self):
        '''
          Returns the date time format by appending time format to current
        locale date format.
        '''

        date_format = self.get_date_format()
        time_format = '%H:%M:%S'
        return '%s %s' % (date_format, time_format)

    def format_date_time(self, field):
        '''
          Formats SQL date time format (YYYY-mm-dd HH:MM:SS) to current locale
        date time format.
        '''

        if field:  # field is a datetime.date object
            return strftime(self.get_date_time_format(), field.timetuple())
        else:
            return ''

    def get_log_pagination(self, total_columns, current_page, max_page_links, total_pages, base_link):
        " Returns html for the foot of the list "

        if total_pages == 1:  # Don't show paging when there is only one page to look
            return ''

        log_pagination = ('<tr>'
                          '  <td colspan="%(total_columns)s">'
                          '    <ul>'
                          '      %(list_items)s'
                          '    </ul>'
                          '  </td>'
                          '</tr>')
        list_items = []

        li_base = '<li><a href="%%(link_page)s" %(selected)s>%%(page)s</a></li>'
        li_selected = li_base % {'selected': 'class="pageselected"'}
        li_normal = li_base % {'selected': ''}

        li_special_base = '<li class="specialpages"><a href="%%s">%(arrow)s</a></li>'
        li_special_left = li_special_base % {'arrow': '&laquo;'}
        li_special_right = li_special_base % {'arrow': '&raquo;'}

        append_li_selected = lambda i: list_items.append(li_selected % {
            'link_page': base_link % i, 'page': i})
        append_li_normal = lambda i: list_items.append(li_normal % {
            'link_page': base_link % i, 'page': i})

        def append_li(i):
            if current_page == i:
                append_li_selected(i)
            else:
                append_li_normal(i)

        append_li_special_left = lambda i: list_items.append(li_special_left % (base_link % i))
        append_li_special_right = lambda i: list_items.append(li_special_right % (base_link % i))

        arrow_left = False
        arrow_right = False
        start = 0
        end = 0

        #Only numbers
        if total_pages <= max_page_links:
            start = 1
            end = total_pages + 1
        #Numbers and special pages
        else:
            num_pages_left = (max_page_links - 1) / 2
            num_pages_right = max_page_links / 2

            if current_page - num_pages_left > 0 and current_page + num_pages_right < total_pages:
                if current_page - num_pages_left != 1:
                    arrow_left = True
                start = current_page - num_pages_left
                end = current_page + num_pages_right + 1
                arrow_right = True
            elif current_page - num_pages_left > 0 and current_page + num_pages_right >= total_pages:
                arrow_left = True
                start_steroids = current_page + num_pages_right - total_pages
                start = current_page - num_pages_left - start_steroids
                end = total_pages + 1
            #Per page, fill numbers and insert special pages
            elif current_page <= max_page_links:
                start = 1
                end = max_page_links + 1
                arrow_right = True

        if arrow_left:
            append_li_special_left(1)

        for i in range(start, end):
            append_li(i)

        if arrow_right:
            append_li_special_right(total_pages)

        return log_pagination % {
            'total_columns': total_columns,
            'list_items': '\n'.join(list_items)}
