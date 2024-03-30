

// 查看 所有 节点 边 类型 
call db.schema.visualization();

//查看 索引
call db.indexes

// with收拢常量，reduce,extract,  中间点 有deepth为null举例
with 
   1 as deepthK, 
   "0x55555556ab40" as fnAdrZ, 
   3365 as tmLen
//深度1定义 定fnAdr 定时tmPnt差(定时刻点长)
MATCH path = (fromLog:V_FnCallLog {fnAdr:fnAdrZ} )-[:E_NxtTmPnt* 1 .. 3365 ]->(toLog:V_FnCallLog {fnAdr:fnAdrZ})   
WHERE 
// 同一次函数调用
  fromLog.fnCallId  = toLog.fnCallId


// 起点fromLog 无 深度字段deepth , 终点toLog 无 深度字段deepth
AND fromLog.deepth is null and toLog.deepth is null
with nodes(path)[1..-1] as mids
// with [i in range(0,size(mids)) | mids[i].deepth] as ds
// WITH extract(node IN mids | node.deepth) AS ds
// WITH reduce(sum = 0, node IN mids | sum + node.deepth) AS deepthSum
WITH reduce(sum = 0, node IN mids | sum + (CASE WHEN node.deepth IS NULL THEN -1 ELSE node.deepth END)) AS deepthSum
// where deepthSum >= 0 // 这个条件可以写在py中， 但是 这个条件正确的前提是 深度从1开始 即叶子的深度为1  而不是现在的叶子的深度为0
// RETURN path
// return size(mids)
// return ds
return deepthSum
limit 10
// limit 20 // 也很慢



//尝试改进 update_deepth_by_fnAdr__tmLen  还是慢
with 
  -1 as nullVal_deepth  ,
  "0x55555556ab40" as fnAdrZ,
  1 as deepthK
MATCH path = (fromLog:V_FnCallLog {fnAdr:fnAdrZ} )-[:E_NxtTmPnt* 1 .. 3365 ]->(toLog:V_FnCallLog {fnAdr:fnAdrZ})   
WHERE 
// 同一次函数调用
  fromLog.fnCallId  = toLog.fnCallId
//深度k定义:
// 1. 存在 中间时刻点 深度为k-1 
and any( nodeK in nodes(path)[1..-1] WHERE   nodeK.deepth = deepthK-1 )
AND fromLog.deepth = nullVal_deepth and toLog.deepth = nullVal_deepth
// 且 
// 2.所有中间时刻点 深度 都 小于等于 k-1
//    等价于 所有中间时刻点 深度 是 已知的    
//       由于 逐步求解深度 即 深度0、深度1、深度2、...、深度k-1、深度k,  而 此时 在求深度k ， 因此 已知深度 只能是 从0到k-1
// 从1、2 可以表明 起点和终点 深度为k, 这是 深度k的准确定义吧
// with deepthK,fromLog, toLog, [i in range(0,size(nodes(path) )-2) | nodes(path)[i].deepth] as x
// with deepthK,fromLog, toLog,  [ node IN nodes(path)[1..-1]   | node.deepth ]    as  x 
// with deepthK,fromLog, toLog, min(x) as z
with nullVal_deepth, deepthK,fromLog, toLog, min( [ node IN nodes(path)[1..-1]   | node.deepth ])    as  z
where nullVal_deepth  > -1
// 起点fromLog 无 深度字段deepth , 终点toLog 无 深度字段deepth
// 放开以下set语句,则变成设置深度为1了
SET fromLog.deepth = deepthK, toLog.deepth = deepthK
// RETURN path
return count(fromLog)+count(toLog) AS updated_rows