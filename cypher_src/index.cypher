
// CREATE INDEX FOR (n:V_FnCallLog) ON (n.logId)  // .ipynb中创建的索引

CREATE INDEX FOR (n:V_FnCallLog) ON (n.deepth) ;
CREATE INDEX FOR (n:V_FnCallLog) ON (n.fnCallId) ;

CREATE INDEX FOR (n:V_FnCallLog) ON (n.fnAdr) ;

CREATE INDEX FOR (n:V_FnCallLog) ON (n.fnAdr,n.direct) ;