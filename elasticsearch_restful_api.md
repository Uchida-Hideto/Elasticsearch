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

