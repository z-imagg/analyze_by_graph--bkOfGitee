####  neo4j-4.4.32-community  安装 (以docker运行)

##### neo4j社区版 启动(以docker)

```shell
docker pull neo4j:4.4.32-community

docker run --network host -d -p 7474:7474 -p 7687:7687 --name neo4j -e "NEO4J_AUTH=neo4j/123456" neo4j:4.4.32-community

#查看neo4j启动日志, 大约十多秒启动完成
docker logs neo4j
```


备忘 所用docker镜像[hub.docker.com/4.4.32-community/image/sha256-ce25409](https://hub.docker.com/layers/library/neo4j/4.4.32-community/images/sha256-ce25409b8c3cfaa9a63f4e182753d09266881893e667d0298935ad4bfb0f11e5?context=explore)


浏览器打开 neo4j的web控制台 http://localhost:7474/browser/  ， 输入用户名 neo4j 、密码 123456  



#####  neo4j安装apoc插件


```bash
#下载apoc插件
wget https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/4.4.0.26/apoc-4.4.0.26-all.jar

#复制到 docker实例 中
docker cp  apoc-4.4.0.26-all.jar  neo4j:/var/lib/neo4j/plugins

#重启 docker实例
docker restart neo4j
```

##### 确认apoc插件正常

打开[neo4j的web控制台](http://localhost:7474/browser/),  在cypher查询中可正常调用apoc函数 举例：  ```RETURN apoc.convert.fromJsonList('[1,2,3]') AS output;```

cypher例子apoc语句参照:  https://neo4j.com/labs/apoc/4.1/overview/apoc.convert/apoc.convert.fromJsonList/

#####  py访问neo4j

```shell
source /app/Miniconda3-py310_22.11.1-1/bin/activate
pip install neo4j==5.18.0
```






