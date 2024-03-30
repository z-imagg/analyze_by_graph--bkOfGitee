//全体置空 deepth字段、tmLen字段
with 
  $fnCallId_remainder10 as fnCallId_remainder10
match (log:V_FnCallLog)
where log.fnCallId %10 = fnCallId_remainder10
set log.deepth=NULL, log.tmLen = NULL
return count(log) as 更新记录数
