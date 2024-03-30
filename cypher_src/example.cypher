// with收拢常量，reduce,extract,  中间点 有deepth为null举例
with 
   1 as deepthK, 
   "0x55555556ab40" as fnAdrZ, 
   3365 as tmLen
//深度1定义 定fnAdr 定时tmPnt差(定时刻点长)
MATCH path = (fromLog:V_FnCallLog {fnAdr:fnAdrZ} )-[:E_NxtTmPnt* 1 .. 3365 ]->(toLog:V_FnCallLog {fnAdr:fnAdrZ})   
WHERE 
// 同一次函数调用
  fromLog.fnCallId  = toLog.fnCallId


// 起点fromLog 无 深度字段deepth , 终点toLog 无 深度字段deepth
AND fromLog.deepth is null and toLog.deepth is null
with nodes(path)[1..-1] as mids
// with [i in range(0,size(mids)) | mids[i].deepth] as ds
// WITH extract(node IN mids | node.deepth) AS ds
// WITH reduce(sum = 0, node IN mids | sum + node.deepth) AS deepthSum
WITH reduce(sum = 0, node IN mids | sum + (CASE WHEN node.deepth IS NULL THEN -1 ELSE node.deepth END)) AS deepthSum
// where deepthSum >= 0 // 这个条件可以写在py中， 但是 这个条件正确的前提是 深度从1开始 即叶子的深度为1  而不是现在的叶子的深度为0
// RETURN path
// return size(mids)
// return ds
return deepthSum
limit 10
// limit 20 // 也很慢


// 分组: fnCallId为key, log数组为value
// fnCallId:logs
MATCH (log:V_FnCallLog {fnAdr:"0x7ffff74349cb"})  
WITH  log.fnCallId AS fnCallId , collect(log) as logs
RETURN  fnCallId,logs
limit 10
/**
╒════════╤══════════════════════════════════════════════════════════════════════╕
│fnCallId│logs                                                                  │
╞════════╪══════════════════════════════════════════════════════════════════════╡
│166153  │[(:V_FnCallLog {fnSym_lineNumber: 152,fnCallId: 166153,fnSym_address: │
│        │"0x7ffff74349cb",fnSym_column: 17,fnAdr: "0x7ffff74349cb",fnSym_name: │
│        │"pointer_to",direct: 1,tmPnt: 332280,fnSym_moduleName: "libtorch.so.1"│
│        │,logId: 332280,fnSym_fileName: "/usr/include/c++/9/ext/new_allocator.h│
│        │",curThreadId: 864575}), (:V_FnCallLog {fnSym_lineNumber: 152,fnCallId│
│        │: 166153,fnSym_address: "0x7ffff74349cb",fnSym_column: 17,fnAdr: "0x7f│
│        │fff74349cb",fnSym_name: "pointer_to",direct: 2,tmPnt: 332285,fnSym_mod│
│        │uleName: "libtorch.so.1",logId: 332285,fnSym_fileName: "/usr/include/c│
│        │++/9/ext/new_allocator.h",curThreadId: 864575})]                      │
├────────┼──────────────────────────────────────────────────────────────────────┤
│166229  │[(:V_FnCallLog {fnSym_lineNumber: 152,fnCallId: 166229,fnSym_address: │
│        │"0x7ffff74349cb",fnSym_column: 17,fnAdr: "0x7ffff74349cb",fnSym_name: │
│        │"pointer_to",direct: 1,tmPnt: 332432,fnSym_moduleName: "libtorch.so.1"│
│        │,logId: 332432,fnSym_fileName: "/usr/include/c++/9/ext/new_allocator.h│
│        │",curThreadId: 864575}), (:V_FnCallLog {fnSym_lineNumber: 152,fnCallId│
│        │: 166229,fnSym_address: "0x7ffff74349cb",fnSym_column: 17,fnAdr: "0x7f│
│        │fff74349cb",fnSym_name: "pointer_to",direct: 2,tmPnt: 332437,fnSym_mod│
│        │uleName: "libtorch.so.1",logId: 332437,fnSym_fileName: "/usr/include/c│
│        │++/9/ext/new_allocator.h",curThreadId: 864575})]                      │
*/


// 分组: fnCallId为key,  value : log数组、logs[1].tmPnt-log[0].tmPnt
// fnCallId:logs
MATCH (log:V_FnCallLog {fnAdr:"0x7ffff74349cb"})  
WITH  log.fnCallId AS fnCallId , collect(log) as logs
WITH fnCallId, logs, logs[1].tmPnt - logs[0].tmPnt AS tmLen
RETURN  fnCallId,logs,tmLen
limit 10
/**
╒════════╤══════════════════════════════════════════════════════════════════════╤═════╕
│fnCallId│logs                                                                  │tmLen│
╞════════╪══════════════════════════════════════════════════════════════════════╪═════╡
│166153  │[(:V_FnCallLog {fnSym_lineNumber: 152,fnCallId: 166153,fnSym_address: │5    │
│        │"0x7ffff74349cb",fnSym_column: 17,fnAdr: "0x7ffff74349cb",fnSym_name: │     │
│        │"pointer_to",direct: 1,tmPnt: 332280,fnSym_moduleName: "libtorch.so.1"│     │
│        │,logId: 332280,fnSym_fileName: "/usr/include/c++/9/ext/new_allocator.h│     │
│        │",curThreadId: 864575}), (:V_FnCallLog {fnSym_lineNumber: 152,fnCallId│     │
│        │: 166153,fnSym_address: "0x7ffff74349cb",fnSym_column: 17,fnAdr: "0x7f│     │
│        │fff74349cb",fnSym_name: "pointer_to",direct: 2,tmPnt: 332285,fnSym_mod│     │
│        │uleName: "libtorch.so.1",logId: 332285,fnSym_fileName: "/usr/include/c│     │
│        │++/9/ext/new_allocator.h",curThreadId: 864575})]                      │     │
├────────┼──────────────────────────────────────────────────────────────────────┼─────┤
│166229  │[(:V_FnCallLog {fnSym_lineNumber: 152,fnCallId: 166229,fnSym_address: │5    │
│        │"0x7ffff74349cb",fnSym_column: 17,fnAdr: "0x7ffff74349cb",fnSym_name: │     │
│        │"pointer_to",direct: 1,tmPnt: 332432,fnSym_moduleName: "libtorch.so.1"│     │
│        │,logId: 332432,fnSym_fileName: "/usr/include/c++/9/ext/new_allocator.h│     │
│        │",curThreadId: 864575}), (:V_FnCallLog {fnSym_lineNumber: 152,fnCallId│     │
│        │: 166229,fnSym_address: "0x7ffff74349cb",fnSym_column: 17,fnAdr: "0x7f│     │
│        │fff74349cb",fnSym_name: "pointer_to",direct: 2,tmPnt: 332437,fnSym_mod│     │
│        │uleName: "libtorch.so.1",logId: 332437,fnSym_fileName: "/usr/include/c│     │
│        │++/9/ext/new_allocator.h",curThreadId: 864575})]                      │     │
├────────┼──────────────────────────────────────────────────────────────────────┼─────┤
*/