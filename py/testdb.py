#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

import mysql.connector as mysql
import socket
from sys import exit


class Test(object):

    def __init__(self):
        pass

    def get_local_ip(self):
        """Obtém o IP real da máquina"""
        try:
            # Conecta a um socket UDP externo para descobrir o IP local
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))  # Google DNS
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            # Fallback para gethostbyname se o método anterior falhar
            return socket.gethostbyname(socket.gethostname())

    def conexao(self):
        connect = None
        try:
            local_ip = self.get_local_ip()
            print(f'IP real detectado: {local_ip}')

            connect = mysql.connect(
                    host=local_ip,
                    user='sicol',
                    password='sicol',
                    database='sicol_v110',
                    port=3306,
                    use_unicode=True,
                    charset='utf8'
                )
            # connect = mysql.connect('localhost','root','sicol','sicol',3306)#,use_unicode=True,charset='utf8')
        except mysql.Error as e:            
            print("Error %d: %s" % (e.args[0],e.args[1]))
            exit(1)
        except:
            raise
        else:
            print('Conexao Efetuada...OK...')
            cursor = connect.cursor()
            try:
                cursor.execute('SELECT place FROM str_collection_event WHERE id_strains=\'0018\';')
            except mysql.Error as e:
                print("Error %d: %s" % (e.args[0],e.args[1]))                
                exit(1)
            except:
                raise
            else:
                print('SELECT executado...OK...')
            a = cursor.fetchone()[0]
            print(a.decode('iso-8859-1'))
            print('encode: ', a.encode('utf8'))
            # print 'encode: ',a.encode('latin1')
            # print 'normal: ',unicode(a,'utf8')
        exit(0)


if __name__ == '__main__':
    Test().conexao()
