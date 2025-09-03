#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#python imports
import ast
import json
from os import path
from .session import Session
from .default_html_report import Default_Html_Report
from .custom_html_report import Custom_Html_Report
from .csv_report import CSV_Report
from .xml_report import XML_Report
from .chart_report import Chart_Report
#from dbgp.client import brk
from .dbconnection import dbConnection
from .dom_xml import Xml
from .labels import label_dict
from xml.dom.minidom import parse, parseString
from .getdata import Getdata
from .label_values_reports import label_values_dict
from .label_values_reports import values_dict

try:
    from hashlib import sha1 as new_sha
except ImportError:
    from sha import new as new_sha

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

#project imports
from .general import General

class Reports(object):

    g = General()

    vetor = None
    cookie_value = None
    global report_index_field
    num_fields = 0
    already_div = False

    def verify_notnull_fields(self, fields='',who=''):
        error = False
        from . import config
        out = config.http_header+'\n\n'
        out += '<b>%s</b>: %s:<br>\n' % (_("Error"), _("Obrigatory fields left blank"))
        main_title = '' #To be used when there is no other title in other languages
        for field in fields:
            if (who == 'doc' and field == 'title'):
                for lang in self.data_lang:
                    fields.append("%s_%s" %(field,list(lang.keys())[0]))
            elif (who == 'doc') and main_title == '' and field.startswith('title_') and self.form.getvalue(field):
                main_title = self.form.getvalue(field)
            elif not self.form.getvalue(field) and who == '':
                error = True
                out += ' - %s <b>%s</b> %s<br>\n' % (_("field"), field.title(), _("must not be empty."))
        if (who == 'doc'):
            if main_title == '': #There must be at least one title filled
                error = True
                out += ' - %s <b>%s</b> %s<br>\n' % (_("field"), field.title(), _("must not be empty."))
            else:
                return main_title
        if error:
            import sys
            sys.stdout.buffer.write(out.encode('utf8'))
            exit(1)

    def __init__(self, form, cookie_value):
        self.cookie_value = cookie_value
        self.form = form
        #Load Session
        self.session = Session()
        self.session.load(cookie_value)
        #Define Database
        self.dbconnection = dbConnection(cookie_value)
        self.execute = self.dbconnection.execute
        self.fetch = self.dbconnection.fetch
        self.cursor = self.dbconnection.cursor

    def prepare_dict(self, lista_filter):
        #brk(host="localhost", port=9000")

        if not lista_filter:
            return

        tmp_list = lista_filter[:]

        for item in tmp_list:
            try:
                if str(item["user_defined"]) == 'True':
                    self.report_index_field += 1
                    if 'value_' + str(self.report_index_field) in self.form:
                        item['value'] = self.form['value_' + str(self.report_index_field)].value
                    else:
                        lista_filter.remove(item)

                # Recursively process child items if they exist
                if 'childs' in item and item['childs']:
                    self.prepare_dict(item['childs'])
            except Exception as e:
                # Log the error but continue processing other items
                import logging
                logging.error(f"Error processing filter item: {str(e)}")
                continue

    def safe_eval_dict(self, dict_string):
        """Safely evaluate dictionary string using multiple methods"""
        if isinstance(dict_string, bytes):
            dict_string = dict_string.decode('utf-8', errors='replace')
        
        # Basic security check - reject potentially dangerous strings
        dangerous_keywords = ['import', 'exec', 'eval', '__builtins__', '__import__', 'open', 'file', 'input', 'raw_input', 'compile']
        dict_lower = dict_string.lower()
        for keyword in dangerous_keywords:
            if keyword in dict_lower:
                raise ValueError(f"Potentially unsafe content detected: '{keyword}' found in dictionary string")
        
        # Try JSON first (safest)
        try:
            # Convert Python dict syntax to JSON syntax
            json_string = dict_string.replace("'", '"').replace('True', 'true').replace('False', 'false').replace('None', 'null')
            return json.loads(json_string)
        except (json.JSONDecodeError, ValueError):
            pass
        
        # Try ast.literal_eval (safer than eval)
        try:
            return ast.literal_eval(dict_string)
        except (ValueError, SyntaxError):
            pass
        
        # Fall back to eval as last resort (already validated above)
        try:
            return eval(dict_string)
        except Exception as e:
            raise Exception(f"Cannot parse dictionary string safely: {str(e)}")

    def show(self):
        # identifica qual tipo do report
        # chama a classe associada ao tipo e imprime o report


        #notnulls = eval(self.form['notnulls'].value)
        #self.verify_notnull_fields(notnulls)

        #brk(host="localhost", port=9000)
        try:
            # Use safer evaluation of xml_dict
            xml_dict_value = self.form['xml_dict'].value
            dict_final = self.safe_eval_dict(xml_dict_value)
        except Exception as e:
            raise Exception(f"Error parsing xml_dict: {str(e)}")

        self.report_index_field = 0

        try:
            self.prepare_dict(dict_final['filters'])
        except Exception as e:
            raise Exception(f"Error preparing filters: {str(e)}")

        dict_final['id_report'] = self.form['id_report'].value
        dict_final['id_language'] = self.form['language'].value

        output = ""

        try:

            if (dict_final['format'].lower() == 'default'):
                dict_final['header_position'] = self.form['options_header'].value
                type = Default_Html_Report(dict_final, self.cookie_value)
                output =  type.mount_report_file()
            elif (dict_final['format'].lower() == 'chart'):
                dict_final['chart_type'] = self.form['options_chart_type'].value
                type = Chart_Report(dict_final, self.cookie_value)
                output =  type.mount_report_file()
            elif (dict_final['format'].lower() == 'csv'):
                if 'with_header' in self.form:
                    dict_final['header'] = str(self.form['with_header'].value == 'on').lower()
                else:
                    dict_final['header'] = 'false'
                dict_final['separator'] = self.form['separator'].value
                type = CSV_Report(dict_final, self.cookie_value)
                output =  type.mount_report_file()
            elif (dict_final['format'].lower() == 'custom'):
                type = Custom_Html_Report(dict_final, self.cookie_value)
                output =  type.mount_report_file()
            elif (dict_final['format'].lower() == 'xml'):
                type = XML_Report(dict_final, self.cookie_value)
                output =  type.mount_report_file()
            else:
                type = Default_Html_Report(dict_final, self.cookie_value)
                output =  type.mount_report_file()

        except Exception as err:
            raise err

        if isinstance(output, bytes):
            output = output.decode('utf-8', errors='replace')
        elif not isinstance(output, str):
            output = str(output)

        return output.replace('%', '%%')

    def new(self):
        step = '1'
        if 'step' in self.form:
            step = self.form['step'].value

        step_next = '1'
        if 'step_next' in self.form:
            step_next = self.form['step_next'].value

        dict = {}
        dict_data = {}

        getattr(self, 'save_data_step' + str(step))()

        dict['screen_name'] = 'reports.form.step' + str(step_next)
        dict['data'] =  getattr(self, 'fill_data_step' + str(step_next))()

        return dict

    def edit(self):
        #brk(host="localhost", port=9000)

        if 'id' in self.form:
            self.session.data['new_report']['id'] = self.form['id'].value

        step = '1'

        if 'step' in self.form:
            step = self.form['step'].value

        step_next = '1'
        if 'step_next' in self.form:
            step_next = self.form['step_next'].value

        dict = {}
        dict_data = {}
        report = []

        if step == '1' and step_next == '1':
            if ('new_report' in self.session.data) == False:
                self.session.data['new_report'] = {}

            data = {}
            data['id_lang'] = self.session.data['id_lang']
            data['id_subcoll'] = self.session.data['id_subcoll']
            data['id_report'] = str(self.session.data['new_report']['id'])
            data['field_order'] = " id_report "
            data['condition'] = " "
            data['paging'] = " "

            self.execute('get_report_data', data, False)
            report = self.fetch('columns')

            temp_id = self.session.data['new_report']['id']


            self.session.data['new_report']['type'] = report['id_report_type']
            self.session.save()

            # Handle both string and bytes data for Python 3 compatibility
            xml_data = report['definition']
            if isinstance(xml_data, bytes):
                xml_data = xml_data.decode("utf8")
            xml_data = xml_data.replace('\r\n',"[_new_line_]").replace("\t","[_tab_]")
            # Ensure xml_data is properly encoded as bytes for parseString
            if isinstance(xml_data, str):
                dom = parseString(xml_data.encode("utf8"))
            else:
                dom = parseString(xml_data)
            xml_dict = {}
            z = Getdata(self.cookie_value, self.form)
            xml_dict = z.xml2dict(dom)

            #brk(host="localhost", port=9000)
            xml_dict['filters'] = self.decodeFilters(xml_dict['filters'])

            self.session.data['new_report'] = xml_dict
            self.session.data['new_report']['name'] = self.ConvertStrUnicode(report['description'])
            self.session.data['new_report']['type'] = report['id_report_type']
            self.session.data['new_report']['id'] = temp_id

            self.session.data['new_report']['action'] = "edit"

            if self.session.data['new_report']['format'] == 'custom':
                self.decodeTemplates(self.session.data['new_report'])

            self.session.save()

        else:
            getattr(self, 'save_data_step' + str(step))()

        dict['screen_name'] = 'reports.form.step' + str(step_next)
        dict['data'] =  getattr(self, 'fill_data_step' + str(step_next))()

        message_name = ""
        message_type = ""
        if self.session.data['new_report'] == {}:
            message_name = dict['data']['name_report']

            if len(report) > 0:
                message_type = report['id_report_type']

            elif 'message_type' in dict['data']:
                message_type = dict['data']['message_type']
        else:
            message_name = self.session.data['new_report']['name']
            message_type = self.session.data['new_report']['type']

        data = {}
        data['id_lang'] = self.session.data['id_lang']
        data['id_report_type'] = message_type
        self.execute('get_report_type', data, False)
        message_type_name = self.fetch('one')

        dict['data']['message'] = '<b>' + self.ConvertStrUnicode(message_name) + '</b><br /><span class="reports">' + str(message_type_name) + '</span><br />'

        return dict

    def mount_filters(self, dic, data, parent):
        #brk(host="localhost", port=9000)
        for value in dic:
            if self.already_div == False:
                data['pageContents'] += "AddDiv('" + parent + "',false,false);\n"
                self.already_div = True
            else:
                data['pageContents'] += "AddDiv('" + parent + "',true,true);\n"

            self.num_fields += 1
            divAtual = "filterDiv_" + str(self.num_fields)

            data['contentValues'] += "$('#field_" + str(self.num_fields) + "').val('" + value['field']+ "');\n"
            data['contentValues'] += "$('#condition_" + str(self.num_fields) + "').val('" + self.safe_encode_utf8(value['condition']).decode('utf8') + "');\n"

            if ('connector' in value):
                data['contentValues'] += "$('#connector_" + str(self.num_fields) + "').val('" + self.safe_encode_utf8(value['connector']).decode('utf8') + "');\n"

            if ('user_defined' in value and value['user_defined'] != ""):
                if value['user_defined'].lower() == "true":
                    data['contentValues'] += "$('#type_" + str(self.num_fields) + "').val('Variable');\n"
                else:
                    data['contentValues'] += "$('#type_" + str(self.num_fields) + "').val('Fixed');\n"
            else:
                data['contentValues'] += "$('#type_" + str(self.num_fields) + "').val('Field');\n"

            data['contentValues'] += "$('#type_" + str(self.num_fields) + "').change();\n"

            if ('field_lookup' in value):
                data['contentValues'] += "$('#anotherfield_" + str(self.num_fields) + "').val('" + value['field_lookup'] + "');\n"

            #brk(host="localhost", port=9000)
            if ('value' in value and value['value'] != ""):
                val = value['value'].replace("'", "\\" + "'").replace('&#34;', '"').replace('&#60;', '<').replace('&#62;', '>')
                data['contentValues'] += "$('#value_" + str(self.num_fields) + "').val('" + val + "');\n"
                data['contentValues'] += "$('#enum_" + str(self.num_fields) + "').val('" + val + "');\n"
                data['contentValues'] += "$('#anotherfield_" + str(self.num_fields) + "').val('" + val + "');\n"


            if len(value['childs']) > 0:
                self.mount_filters(value['childs'], data, divAtual)

    def fill_data_step1(self):
        data = {}
        data['position_focus'] = "$('#name_report').focus();"

        data['name_report'] = self.session.data.get('new_report', {'name':''})['name'].replace('"', '&#34;')

        self.execute ("get_reports_types", {'id_lang':self.session.data['id_lang']})
        types = self.fetch("all")

        return_types = []

        for type in types:
            if self.session.data.get('new_report', {'type':''})['type'] == type['id_report_type']:
                return_types.extend("<option  value='" + str(type['id_report_type']) + "' selected='selected'>" + type['type'] + "</option>")

                data['message_type'] = type['id_report_type']
            else:
                return_types.extend("<option  value='" + str(type['id_report_type']) + "'>" + type['type'] + "</option>")

        data['type'] = "".join(return_types)
        #self.session.data['new_report'] = {}

        return data

    def fill_data_step2(self):
        data = {}

        #brk(host="localhost", port=9000)

        self.get_fields_definition()

        field = self.session.data.get('new_report', {'field':''}).get('field', [])

        select = self.session.data.get('new_report', {'select':''}).get('select', [])

        group = self.session.data.get('new_report', {'group':''}).get('group', [])

        total = []
        total.append(self.session.data.get('new_report', {'total':{'name':''}}).get('total',{}).get('name',''))


        return_field = []
        return_select = []
        return_group = []
        return_total = []

        keys = self.order_keys

        for item in select:
            return_select.extend("<li id='" + item + "'>" + label_dict[self.fields_definition[item]['label']] + "</li>")
            keys.remove(item)

        for item in group:
            return_group.extend("<li id='" + item + "'>" + label_dict[self.fields_definition[item]['label']] + "</li>")
            keys.remove(item)

        if total[0] != '':
            return_total.extend("<li id='" + total[0] + "'>" + label_dict[self.fields_definition[total[0]]['label']] + "</li>")
            keys.remove(total[0])

        for item in keys:
            return_field.extend("<li id='" + item + "'>" + label_dict[self.fields_definition[item]['label']] + "</li>")

        data['field'] = "".join(return_field)
        data['select'] = "".join(return_select)
        data['group'] = "".join(return_group)
        data['total'] = "".join(return_total)

        return data

    def fill_data_step3(self):
        #brk(host="localhost", port=9000)

        data = {}

        self.get_fields_definition()

        data['arrayFields'] = []
        data['arrayFieldsValues'] = []
        data['arrayFieldsDef'] = "{"
        data['arrayConnectors'] = []
        data['arrayConditions'] = []
        data['arrayTypes'] = []
        data['lang_code'] = self.session.data['label_lang_code']

        for key in self.order_keys:
            data['arrayFieldsValues'].append(str(key))
            data['arrayFields'].append(str(label_dict[self.fields_definition[key]['label']]))
            data['arrayFieldsDef'] += key + ": '" + str(self.fields_definition[key]['data_type']) +"', "

        data['arrayFieldsDef'] = data['arrayFieldsDef'][0:len(data['arrayFieldsDef'])-2] + "}";


        data['arrayConditions'] = [self.ConvertStrUnicode(_("Equals")),self.ConvertStrUnicode(_("Differs")), self.ConvertStrUnicode(_("Contains")),self.ConvertStrUnicode(_("In")),
                                   self.ConvertStrUnicode(_("Not in")),self.ConvertStrUnicode(_("Greater")),self.ConvertStrUnicode(_("Greater or equal")),
                                   self.ConvertStrUnicode(_("Less")),self.ConvertStrUnicode(_("Less or equal"))]

        data['arrayConnectors'] = ['AND','OR']

        data['arrayTypes'].append(self.ConvertStrUnicode(_('Fixed')))
        data['arrayTypes'].append(self.ConvertStrUnicode(_('Variable')))
        data['arrayTypes'].append(self.ConvertStrUnicode(_('Field')))

        data['enum_label_values'] = str(label_values_dict).replace(": u'",": '")
        data['enum_values'] = str(values_dict).replace(": u'",": '")

        if "filters" in self.session.data.get("new_report"):
            num_fields = 0;

            dicFilters = self.session.data.get("new_report").get("filters")
            data['startup'] = ''
            data['pageContents'] = ''
            data['contentValues'] = ''
            #brk(host="localhost", port=9000)
            self.mount_filters(dicFilters, data, 'filterDiv_0')
            x = 1
            while x <= self.num_fields:
                data['contentValues'] += ("validateField(" + str(x) + ",window.event);\n");
                x+= 1

            data['pageContents'] = "<script language='javascript'>" + data['pageContents'] + data['contentValues'] + "</script>"
        else:
            data['startup'] = "AddDiv('filterDiv_0', false, false);"

        return data

    def fill_data_step4(self):
        #brk(host="localhost", port=9000)

        data = {}

        self.get_fields_definition()

        #format options
        options = '<option value =1>' + label_dict['label_Rep_Default_HTML'] + '</option>'
        options = options + '<option value =2>' + label_dict['label_Rep_CSV'] + '</option>'
        options = options + '<option value =3>' + label_dict['label_Rep_Chart'] + '</option>'
        options = options + '<option value =4>' + label_dict['label_Rep_Custom_HTML'] + '</option>'
        options = options + '<option value =5>' + label_dict['label_Rep_XML'] + '</option>'

        data['format'] = options
        data['label_format'] = label_dict['label_Rep_Format']


        #default html options
        data['label_header'] = label_dict['label_Rep_Header']
        options = '<option value =1>' + label_dict['label_Rep_Internal'] + '</option>'
        options = options + '<option value =2>' + label_dict['label_Rep_External'] + '</option>'
        options = options + '<option value =3>' + label_dict['label_Rep_None'] + '</option>'
        data['options_header'] = options

        #csv options
        data['label_with_header'] = label_dict['label_Rep_Header']
        data['label_separator'] = label_dict['label_Rep_Separator']

        #chart options
        data['label_chart_type'] = label_dict['label_Rep_chart_type']
        options = '<option value =1>' + label_dict['label_Rep_Bar'] + '</option>'
        options = options + '<option value =2>' + label_dict['label_Rep_Pie'] + '</option>'
        options = options + '<option value =3>' + label_dict['label_Rep_Line'] + '</option>'
        options = options + '<option value =4>' + label_dict['label_Rep_Column'] + '</option>'
        data['options_chart_type'] = options


        #custom html options
        data['label_with_subcoll_template'] = label_dict['label_Rep_subcoll_template']
        data['label_header_template'] = label_dict['label_Rep_header_template']
        data['label_footer_template'] = label_dict['label_Rep_footer_template']
        data['label_data_template'] = label_dict['label_Rep_data_template']
        data['label_css_template'] = label_dict['label_Rep_css_template']

        #brk(host="localhost", port=9000)
        group = ''
        group_list = self.session.data.get('new_report', {'group':[]})['group']

        for item in group_list:

            groupitem = ''' <p>
                            <label for="id_label_@field_header" id="label_@field_header">@label_field_header</label><img src="../img/icon_fieldlink.png" title="%(label_Fieldlink_Support)s" alt="%(label_Fieldlink_Support)s" /><br /><br />
                                <div class="DivHtmlTemplate">
                                <div class="FieldLinkTab"><img style="cursor:pointer" onclick="return openFieldLinkPopUp('@field|header|@label_name', '@field', '@label_name');" src="../img/fieldlink.gif" /></div>
                                    <div class="DivTextAreaTemplate">
                                        <textarea class="HtmlTemplate" rows="5" cols="600"  id="@field|header|@label_name" name="@field_header"></textarea>
                                    </div>
                                </div>
                            </p>'''


            groupitem = groupitem.replace("@field", item)

            groupitem = groupitem.replace("@label_field_header", "Field " + label_dict[self.fields_definition[item]['label']] + " " + label_dict['label_Rep_header'])
            groupitem = groupitem.replace("@label_name", label_dict[self.fields_definition[item]['label']])

            group = group + groupitem

        data['group_header'] = group

        group = ''
        group_list.reverse()
        for item in group_list:


            groupitem = ''' <p>
                            <label for="id_label_@field_footer" id="label_@field_footer">@label_field_footer</label><img src="../img/icon_fieldlink.png" title="%(label_Fieldlink_Support)s" alt="%(label_Fieldlink_Support)s" /><br /><br />
                                <div class="DivHtmlTemplate">
                                <div class="FieldLinkTab"><img style="cursor:pointer" onclick="return openFieldLinkPopUp('@field|footer|@label_name', '@field', '@label_name');" src="../img/fieldlink.gif" /></div>
                                    <div class="DivTextAreaTemplate">
                                        <textarea class="HtmlTemplate" rows="5" cols="600"  id="@field|footer|@label_name" name="@field_footer"></textarea>
                                    </div>
                                </div>
                            </p>'''

            groupitem = groupitem.replace("@field", item)

            groupitem = groupitem.replace("@label_field_footer", "Field " + label_dict[self.fields_definition[item]['label']] + " " + label_dict['label_Rep_footer'])
            groupitem = groupitem.replace("@label_name", label_dict[self.fields_definition[item]['label']])

            group = group + groupitem

        data['group_footer'] = group

        #brk(host="localhost", port=9000)
        #data already loaded
        self.fill_session_data_step4('new_report', data)



        return data


    def fill_system_fieldlinks(self, data):

        data['label_Rep_fieldlink_Type'] = label_dict['label_Rep_fieldlink_Type']
        data['label_Rep_System_Fields'] = label_dict['label_Rep_System_Fields']
        data['label_Rep_Report_Fields'] = label_dict['label_Rep_Report_Fields']
        data['label_Rep_fieldlink_Insert'] = label_dict['label_Rep_fieldlink_Insert']
        data['label_Rep_fieldlink_Cancel'] = label_dict['label_Rep_fieldlink_Cancel']

        data['label_Rep_Date'] = label_dict['label_Rep_Date']
        data['label_Rep_Time'] = label_dict['label_Rep_Time']
        data['label_Rep_Name_Coll'] = label_dict['label_Rep_Name_Coll']
        data['label_Rep_Code_Coll'] = label_dict['label_Rep_Code_Coll']
        data['label_Rep_Name_Subcoll'] = label_dict['label_Rep_Name_Subcoll']
        data['label_Rep_Code_Subcoll'] = label_dict['label_Rep_Code_Subcoll']
        data['label_Rep_User'] = label_dict['label_Rep_User']
        data['label_Rep_Description'] = label_dict['label_Rep_Description']

        #brk(host="localhost", port=9000)
        if len(self.session.data.get('new_report', {})) > 0:

            self.get_fields_definition()
            options = ''
            list = self.session.data.get('new_report', {'select':[]}).get('select', [])

            if len(list) == 0:
                name = (self.session.data.get('new_report', {'total':{'name':'', 'function':''}}).get('total', {'name':'', 'function':''})['name'])
                f = self.session.data.get('new_report', {'total':{'name':'', 'function':''}}).get('total', {'name':'', 'function':''})['function']
                function = ''
                if f == 'count':
                    function = f + '(*)'
                    options = '<option value=\"' + name + '\">' + label_dict[self.fields_definition[name]['label']] + '</option>'
                elif f == 'sum':
                    function = f + '(' + name + ')'

                options+= '<option value=\"' + function + '\">' + label_dict['label_Rep_totalizer'] + '</option>'

            else:
                for field in list:
                    option = '<option value=\"' + field + '\">'
                    #tem que colocar o nome da label correta
                    option+= label_dict[self.fields_definition[field]['label']] + '</option>'
                    options+= option

            data['Report_Fields'] = options



    def fill_session_data_step4(self, name_report, data):

        import base64

        #brk(host="localhost", port=9000)
        if 'total' in self.session.data[name_report] and self.session.data[name_report]['total'] != {}:
            data['allow_chart'] = 'true';
        else:
            data['allow_chart'] = 'false';


        if 'format' in self.session.data[name_report]:
            format = self.session.data[name_report]['format']


            #default html
            if format == 'default':
                data['format'] = data['format'].replace('=1' , '=1 SELECTED')

                data['display_default_html'] = 'block'
                data['display_csv'] = 'none'
                data['display_chart'] = 'none'
                data['display_custom_html'] = 'none'

                header_position = self.session.data[name_report]['header_position']

                op = 1
                if header_position == 'internal':
                    op = 1
                elif header_position == 'external':
                    op = 2
                else:
                    op = 3

                data['options_header'] = data['options_header'].replace('=' + str(op), '=' + str(op) + ' SELECTED')

            #csv
            elif format == 'csv':
                data['format'] = data['format'].replace('=2' , '=2 SELECTED')
                data['display_default_html'] = 'none'
                data['display_csv'] = 'block'
                data['display_chart'] = 'none'
                data['display_custom_html'] = 'none'

                if self.session.data[name_report]['header'] == 'true':
                    data['with_header'] = 'checked=\"checked\"'
                else:
                    data['with_header'] = ''

                data['value_separator'] = self.session.data[name_report]['separator']


            #chart
            elif format == 'chart':
                data['format'] = data['format'].replace('=3' , '=3 SELECTED')
                data['display_default_html'] = 'none'
                data['display_csv'] = 'none'
                data['display_chart'] = 'block'
                data['display_custom_html'] = 'none'

                chart_type = self.session.data[name_report]['chart_type']
                op = 1
                if chart_type == 'bar':
                    op = 1
                elif chart_type == 'pie':
                    op = 2
                elif chart_type == 'line':
                    op = 3
                elif chart_type == 'column':
                    op = 4

                data['options_chart_type'] = data['options_chart_type'].replace('=' + str(op), '=' + str(op) + ' SELECTED')

            #custom html
            elif format == 'custom':

                import base64

                data['format'] = data['format'].replace('=4' , '=4 SELECTED')
                data['display_default_html'] = 'none'
                data['display_csv'] = 'none'
                data['display_chart'] = 'none'
                data['display_custom_html'] = 'inline-block'

                if self.session.data[name_report].get('append_subcoll_templates', 'false') == 'true':
                    data['with_subcoll_template'] = 'checked=\"checked\"'
                else:
                    data['with_subcoll_template'] = ''


                #brk(host="localhost", port=9000)
                data['value_header_template'] = (self.session.data[name_report]['templates']['main']['header'])
                data['value_footer_template'] = (self.session.data[name_report]['templates']['main']['footer'])
                data['value_data_template'] = (self.session.data[name_report]['templates']['main']['data'])
                data['value_css_template'] = (self.session.data[name_report]['templates']['main']['css'])

                group_list = list(self.session.data[name_report]['templates']['group'].keys())
                for field in group_list:
                    data['group_header'] = data['group_header'].replace('name=\"' + field + '_header\">' ,'name=\"' + field + '_header\">' + (self.session.data[name_report]['templates']['group'][field]['header']))
                    data['group_footer'] = data['group_footer'].replace('name=\"' + field + '_footer\">' ,'name=\"' + field + '_footer\">' + (self.session.data[name_report]['templates']['group'][field]['footer']))

            #xml
            elif format == 'xml':
                data['format'] = data['format'].replace('=5' , '=5 SELECTED')

                data['display_default_html'] = 'none'
                data['display_csv'] = 'none'
                data['display_chart'] = 'none'
                data['display_custom_html'] = 'none'

        else:
            data['display_default_html'] = 'block'
            data['display_csv'] = 'none'
            data['display_chart'] = 'none'
            data['display_custom_html'] = 'none'



    def fill_data_step5(self):
        #brk(host="localhost", port=9000)
        self.session.data['groups_table'] = ""
        self.session.save()

        action = ""

        if ('action' in self.session.data.get('new_report', {'action':''})) == False:
            action = "new"
        else:
            action = "edit"

        self.g.security_tab(self.cookie_value, action, self.session.data, 'reports')

        return self.session.data

    def save_data_step1(self):
        if ('new_report' in self.session.data) == False:
            self.session.data['new_report'] = {}

        if 'name_report' in self.form:
            self.session.data['new_report']['name'] = self.form['name_report'].value
        else:
            self.session.data['new_report']['name'] = ""

        if 'type' in self.form:

            if self.session.data['new_report']['type'] != int(self.form['type'].value):
                self.clean_session_report('new_report', 2)
                self.clean_session_report('new_report', 3)
                self.clean_session_report('new_report', 4)

            self.session.data['new_report']['type'] = int(self.form['type'].value)
        else:
            self.session.data['new_report']['type'] = ""

        self.session.save()

    def save_data_step2(self):
        #brk(host="localhost", port=9000)

        mudou = False

        selectAntigo = self.session.data['new_report'].get('select', [])

        if 'hdn_select' in self.form:
            self.session.data['new_report']['select'] = self.form['hdn_select'].value[1:-1].split(',')
        else:
            self.session.data['new_report']['select'] = []

        if selectAntigo != self.session.data['new_report'].get('select', []):
            mudou = True

        groupAntigo = self.session.data['new_report'].get('group', [])
        if 'hdn_group' in self.form:
            self.session.data['new_report']['group'] = self.form['hdn_group'].value[1:-1].split(',')
        else:
            self.session.data['new_report']['group'] = []

        if groupAntigo != self.session.data['new_report'].get('group', []):
            mudou = True

        totalAntigo = self.session.data['new_report'].get('total', {})
        total = {}
        if 'hdn_total' in self.form:
            self.get_fields_definition()
            total['name'] = self.form['hdn_total'].value[1:-1].split(',')[0]
            total['function'] = self.fields_definition[total['name']]['aggregate_function']

        self.session.data['new_report']['total'] = total

        if totalAntigo != total:
            mudou = True

        if mudou == True:
            self.clean_session_report('new_report', 3)
            self.clean_session_report('new_report', 4)

        self.session.save()


    def save_data_step3(self):
        #brk(host="localhost", port=9000)

        if ('new_report' in self.session.data) == False:
            self.session.data['new_report'] = tmp
        else:
            if ('allFilters' in self.form):
                self.session.data['new_report']['filters'] = eval(self.form['allFilters'].value)

        self.session.save()

    def save_data_step4(self):
        #brk(host="localhost", port=9000)

        format = int(self.form['format'].value)

        #self.clean_session_report('new_report', 4)

        self.session.data['new_report']['format'] = format

        #default html
        if format == 1:

            self.session.data['new_report']['format'] = 'default'

            header_position = int(self.form['options_header'].value)

            if header_position == 1:
                header_position = 'internal'
            elif header_position == 2:
                header_position = 'external'
            else:
                header_position = 'none'

            self.session.data['new_report']['header_position'] = header_position

        # csv
        elif format == 2:

            self.session.data['new_report']['format'] = 'csv'
            if 'with_header' in self.form:
                header = self.form['with_header'].value
                if header == 'on':
                    self.session.data['new_report']['header'] = 'true'
                else:
                    self.session.data['new_report']['header'] = 'false'

            else:
                self.session.data['new_report']['header'] = 'false'

            if 'separator' in self.form:
                self.session.data['new_report']['separator'] = self.form['separator'].value
            else:
                self.session.data['new_report']['separator'] = ''


        #chart
        elif format == 3:

            self.session.data['new_report']['format'] = 'chart'
            chart_type = int(self.form['options_chart_type'].value)

            if chart_type == 1:
                self.session.data['new_report']['chart_type'] = 'bar'
            elif chart_type == 2:
                self.session.data['new_report']['chart_type'] = 'pie'
            elif chart_type == 3:
                self.session.data['new_report']['chart_type'] = 'line'
            elif chart_type == 4:
                self.session.data['new_report']['chart_type'] = 'column'
            else:
                self.session.data['new_report']['chart_type'] = 'bar'

        #custom html
        elif format == 4:
            import base64
            self.session.data['new_report']['format'] = 'custom'
            if 'with_subcoll_template' in self.form:
                with_subcoll_template = self.form['with_subcoll_template'].value
                if with_subcoll_template == 'on':
                    self.session.data['new_report']['append_subcoll_templates'] = 'true'
                else:
                    self.session.data['new_report']['append_subcoll_templates'] = 'false'
            else:
                self.session.data['new_report']['append_subcoll_templates'] = 'false'

            templates = {'main':{'data':'', 'header':'', 'footer':'', 'css':''}, 'group':''}

            #brk(host="localhost", port=9000)
            if 'header_template' in self.form:
                templates['main']['header'] = (self.form['header_template'].value)
            if 'footer_template' in self.form:
                templates['main']['footer'] = (self.form['footer_template'].value)
            if 'data_template' in self.form:
                templates['main']['data'] = (self.form['data_template'].value)
            if 'css_template' in self.form:
                templates['main']['css'] = (self.form['css_template'].value)

            group = {}
            group_list = self.session.data.get('new_report', {'group':[]})['group']

            #brk(host="localhost", port=9000)
            for field in group_list:
                group[field] = {'header':'', 'footer':''}
                if field + '_header' in self.form:
                    group[field]['header'] = (self.form[field + '_header'].value)
                if field + '_footer' in self.form:
                    group[field]['footer'] = (self.form[field + '_footer'].value)

            templates['group'] = group

            self.session.data['new_report']['templates'] = templates

        #xml
        elif format == 5:

            self.session.data['new_report']['format'] = 'xml'


        #brk(host="localhost", port=9000)
        self.session.save()


    def save_data_step5(self):
        #brk(host="localhost", port=9000)
        perm = {}
        for i in self.form:
            i_parts = i.split('_')
            if i_parts[0] == 'perm':
              role_id = i_parts[1]
              perm_value = self.form['perm_' + str(role_id)].value

              if perm_value == 'w' or perm_value == 'r' or role_id == '1':
                perm[int(str(role_id)+'L')] = perm_value

        self.session.data['new_report']['report_permissions'] = perm

        self.session.save()

    def get_fields_definition(self, id_report=None):
        #brk(host="localhost", port=9000)
        sql = '''
                SELECT
                    fields_definition
                FROM
                    report_types
                WHERE
                    id_report_type = '''

        if (id_report == None):
            id = self.session.data.get('new_report', {'type':'1'})['type']
        else:
            id = id_report

        sql = sql + str(id)

        self.execute("", fixed_sql = sql)
        data = self.fetch('columns')

        tmp = Xml("field", data['fields_definition'])
        self.fields_definition = tmp.get_dict('name', ['label', 'data_type', 'aggregate_function', 'label_value_lookup', 'function_lookup'])
        self.order_keys = []

        newArray = []
        for key,value in list(self.fields_definition.items()):
            dicTmp = label_dict[self.fields_definition[key]['label']] + "#" + key
            newArray.append(dicTmp)

        newArray = sorted(newArray)

        for x in newArray:
            self.order_keys.append(x.split("#")[1])

    def clean_session_report(self, name, step):

        if step == 2:
            if name in self.session.data:
                self.session.data[name]['field'] = []
                self.session.data[name]['select'] = []
                self.session.data[name]['group'] = []
                self.session.data[name]['total'] = {}

        elif step == 3:
            if name in self.session.data:
                self.session.data[name]['filters'] = {}

        elif step == 4:
            if name in self.session.data:
                if 'format' in self.session.data[name]:
                    self.session.data[name].pop('format')

                if 'header_position' in self.session.data[name]:
                    self.session.data[name].pop('header_position')

                if 'header' in self.session.data[name]:
                    self.session.data[name].pop('header')

                if 'separator' in self.session.data[name]:
                    self.session.data[name].pop('separator')

                if 'chart_type' in self.session.data[name]:
                    self.session.data[name].pop('chart_type')

                if 'append_subcoll_templates' in self.session.data[name]:
                    self.session.data[name].pop('append_subcoll_templates')

                if 'templates' in self.session.data[name]:
                    self.session.data[name].pop('templates')



    def decodeTemplates(self, dict):
        import base64

        dict['templates']['main']['header'] = base64.b64decode(dict['templates']['main']['header'])
        dict['templates']['main']['data'] = base64.b64decode(dict['templates']['main']['data'])
        dict['templates']['main']['footer'] = base64.b64decode(dict['templates']['main']['footer'])
        dict['templates']['main']['css'] = base64.b64decode(dict['templates']['main']['css'])

        group_list = list(dict['templates']['group'].keys())
        for field in group_list:
            dict['templates']['group'][field]['header'] =  base64.b64decode(dict['templates']['group'][field]['header'])
            dict['templates']['group'][field]['footer'] =  base64.b64decode(dict['templates']['group'][field]['footer'])


    def decodeFilters(self, filters):
        import base64
        #brk(host="localhost", port=9000)
        for filter in filters:
            if filter['value'] != '':
                filter['value'] = self.ConvertStrUnicode(base64.b64decode(filter['value']))

            if len(filter['childs']) > 0:
                filter['childs'] = self.decodeFilters(filter['childs'])

        return filters


    def ConvertStrUnicode(self, valor):
        retorno = '';
        if isinstance(valor, (int, float)):
            return str(valor)

        if isinstance(valor, bytes):
            retorno = valor.decode("utf8")
        else:
            retorno = str(valor)

        return retorno

    def safe_encode_utf8(self, valor):
        """Safely encode a value to UTF-8 bytes, handling both str and bytes inputs"""
        converted = self.ConvertStrUnicode(valor)
        if isinstance(converted, str):
            return converted.encode("utf8")
        elif isinstance(converted, bytes):
            return converted
        else:
            return str(converted).encode("utf8")
