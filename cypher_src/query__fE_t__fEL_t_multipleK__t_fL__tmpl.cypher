//  模式【起_重复点k_终】 ： 入  --t-->    重复'BJ--fJ-->LJ--tJ'  -->  出 
//  模式【起_重复点k_终】 写作 逐小重复节往前拱 的样子，即：
//    起点--t入-->B0--f0-->L0--t0-->            循环体0
//     L0--t0-->B1--f1-->L1--t1-->             循环体1
//     _________                                   重叠部
//     L1--t1-->B2--f2-->L2--t2-->             循环体2
//     _________                                   重叠部
//         ...
//  LJ_1--tJ_1-->BJ--fJ-->LJ--tJ-->           循环体J     其中 J_1==J-1
//     _________                                   重叠部
//         ...
//     LJ--t8-->B9--f9-->L9--t9-->   终点       循环体3
//     _________             t出                     重叠部 其中 t出==t9

// 写在一行 即:
//    起点     --t入-->B0--f0-->L0--t0-->    B1--f1-->L1--t1-->   B2--f2-->L2--t2-->  ...  BJ--fJ-->LJ--tJ-->  ...  B9--f9-->L9--t出-->  终点

//  本脚本 捕捉 ： 重复'--t-->BJ--fJ-->LJ--tJ' 
// 
//  已知 深度k 递推的 求 深度k+1
with 
$from_fnCallId as param_from_fnCallId,
1 AS FnEnter, //Enter == Begin == B
2 as FnLeave //Leave == End == L
MATCH path= 
// (B:V_FnCallLog {fnCallId:param_fnCallId, direct: FnEnter }) - 
[tJ_1:E_NxtTmPnt WHERE tJ_1.from_fnCallId = param_from_fnCallId] ->

  (BJ:V_FnCallLog where BJ.direct=FnEnter   ) - [fJ:E_FnEL] -> (LJ:V_FnCallLog where LJ.direct=FnLeave  ) - [tJ:E_NxtTmPnt] 
  
// ->  (L:V_FnCallLog {fnCallId:param_fnCallId,  direct: FnLeave} )
WHERE  true
// B.fnCallId = L.fnCallId and B.fnCallId=166153 //开发调试用，生产不要使用

and  BJ.fnCallId = LJ.fnCallId

return  
path as 路径
,BJ