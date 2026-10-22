#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import re

from .dbconnection import dbConnection


class StrainFormatterError(Exception):
    pass


class StrainFormatter(object):
    def __init__(self, cookie_value='', conn=None):
        if (conn == None):
            conn = dbConnection(cookie_value)
            
        self.dbconnection = conn
        self.execute = self.dbconnection.execute
        self.cursor = self.dbconnection.cursor
        self.fetch = self.dbconnection.fetch

    def check_pattern(self, pattern):
        """
        Check if the given pattern is valid.
        """

        if not pattern.count('#'):
            raise StrainFormatterError("pattern '%s' does not have at least one #" % pattern)

        return True

    def convert_to_usual_pattern(self, pattern):
        """
        Convert the pattern with sharps to usual programming pattern.
        """

        self.check_pattern(pattern)

        sharp_count = pattern.count('#')
        pattern = pattern.replace('#' * sharp_count, '%%0%dd' % sharp_count)

        return pattern

    def get_division_list(self, id_subcoll):
        """
        Return a tuple with the list of division filtered by subcollection and
        language.
        """

        self.execute('get_division_list', {'id_subcoll': id_subcoll})
        divisions = self.fetch('all')

        return tuple(divisions)

    def get_division_pattern(self, id_division):
        """
        Return the pattern given a division id.
        """

        self.execute('get_division_pattern',
                     {'id_division': id_division})
        pattern = self.fetch('one')

        if not pattern:
            raise StrainFormatterError("division does not exists")

        return pattern

    def format_strain_code_with_division(self, code, id_division):
        """
        Return the formatted strain code given the number code and a division id.
        """

        pattern = self.get_division_pattern(id_division)
        formatted = self.format_strain_code_with_pattern(code, pattern)

        return formatted

    def format_strain_code_with_pattern(self, code, pattern):
        """
        Return the formatted strain code given the number code and the pattern
        to format.
        """

        sharp_count = pattern.count('#')

        try:
            code = int(code)
        except (ValueError, TypeError):
            raise StrainFormatterError('invalid numeric code')

        formatted = self.convert_to_usual_pattern(pattern) % code

        return formatted

    @staticmethod
    def format_subcoll_code_with_pattern(subcoll_code, pattern, acronym):
        """
        Return the strain subcollection code formatted with the division
        pattern, replacing the division fixed text by the subcollection
        acronym (e.g. pattern 'DIV-###', acronym 'CCbr', code 7 -> 'CCbr-007').

        Separators around the sharps are kept. If the pattern is missing or
        has no sharps, returns acronym-code.
        """

        if not subcoll_code:
            return ''

        subcoll_code = str(subcoll_code).strip()
        match = re.search('#+', pattern or '')
        if not match:
            return '%s-%s' % (acronym, subcoll_code)

        prefix = pattern[:match.start()]
        suffix = pattern[match.end():]

        #Replace the alphanumeric part of the fixed text (prefix first, else suffix) by the acronym
        alnum_span = re.compile(r'[^\W_](.*[^\W_])?', re.UNICODE)
        if alnum_span.search(prefix):
            prefix = alnum_span.sub(lambda m: acronym, prefix, count=1)
        elif alnum_span.search(suffix):
            suffix = alnum_span.sub(lambda m: acronym, suffix, count=1)
        else:
            prefix = acronym + prefix

        #Zero padding like the strain code; legacy non-numeric values are shown as they are
        if subcoll_code.isdigit():
            subcoll_code = '%0*d' % (len(match.group(0)), int(subcoll_code))

        return prefix + subcoll_code + suffix

    def insert_division(self, id_subcoll, pattern, division):
        """
        Insert a division given an subcoll id and a pattern.

        If the pattern is malformed raises an exception.
        """

        self.check_pattern(pattern)

        self.execute('insert_division', {'id_subcoll': id_subcoll,
                                         'pattern': pattern,
                                         'division': division, })
        self.execute('last_insert_id')

        id_division = self.fetch('one')

        self.dbconnection.connect.commit()

        return id_division

    def update_division_pattern(self, id_division, division, pattern, commit = True):
        """
        Update the division pattern and update all strains that are using this
        division id.

        If the pattern is malformed raises an exception.
        """

        self.check_pattern(pattern)

        self.execute('update_division_pattern',
                     {'division': division,
                      'pattern': pattern,
                      'id_division': id_division})

        self.execute('get_strain_by_division',
                     {'id_division': id_division})
        strains = self.fetch('all')

        for strain in strains:
            code = self.format_strain_code_with_pattern(strain['numeric_code'], pattern)
            self.execute('update_strain_code',
                         {'code': code,
                          'id_strain': strain['id_strain']})

        if commit:
            self.dbconnection.connect.commit()

        return len(strains)

    def delete_division(self, id_division):
        """
        Delete a whole division, if the division it's used by any strain raises
        an exception.
        """

        self.execute('count_strains_using_division', {'id_division': id_division, })
        total = self.fetch('one')
        if total:
            raise StrainFormatterError('division %s is in use' % id_division)

        self.execute('delete_division', {'id_division': id_division, })

        self.dbconnection.connect.commit()

        return True

    def division_select_options(self, id_subcoll, id_division=0):
        divisions = self.get_division_list(id_subcoll)
        div_options = []
        for division in divisions:
            if division['id_division'] == id_division:
                div_options.append('<option selected value="%s">%s</option>' % (division['id_division'], division['division']))
            else:
                div_options.append('<option value="%s">%s</option>' % (division['id_division'], division['division']))
        return "\n".join(div_options)

    def division_javascript_options(self, id_subcoll):
        divisions = self.get_division_list(id_subcoll)
        js_strain_format = []
        for division in divisions:
            js_strain_format.append("strain_format['%s'] = '%s';" % (division['id_division'],
                                                                     self.convert_to_usual_pattern(division['pattern'])))
        return "\n".join(js_strain_format)
