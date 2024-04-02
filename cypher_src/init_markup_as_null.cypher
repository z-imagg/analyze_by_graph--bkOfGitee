//全体置空markup字段
with 
  $fnCallId_remainder10 as fnCallId_remainder10
match (log:V_FnCallLog)
where log.fnCallId %10 = fnCallId_remainder10
set log.markup=NULL
return count(log) as 更新记录数
