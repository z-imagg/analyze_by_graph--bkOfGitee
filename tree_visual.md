```cypher
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
return count(v) as 点数
```

```
╒════╕
│点数 │
╞════╡
│6987│
└────┘
```