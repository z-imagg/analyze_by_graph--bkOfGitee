// 对给定fnCallId的起点、终点， 新增markup字段并赋值为参数$prm_markup
// 【术语】prm == param
with
$prm_markup as prmMarkup ,
$prm_fnCallId as prmFnCallId 
MATCH (fromLog:V_FnCallLog {fnCallId:prmFnCallId} )-[:E_FnEL]->(toLog:V_FnCallLog  {fnCallId:prmFnCallId} )
SET fromLog.markup = prmMarkup, toLog.markup = prmMarkup 
return count(fromLog)+count(toLog)   as 更新记录数