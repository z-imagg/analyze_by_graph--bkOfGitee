//  起空_重复点k_终空 ： 入d==k+1  重复'--tJ-->BJ--fJ-->LJ'  --t2-->  出d=k+1
//  已知 深度k 递推的 求 深度k+1
with 
1 AS FnEnter, //Enter == Begin == B
2 as FnLeave, //Leave == End == L
$K as k,
$K+1 as kp1
//k+1 as k_plus_1
MATCH path= 
(B_kp1:V_FnCallLog {direct: FnEnter }) 

- [tJ:E_NxtTmPnt] -> (BJ:V_FnCallLog where BJ.direct=FnEnter   ) - [fJ:E_FnEL] -> (LJ:V_FnCallLog where LJ.direct=FnLeave  )  //点k路径（模板）

- [t2:E_NxtTmPnt] -> (L_kp1:V_FnCallLog { direct: FnLeave} )
WHERE  
B_kp1.deepth is null  // 起空
and  L_kp1.deepth is null // 终空

and  BJ.deepth <= k and BJ.deepth >= 0       and  LJ.deepth <= k and LJ.deepth >= 0  and BJ.fnCallId = LJ.fnCallId //点k条件（模板）

set B_kp1.deepth = kp1 , L_kp1.deepth = kp1
return  count(path) as 路径数目
