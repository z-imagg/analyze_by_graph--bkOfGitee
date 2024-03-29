// neo4j cypher 脚本例子

//参考 
// https://wy-ei.gitee.io/notebook/posts/2018/neo4j-cql/
// https://blog.csdn.net/weixin_42487460/article/details/125147525 
// https://www.cnblogs.com/ljhdo/p/5516793.html

// 浏览器 打开 neo4j 终端 http://localhost:7474/browser/ , 执行以下脚本


// 查看 所有 节点 边 类型 
call db.schema.visualization();

// 查看 所有 索引
call db.indexes();

////////////////// 深度为0的函数(叶子函数)
// 叶子函数 深度deepth设置为0
MATCH (fromLog:V_FnCallLog)-[:E_FnEL]->(toLog:V_FnCallLog)
WHERE   (fromLog)-[:E_NxtTmPnt]->(toLog)
//以下只能有一行
// return fromLog limit 10
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


////////////////// 深度为1的函数(第1层函数)

// 给 点类型V_FnCallLog的字段deepth 创建索引
CREATE INDEX FOR (n:V_FnCallLog) ON (n.deepth)

// 创建索引:  点类型V_FnCallLog 的 字段deepth 
CREATE INDEX FOR (n:V_FnCallLog) ON (n.fnCallId)

//查询 深度为1的函数调用
// 从 起点fromLog 中间经过了 至少1个 边E_NxtTmPnt时刻点 到达 终点toLog
// 指定 起点fromLog 终点toLog 的 fnCallId , 以 阻止 组合爆炸, 可以 快速执行完
MATCH path = (fromLog:V_FnCallLog {fnCallId:11} )-[:E_NxtTmPnt*1..]->(toLog:V_FnCallLog {fnCallId:11})
WHERE 
// 所有 中间点 的深度为0 即 所有 中间点 为 叶子节点
all( nodeK in nodes(path)[1..-1] WHERE   nodeK.deepth = 0 )
// 起点fromLog 无 深度字段deepth
AND (NOT exists(fromLog.deepth) )
// 终点toLog 无 深度字段deepth
AND (NOT exists(toLog.deepth)  )
//开发调试时用 的范围条件, 生产时 请屏蔽
// AND fromLog.fnCallId < 10000 AND  toLog.fnCallId < 10000
//以下只能有一行
// RETURN fromLog AS 起点, nodes(path)[1..-1] AS 中间节点, toLog AS 终点
return path
// return nodes(path)
