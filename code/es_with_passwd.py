from elasticsearch import Elasticsearch


HOST = ''
port = 9200
user = ''
passwd = ''
es = Elasticsearch(hosts=HOST, http_auth=(user,passwd), port=port)
print(es.ping())