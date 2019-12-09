from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from elasticsearch.client import CatClient
import json
host = '192.168.15.168'

es = Elasticsearch(hosts=host)
print(es.ping())

index_cli = IndicesClient(es)
# print(index_cli)
cat_cli = CatClient(es)

all_index = cat_cli.indices()
# print(all_index)

# get all index name
index_list_source = all_index.split('\n')[:-1]
index_list = []
for i in index_list_source:
    index = i.split()[2]
    index_list.append(index)

# print(index_list)

# get index  mapping info
for i in index_list:
    mapping_info = index_cli.get_mapping(index=i)
    mapping_info = json.dumps(mapping_info, indent=2,ensure_ascii=False)
    print('============')
    # print(i,mapping_info)


# set index mapping info
index_last = index_list[0]
print(index_last)

# mapping = {
#     'properties': {
#         'text': {
#             'type': 'text',
#             'analyzer': 'ik_max_word',
#             'search_analyzer': 'ik_max_word'
#         },
#         'title': {
#             'type': 'text',
#             'analyzer': 'ik_max_word',
#             'search_analyzer': 'ik_max_word'
#         }
#     }
# }
# result = es.indices.put_mapping(index=index_last, body=mapping)
# print(result)

# rebuild index
# reindex_info = {
#     'source': {'index': '192.168.15.168'},
#     'dest': {'index':'new_192.168.15.168'}
# }
# reindex_info = es.reindex(body=reindex_info)
# print(reindex_info)


# create index alias

index_alias_info = {
    'actions': [
        {'add': {'index': 'new_192.168.15.168', 'alias': '192.168.15.168'}},
        {'remove_index': {'index': '192.168.15.168'}}
    ]
}
# result = index_cli.update_aliases(body=index_alias_info)
# print(result)
