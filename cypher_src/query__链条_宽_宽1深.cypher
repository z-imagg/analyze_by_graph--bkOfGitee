// 宽>=? 且 宽1深>=?
// 【术语】 孤立群 == 链条 == chain , 记录行数 == 点数
// 1. 利用以下语句 查出 主要链条 的 chainBegin_fnCallId 、 chainEnd_fnCallId
// MATCH (v:V_Chain__BzWriteDeepth)   RETURN v.root_fnCallId as chainBegin_fnCallId, v.end_fnCallId as chainEnd_fnCallId 
// 2. 根据以下语句 返回的 记录行数 尝试 选合适的 beginW 、 w1BeginD
//      通常 w1BeginD >= beginW
with 
2 as beginW,
2 as w1BeginD,
8 as chainBegin_fnCallId, //链条 起点
59127-1 as chainEnd_fnCallId //链条 终点
match (v:V_FnCallLog {direct:1})
where v.fnCallId >= chainBegin_fnCallId and v.fnCallId<=chainEnd_fnCallId
and ( v.width>=beginW or  ( v.deepth>=w1BeginD  and v.width>=1)  ) 
return v.logId as logId , v.curThreadId as curThreadId, v.tmPnt as tmPnt,   v.fnCallId as fnCallId, v.direct as direct,   v.fnAdr as fnAdr, v.fnSym_moduleName as fnSym_moduleName, v.fnSym_address as fnSym_address, v.fnSym_name as fnSym_name, v.fnSym_fileName as fnSym_fileName, v.fnSym_lineNumber as fnSym_lineNumber, v.fnSym_column as fnSym_column, v.width  as width_origin, toInteger(1.95^toInteger(log( v.width+1)))  as width, v.deepth as deepth, v.sonFnCallIdLs as sonFnCallIdLs
// return count(v) as 点数 //开发用   //  点数==713
