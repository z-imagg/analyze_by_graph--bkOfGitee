// neo4j cypher 脚本例子

//参考 
// https://wy-ei.gitee.io/notebook/posts/2018/neo4j-cql/
// https://blog.csdn.net/weixin_42487460/article/details/125147525 
// https://www.cnblogs.com/ljhdo/p/5516793.html

// 浏览器 打开 neo4j 终端 http://localhost:7474/browser/ , 执行以下脚本


// 叶子函数 深度deepth设置为0
MATCH (fromLog:V_FnCallLog)-[:E_FnEL]->(toLog:V_FnCallLog)
WHERE   (fromLog)-[:E_NxtTmPnt]->(toLog)
SET fromLog.deepth = 0, toLog.deepth = 0                      //增字段 // Set 446706 properties 
return count(fromLog)   as 叶子调用次数, COUNT(DISTINCT fromLog.fnSym_address) AS 叶子函数个数
