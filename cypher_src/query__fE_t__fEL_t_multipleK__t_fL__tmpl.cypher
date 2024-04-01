//  起_重复点k_终 ： 入  --t-->    重复'BJ--fJ-->LJ--tJ'  -->  出 
//  已知 深度k 递推的 求 深度k+1
with 
1 AS FnEnter, //Enter == Begin == B
2 as FnLeave //Leave == End == L
MATCH path= 
(B:V_FnCallLog {fnCallId:$fnCallId, direct: FnEnter }) - [tB:E_NxtTmPnt] ->

  (BJ:V_FnCallLog where BJ.direct=FnEnter   ) - [fJ:E_FnEL] -> (LJ:V_FnCallLog where LJ.direct=FnLeave  ) - [tJ:E_NxtTmPnt] -> //直接调用平链元素(模板)(match)

(L:V_FnCallLog {fnCallId:$fnCallId,  direct: FnLeave} )
WHERE  true
// B.fnCallId = L.fnCallId and B.fnCallId=166153 //开发调试用，生产不要使用

and  BJ.fnCallId = LJ.fnCallId //直接调用平链元素(模板)(where)

return  
path as 路径
,BJ //直接调用平链元素(模板)(return)
//结尾的换行是必须的,否则模板处理结果不对（实际情况是 若结尾无换行 则模板处理比较麻烦）