from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
import json
import jieba
import math


# query_1 = {
#   "query": {"multi_match": {
#       "query": value,
#       "type": "most_fields",
#       "fields": "content",
#       "minimum_should_match":"100%"}},
#   "from": 0,
#   "highlight": {"fields": {
#         "content": {}}}
#   , "_source": ["title","highlight"]
# }

es = Elasticsearch(hosts='127.0.0.1:9200')
index_cli = IndicesClient(es)

multi_phase_query = {
    "query": {
        "match_phrase_prefix": {
            "title":{}
        }
    },
    "_source": ["title", "filepath", "time"]
}

prefix_query = {}
# value = ""
index = "test_index0"

seg_list = jieba.cut("测试字段",cut_all=False)
user_list = []
for i in seg_list:
    user_list.append(i)
num = math.ceil(len(user_list)/2)
print(num)
value = "".join(user_list[:num])
print(value)
print(user_list[:num])
multi_phase_query["query"]["match_phrase_prefix"]["title"]["query"] = value
multi_phase_query["query"]["match_phrase_prefix"]["title"]["slop"] = 50
multi_phase_query["query"]["match_phrase_prefix"]["title"]["max_expansions"] = 50
print(multi_phase_query)
result = es.search(index=index, body=multi_phase_query)
result = json.dumps(result, indent=2, ensure_ascii=False)
print(result)
