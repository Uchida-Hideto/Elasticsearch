import os
import time
import logging
import docx
from win32com import client as wc

import configparser
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
# from win32com import client
current_path = str(os.getcwd())
CONF_PATH = r'{}\elastic.conf'.format(current_path)

# LOGPATH = r'C:\Users\houji\Desktop'
# TIMESPAN = 60
# INDEX = 'test_index0'
# FILEPATH = r'C:\Users\houji\Desktop\Code'
# HOSTS = '192.168.127.132:9200'

# read config
current_path = os.getcwd()
cf_parser = configparser.ConfigParser()
cf_parser.read(CONF_PATH)
LOGPATH = cf_parser.get('DEFAULT', 'LOGPATH')
LOGNAME = cf_parser.get('DEFAULT', 'LOGNAME')
TIMESPAN = int(cf_parser.get('DEFAULT', 'TIMESPAN'))
INDEX = cf_parser.get('DEFAULT', 'INDEX')
FILEPATH = cf_parser.get('DEFAULT', 'FILEPATH')
HOSTS = cf_parser.get('DEFAULT', 'HOSTS')

# add log handler
LOG = logging.getLogger('Insert_ES_index')
LOG.setLevel(level=logging.DEBUG)
file_handler = logging.FileHandler(r'{}\{}'.format(LOGPATH, LOGNAME))
file_handler.setLevel(level=logging.DEBUG)
log_format = logging.Formatter('%(asctime)s %(name)s %(process)d %(levelname)s %(message)s')
file_handler.setFormatter(log_format)
LOG.addHandler(file_handler)


class ElasticClient(object):

    def __init__(self):
        self.es = Elasticsearch(hosts=HOSTS)

    def ping(self):
        """
        This function will determine whether the
        elasticsearch service is running normally or not.
         :return:
        """
        ping_status = self.es.ping()
        # LOG.info('The Elasticsearch service status is {}'.format(ping_status))

        return ping_status

    def get_index(self, index=INDEX):
        """
        get the index status
        :param index:
        :return: True or False
        """
        try:
            indexcli = IndicesClient(self.es)
            index_status = indexcli.exists(index=index)
            LOG.info('Get index status successful ,index status is {}'.format(index_status))
            return index_status
        except Exception as e:
            LOG.error('Get index status failed ,cause {}'.format(e))

    def set_mapping_info(self):
        """
        setting maping info to index
        :return:
        """
        try:
            mapping = {
                'properties': {
                    'content': {
                        'type': 'text',
                        'analyzer': 'ik_max_word',
                        'search_analyzer': 'ik_max_word'
                    }
                }
            }
            update_mapping = self.es.indices.put_mapping(index=INDEX, body=mapping, ignore=400)
            LOG.info('Set Elasticsearch mapping info successful,return message is {}'.format(update_mapping))
            return update_mapping
        except Exception as e:
            LOG.error('Set Elasticsearch mapping info failed ,cause {}'.format(e))
            return None

    def create_index(self):
        """
        create index
        :return:
        """
        try:
            index_info = self.es.indices.create(index=INDEX, ignore=400)
            mapping_info = self.set_mapping_info()
            LOG.info('Create Elasticsearch index successful ,create info is {} {}'.format(index_info, mapping_info))

        except Exception as e:
            LOG.error('Create Elasticsearch index failed ,cause {}'.format(e))

    def insert_data_to_es_index(self):
        """
        insert data(read from file ) to es index
        :return:
        """
        # if can not connection to es,it will return
        ping_status = self.ping()
        if not ping_status:
            LOG.warning('The Elasticsearch service is not run!')
            return
        # if no index ,create it
        index_status = self.get_index()
        if not index_status:
            LOG.info('Index is not exist ,start to create index')
            self.create_index()

        # judge the file exist or not
        # if file exist insert it
        file_name_list = os.listdir(FILEPATH)
        LOG.info('current file name list is {}'.format(file_name_list))
        if not file_name_list:
            LOG.info('The directory is empty')
            return

        for file_name in file_name_list:
            file_name_dir = os.path.join(FILEPATH, file_name)
            try:
                # if the file is doc save as docx
                if file_name.endswith('doc'):
                    convert_name = file_name_dir + 'x'
                    self.convert_to_docx(file_name_dir, convert_name)
                    # the file name is not convert filename,we will use the name as title
                    # and convert name use for open file and insert data
                    self.read_docx_file(file_name, convert_name)

                elif file_name.endswith('dot'):
                    convert_name = os.path.splitext(file_name_dir)[0] + '.docx'
                    self.convert_to_docx(file_name_dir, convert_name)
                    # the file name is not convert filename,we will use the name as title
                    # and convert name use for open file and insert data
                    self.read_docx_file(file_name, convert_name)

                # read the file by third module python-docx
                # if find temporary file ,we will not insert and will remove it
                elif file_name_dir.startswith('~$'):
                    os.remove(file_name_dir)
                    LOG.warning('This file is temporary file,should delete it')
                    break
                    
                elif file_name_dir.endswith('docx'):
                    self.read_docx_file(file_name,file_name_dir)
                    
            except Exception as e:
                LOG.error('Can not insert info to index ,cause {} filename is {}'.format(e,file_name_dir))
   
    def read_docx_file(self,file_name,file_name_dir):
        print(file_name)
        print(file_name_dir)
        data = docx.Document(file_name_dir)
        data_list = []
        for index, paras in enumerate(data.paragraphs):
            data_list.append(paras.text)
    
        # change the list to str
        data_str = ''.join(data_list)
        es_data = {
            'title': '{}'.format(file_name),
            'content': '{}'.format(data_str)
        }
        print(es_data)
    
        insert_data = self.es.index(index=INDEX, body=es_data)
        LOG.info(
            'Insert info to index successful ,filename is {} ,return message is {}'.format(file_name_dir,
                                                                                           insert_data))
        # after insert data ,remove the file
        os.remove(file_name_dir)

    def convert_to_docx(self, file_name_dir, converted_name):
        LOG.info('Start to Convert to docx, convert filename is {}'.format(file_name_dir))
        file_name = file_name_dir
        coverted_name = converted_name
        try:
            word_client = wc.Dispatch("Word.Application")
            doc = word_client.Documents.Open(file_name)
            # save the file as docx
            # print(docx_name)
            doc.SaveAs(coverted_name, 16)
            doc.Close()
            word_client.Quit()
            # if the convert sucessful ,remove it
            os.remove(file_name_dir)
        except Exception as e:
            if os.path.exists(file_name):
                os.remove(coverted_name)
            print('convert the file {} failed,cause by {}'.format(file_name_dir, e))
        return coverted_name


if __name__ == '__main__':
    print(CONF_PATH)
    es = ElasticClient()
    while True:
        es.insert_data_to_es_index()
        time.sleep(TIMESPAN)
