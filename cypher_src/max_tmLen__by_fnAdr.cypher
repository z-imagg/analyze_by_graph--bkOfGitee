//术语  tmLen == timeLength == 时间长度 == 时刻点timePointA数值 - 时刻点timePointB数值
//定fnAdr max 组fnCallId内max(差tmPnt)
MATCH (log:V_FnCallLog {fnAdr:$fnAdr})  //"0x7ffff74349cb"
WITH log.fnCallId AS fnCallId, log.tmPnt AS tmPnt
ORDER BY fnCallId, tmPnt
// 以下各with比sql的groupBy强
//各with给人感觉是逐步向后传递的, 因为后面的with可以用前面with中的结果量
WITH fnCallId, collect(tmPnt) AS tmPnts
// tmPnts[0] 是 函数进入 时刻点 ,  tmPnts[1] 是 函数退出 时刻点; tmLen是此次函数调用持续的时间长度
WITH fnCallId, tmPnts[1] - tmPnts[0] AS tmLen
// RETURN fnCallId, tmLen
RETURN   max(tmLen) AS max_tmLen
// maxMaxDifference 5