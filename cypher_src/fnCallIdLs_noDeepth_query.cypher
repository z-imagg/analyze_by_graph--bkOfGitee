MATCH (logV:V_FnCallLog )
WHERE   logV.deepth is NULL
return distinct logV.fnCallId  as _fnCallId