//深度1定义 定fnAdr 定时tmPnt差(定时刻点长)
MATCH path = (fromLog:V_FnCallLog {fnAdr:"0x7ffff74349cb"} )-[:E_NxtTmPnt* 1 .. 5 ]->(toLog:V_FnCallLog {fnAdr:"0x7ffff74349cb"})
WHERE 
// 同一次函数调用
  fromLog.fnCallId  = toLog.fnCallId
// 1. 存在 中间时刻点 深度比该深度小1 
and any( nodeK in nodes(path)[1..-1] WHERE   nodeK.deepth = 1-1 )
// 且 
// 2.所有中间时刻点 深度 都 已知 
//    即 所有中间时刻点 深度 都 小于等于 该深度-1 , 因为 当前所有已知深度 就是 小于等于 该深度-1
// 可以表明 起点和终点 为 该深度, 这是 深度准确定义吧
AND all( nodeK in nodes(path)[1..-1] WHERE   nodeK.deepth  is not null )

// 起点fromLog 无 深度字段deepth , 终点toLog 无 深度字段deepth
AND fromLog.deepth is null and toLog.deepth is null
// 放开以下set语句,则变成设置深度为1了
SET fromLog.deepth = 1, toLog.deepth = 1
// RETURN path
return count(fromLog)+count(toLog) AS updated_rows