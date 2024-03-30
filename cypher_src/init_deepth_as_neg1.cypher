//全体增加deepth字段（-1）
with 
  $fnCallId_remainder10 as fnCallId_remainder10
match (log:V_FnCallLog)
where log.fnCallId %10 = fnCallId_remainder10
set log.deepth=-1
return count(log) as 更新记录数