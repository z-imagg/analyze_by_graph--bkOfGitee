//查询函数地址列表(不重复)
match (log:V_FnCallLog)
return distinct log.fnAdr as fnAdr 
// ...                    as 函数地址
limit 3
// 函数地址 "0x7ffff74349cb", "0x7ffff7435cc5", "0x7ffff7436c9d"