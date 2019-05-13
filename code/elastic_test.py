import os
import time
import logging

from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
import docx
from win32com import client

# word = client.Dispatch('Word.Application')

LOGPATH = r'C:\Users\houji\Desktop'
TIMESPAN = 60
INDEX = 'test_index0'
FILEPATH = r'C:\Users\houji\Desktop\Code'
HOSTS = '192.168.127.132:9200'


LOG = logging.getLogger('Insert_ES_index')
LOG.setLevel(level=logging.DEBUG)
file_handler = logging.FileHandler(r'{}\ElasticSearch_index.log'.format(LOGPATH))
file_handler.setLevel(level=logging.DEBUG)
log_format = logging.Formatter('%(asctime)s %(name)s %(process)d %(levelname)s %(message)s')
file_handler.setFormatter(log_format)
LOG.addHandler(file_handler)



class ElasticClient(object):

    def __init__(self):
        self.es = Elasticsearch(hosts=HOSTS)
        self.word_client = client.Dispatch("Word.Application")

    def ping(self):
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
        # if not index ,create it
        index_status = self.get_index()
        if not index_status:
            LOG.info('Index is not exist ,start to create index')
            self.create_index()

        # judge the file exist or not
        # if file exist insert it
        file_name_list = os.listdir(FILEPATH)
        if not file_name_list:
            LOG.info('The directory is empty')
            return

        for file_name in file_name_list:
            file_name_dir = os.path.join(FILEPATH, file_name)
            try:
                # if the file is doc save as docx
                # if file_name.endswith('doc'):
                # 	self.dox_to_docx(file_name_dir)

                # read the file by third module python-docx
                if file_name_dir.endswith('docx'):
                    data = docx.Document(file_name_dir)
                    data_list = []
                    for index, paras in enumerate(data.paragraphs):
                        data_list.append(paras.text)
                    data_str = ''.join(data_list)
                    es_data = {
                        'title': '{}'.format(file_name),
                        'content': '{}'.format(data_str)
                    }
                    insert_data = self.es.index(index=INDEX, body=es_data)
                    LOG.info(
                        'Insert info to index successful ,filename is {} ,return message is {}'.format(file_name_dir,
                                                                                                       insert_data))
            except Exception as e:
                LOG.error('Can not insert info to index ,cause {}'.format(e))

                # after insert data ,remove the file
            os.remove(file_name_dir)

    # def dox_to_docx(self, file_name_dir):
    #     try:
    #         doc_name = file_name_dir
    #         doc = self.word_client.Documents.Open(doc_name)
    #         # save the file as docx
    #         docx_name = 'x'.join(doc_name)
    #         doc.SaveAs(docx_name, 16)
    #         # if the convert sucessful ,remove it
    #         os.remove(file_name_dir)
    #     except Exception as e:
    #         print('convert the file {} failed,cause by {}'.format(file_name_dir, e))

# def processfunc(self,file_name):
# 	file_name_dir = os.path.join(PATH, file_name)
#
# 	# read the file by third module python-docx
# 	data = docx.Document(file_name_dir)
# 	data_list = []
# 	for index, paras in enumerate(data.paragraphs):
# 		data_list.append(paras.text)
# 	data_str = ''.join(data_list)
# 	es_data = {
# 		'title': '{}'.format(file_name),
# 		'content': '{}'.format(data_str)
# 	}
# 	insert_data = self.es.index(index=INDEX, body=es_data)
#
# 	# after insert data ,remove the file
# 	os.remove(file_name_dir)


if __name__ == '__main__':
    es = ElasticClient()
    while True:
        es.insert_data_to_es_index()
        time.sleep(TIMESPAN)
