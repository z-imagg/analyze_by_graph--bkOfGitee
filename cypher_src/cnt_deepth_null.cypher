// 深度为空的节点个数
match (logV:V_FnCallLog)
where logV.deepth is   null
return count(logV) as 深度为空的节点个数