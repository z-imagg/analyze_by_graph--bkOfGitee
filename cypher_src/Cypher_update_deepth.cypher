// 来自文件 neo4j_Cypher_example.cypher
MATCH path = (fromLog:V_FnCallLog {fnCallId:$fnCallId} )-[:E_NxtTmPnt* 1 .. __tmPntLength__ ]->(toLog:V_FnCallLog {fnCallId:$fnCallId})
WHERE 
// 1. 存在 中间时刻点 深度比该深度小1 
any( nodeK in nodes(path)[1..-1] WHERE   nodeK.deepth = $this_deepth-1 )
// 且 
// 2.所有中间时刻点 深度 都 已知 
//    即 所有中间时刻点 深度 都 小于等于 该深度-1 , 因为 当前所有已知深度 就是 小于等于 该深度-1
// 可以表明 起点和终点 为 该深度, 这是 深度准确定义吧
AND all( nodeK in nodes(path)[1..-1] WHERE   nodeK.deepth  is not null )
// 起点fromLog 无 深度字段deepth
AND fromLog.deepth is null
// 终点toLog 无 深度字段deepth
AND toLog.deepth is null
//neo4j的索引, 为何 范围条件 比 精确条件 快?
// 范围条件
AND  $fnCallId=fromLog.fnCallId  AND   $fnCallId=toLog.fnCallId
SET fromLog.deepth = $this_deepth, toLog.deepth = $this_deepth
// RETURN fromLog,toLog
return count(fromLog)+count(toLog) AS updated_rows