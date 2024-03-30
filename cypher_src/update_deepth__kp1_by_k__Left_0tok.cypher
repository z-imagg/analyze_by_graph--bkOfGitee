//  四点深度递推模式(左自由深度) ： 入d==k+1  --t1-->  入d==0..k  --f-->  出d==k  --t2-->  出d=k+1
//  已知 深度k 递推的 求 深度k+1
with 
1 AS FnEnter, //Enter == Begin == B
2 as FnLeave, //Leave == End == L
$K as k,
$K+1 as kp1
//k+1 as k_plus_1
MATCH path= 
(B_kp1:V_FnCallLog {direct: FnEnter }) 
- [t1:E_NxtTmPnt] -> (B_k:V_FnCallLog { direct: FnEnter } ) 
- [f:E_FnEL] -> (L:V_FnCallLog { direct: FnLeave, deepth: k}) 
- [t2:E_NxtTmPnt] -> (L_kp1:V_FnCallLog { direct: FnLeave} )
WHERE  
B_kp1.deepth is null  
and  B_k.deepth <= k and B_k.deepth >= 0
and L_kp1.deepth is null
set B_kp1.deepth = kp1 , L_kp1.deepth = kp1
return  count(path) as 路径数目
