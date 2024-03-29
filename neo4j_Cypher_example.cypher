// neo4j cypher 脚本例子

//参考 
// https://wy-ei.gitee.io/notebook/posts/2018/neo4j-cql/
// https://blog.csdn.net/weixin_42487460/article/details/125147525 
// https://www.cnblogs.com/ljhdo/p/5516793.html

// 浏览器 打开 neo4j 终端 http://localhost:7474/browser/ , 执行以下脚本


// 查看 所有 节点 边 类型 
call db.schema.visualization();

acted_in = (:Person)-[:ACTED_IN]->(:Movie)

////////////////// 深度为0的函数(叶子函数)
// 叶子函数 深度deepth设置为0
MATCH (fromLog:V_FnCallLog)-[:E_FnEL]->(toLog:V_FnCallLog)
WHERE   (fromLog)-[:E_NxtTmPnt]->(toLog)
//以下只能有一行
// return count(fromLog)   as 叶子调用次数                      //查询   // 223353        
// RETURN COUNT(DISTINCT fromLog.fnSym_address) AS 叶子函数个数 //查询   // 977
SET fromLog.deepth = 0, toLog.deepth = 0                      //增字段 // Set 446706 properties 

// 查询  深度为0 的 日志
//  即 叶子函数
MATCH (log:V_FnCallLog {deepth: 0})
return log
limit 10

MATCH (log:V_FnCallLog {deepth: 0})
return COUNT(log) AS 叶子函数调用次数
// 叶子函数调用次数 446706
