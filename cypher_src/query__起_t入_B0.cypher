//模式 ： 起点--t入-->B0
// 此即为 query_BJ_fJ_LJ_tJ_.cypher 中提到的 "开头"

//完整情况 请参考 脚本 query_BJ_fJ_LJ_tJ_.cypher


with 
$fnCallId as param_fnCallId, 
//14 as param_fnCallId, //开发调试用，生产不要使用
1 AS FnEnter, //Enter == Begin == B
2 as FnLeave //Leave == End == L
MATCH path= 

  (B1:V_FnCallLog  {fnCallId:param_fnCallId, direct: FnEnter } ) - [t:E_NxtTmPnt] -> (B2:V_FnCallLog {direct:FnEnter}  ) 
  
WHERE   B1.fnCallId <> B2.fnCallId  //此条件可有可无

return  
path as 路径,
B2