
## 丑陋但正确且速度正常的遍历器（小节 起_t入_B0__BJ_fJ_LJ_tJ_ 逐前拱）结论

”看起来思路正确、执行正常、效率正常、但很丑/遍历器（小节逐前拱即丑陋的neo4j路径匹配分拆：起_t入_B0__BJ_fJ_LJ_tJ_）,看起来运行效率正常“ 

0. 不平衡点为函数_start

  函数_start是编译器生成的入口函数，其只进不出，也算说的过去吧。是不是真的这样 还有待排查。
  
  这也是 [frida_js 从frida_trace改为frida 97a1ec](http://giteaz:3000/frida_analyze_app_src/frida_js/commit/97a1ec655ba4e01824619c78671784ed9485240c)导致的效果

1. 孤立点群 情况改善了

  这说明[frida_js 从frida_trace改为frida 97a1ec](http://giteaz:3000/frida_analyze_app_src/frida_js/commit/97a1ec655ba4e01824619c78671784ed9485240c)的路子是对的

2. 遍历完所有日志记录行大约 deepth 52分钟， width 52分钟， markup 81分钟到130分钟

  比之前有很大提升， 

  前一版本 ["...遍历器（路径模式很漂亮：起空_重复点k_终空）...282cb"](http://giteaz:3000/frida_analyze_app_src/analyze_by_graph/commit/282cb106d56fc3615f413133f3f0fd0083e413c7) 遍历完一趟所有日志记录行数大约需要8天

## 不平衡点  fnCallId==1 ==_start

**编译器生成的入口函数_start只入不出？，听起来有点合理？**
是不是真的这样 还有待排查。

[6500f/fridaLog-sqlite3-neo4j.ipynb](http://giteaz:3000/frida_analyze_app_src/analyze_by_graph/raw/commit/6500f6561f4adc5163d367ee9f6c8aa079c6c493/fridaLog-sqlite3-neo4j.ipynb)

```
找到不平衡的fnCallIdLs [1]
找到不平衡的tmPntLs= [1]
```

```
找到不平衡的FnSym列表 _symLs_nBl= [{'address': '0x5555555659e0', 'name': '_start', 'moduleName': 'simple_nn.elf', 'fileName': '', 'lineNumber': 0, 'column': 0}]
```


##  孤立点群 情况改善了

孤立点群 数 变少了， 同时 大群够大， 但依然有孤立点群

解决 孤立点群 问题 要改善 [frida_js.git](http://giteaz:3000/frida_analyze_app_src/frida_js.git)

### 编译器 生成的入口代码 导致的 合理的 孤立点群



####  fnCallId==2 == _init

**编译器生成的初始化函数_init不调用应用程序，看起来也是合理的？**

```cypher
match (v:V_FnCallLog {fnCallId:2})
return v
```

```
╒══════════════════════════════════════════════════════════════════════╕
│v                                                                     │
╞══════════════════════════════════════════════════════════════════════╡
│(:V_FnCallLog {fnSym_lineNumber: 0,fnCallId: 2,fnSym_address: "0x55555│
│5565000",fnSym_column: 0,fnAdr: "0x555555565000",fnSym_name: "_init",t│
│mPnt: 2,direct: 1,fnSym_moduleName: "simple_nn.elf",logId: 2,fnSym_fil│
│eName: "",curThreadId: 11557})                                        │
├──────────────────────────────────────────────────────────────────────┤
│(:V_FnCallLog {fnSym_lineNumber: 0,fnCallId: 2,fnSym_address: "0x55555│
│5565000",fnSym_column: 0,fnAdr: "0x555555565000",fnSym_name: "_init",t│
│mPnt: 3,direct: 2,fnSym_moduleName: "simple_nn.elf",logId: 3,fnSym_fil│
│eName: "",curThreadId: 11557})                                        │
└──────────────────────────────────────────────────────────────────────┘
```

#### fnCallId==5 == _GLOBAL__sub_I_main


**编译器生成的啥作用的函数_GLOBAL__sub_I_main不调用应用程序，看起来也是合理的？**

```cypher
match (v:V_FnCallLog {fnCallId:5})
return v
```

```
╒══════════════════════════════════════════════════════════════════════╕
│v                                                                     │
╞══════════════════════════════════════════════════════════════════════╡
│(:V_FnCallLog {fnSym_lineNumber: 0,fnCallId: 5,fnSym_address: "0x55555│
│5566008",fnSym_column: 0,fnSym_name: "_GLOBAL__sub_I_main",fnAdr: "0x5│
│55555566008",tmPnt: 8,direct: 1,fnSym_moduleName: "simple_nn.elf",logI│
│d: 8,fnSym_fileName: "",curThreadId: 11557})                          │
├──────────────────────────────────────────────────────────────────────┤
│(:V_FnCallLog {fnSym_lineNumber: 0,fnCallId: 5,fnSym_address: "0x55555│
│5566008",fnSym_column: 0,fnSym_name: "_GLOBAL__sub_I_main",fnAdr: "0x5│
│55555566008",tmPnt: 23,direct: 2,fnSym_moduleName: "simple_nn.elf",log│
│Id: 23,fnSym_fileName: "",curThreadId: 11557})                        │
└──────────────────────────────────────────────────────────────────────┘
```

### 大 孤立点群

#### 现象
从 fnCallId==13 开始遍历 ，遍历到 fnCallId==229371 停止，

- deepth耗时约15分钟， 更新记录数458718

- width 耗时约15分钟， 更新记录数458718

- markup耗时约23分钟， 更新记录数286214

叶子节点不填写markup字段，因此markup更新记录少是正常的

因为markup字段是大json文本，耗时长正常

####  估计
由此估计 记录数一共1619590， :

- deepth耗时约52分钟， 

- width 耗时约52分钟， 

- markup耗时约81分钟到130分钟

### 下一个 孤立点群

[孤立函数  __call_tls_dtors 调用了 函数 _ZN5torch3jit6tracer13ArgumentStashD1Ev 0x7ffff766da32  ， 若frida_js拦截 __call_tls_dtors 可合并由此导致的 若干孤立群 ， a38b2](http://giteaz:3000/frida_analyze_app_src/frida_js/commit/a38b2b49c3ac3d52a8368ee5fe652f730645593c)

由此可知 frida_js 需要 拦截 __call_tls_dtors 能聚拢 因 没拦截 __call_tls_dtors 导致的 若干孤立群

下一个 孤立点群 起点 是 fnCallId==229372， 终点 要 从该起点遍历后 才知道

fnCallId==229372的 函数名```_ZN5torch3jit6tracer13ArgumentStashD1Ev```,  demangle解码后为```torch::jit::tracer::ArgumentStash::~ArgumentStash()```  

所用 demangle解码网站 http://demangler.com/

```cypher
match (v:V_FnCallLog {fnCallId:229372})
return v
```

```
╒══════════════════════════════════════════════════════════════════════╕
│v                                                                     │
╞══════════════════════════════════════════════════════════════════════╡
│(:V_FnCallLog {fnSym_lineNumber: 0,fnCallId: 229372,fnSym_address: "0x│
│7ffff766da32",fnSym_column: 0,fnAdr: "0x7ffff766da32",fnSym_name: "_ZN│
│5torch3jit6tracer13ArgumentStashD1Ev",tmPnt: 458742,direct: 1,fnSym_mo│
│duleName: "libtorch.so.1",logId: 458742,fnSym_fileName: "",curThreadId│
│: 11557})                                                             │
├──────────────────────────────────────────────────────────────────────┤
│(:V_FnCallLog {fnSym_lineNumber: 0,fnCallId: 229372,fnSym_address: "0x│
│7ffff766da32",fnSym_column: 0,fnAdr: "0x7ffff766da32",fnSym_name: "_ZN│
│5torch3jit6tracer13ArgumentStashD1Ev",tmPnt: 458791,direct: 2,fnSym_mo│
│duleName: "libtorch.so.1",logId: 458791,fnSym_fileName: "",curThreadId│
│: 11557})                                                             │
└──────────────────────────────────────────────────────────────────────┘
```

## 情况展示

### 字段witdh

字段witdh 填写范围 fnCallId从 13 到 229371 ，被填写日志行数458718

```cypher
match (v:V_FnCallLog)
where v.width is not null
return count(v) as 有w行数, min(v.fnCallId) as 有w最小fnCId, max(v.fnCallId) as 有w最大fnCId
```

```
╒══════╤═════════╤═════════╕
│有w行数  │有w最小fnCId│有w最大fnCId│
╞══════╪═════════╪═════════╡
│458718│13       │229371   │
└──────┴─────────┴─────────┘
```

### 字段deepth

字段deepth 填写范围 fnCallId从 13 到 229371 ，被填写日志行数458718


```cypher
match (v:V_FnCallLog)
where v.deepth is not null
return count(v) as 有d行数, min(v.fnCallId) as 有d最小fnCId, max(v.fnCallId) as 有d最大fnCId
```

```
╒══════╤═════════╤═════════╕
│有d行数  │有d最小fnCId│有d最大fnCId│
╞══════╪═════════╪═════════╡
│458718│13       │229371   │
└──────┴─────────┴─────────┘
```

### 字段markup 

字段markup 填写范围 fnCallId从 13 到 229370， 被填写日志行数286214

叶子不填写字段markup， 所以 比对 字段witdh、字段deepth 可知， 差异的 fnCallId==229371的两行日志 一定是叶子

```cypher
match (v:V_FnCallLog)
where v.markup is not null
return count(v) as 有m行数, min(v.fnCallId) as 有m最小fnCId, max(v.fnCallId) as 有m最大fnCId
```

```
╒══════╤═════════╤═════════╕
│有m行数  │有m最小fnCId│有m最大fnCId│
╞══════╪═════════╪═════════╡
│286214│13       │229370   │
└──────┴─────────┴─────────┘
```


查询  差异的 fnCallId==229371的两行日志 ， 此两行 deepth==0 即为叶子节点

```cypher
match (v:V_FnCallLog {fnCallId:229371})
return v.logId,v.fnCallId, v.fnAdr,v.fnSym_moduleName, v.fnSym_fileName, v.fnSym_name, v.deepth,v.width
```


```
╒═══════╤══════════╤════════════════╤══════════════════╤════════════════╤════════════════════════════════════════════════════════╤════════╤═══════╕
│v.logId│v.fnCallId│v.fnAdr         │v.fnSym_moduleName│v.fnSym_fileName│v.fnSym_name                                            │v.deepth│v.width│
╞═══════╪══════════╪════════════════╪══════════════════╪════════════════╪════════════════════════════════════════════════════════╪════════╪═══════╡
│458734 │229371    │"0x55555556c6ea"│"simple_nn.elf"   │""              │"_ZNSt12__weak_countILN9__gnu_cxx12_Lock_policyE2EED2Ev"│0       │0      │
├───────┼──────────┼────────────────┼──────────────────┼────────────────┼────────────────────────────────────────────────────────┼────────┼───────┤
│458735 │229371    │"0x55555556c6ea"│"simple_nn.elf"   │""              │"_ZNSt12__weak_countILN9__gnu_cxx12_Lock_policyE2EED2Ev"│0       │0      │
└───────┴──────────┴────────────────┴──────────────────┴────────────────┴────────────────────────────────────────────────────────┴────────┴───────┘
```


##  torch1.3.1 的 链条们 

根据 [临时粗略改造，为了跳过短链条，找到下一个长链条  ea5b0 ](http://giteaz:3000/frida_analyze_app_src/analyze_by_graph/commit/ea5b057e26ca4d0761dd880da13e33dab8b4504f)  ,  [遍历器 ，代码无修改，记录几个小孤立群  bfc1 ](http://giteaz:3000/frida_analyze_app_src/analyze_by_graph/commit/bfc1a6837cefb4a828ad3e8d8dadb39d416907fb)  

直观获得以下  链条们 


```cypher
// 查询各链条的起点
match (v:V_FnCallLog {direct:1})
where v.fnCallId in [2,3,5,13,229372,229401,229470,229539,229608,229625,229635,229637,229638]
return v.fnCallId,v.fnSym_name,v.fnSym_moduleName
order by v.fnCallId asc



```

各链条的起点如下：

```

╒══════════╤══════════════════════════════════════════════════════════════════════╤══════════════════╕
│v.fnCallId│v.fnSym_name                                                          │v.fnSym_moduleName│
╞══════════╪══════════════════════════════════════════════════════════════════════╪══════════════════╡
│2         │"_init"                                                               │"simple_nn.elf"   │
├──────────┼──────────────────────────────────────────────────────────────────────┼──────────────────┤
│3         │"frame_dummy"                                                         │"simple_nn.elf"   │
├──────────┼──────────────────────────────────────────────────────────────────────┼──────────────────┤
│5         │"_GLOBAL__sub_I_main"                                                 │"simple_nn.elf"   │
├──────────┼──────────────────────────────────────────────────────────────────────┼──────────────────┤
│13        │"main"                                                                │"simple_nn.elf"   │ 长链条
├──────────┼──────────────────────────────────────────────────────────────────────┼──────────────────┤
│229372    │"__call_tls_dtors"                                                    │"libc.so.6"       │
├──────────┼──────────────────────────────────────────────────────────────────────┼──────────────────┤
│229401    │"_ZN3c1021TensorTypeIdRegistrarD1Ev"                                  │"libc10.so"       │ 析构函数； 从这里开始以下都是析构（资源回收）？
├──────────┼──────────────────────────────────────────────────────────────────────┼──────────────────┤
│229470    │"_ZN3c1021TensorTypeIdRegistrarD1Ev"                                  │"libc10.so"       │ 析构函数；
├──────────┼──────────────────────────────────────────────────────────────────────┼──────────────────┤
│229539    │"_ZN3c1021TensorTypeIdRegistrarD1Ev"                                  │"libc10.so"       │ 析构函数；
├──────────┼──────────────────────────────────────────────────────────────────────┼──────────────────┤
│229608    │"_ZNSt10unique_ptrIN2at29LegacyDeviceTypeInitInterfaceESt14default_del│"libcaffe2.so"    │ 析构函数；
│          │eteIS1_EED1Ev"                                                        │                  │
├──────────┼──────────────────────────────────────────────────────────────────────┼──────────────────┤
│229625    │"_ZNSt6vectorISt10shared_ptrIN5torch3jit6script4TreeEESaIS5_EED1Ev"   │"simple_nn.elf"   │ 析构函数；
├──────────┼──────────────────────────────────────────────────────────────────────┼──────────────────┤
│229635    │"__do_global_dtors_aux"                                               │"simple_nn.elf"   │ c++处理全局变量的析构函数调用
├──────────┼──────────────────────────────────────────────────────────────────────┼──────────────────┤
│229637    │"_fini"                                                               │"simple_nn.elf"   │ 链接器生成，在程序结束时会被自动调用
├──────────┼──────────────────────────────────────────────────────────────────────┼──────────────────┤
│229638    │"__do_global_dtors_aux"                                               │"libtorch.so.1"   │ c++处理全局变量的析构函数调用; 长链条
└──────────┴──────────────────────────────────────────────────────────────────────┴──────────────────┘


```


```D1Ev == 'D表示析构（Destructor），1表示该函数没有参数，Ev表示返回值为void' ```