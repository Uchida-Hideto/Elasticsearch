from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from elasticsearch.client import CatClient
import json

host = '127.0.0.1:9200'
es = Elasticsearch(hosts=host)
index_cli = IndicesClient(es)
cat_cli = CatClient(es)

index_list = cat_cli.indices()
print(index_list)
result = index_cli.get_settings(index="test_index0")

# result = json.dumps(result,indent=2)
print(result)
