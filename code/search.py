import json
from elasticsearch import Elasticsearch


class ElasticSearchTest(object):
    def __init__(self):
        self.es = Elasticsearch()

    def create_index(self):
        # add mapping info
        mapping = {
            'properties': {
                'title': {
                    'type': 'text',
                    'analyzer': 'ik_max_word',
                    'search_analyzer': 'ik_max_word'
                }
            }
        }

        self.es.indices.create(index='news_politics', ignore=400)
        update_mapping = self.es.indices.put_mapping(index='news_politics',body=mapping, ignore=400)
        print(update_mapping)

    def insert_data(self):
        datas = [

            {
                'title': '美国留给伊拉克的是个烂摊子吗',
                'url': 'http://view.news.qq.com/zt2011/usa_iraq/index.htm',
                'date': '2011-12-16'
            },
            {
                'title': '公安部：各地校车将享最高路权',
                'url': 'http://www.chinanews.com/gn/2011/12-16/3536077.shtml',
                'date': '2011-12-16'
            },
            {
                'title': '中韩渔警冲突调查：韩警平均每天扣1艘中国渔船',
                'url': 'https://news.qq.com/a/20111216/001044.htm',
                'date': '2011-12-17'
            },
            {
                'title': '中国驻洛杉矶领事馆遭亚裔男子枪击 嫌犯已自首',
                'url': 'http://news.ifeng.com/world/detail_2011_12/16/11372558_0.shtml',
                'date': '2011-12-18'
            }
        ]
        for data in datas:
            insert_data = self.es.index(index='news_politics', body=data)
            print('add data successful {}'.format(insert_data))

    def search(self):
        search_info = self.es.search(index='news_politics')
        print('get the search info {}'.format(search_info))

    def query_search(self, key_word):
        # full text search

        dsl = {
            'query': {
                'match': {
                    'title': '{}'.format(key_word)
                }
            }
        }
        search = self.es.search(index='news_politics', body=dsl)
        search_info = json.dumps(search, indent=2, ensure_ascii=False)
        print(search_info)


if __name__ == '__main__':
    elastic = ElasticSearchTest()
    #elastic.create_index()
    #elastic.insert_data()
    elastic.search()
    elastic.query_search('伊拉克 中国')
