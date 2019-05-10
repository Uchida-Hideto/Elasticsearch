
import os
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
import docx

INDEX = 'text_docx'
PATH = '/home/1'

class ElasticClient():

	def __init__(self):
		self.es = Elasticsearch()

	def get_index(self, index=INDEX):
		# check the index whether it exist or not
		indexcli = IndicesClient(self.es)
		# if the index exist the value is True ,else if False
		index_status = indexcli.exists(index=index)
		return index_status

	def set_mapping_info(self):
		"""
		setting maping info to index
		:return:
		"""
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

	def create_index(self):
		"""
		create index
		:return:
		"""
		self.es.indices.create(index=INDEX,ignore=400)
		self.set_mapping_info()

	def insert_data_to_es_index(self):
		"""
		insert data(read from file ) to es index
		:return:
		"""

		# if not index ,create it
		index_status = self.get_index()
		if not index_status:
			self.create_index()

		# judge the file exist or not
		# if not file do nothing and return
		# if file exist insert it to index
		file_name_list = os.listdir(PATH)
		if not file_name_list:
			return
		for file_name in file_name_list:
			file_name_dir = os.path.join(PATH, file_name)

			# read the file by third module python-docx
			data = docx.Document(file_name_dir)
			data_list = []
			for index, paras in enumerate(data.paragraphs):
				data_list.append(paras.text)
			data_str = ''.join(data_list)
			es_data = {
				'title': '{}'.format(file_name),
				'content': '{}'.format(data_str)
			}
			insert_data = self.es.index(index=INDEX, body=es_data,id=1)

			# after insert data ,remove the file
			#os.remove(file_name_dir)

if __name__ == '__main__':
    es = ElasticClient()
    es.insert_data_to_es_index()






