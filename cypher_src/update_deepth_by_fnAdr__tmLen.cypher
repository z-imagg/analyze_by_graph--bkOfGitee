//深度1定义 定fnAdr 定时tmPnt差(定时刻点长)
with 
  -1 as nullVal_deepth // deepth字段准空值 为 -1
MATCH path = (fromLog:V_FnCallLog {fnAdr:$fnAdr} )-[:E_NxtTmPnt* 1 .. __tmLen__ ]->(toLog:V_FnCallLog {fnAdr:$fnAdr})  // fnAdr = "0x7ffff74349cb" , tmLen = 5
WHERE 
// 同一次函数调用
  fromLog.fnCallId  = toLog.fnCallId
//深度k定义:
// 1. 存在 中间时刻点 深度为k-1 
and any( nodeK in nodes(path)[1..-1] WHERE   nodeK.deepth = $deepthK-1 )
// 且 
// 2.所有中间时刻点 深度 都 小于等于 k-1
//    等价于 所有中间时刻点 深度 是 已知的    
//       由于 逐步求解深度 即 深度0、深度1、深度2、...、深度k-1、深度k,  而 此时 在求深度k ， 因此 已知深度 只能是 从0到k-1
// 从1、2 可以表明 起点和终点 深度为k, 这是 深度k的准确定义吧
AND all( nodeK in nodes(path)[1..-1] WHERE   nodeK.deepth  > nullVal_deepth )

// 起点fromLog 无 深度字段deepth , 终点toLog 无 深度字段deepth
AND fromLog.deepth = nullVal_deepth and toLog.deepth = nullVal_deepth
// 放开以下set语句,则变成设置深度为1了
SET fromLog.deepth = $deepthK, toLog.deepth = $deepthK
// RETURN path
return count(fromLog)+count(toLog) AS updated_rows