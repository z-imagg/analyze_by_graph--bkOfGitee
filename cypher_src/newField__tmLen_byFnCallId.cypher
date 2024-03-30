// 对 给定的 fnCallId 新增字段tmLen
MATCH (log:V_FnCallLog)
WHERE   log.fnCallId in $fnCallIdLs
//                   in [1, 2, 3]
SET log.tmLen = $tmLen             //增字段tmLen
return count(log)   as 日志个数, COUNT(DISTINCT log.fnSym_address) AS 函数个数
