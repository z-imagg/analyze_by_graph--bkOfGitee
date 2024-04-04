**neo4j社区版， 查询语言Cypher或APOC**
#### neo4j 社区版 安装

##### docker

```shell
docker pull neo4j:4.4.32-community

docker run -d -p 7474:7474 -p 7687:7687 --name neo4j -e "NEO4J_AUTH=neo4j/123456" neo4j:4.4.32-community
```


https://hub.docker.com/layers/library/neo4j/4.4.32-community/images/sha256-ce25409b8c3cfaa9a63f4e182753d09266881893e667d0298935ad4bfb0f11e5?context=explore


http://localhost:7474/browser/  ， 输入用户名、密码，  到达 neo4j 的web控制台



https://developer.aliyun.com/article/994642

https://neo4j.com/docs/operations-manual/current/docker/introduction/


修改 neo4j 线程数目为 4 ： ```dbms.threads.worker_count=4```

```shell
docker exec -it neo4j  cp  /var/lib/neo4j/conf/neo4j.conf /var/lib/neo4j/conf/neo4j.conf.backup.$(date +%s)
docker exec -it neo4j  sed -i  's/#dbms.threads.worker_count=/dbms.threads.worker_count=4/' /var/lib/neo4j/conf/neo4j.conf 

```
#####  neo4j安装apoc插件

https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/

[neo4j-apoc-procedures/apoc-4.4.0.26-all.jar](https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/4.4.0.26/apoc-4.4.0.26-all.jar)

```bash
wget https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/4.4.0.26/apoc-4.4.0.26-all.jar

docker cp  apoc-4.4.0.26-all.jar  neo4j:/var/lib/neo4j/plugins

docker restart neo4j
```

打开[neo4j web控制台](http://localhost:7474/browser/),  在cypher查询中可正常调用apoc函数 举例：  ```RETURN apoc.convert.fromJsonList('[1,2,3]') AS output;```


cypher例子apoc语句参照:  https://neo4j.com/labs/apoc/4.1/overview/apoc.convert/apoc.convert.fromJsonList/

####  py访问neo4j

```pip install neo4j==5.18.0```

版本列表， https://github.com/neo4j/neo4j-python-driver/wiki

```neo4j==5.18.0``` 支持```Python 3.10```, https://neo4j.com/docs/api/python-driver/5.18/, 同时 这里有 py例子


https://pypi.org/project/neo4j/


不要用淘汰了的py2neo


### 树形结构图形化库 

https://www.cssscript.com/best-tree-view/



### 运行效果基本正面：  丑陋但正确且速度正常的遍历器（小节 起_t入_B0__BJ_fJ_LJ_tJ_ 逐前拱）

http://giteaz:3000/frida_analyze_app_src/analyze_by_graph/src/branch/main/result.md





### 收获（微小初步分析torch1.3.1源码）

http://giteaz:3000/frida_analyze_app_src/analyze_by_graph/src/branch/main/gain.md

