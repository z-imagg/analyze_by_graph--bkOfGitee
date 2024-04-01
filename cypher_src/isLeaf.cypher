with 
1 AS FnEnter,
2 as FnLeave
// 叶子定义 ：
//   1. 作为一次函数调用 的 起点fromLog 和 终点toLog
MATCH (fromLog:V_FnCallLog {fnCallId:$fnCallId, direct:FnEnter})-[:E_FnEL]->(toLog:V_FnCallLog {fnCallId:$fnCallId, direct:FnLeave})
//   2. 从 起点fromLog 到 终点toLog 只有一个 时刻点tmPnt
WHERE   (fromLog)-[:E_NxtTmPnt]->(toLog)

return count(fromLog) as 匹配节点个数, count(fromLog) =1 as 是叶子
