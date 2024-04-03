//全体置空width字段
with 
  $fnCallId_remainder10 as fnCallId_remainder10
match (log:V_FnCallLog)
where log.fnCallId %10 = fnCallId_remainder10
set log.width=NULL, log.sonFnCallIdLs=NULL
return count(log) as 更新记录数
