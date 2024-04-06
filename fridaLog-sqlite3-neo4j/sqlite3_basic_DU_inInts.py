#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 sqlite删改函数
#【术语】 
#【备注】 
#【术语】 

from sqlite3 import Row as sqlite3Row
import typing

from sqlite3_basic_func import sq3DU
from basic_tool import joinInts
## sqlite删改函数

### sq3DU_inInts: sqlite3执行sql删改 携带in整数列表条件  
def sq3DU_inInts(sq3dbConn,sqlInIntLs,intLs):
    intStrLs=joinInts(intLs)
    sqlTxt=sqlInIntLs.format(lsVar=intStrLs)
    return sq3DU(sq3dbConn,sqlTxt)

#调用举例
# sq3DU_inInts(sq3dbConn,"select  *  from t_FnCallLog where fnCallId in ({lsVar}) ",[-1,-20]    )
# -1

