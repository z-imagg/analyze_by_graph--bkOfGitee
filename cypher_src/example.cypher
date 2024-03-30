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


// 有模式： 深度为0的点 的 前一时刻的点 的深度未知
// 有模式： 深度为0的点 的 前一时刻t的点 的深度未知, 那么该时刻t有可能是深度为1的点
MATCH path=(fromLog:V_FnCallLog)-[:E_NxtTmPnt]->(toLog:V_FnCallLog) //后面的是方便开发调试观看加的  -[:E_NxtTmPnt]->(toLog2:V_FnCallLog)
WHERE  fromLog.deepth is null and   toLog.deepth=0
return  path
limit 10

// 更进一步， 限制方向
// 有模式： 深度为0的点 的 前一时刻的点 的深度未知
// 有模式： 深度为0的点 的 前一时刻t的点 的深度未知, 那么该时刻t有可能是深度为1的点
with 
1 AS FnEnter,
2 as FnLeave
MATCH path=(depMayBeK:V_FnCallLog {direct: FnEnter }) - [:E_NxtTmPnt]->(depKsub1:V_FnCallLog {deepth:0, direct: FnEnter} )  //后面的是方便开发调试观看加的 - [:E_NxtTmPnt]->(toLog2:V_FnCallLog)
WHERE  depMayBeK.deepth is null  
return  path
limit 10
