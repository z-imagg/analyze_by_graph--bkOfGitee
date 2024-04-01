with 
1 AS FnEnter,
2 as FnLeave

MATCH (logV:V_FnCallLog {fnCallId:$fnCallId, direct:FnLeave})
return logV