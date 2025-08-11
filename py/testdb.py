#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import MySQLdb as mysql
from sys import exit

class Test(object):
    
    def __init__(self):
        pass
        
    def conexao(self):
        connect = None
        try:
            connect = mysql.connect('localhost','root','sicol','sicol',3306)#,use_unicode=True,charset='utf8')
        except mysql.Error, e:            
            print "Error %d: %s" % (e.args[0],e.args[1])
            exit(1)
        except:
            raise
        else:
            print 'Conexao Efetuada...OK...'
            cursor = connect.cursor()
            try:
                cursor.execute('SELECT place FROM str_collection_event WHERE id_strains=\'0018\';')
            except mysql.Error, e:
                print "Error %d: %s" % (e.args[0],e.args[1])                
                exit(1)
            except:
                raise
            else:
                print 'SELECT executado...OK...'
            a = cursor.fetchone()[0]
            print a.decode('iso-8859-1')
            print 'encode: ',a.encode('utf8')
            #print 'encode: ',a.encode('latin1')
            #print 'normal: ',unicode(a,'utf8')		
        exit(0)

if __name__ == '__main__':
    Test().conexao()
