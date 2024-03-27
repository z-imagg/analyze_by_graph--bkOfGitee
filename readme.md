**neo4j社区版， 查询语言Cypher或APOC**
#### neo4j 社区版 安装

##### docker

```shell
docker run -d -p 7474:7474 -p 7687:7687 --name neo4j -e "NEO4J_AUTH=neo4j/123456" neo4j:4.4.32-community
```

https://hub.docker.com/layers/library/neo4j/4.4.32-community/images/sha256-ce25409b8c3cfaa9a63f4e182753d09266881893e667d0298935ad4bfb0f11e5?context=explore


http://localhost:7474/browser/  ， 输入用户名、密码，  到达 neo4j 的web控制台



https://developer.aliyun.com/article/994642

https://neo4j.com/docs/operations-manual/current/docker/introduction/

####  py访问neo4j

```pip install neo4j==5.18.0```

版本列表， https://github.com/neo4j/neo4j-python-driver/wiki

```neo4j==5.18.0``` 支持```Python 3.10```, https://neo4j.com/docs/api/python-driver/5.18/, 同时 这里有 py例子


https://pypi.org/project/neo4j/


不要用淘汰了的py2neo