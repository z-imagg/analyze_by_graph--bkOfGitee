// 宽>=? 且 宽1深>=?
//  孤立群 == 链条 == chain
with 
4 as beginW,
5 as w1BeginD,
13 as chainBegin_fnCallId, //链条 起点
229638-1 as chainEnd_fnCallId //链条 终点
match (v:V_FnCallLog {direct:1})
where v.fnCallId >= chainBegin_fnCallId and v.fnCallId<=chainEnd_fnCallId
and ( v.width>=beginW or  ( v.deepth>=w1BeginD  and v.width>=1)  ) 
return v.logId as logId , v.curThreadId as curThreadId, v.tmPnt as tmPnt,   v.fnCallId as fnCallId, v.direct as direct,   v.fnAdr as fnAdr, v.fnSym_moduleName as fnSym_moduleName, v.fnSym_address as fnSym_address, v.fnSym_name as fnSym_name, v.fnSym_fileName as fnSym_fileName, v.fnSym_lineNumber as fnSym_lineNumber, v.fnSym_column as fnSym_column, v.width  as width_origin, toInteger(log(v.width*10000+1))  as width, v.deepth as deepth, v.sonFnCallIdLs as sonFnCallIdLs
// return count(v) as 点数 //开发用   //  点数==6987
