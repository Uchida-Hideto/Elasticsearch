### es plugin install



1.执行命令

```
sudo sh /usr/share/elasticsearch/bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.0.0/elasticsearch-analysis-ik-7.0.0.zip
```





2.开启通过IP:PORT 访问ES （需要root权限账户访问）

```
vim  /etc/elasticsearch/elasticsearch.yml
```

添加如下内容

```
network.host: 0.0.0.0
```

修改参数

```
cluster.initial_master_nodes: ["node-1"]
```



重启es服务

```
systemctl status elasticsearch
systemctl restart elasticsearch
```