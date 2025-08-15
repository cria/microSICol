#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

#python imports
from os import pardir, sep, path, getcwd
#from dbgp.client import brk

#project imports
# from .external.BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup


class Xml(object):
    '''Aparentemente essa lib foi criada para lidar com dois padrões de arquivos 
       XML, ambos com apenas um nível abaixo da tag principal e sempre com o mesmo
       nome de tag. O primeiro padrão é utilizado pelo arquivo de configuração do 
       sistema (config.xml):
       <configs>
         <config name="config1">some value1</config>
         <config name="config2">some value2</config>
       </configs>
       O método "get" busca o conteúdo da tag com base no valor do atributo "name":
       xml = Xml('config', xml_content)
       config1 = xml.get('config1') # <- some value1
       O outro padrão é usado na configuração dos relatórios:
       <fields>
         <field name="id_doc" label="label_Rep_Doc_ID" data_type="integer" aggregate_function="count" />
         <field name="code" label="label_Rep_Doc_Code" data_type="varchar" aggregate_function="count" />
         <field name="qualifier" label="label_Rep_Doc_Qualifier" data_type="varchar" aggregate_function="count" />
      </fields>
      Para este padrão costuma-se usar o método get_dict:
      xml = Xml('config', xml_content)
      fields_def = xml.get_dict('name', ['label', 'data_type'])
      # {'id_doc': {'label': 'label_Rep_Doc_ID', 'data_type': 'integer'},
         'code': {'label': 'label_Rep_Doc_Code', 'data_type': 'varchar'},
         ...
      # }
    '''
    def __init__(self, tag_name, content):
        # Use 'xml' parser for XML files
        self.soup = BeautifulSoup(content, 'xml')
        self.tag_name = tag_name

    def get(self, name):
        tag = self.soup.find(self.tag_name, {'name': name})
        if not tag:
            return ''
        # Retorna o texto da tag (CDATA ou texto comum)
        return tag.get_text(strip=True)

    def get_dict(self, label, internal_labels):
        # Retorna um dicionário com o valor de 'label' como chave e os internos como dict
        result = {}
        for item in self.soup.find_all(self.tag_name):
            tmp = {}
            for int_label in internal_labels:
                if item.has_attr(int_label):
                    tmp[int_label] = item[int_label]
            result[item[label]] = tmp
        return result
