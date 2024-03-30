// 给定 地址， 查询其 函数调用日志 们 各自 的 时间长度 tmLen
MATCH (log:V_FnCallLog {fnAdr:$fnAdr})    // "0x7ffff74349cb"
WITH  log.fnCallId AS fnCallId , collect(log) as logs
WITH fnCallId, logs, logs[1].tmPnt - logs[0].tmPnt AS tmLen
RETURN  fnCallId,tmLen
// RETURN  fnCallId,logs,tmLen
// limit 10


//返回结果如下
// ╒════════╤══════════════════════════════════════════════════════════════════════╤═════╕
// │fnCallId│logs                                                                  │tmLen│
// ╞════════╪══════════════════════════════════════════════════════════════════════╪═════╡
// │166153  │[(:V_FnCallLog {fnSym_lineNumber: 152,fnCallId: 166153,fnSym_address: │5    │
// │        │"0x7ffff74349cb",fnSym_column: 17,fnAdr: "0x7ffff74349cb",fnSym_name: │     │
// │        │"pointer_to",direct: 1,tmPnt: 332280,fnSym_moduleName: "libtorch.so.1"│     │
// │        │,logId: 332280,fnSym_fileName: "/usr/include/c++/9/ext/new_allocator.h│     │
// │        │",curThreadId: 864575}), (:V_FnCallLog {fnSym_lineNumber: 152,fnCallId│     │
// │        │: 166153,fnSym_address: "0x7ffff74349cb",fnSym_column: 17,fnAdr: "0x7f│     │
// │        │fff74349cb",fnSym_name: "pointer_to",direct: 2,tmPnt: 332285,fnSym_mod│     │
// │        │uleName: "libtorch.so.1",logId: 332285,fnSym_fileName: "/usr/include/c│     │
// │        │++/9/ext/new_allocator.h",curThreadId: 864575})]                      │     │
// ├────────┼──────────────────────────────────────────────────────────────────────┼─────┤
// │166229  │[(:V_FnCallLog {fnSym_lineNumber: 152,fnCallId: 166229,fnSym_address: │5    │
// │        │"0x7ffff74349cb",fnSym_column: 17,fnAdr: "0x7ffff74349cb",fnSym_name: │     │
// │        │"pointer_to",direct: 1,tmPnt: 332432,fnSym_moduleName: "libtorch.so.1"│     │
// │        │,logId: 332432,fnSym_fileName: "/usr/include/c++/9/ext/new_allocator.h│     │
// │        │",curThreadId: 864575}), (:V_FnCallLog {fnSym_lineNumber: 152,fnCallId│     │
// │        │: 166229,fnSym_address: "0x7ffff74349cb",fnSym_column: 17,fnAdr: "0x7f│     │
// │        │fff74349cb",fnSym_name: "pointer_to",direct: 2,tmPnt: 332437,fnSym_mod│     │
// │        │uleName: "libtorch.so.1",logId: 332437,fnSym_fileName: "/usr/include/c│     │
// │        │++/9/ext/new_allocator.h",curThreadId: 864575})]                      │     │
// ├────────┼──────────────────────────────────────────────────────────────────────┼─────┤