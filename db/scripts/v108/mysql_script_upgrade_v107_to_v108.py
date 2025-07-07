import MySQLdb as mysql
import re

 
def dump_sql(table, sql):
    print("--")
    print("-- table %s"  % (table))
    print("--")
    print()
    print("LOCK TABLES `%s` WRITE;" % (table))
    print("/*!40000 ALTER TABLE `%s` DISABLE KEYS */;" % (table))
    print("DELETE FROM `%s`;" % (table))
    print(sql)
    print("/*!40000 ALTER TABLE `%s` ENABLE KEYS */;" % (table))
    print("UNLOCK TABLES;")
    print()

def run(cursor, sql):
    cursor.execute(sql)
    rows = cursor.fetchall()
    col_names = cursor.description
    data_dicts = []
    for line in rows:
        data_dict = {}
        for i in xrange (len(line)):
            data_dict[col_names[i][0]] = line[i]
        data_dicts.append(data_dict)
    return data_dicts

def italic(name):
    if re.match(r'^sp\.$', name):
        return name
    return '<i>%s</i>' % name

def fmt(attr):
    attr = attr.strip()
    if not attr:
        return 'NULL'

    return "'%s'" % attr

def isnumeric(obj):
    # consider only ints and floats numeric
    return isinstance(obj,int) or isinstance(obj,float)

def fmtsql(sql):
    pos = sql.rfind(',')
    sql = sql[0:pos] + ';' + sql[pos+1:]
    return sql

def fmtfield(val):
    if not val:
        return None
    
    val = val.replace("\n", r"\n")
    val = val.replace("'", r"\'")
    return val

# para cada especie
old_db = mysql.connect('localhost', 'root', 'tempra', 'sicol_v107_cbmai', 3306, use_unicode=True, charset='utf8')
new_db = mysql.connect('localhost', 'root', 'tempra', 'sicol_v108_cbmai', 3306, use_unicode=True, charset='utf8')

hierarchy_dict = {
    'genus': 18,
    'subgenus': 19,
    'species': 21,
}

subdiv_dict = {
    'var.': 23,
    'subsp.': 22,
    'f.': 25,
    'pv.': 29,
}

caseFormatters = { 
    'none': lambda name: name,
    'ucfirst': lambda name: name.capitalize(),
    'upper': lambda name: name.upper(), 
    'lower': lambda name: name.lower(), 
}

formatFormatters = {
    'none': lambda name: name,
    'italic': lambda name: italic(name),
    'bold': lambda name: '<b>%s</b>' % name,
}


formatters = {
    'string_case': caseFormatters,
    'string_format': formatFormatters,
}

#raise str(formatters['string_case']['ucfirst']('<i>Aspergillus</i>'))

cursor_new = new_db.cursor()
cursor = old_db.cursor()
sql = """
SELECT 
    id_species, id_coll, id_subcoll, id_taxon_group, genus, subgenus, species, author, 
    sub.subdiv, infra_name, infra_author, id_name_qualifier, taxon_ref, synonym, hazard_group, 
    hazard_group_ref, id_alt_states, alt_states_type, comments, last_update 
FROM 
    species 
    LEFT JOIN spe_subdiv sub USING (id_subdiv)
"""


# criar um nome cientifico
rows = run(cursor, sql)

field_names = []
for field in rows[0]:
    if field in ('genus', 'subgenus', 'species', 'author', 'subdiv', 'infra_name', 'infra_author'):
        continue

    field_names.append(field)
    
sql_sciname = "INSERT INTO scientific_names (id_sciname, hi_tax, sciname, sciname_no_auth) VALUES\n"
sql_sciname_hier = 'INSERT INTO scientific_names_hierarchy (id_sciname, id_hierarchy, value, author) VALUES\n'
sql_species_all = "INSERT INTO species (id_sciname, %s) VALUES\n" % (', '.join(field_names))

id_sciname = 1
for row in rows:
    sciname_dict = {}
    #sqls = []
    #sqls.append('-- Species %s - %s' % (row['id_species'], row['species']))
    
    sql_template = "(%s, %s, '%s', %s), -- %s\n"
    for key in row:
        if row[key]:
            if key in hierarchy_dict:
                auth_name = None
                if row['author'] and key == 'species':
                    author = "'" + fmtfield(row['author']) + "'"
                    auth_name = row['author']
                else:
                    author = 'NULL'
                id_hierarchy = hierarchy_dict[key]
                sciname_dict[id_hierarchy] = (row[key], auth_name)
                sql_sciname_hier += sql_template % (id_sciname, id_hierarchy, fmtfield(row[key]), author, key)

    if row['subdiv'] in subdiv_dict:
        if row['infra_author']:
            author = "'" + fmtfield(row['infra_author']) + "'"
        else:
            author = 'NULL'
        id_hierarchy = subdiv_dict[row['subdiv']] 
        sciname_dict[id_hierarchy] = (row['infra_name'], row['infra_author'])
        sql_sciname_hier += sql_template % (id_sciname, id_hierarchy, fmtfield(row['infra_name']), author, row['subdiv'])
    
    hrows = run(cursor_new, """
        SELECT 
            id_hierarchy, id_taxon_group, id_subcoll, seq, id_lang, rank, hi_tax, 
            has_author, use_author, in_sciname, required, important, string_case, 
            prefix, suffix, default_value, string_format
        FROM
            view_hierarchy
        WHERE
            id_taxon_group = %s AND id_lang = 1
        ORDER BY
            seq""" % (row['id_taxon_group']))
    
    hitax = ''
    sciname = ''
    sciname_no_auth = ''
        
    for hrow in hrows:
        if not hrow['id_hierarchy'] in sciname_dict:
            continue
        
        values = sciname_dict[hrow['id_hierarchy']]
        value = values[0]
        author = fmtfield(values[1])
        
        if value:
            temp = value
            for field in hrow:
                if hrow[field]:
                    if field in formatters:
                        format_function_dict = formatters[field]
                        format_function = format_function_dict[hrow[field]]
                        if format_function:
                            temp = format_function(temp)
            
            name = temp
            if hrow['prefix']:
                name = hrow['prefix'] + name
            if hrow['suffix']:
                name = name + hrow['suffix']
            
            if not hrow['hi_tax'] == 1:
                sciname_no_auth += name + ' '
            
            if author and hrow['has_author'] == 1 and hrow['use_author'] == 1:
                name += ' ' + author
            
            if hrow['hi_tax'] == 1:
                hitax += name + ' '
            else:
                sciname += name + ' '
    
    hitax = fmt(hitax)
    sciname = fmt(sciname)
    sciname_no_auth = fmt(sciname_no_auth)
    sql_sciname += '(%s, %s, %s, %s),\n' % (id_sciname, hitax, sciname, sciname_no_auth)
    
    sql_species = '(%s),\n'
    fields = ['id_sciname']
    values = [str(id_sciname)]
    
    for field in row:
        if field in ('genus', 'subgenus', 'species', 'author', 'subdiv', 'infra_name', 'infra_author'):
            continue
        
        fields.append(field)
        val = row[field]
        if not val:
            val = 'NULL'
        else:
            if isnumeric(val):
                val = str(val)
            else:
                val = fmtfield(str(val))
                val = "'%s'" % (str(val))
            
        values.append(val)
    
    sql_species_all += sql_species % (', '.join(values))
    
    id_sciname += 1

print("""/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
""")

dump_sql('scientific_names', fmtsql(sql_sciname));
dump_sql('scientific_names_hierarchy', fmtsql(sql_sciname_hier))
dump_sql('species', fmtsql(sql_species_all))

print("""/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;""")
