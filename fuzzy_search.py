import json
import logging
from elasticsearch import Elasticsearch

LOG = logging.getLogger('Fuzzy-Search')
LOG.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('FuzzySearch.log')
file_handler.setLevel(logging.DEBUG)
log_format = logging.Formatter('%(asctime)s %(name)s %(process)d %(levelname)s %(message)s')
file_handler.setFormatter(log_format)
LOG.addHandler(file_handler)

class FuzzySearch(object):
    def __init__(self):
        self.es  = Elasticsearch('localhost:9200')

    def ping(self):
        try:
            self.es.ping()
            LOG.info('Connection ElasticSearch Successful')
        except Elasticsearch as e:
            LOG.error('Connection Elasticsearch Failed, cause {}'.format(e))

    def fuzzy_search(self, text, fuzziness=1):
        dsl = {
            "query": {
                "match": {
                    "doc": {
                        "query": '{}'.format(text),
                        "fuzziness": '{}'.format(fuzziness)
                    }
                }
            }
        }
        search = self.es.search(index='bank',body=dsl)
        search_info = json.dumps(search, indent=2, ensure_ascii=False)
        LOG.info('Get the Search result is {}'.format(search_info))


if __name__ == '__main__':
    fuzzy = FuzzySearch()
    fuzzy.ping()
    fuzzy.fuzzy_search('lane', 1)
