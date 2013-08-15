#!/usr/bin/env python
#-*- coding: utf-8 -*-

#python imports
#from dbgp.client import brk
from cgi import escape
from urlparse import urljoin
from re import findall
from sys import exit
from urllib import urlencode
import cgi

#project imports
from session import Session
from dbconnection import dbConnection
from reports_common import Reports_Common
from labels import label_dict
from dom_xml import Xml
from label_values_reports import label_values_dict
from label_values_reports import values_dict

class Chart_Report(Reports_Common):
    def __init__(self, param, cookie_value, conn=None):
        self.report_params = param
        self.fields_definition = {}
        self.code   = ""
        self.header = ""
        self.footer = ""
        self.css    = ""
        self.reserved_fields = {}        
            
        if (conn == None):
            conn = dbConnection(cookie_value)
            
        self.sqliteConnection = dbConnection()        
        self.executesqlite = self.sqliteConnection.execute
        self.fetchsqlite = self.sqliteConnection.fetch
            
        self.dbconnection = conn   
            
        self.execute = conn.execute
        self.fetch = conn.fetch
        self.cursor = conn.cursor
            
        self.session = Session()
        self.session.load(cookie_value)
            
        self.get_report_info()
        
        self.execute('get_lang_by_code', {'code': self.report_params['id_language']} )
        self.id_report_lang = self.fetch('one')
        
        self.colors = ["#4572A7","#AA4643","#89A54E","#C16100"]
        self.color_counter = 0
    
    def write_report(self, param, num_group_by, append_where):
        #brk(host="localhost", port=9000)
        
        import random
        import datetime
        
        id  = "id_" + str(str(datetime.datetime.now()) + str(random.random())).replace("-", "").replace(" ", "").replace(":", "").replace(".", "")
        
        output = ""
            
        space = ""
        i = 0
            
        while i < num_group_by:
            space = space + "<td>&nbsp &nbsp &nbsp &nbsp</td>"
            i = i + 1
            
        if len(param['group']) == 0 or num_group_by >= len(param['group']):
            #print space, "Final"
            #brk(host="localhost", port=9000)    
            select, aggr = self.mount_total(param['total']['name'], param['total']['function'])      
                
            group = []
            group.append(param['total']['name'])
                
            try:
                list = self.get_data(select, param['filters'], append_where, group)
            except Exception, err:
                    raise err
                
            output = output + "<tr>" + space + "<td colspan=2>"                
                
            chart = ""
                
            if param['chart_type'] == 'bar':
                chart = self.write_bar_chart(id, id, "slice", list, param['total']['name'], aggr)
            elif param['chart_type'] == 'pie':
                chart = self.write_pie_chart(id, id, "slice", list, param['total']['name'], aggr)
            elif param['chart_type'] == 'line':
                chart = self.write_line_chart(id, id, "slice", list, param['total']['name'], aggr)
            elif param['chart_type'] == 'column':
                chart = self.write_column_chart(id, id, "slice", list, param['total']['name'], aggr)
                
            output = output + chart + "</td><tr>"
            
        else:        
            select = []
            select.append(param['group'][num_group_by])        
            group = []
            group.append(param['group'][num_group_by])
                  
            try:          
                list_group = self.get_data(select, param['filters'], append_where, group, True)
            except Exception, err:
                    raise err
            
            for item in list_group:
                colspan = len(param['group']) + len(param['select']) - num_group_by
                colspan = colspan + 1
                if len(param['total']) > 0:
                    colspan = colspan + 1
                
                output = output + "<tr>" + space + "<td class=\"group\" colspan=\"" + str(colspan) + "\">" +  self.process_field(param['group'][num_group_by], item[param['group'][num_group_by]]) + "</td>" + "</tr>\n"
                
                group_value = ''
                tmp = type(item[param['group'][num_group_by]]).__name__
                if tmp != "str":
                    group_value = param['group'][num_group_by] + " LIKE x'" + self.ConvertStrUnicode(item[param['group'][num_group_by]]).encode("utf-8").encode("hex") + "' "
                else:
                    group_value = param['group'][num_group_by] + " IS NULL "
                    
                output = output + self.write_report(param, 1 + num_group_by, append_where + " AND " + group_value)
                    
        return output

    def get_report_info(self):
        #brk(host="localhost", port=9000)
        sql = '''
                SELECT reports.id_subcoll as id_subcoll,
                    report_types.code as code,
                    report_types.fields_definition as fields_definition
                    FROM
                    (reports JOIN report_types on reports.id_report_type = report_types.id_report_type)
                    WHERE reports.id_report = '''
        sql = sql + str(self.report_params['id_report'])
        
        self.execute("", fixed_sql = sql)
        data = self.fetch('all')              
        
        sqlite = '''
                    SELECT subcoll_report_conf.header as header,
                    subcoll_report_conf.footer as footer,
                    subcoll_report_conf.styles as styles,
                    coll.code as code_coll,
                    coll.name as name_coll,
                    subcoll.code as code_subcoll,
                    subcoll.name as name_subcoll                
                    
                        FROM
                        subcoll_report_conf JOIN subcoll on (subcoll_report_conf.id_subcoll = subcoll.id_subcoll)
                        JOIN coll on (subcoll.id_coll = coll.id_coll)
                        
                        WHERE subcoll_report_conf.id_subcoll = '''
        sqlite = sqlite + str(data[0]['id_subcoll'])
        
        self.executesqlite("", fixed_sql = sqlite)
        data_sqlite = self.fetchsqlite('all')
       
        
        
        tmp = Xml("field", data[0]['fields_definition'])        
        self.fields_definition = tmp.get_dict('name', ['label', 'data_type', 'aggregate_function', 'label_value_lookup', 'function_lookup'])
        
        #brk(host="localhost", port=9000)
        
        self.header            =     data_sqlite[0]['header']
        self.footer            =     data_sqlite[0]['footer']
        self.css               =     data_sqlite[0]['styles']
        
        self.reserved_fields['code_coll']       = data_sqlite[0]['code_coll']
        self.reserved_fields['name_coll']       = data_sqlite[0]['name_coll']
        self.reserved_fields['code_subcoll']    = data_sqlite[0]['code_subcoll']
        self.reserved_fields['name_subcoll']    = data_sqlite[0]['name_subcoll']
        
        self.reserved_fields['user']            = self.session.data['user_name']
        
        
        self.code = data[0]['code']   
    
    def mount_report_file(self):
        #brk(host="localhost", port=9000)
        
        self.timeout = 0
        
        import base64
        
        output = "<html>\n"
        output = output + "<head>\n"
        output = output + self.getPageTitle()
        output = output + "<style type=\"text/css\">\n"
        output = output + self.ConvertStrUnicode(base64.b64decode(self.css)) + "\n"
        output = output + "</style>\n"
            
        output = output + '''
                            <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js" type="text/javascript"></script>
                            <script src="../js/external/highcharts.js" type="text/javascript"></script>
                          '''
            
        output = output + "\n</head>\n"
        output = output + "<body>\n"
        output = output + self.fill_reserved_fields(self.header) + "\n"
            
        output = output + "<table border=1>\n"
           
        try: 
            table = self.write_report(self.report_params, 0, "")
        except Exception, err:
                    raise err
            
        output = output + table
            
        output = output + "</table>\n"
        output = output + self.fill_reserved_fields(self.footer) + "\n"
        output = output + "</body>\n"
        output = output + "</html>\n"    
            
        return output
    
    def write_bar_chart(self, chart_name, container, name, list, field_name, aggr_func):
        categories = "["
        data = "["
            
        max = 0
            
        for line in list:
            string = ''
            if line.has_key(field_name):
                string = self.process_field(field_name, line[field_name])
            else:
                string = label_dict[self.fields_definition.get(field_name, {'label':''})['label']]
            if len(string) > max:
                max = len(string)
            
            if string == "":
                string = " ";
            
            item  = "'" + string + "', "
            value = str(line[aggr_func]) + ", "
                
            categories = categories + item
            data = data + value
                
        if len(data) == 1:
            data = data + "]"
        else:
            data = data[:len(data)-2] + "]"
            
        if len(categories) == 1:
            categories = categories + "]"
        else:
            categories = categories[:len(categories)-2] + "]"

        width = "750px"
        height = str(70 + 35 * len(list)) + "px"
            
        string = '''
            <script type="text/javascript">		
                var chart;
                $(document).ready(function() {
                    @chart_name = new Highcharts.Chart({
                        chart: {
                            renderTo: '@container',
                            defaultSeriesType: 'bar'
                        },
                        title: {
                            text: ""
                        },
                        credits: {
                                enabled: false
                            },                    
                        xAxis: {
                            categories: @categories,
                            labels: {
                                align: 'right',
                                rotation: 315
                            }
                        },
                        yAxis: {
                            min: 0,
                            allowDecimals: false,
                            title: {
                                    text: 'Total'
                            },
                            labels: {
                                formatter: function() {
                                    return Highcharts.numberFormat(this.value, 0, '@decimal_separator', '@thousand_separator');
                                }
                            }
                        },
                        legend: {
                            layout: 'vertical',
                            align: 'right',
                            verticalAlign: 'top',
                            x: -10,
                            y: 1,
                            backgroundColor: '#FFFFFF'
                        },
                        tooltip: {
                            formatter: function() {
                                return '<b>' + this.x + '</b>: '+ Highcharts.numberFormat(this.y, 0, '@decimal_separator', '@thousand_separator');
                            }
                        },
                        plotOptions: {
                        },
                        series: [{
                            name: '@field_name',
                            data: @data,
                            color: '@color'
                        }]
                    });			
                });
            </script>
                
            <div id="@container" style="width: @width; height: @height; margin: 0 auto"></div>
        '''
        
        if self.session.data['id_lang'] == 1:
            decimal_separator = '.'
            thousand_separator = ','
        else:
            decimal_separator = ','
            thousand_separator = '.'
            
        string = string.replace('@chart_name', chart_name)
        string = string.replace('@field_name', label_dict[self.fields_definition[field_name]['label']])
        string = string.replace('@container', container)
        string = string.replace('@data', data)
        string = string.replace('@categories', categories)
        string = string.replace('@width', width)
        string = string.replace('@height', height)
        string = string.replace('@decimal_separator', decimal_separator)
        string = string.replace('@thousand_separator', thousand_separator)
        
        string = string.replace('@color', self.colors[self.color_counter%len(self.colors)])
        self.color_counter+= 1
            
        return string

    def write_pie_chart(self, chart_name, container, name, list, field_name, aggr_func):
        #brk(host="localhost", port=9000)
        total = 0
        data = "[ "
        
        for line in list:
            temp = ''
            if line.has_key(field_name):
                temp = self.process_field(field_name, line[field_name])
            else:
                temp = label_dict[self.fields_definition.get(field_name, {'label':''})['label']]
                        
            if temp == "":
                temp = " ";
                
            item = "['" + temp + "', " + str(line[aggr_func]) + "]"
            
            total = total + line[aggr_func]
            
            data = data + item + ", "     
            
        if len(data) == 1:
            data = data + "]"
        else:
            data = data[:len(data)-2] + "]"

        width = "750px"
        height = "300px"
        
        string = '''
        <script type="text/javascript">		
            var chart;
                $(document).ready(function() {
                    @chart_name = new Highcharts.Chart({
                        chart: {
                                        renderTo: '@container',
                                        backgroundColor: '',
                                        plotBackgroundColor: null,
                                        plotBorderWidth: null,
                                        plotShadow: false
                                },
                        title: {
                                text: ''
                        },
                        credits: {
                                enabled: false
                            },                        
                        tooltip: {
                                formatter: function() {
                                    var total = @total;
                                    return '<b>' + this.point.name + '</b>: '+ Highcharts.numberFormat(Math.round((this.y/total*100)*10)/10, 1, '@decimal_separator', '@thousand_separator') + '%%';
                                }
                        },
                        plotOptions: {
                                pie: {
                                        allowPointSelect: true,
                                        cursor: 'pointer',
                                        dataLabels: {
                                                enabled: true,
                                                color: '#000000',
                                                connectorColor: '#000000',
                                                formatter: function() {
                                                        return '<b>'+ this.point.name +'</b>: '+ Highcharts.numberFormat(this.y, 0, '@decimal_separator', '@thousand_separator');
                                                }
                                        }
                                }
                        },
                        series: [{
                                    type: 'pie',
                                    name: '@name',
                                    data: @data
                            }]
                    });
                });				
        </script>
        <div id="@container" style="width: @width; height: @height; margin: 0 auto"></div>
        '''
        
        if self.session.data['id_lang'] == 1:
            decimal_separator = '.'
            thousand_separator = ','
        else:
            decimal_separator = ','
            thousand_separator = '.'
        
        string = string.replace('@chart_name', chart_name)
        string = string.replace('@container', container)
        string = string.replace('@name', name)
        string = string.replace('@data', data)
        string = string.replace('@total', str(total))
        string = string.replace('@width', width)
        string = string.replace('@height', height)
        string = string.replace('@decimal_separator', decimal_separator)
        string = string.replace('@thousand_separator', thousand_separator)
        
        return string
    
    def write_line_chart(self, chart_name, container, name, list, field_name, aggr_func):
        #brk(host="localhost", port=9000)
        categories = "["
        data = "["
            
        max = 0
            
        for line in list:
            string = ''
            if line.has_key(field_name):
                string = self.process_field(field_name, line[field_name])
            else:
                string = label_dict[self.fields_definition.get(field_name, {'label':''})['label']]
            
            if len(string) > max:
                max = len(string)
            
            if string == "":
                string = " ";
                
            item  = "'" + string + "', "
            value = str(line[aggr_func]) + ", "
                
            categories = categories + item
            data = data + value
                
        if len(data) == 1:
            data = data + "]"
        else:
            data = data[:len(data)-2] + "]"
            
        if len(categories) == 1:
            categories = categories + "]"
        else:
            categories = categories[:len(categories)-2] + "]"
            
        tw = 6
            
        if len(list) > 6:
            tw = len(list)
        
        width = str(100 * tw) + "px"
        height = "300px"
            
        string = '''
            <script type="text/javascript">		
                var chart;
                $(document).ready(function() {
                    @chart_name = new Highcharts.Chart({
                        chart: {
                            renderTo: '@container',
                            defaultSeriesType: 'line'
                        },
                        title: {
                            text: ""
                        },
                        credits: {
                                enabled: false
                            },                    
                        xAxis: {
                            categories: @categories,
                            labels: {
                                align: 'right',
                                rotation: 315
                            }
                        },
                        yAxis: {
                            min: 0,
                            allowDecimals: false,
                            title: {
                                    text: 'Total'
                            },
                            labels: {
                                formatter: function() {
                                    return Highcharts.numberFormat(this.value, 0, '@decimal_separator', '@thousand_separator');
                                }
                            }
                        },
                        legend: {
                            layout: 'vertical',
                            align: 'right',
                            verticalAlign: 'top',
                            x: -10,
                            y: 1,
                            backgroundColor: '#FFFFFF'
                        },
                        tooltip: {
                            formatter: function() {
                                return '<b>' + this.x +'</b>: '+ Highcharts.numberFormat(this.y, 0, '@decimal_separator', '@thousand_separator');
                            }
                        },
                        series: [
                            {
                                name: '@serie_name',
                                data: @serie_data,
                                color: '@color'
                            }
                        ]
                    });			
                });
            </script>
                
            <div id="@container" style="width: @width; height: @height; margin: 0 auto"></div>
        '''
            
        if self.session.data['id_lang'] == 1:
            decimal_separator = '.'
            thousand_separator = ','
        else:
            decimal_separator = ','
            thousand_separator = '.'
            
        string = string.replace('@chart_name', chart_name)
        string = string.replace('@container', container)
        string = string.replace('@serie_name', label_dict[self.fields_definition[field_name]['label']])
        string = string.replace('@serie_data', data)
        string = string.replace('@categories', categories)
        string = string.replace('@width', width)
        string = string.replace('@height', height)
        string = string.replace('@decimal_separator', decimal_separator)
        string = string.replace('@thousand_separator', thousand_separator)
        
        string = string.replace('@color', self.colors[self.color_counter%len(self.colors)])
        self.color_counter+= 1
            
        return string

    def write_column_chart(self, chart_name, container, name, list, field_name, aggr_func):
        categories = "["
        data = "["
            
        max = 0
            
        for line in list:
            string = ''
            if line.has_key(field_name):
                string = self.process_field(field_name, line[field_name])
            else:
                string = label_dict[self.fields_definition.get(field_name, {'label':''})['label']]
             
            if len(string) > max:
                max = len(string)
            
            if string == "":
                string = " ";
                
            item  = "'" + string + "', "
            value = str(line[aggr_func]) + ", "
                
            categories = categories + item
            data = data + value
                
        if len(data) == 1:
            data = data + "]"
        else:
            data = data[:len(data)-2] + "]"
            
        if len(categories) == 1:
            categories = categories + "]"
        else:
            categories = categories[:len(categories)-2] + "]"
            
        tw = 6
            
        if len(list) > 6:
            tw = len(list)
        
        width = str(75 * tw) + "px"
        height = "300px"
            
        string = '''
            <script type="text/javascript">		
                var chart;
                $(document).ready(function() {
                    @chart_name = new Highcharts.Chart({
                        chart: {
                            renderTo: '@container',
                            defaultSeriesType: 'column'
                        },
                        title: {
                            text: ""
                        },
                        credits: {
                                enabled: false
                            },                    
                        xAxis: {
                            categories: @categories,
                            labels: {
                                align: 'right',
                                rotation: 315
                            }
                        },
                        yAxis: {
                            min: 0,
                            allowDecimals: false,
                            title: {
                                    text: 'Total'
                            },
                            labels: {
                                formatter: function() {
                                    return Highcharts.numberFormat(this.value, 0, '@decimal_separator', '@thousand_separator');
                                }
                            }
                        },
                        legend: {
                            layout: 'vertical',
                            align: 'right',
                            verticalAlign: 'top',
                            x: -10,
                            y: 1,
                            backgroundColor: '#FFFFFF'
                        },
                        tooltip: {
                            formatter: function() {
                                return '<b>' + this.x +'</b>: ' + Highcharts.numberFormat(this.y, 0, '@decimal_separator', '@thousand_separator');
                            }
                        },
                        plotOptions: {
                        },
                        series: [{
                            name: '@field_name',
                            data: @data,
                            color: '@color'
                        }]
                    });			
                });
            </script>
                
            <div id="@container" style="width: @width; height: @height; margin: 0 auto"></div>
        '''
            
        if self.session.data['id_lang'] == 1:
            decimal_separator = '.'
            thousand_separator = ','
        else:
            decimal_separator = ','
            thousand_separator = '.'
           
        string = string.replace('@chart_name', chart_name)
        string = string.replace('@field_name', label_dict[self.fields_definition[field_name]['label']])
        string = string.replace('@container', container)
        string = string.replace('@data', data)
        string = string.replace('@categories', categories)
        string = string.replace('@width', width)
        string = string.replace('@height', height)
        string = string.replace('@decimal_separator', decimal_separator)
        string = string.replace('@thousand_separator', thousand_separator)
        
        string = string.replace('@color', self.colors[self.color_counter%len(self.colors)])
        self.color_counter+= 1
            
        return string
