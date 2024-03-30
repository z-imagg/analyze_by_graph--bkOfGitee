//定fnAdr max 组fnCallId内max(差tmPnt)
MATCH (log:V_FnCallLog {fnAdr:"0x7ffff74349cb"})
WITH log.fnCallId AS fnCallId, log.tmPnt AS tmPnt
ORDER BY fnCallId, tmPnt
// 以下各with比sql的groupBy强
//各with给人感觉是逐步向后传递的, 因为后面的with可以用前面with中的结果量
WITH fnCallId, collect(tmPnt) AS tmPnts
WITH fnCallId, [i in range(0, size(tmPnts)-2) | tmPnts[i+1] - tmPnts[i]] AS differences
WITH fnCallId, max(differences) AS maxDifference
// RETURN fnCallId, maxDifference
// 从开头 到这里 跟 "定fnAdr组fnCallId内max(差tmPnt)" 一样
RETURN max(maxDifference) AS maxMaxDifference 
// maxMaxDifference [5]