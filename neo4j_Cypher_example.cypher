// neo4j cypher 脚本例子

//参考 
// https://wy-ei.gitee.io/notebook/posts/2018/neo4j-cql/
// https://blog.csdn.net/weixin_42487460/article/details/125147525 
// https://www.cnblogs.com/ljhdo/p/5516793.html

// 浏览器 打开 neo4j 终端 http://localhost:7474/browser/ , 执行以下脚本


// 查看 所有 节点 边 类型 
call db.schema.visualization();

acted_in = (:Person)-[:ACTED_IN]->(:Movie)


// 叶子函数 深度deepth设置为0
MATCH (fromLog:V_FnCallLog)-[:E_NxtTmPnt]->(toLog:V_FnCallLog)
WHERE   (fromLog)-[:E_FnEL]->(toLog)
SET fromLog.deepth = 0, toLog.deepth = 0
// Set 446706 properties, completed after 3084 ms.

// 查询  深度为0 的 日志
//  即 叶子函数
MATCH (log:V_FnCallLog {deepth: 0})
return log
limit 10

MATCH (log:V_FnCallLog {deepth: 0})
return COUNT(log) AS 叶子函数调用次数
// 叶子函数调用次数 446706