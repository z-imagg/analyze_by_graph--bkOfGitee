# 两个neo4j的DOCKER实例端口错误的被接上 导致的事故 


neo4j社区版 同一个服务下 同时只能访问一个数据库，因此再开一个neo4j服务

大致解释：  两个neo4j的docker实例 的端口被偶然对接上 造成 对第一个docker实例查询请求 进入了第二个docker实例 并 在第二个docker实例的首条CREATE点语句的触发下变成了大量空白点

### 第一个docker 
第一个docker启动命令 ：
```docker run -d -p 7474:7474 -p 7687:7687 --name neo4j  -e "NEO4J_AUTH=neo4j/123456" neo4j:4.4.32-community```

### 第二个docker
第二个docker启动命令 ：
```docker run -d -p 5474:7474 -p 5687:7687 --name neo4j_anlz -e "NEO4J_AUTH=neo4j/123456" neo4j:4.4.32-community```

### 事故过程

1. 此时第一个docker实例在正常运行，

第二个docker端口被我错误的写成了 '-p 7474:5474 -p 7687:5687'  （  正确的应该是 '-p 5474:7474 -p 5687:7687 ' ）

2. 按照错误的端口启动 第二个docker实例， 当然第二个docker实例肯定是启动失败 ，

3. 然后我删除该第二个docker死实例子，

4. 此时 若 重启第一个docker实例 可以 阻止 第一个docker和第二个docker的端口 连通 ，这样事故并不会发生  ， 但 没做这一步 

5. 重新用正确的端口启动第二个docker实例 这样第二个docker实例启动正常

6. 此时 第一个docker和第二个docker的端口 连通 ，事故 已经 可以  发生了


7. visual_main.py 先查询第一个docker 再对第二个docker循环创建节点

visual_main.py  对 第二个docker实例 插入 点 发生了怪异的事情 一条CREATE (x:V_FnCallLog_Analz) 创建了25988条空白点

具体是 此文件visual_main.py代码 中 '####循环插入点V_FnCallLog_Analz' 中的 第一个循环体 所执行的 'sess_anlz.run("CREATE (x:V_FnCallLog_Analz {...})' 导致 neo4j_anlz中多了 25988条空白点，这些点 只有自带字段 <elementId>	、<id> 没有任何语句中指定的字段 

这些点的统计个数如下：

//按类型们(labels)统计 点数
MATCH (n) 
with  labels(n) as labs, n
RETURN  labs, count(n)

结果如下：
╒═════════════════════╤════════╕
│labs                 │count(n)│
╞═════════════════════╪════════╡
│[]                   │25988   │
├─────────────────────┼────────┤
│["V_FnCallLog_Analz"]│6987    │
└─────────────────────┴────────┘


### 如何 解决的？

8. 停止 第一个docker实例  ，  这一步很重要 

9. 停止 第二个docker实例  ，  删除 第二个docker实例， 重新建立第二个docker实例 ，

10. 启动 第一个docker实例

11. visual_main.py  再写入 则 点数目 正常 

### 事故原因

曾经错误的端口对应  '-p 7474:5474 -p 7687:5687'  正好将 第一个docker端口 转发到 第二个docker端口上了，  这些 空白点 应该就是来自 第一个docker实例 的查询结果 灌入 了 第二个docker实例 形成了空白节点