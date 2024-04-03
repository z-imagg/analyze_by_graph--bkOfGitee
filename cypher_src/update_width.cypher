// 对给定fnCallId的起点、终点， 新增width字段并赋值为参数$prm_width
// 【术语】prm == param
with
$prm_width as prmWidth ,
$prm_sonFnCallIdLs as prmSonFnCallIdLs ,
$prm_fnCallId as prmFnCallId 
MATCH (fromLog:V_FnCallLog {fnCallId:prmFnCallId} )-[:E_FnEL]->(toLog:V_FnCallLog  {fnCallId:prmFnCallId} )
SET fromLog.width = prmWidth, toLog.width = prmWidth , fromLog.sonFnCallIdLs = prmSonFnCallIdLs , toLog.sonFnCallIdLs = prmSonFnCallIdLs
return count(fromLog)+count(toLog)   as 更新记录数