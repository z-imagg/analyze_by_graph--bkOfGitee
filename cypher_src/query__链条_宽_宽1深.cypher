// tag_release__neo4j_log_transform__qemu_v8.2.2__linux_v5.11 三个线程中的一个线程 中选了一个长链条 ，给 cytoscape 准备数据
// 宽>=? 且 宽1深>=?
// 【术语】 孤立群 == 链条 == chain , 记录行数 == 点数
// 语句1. 利用以下语句 查出 主要链条 的 chainBegin_fnCallId 、 chainEnd_fnCallId
// MATCH (v:V_Chain__BzWriteDeepth)   RETURN v.root_fnCallId as chainBegin_fnCallId, v.end_fnCallId as chainEnd_fnCallId 
//    有很多个链条, 以下只是选了 其中一个长链条 即 fnCallId 从 173654 到 487355
//        当前单独一个线程 不独占fnCallId的全部分配值 因此 此链条含有的记录行数 小于 fnCallId端点值之差，具体如下
//           frida_js 的  一段fnCallId分配给单应用进程的全部线程， 而在sqlite3那里已经将另外两个线程的日志删掉了
// 语句2. 根据以下语句 返回的 记录行数 尝试 选合适的 beginW 、 w1BeginD
//      通常 w1BeginD >= beginW
with 
3 as beginW,
3 as w1BeginD,
173654 as chainBegin_fnCallId, //链条 起点
487355 as chainEnd_fnCallId //链条 终点
match (v:V_FnCallLog {direct:1})
where v.fnCallId >= chainBegin_fnCallId and v.fnCallId<=chainEnd_fnCallId
and ( v.width>=beginW or  ( v.deepth>=w1BeginD  and v.width>=1)  ) 
return v.logId as logId ,v.processId  as processId, v.curThreadId as curThreadId, v.tmPnt as tmPnt,   v.fnCallId as fnCallId, v.direct as direct,   v.fnAdr as fnAdr, v.fnSym_moduleName as fnSym_moduleName, v.fnSym_address as fnSym_address, v.fnSym_name as fnSym_name, v.fnSym_fileName as fnSym_fileName, v.fnSym_lineNumber as fnSym_lineNumber, v.fnSym_column as fnSym_column, v.width  as width_origin, toInteger(1.95^toInteger(log( v.width+1)))  as width, v.deepth as deepth, v.sonFnCallIdLs as sonFnCallIdLs
// return count(v) as 点数 //开发用   //  点数==19125



// 语句1 的变形 , 按照 链条长度排序
//  MATCH (v:V_Chain__BzWriteDeepth)   
//  with v.root_fnCallId as chainBegin_fnCallId, v.end_fnCallId as chainEnd_fnCallId,  v.end_fnCallId-v.root_fnCallId  as  chainLen 
//  order by chainLen desc
//  RETURN chainBegin_fnCallId,  chainEnd_fnCallId ,   chainLen



