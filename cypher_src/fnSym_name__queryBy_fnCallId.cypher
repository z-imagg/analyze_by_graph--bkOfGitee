MATCH (logV:V_FnCallLog )
WHERE   logV.fnCallId =$fnCallId
return  logV