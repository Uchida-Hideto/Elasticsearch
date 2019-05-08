1.创建索引

~~~
curl -X PUT 'http://localhost:9200/{索引名}'
~~~

2.查看已创建的所有索引

```
curl -X GET 'http://localhost:9200/_cat/indices?v&pretty'
```

3.索引一个文档

```
curl -H 'Content-Type:application/json' -X POST 'http://localhost:9200/{索引名}/{type类型名}/{文档id}?pretty' -d '{"name":"test"}'
```

- 创建索引文档是可以不必先创建索引，索引文档是会自动创建搜索引，如果创建索引文档时索引不存在的情况下。
- 在当前版本使用curl命令索引文档需要手动指定type类型为_doc
- 一个索引最好只有一个类型
- **从6.0.0开始限定仅包含一个映射类别定义（ "index.mapping.single_type": true ），兼容5.x中的多映射类别。从7.0开始将移除映射类别。**
  **为了与未来的规划匹配，请现在将这个唯一的映射类别名定义为“_doc”,因为索引的请求地址将规范为：PUT {index}/_doc/{id} and POST {index}/_doc**

4.查询指定的文档

```
curl -X GET 'http://localhost:9200/{索引名}/{type类型}/{文档id}'
```

只查询指定的字段

```
curl -X GET 'localhost:9200/test_index/_doc/1/_source?pretty'
```

5.删除索引

```
curl -X DELETE 'http://localhost:9200/{索引名}？pretty&pretty'
```

6.查看cluster状态

```
curl -X GET 'http://localhost:9200/_cat/health?v&pretty'
```

7.查看分片状态

```
curl -X GET 'http://localhost:9200/_cluster/health?pretty'
```

8.获取集群节点列表

```
curl -X GET 'http://localhost:9200/_cat/nodes?v&pretty'
```

9.1.索引替换文档内容，指定相同文档id即可替换

```
curl -H 'Content-Type:application/json' -X PUT 'http://localhost:9200/{索引名}/{type类型}/{文档id}' -d '{"name":"test2"}'
```

9.2更新文档

 ```
curl -H 'Content-Type:application/json' -X POST 'http://localhost:9200/test_index/_doc/1/_update?pretty' -d '{"doc":{"name":"test3"}}'
 ```

9.3更新文档同时添加新的字段

```
curl -H 'Content-Type:application/json' -X POST 'http://localhost:9200/test_index/_doc/1/_update?pretty' -d '{"doc":{"name":"hide","age":34}}'
```

10.1删除文档（通过指定id来进行删除）

```
curl -X DELETE 'http://localhost:9200/test_index/_doc/JTt-YmoBHEwUVvFEdcB3?pretty'
```

10.2删除文档（通过查询来进行删除）

```
curl -H 'Content-Type:application/json' -X POST 'localhost:9200/test_index/_doc/_delete_by_query?pretty' -d '{"query":{"match":{"name":"delete"}}}'
```

11.1批处理（索引文档）

```
curl -H 'Content-Type:application/json' -X POST 'localhost:9200/test_index/_doc/_bulk?pretty' -d '{"index":{"_id":"4"}}{"name":"uchida"}{"index":{"id":"5"}}{"name:"mushroom"}'
```

- body中需要添加换行

11.2批处理（更新）

```
curl -H 'Content-Type":application/json' -X POST 'localhost:9200/test_index/_doc/_bulk?pretty' -d '
{"update":{"_id":"1"}}
{"doc":{"name":"update_test"}}
{"update":{"_id":1}}
{"doc":{"age":"23"}}
'
```

11.3批处理（导入）

```
curl -H 'Content-Type:application/json' -X POST 'localhost:9200/bank/account/_bulk?pretty&fresh'--data-binary "@account.json 
curl -X GET 'localhost:9200/_cat/indices?v
```

12.1 搜索(搜索全部)

```
curl -X GET 'localhost:9200/bank/_search?q=*&sort=account_number:asc&pretty'
```

```
curl -H 'Content-Type:application/json' -X GET 'localhost:9200/bank/_search?pretty' -d '
{
"query":{"match_all":{}},
"sort":{"account_number":"asc"}
}
'
```

在响应中，我们可以看到以下几个部分 : 

- **took** - **Elasticsearch** 执行搜索的时间（毫秒）
- **time_out** - 告诉我们搜索是否超时
- **_shards** - 告诉我们多少个分片被搜索了，以及统计了成功/失败的搜索分片
- **hits** - 搜索结果
- **hits.total** - 搜索结果
- **hits.hits** - 实际的搜索结果数组（默认为前 **10** 的文档）
- **sort** - 结果的排序 **key**（键）（没有则按 **score** 排序）
- ***score*** 和 **max_score** -现在暂时忽略这些字段

12.2搜索(条件)

- 匹配指定字段

```
 curl -H 'Content-Type:application/json' -X GET 'localhost:9200/bank/_search?pretty' -d '{"query":{"match":{"account_number":"20"}}}'
```

- 匹配多个字段

```
curl -H 'Content-Type:application/json' -X GET 'localhost:9200/bank/_search?pretty' -d {"query":{"match":{"address":"mill lane"}}}
match匹配多个字段为或关系
```

```
curl -H 'Content-Type:application/json' -X GET 'localhost:9200/bank/_search?pretty' -d {"query":{"match_phrase":{"address":"mill lane"}}}
match_phrase匹配字段之间为与关系
```

- **bool** 查询

```
curl -H 'Content-Type:application/json' -X GET 'localhost:9200/bank/_search?pretty' -d '{"query":{"bool":{"must":[{"match":{"address":"mill"}},{"match":{"address":"lane"}}]}}}'
```

```
curl -H 'Content-Type:application/json' -X GET 'localhost:9200/bank/_search?pretty' -d '{"query":{"bool":{"should":[{"match":{"address":"mill"}},{"match":{"address":"lane"}}]}}}'
```

```
curl -H 'Content-Type:application/json' -X GET 'localhost:9200/bank/_search?pretty' -d '{"query":{"bool":{"must_not":[{"match":{"address":"mill"}},{"match":{"address":"lane"}}]}}}'
```

- **must** 查询到全为**True**的值
- **should** 查询到有一个或多个**True**的值
- **must_not** 查询到全不为**True**的值

13.过滤

```
curl -H 'Content-Type:application/json' -X GET 'localhost:9200/bank/_search?pretty' -d '{"query":{"bool":{"must":{"match_all":{}},"filter":{"range":{"balance":{"gte":"20000","lte":"30000"}}}}}}'
```









优化参数

1.调整translog同步策略

默认情况下，translog的持久化策略是，对于每个写入请求都做一次flush，刷新translog数据到磁盘上。这种频繁的磁盘IO操作是严重影响写入性能的，如果可以接受一定概率的数据丢失（这种硬件故障的概率很小），可以通过下面的命令调整 translog 持久化策略为异步周期性执行，并适当调整translog的刷盘周期。

```
curl -H “Content-Type:application/json” -X PUT  "localhost:9200/{index名称}/" -d '{"settings": {"index": {"translog": {"sync_interval": "5s","durability": "async"}}}}'
```

2.调整refresh_interval

写入Lucene的数据，并不是实时可搜索的，ES必须通过refresh的过程把内存中的数据转换成Lucene的完整segment后，才可以被搜索。默认情况下，ES每一秒会refresh一次，产生一个新的segment，这样会导致产生的segment较多，从而segment merge较为频繁，系统开销较大。如果对数据的实时可见性要求较低，可以通过下面的命令提高refresh的时间间隔，降低系统开销

```
curl -H "Content-Type:application/json" -X PUT "localhost:9200/aaaaaa11" -d '{"settings":{"index":{"refresh_interval":"30s"}}}'
```



**4.** **merge****并发****控制**

ES的一个index由多个shard组成，而一个shard其实就是一个Lucene的index，它又由多个segment组成，且Lucene会不断地把一些小的segment合并成一个大的segment，这个过程被称为merge。当节点配置的cpu核数较高时，merge占用的资源可能会偏高，影响集群的性能，可以通过下面的命令调整某个index的merge过程的并发度：

```
curl -H "Content-Type:application/json" -X PUT "localhost:9200/bank/_settings" -d '{"index.merge.scheduler.max_thread_count":2}'
```



安装

1.确认JDK版本

2.安装ES

```
curl -L -O 
https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.0.1-linux-x86_64.tar.gz
```

