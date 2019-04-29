from elasticsearch import Elasticsearch
import logging

LOG = logging.getLogger('Paging-Search')
LOG.setLevel(level=logging.DEBUG)
file_handler = logging.FileHandler('ElasticSearch.log')
file_handler.setLevel(level=logging.DEBUG)
log_format = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
file_handler.setFormatter(log_format)
LOG.addHandler(file_handler)


class PagingSearch(object):
    def __init__(self):

        self.es = Elasticsearch('localhost:9200')

    def ping(self):
        try:
            self.es.ping()
            LOG.info('Connection ElasticSearch Success!')
        except Exception as e:
            LOG.error('Can not connection Elasticsearch cause {}'.format(e))

    def paging_search(self):
        index = 'bank'
        try:
            count = self.es.count(index=index)['count']
            LOG.info('Get the index {} count is {}'.format(index,count))
        except Exception as e:
            LOG.error('Can not get index {} count,cause {}'.format(index, e))
        page_line = 5
        page_remainder = count % page_line
        if page_remainder == 0:
            page = int(count/page_line)
        else:
            page = int(count/page_line+1)
        for i in range(0, page):
            dsl = {
                "query": {"match_all": {}},
                "from": i*page_line,
                "size": page_line
            }
            try:
                result = self.es.search(index=index, body=dsl)
                LOG.info('Get the result is {}'.format(result))
            except Exception as e:
                LOG.error('Can not paging search cause {}'.format(e))


if __name__ == '__main__':
    search = PagingSearch()
    search.ping()
    search.paging_search()
