import json

from elasticsearch import Elasticsearch

es = Elasticsearch(hosts='localhost:9200')

filter_query = {
    "query": {
        "bool": {
            "must": {"match_all": {}},
            "filter": {
                "range": {
                    "balance": {
                        "gte": 20000,
                        "lte": 30000
                    }
                }
            }
        }
    }
}
search = es.search(index='bank', body=filter_query)
search_info = json.dumps(search, indent=2, ensure_ascii=False)
print(search_info)
