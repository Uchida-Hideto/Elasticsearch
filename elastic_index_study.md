可以作为一个大型分布式集群（数百台服务器）技术,处理PB级数据,服务大公司;也可以运行在单机上,服务小公司。

Apache Lucene是一个用Java编写的高性能，功能齐全信息检索库。Elasticsearch内部利用Lucene来构建的分布式和分析功能。提供了 REST API 的操作接口，开箱即用。

Elasticsearch在后台使用Lucene来提供最强大的全文检索，提供任何开源产品的能力。搜索自带的多语言支持，强大的查询语言，地理位置支持，上下文感知的建议，自动完成和搜索片段。

Elasticsearch允许你快速上手。简单的指定一个JSON文档将自动检测数据的结构和类型，创建一个索引，并使你的数据检索。还拥有完全控制，以自定义数据是如何被索引。



##### 一.基本概念

###### 1.1 Node

Elastic是一个分布式数据库，可以运行在多个节点上，多个节点可以组成一个集群。

###### 1.2 Index

Elastic 会索引所有字段，经过处理后写入反向索引（Inverted Index），当查找时会直接查找这个索引。

索引，Elastic数据管理的顶层就是Index(索引)，它是单个数据库的同义词。每个Index的名称必须是小写。

###### 1.3 Document

Index 里面单条的记录成为Document(文档)，许多个Document 构成了一个Index

Document  使用JSON格式表示。同一个Index中的Document不要求使用相同的结构（Schema）,但是最好使用相同的，这样有利于提高查询效率。

###### 1.4Type

用于将Document分组，但是不同的Type 需要有相同的数据结构，如果有不同的数据结构，应该存在不同的Index中。由于Type可以分组但是却要求有相同的数据结构，这样不利于查询的效率。在6.X版中一个Index只可以有一个Type,在7.X版本中可以不指定Type.

###### 1.6 Shard

每个Index上包含多个Shard,默认是5个，分散在不同节点上，不会存在两个相同的Shard存在同一个Node上。Shard是最小的Lucene索引单元。

当Document 存储时Elastic会通过doc id进行hash来确定存储到哪一个Shard上，然后再Shard上面进行索引存储。

##### 二.Elastic索引深入探究

Elasticsearch索引的精髓是

> 一切设计都是为了提高搜索的性能

在插入数据的同时，会为每一个字段建立索引——倒排索引。

有如下要存的数据

> 1. The quick brown fox jumped over the lazy dog
> 2. Quick brown foxes leap over lazy dogs in summer

为了建立倒排索引首先将每个文档的Content分成一个个单独的词（可以称之为词条或者是Tokens）创建一个不重复的词条的排序列表。

得到如下的结构

![](C:\Users\acer\iCloudDrive\md文档\elastic pic\68747470733a2f2f6368616e6773697975616e2e6769746875622e696f2f696d616765732f656c6b2f312d332e706e67.png)

假设doc1的id为1，doc2的id为2，这个ID是Elasticsearch自建的文档ID,那么经过倒排索引之后我们得到如下的对应关系

> **Term** **Posting List**
>
> The 【1】
>
> quick 【1,2】
>
> brown 【1,2】
>
> fox 【1】
>
> ...... ...... 

Elasticsearch为了能快速查找到某一个term，将所有的term排个序，然后使用二分法查找term,logN的查找效率，就像通过字典查找一样，这就是**Term  Dictionary** 

**Term Index**

如果数据量大的话使用**Term Dictionary**依然会开销过大，放内存中不现实，因此有了Term Index，就像字典里面的索引一样。比如存储A开头的有哪些term 存在哪一页等。可以将Term Index看作是一棵树。

![](C:\Users\acer\iCloudDrive\md文档\elastic pic\term-index.png)

这棵树不会包含所有的term,包含的是term的一些前缀。通过Term  Index可以快速的定位到Term Dictionary的某个offset，然后从这个位置继续进行查找。

![](C:\Users\acer\iCloudDrive\md文档\elastic pic\index.png)

因此Term Index不需要存储所有的Term,存储的是Term 的前缀与Term Dictionary的block之间的关系，再结合FST的压缩技术可以将Term Index 缓存到内存中。

从term index查到对应的term dictionary的block位置之后，再去磁盘上找term，大大减少了磁盘随机读的次数。

##### 三.Elastic 存储过程



![](C:\Users\acer\iCloudDrive\md文档\elastic pic\0_SFtJWPp4A0lLY1k6.jpeg)



1.新document首先写入内存buffer缓存中，

2.每隔一段时间，执行commit point操作 buffer写入新Segment中

3.新segment写入文件系统缓存filesystem cache中

4.文件系统缓存中的index segment 被fsync强制刷到磁盘上，确保物理写入。此时新segment被打开供search操作。

5.清空内存buffer,可以接收新的文档。

6.以上是传统的写入步骤，实际上ES为保证实时性，会进行refresh操作。

7.在新的文档写入后，写入index buffer的同时会写入translog

8.reflush操作使得写入文档搜索可见

9.flush操作使得filesystem cache 写入磁盘，以达到持久化的目的。

##### 四.Elastic 读取过程

![](C:\Users\acer\iCloudDrive\md文档\elastic pic\0_2DAJ28Q4tnGmOLu4.jpeg)

##### 五.Elastic 搜索相关性

*The relevance is determined by a score that Elasticsearch gives to each document returned in the search result. The default algorithm used for scoring is tf/idf (term frequency/inverse document frequency). The term frequency measures how many times a term appears in a document (higher frequency == higher relevance) and inverse document frequency measures how often the term appears in the entire index as a percentage of the total number of documents in the index (higher frequency == less relevance). The final score is a combination of the tf-idf score with other factors like term proximity (for phrase queries), term similarity (for fuzzy queries), etc.*













