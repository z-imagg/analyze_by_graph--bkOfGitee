### 将neo4j的 点V_FnCallLog_Analz、边E_P2S 可视化到 cytoscape
执行以下cypher脚本 ， 将 顶点 V_FnCallLog_Analz 的字段fnSym_fileName 的前缀 '/fridaAnlzAp/cgsecurity--testdisk/src/' 删除

```cypher
MATCH (n:V_FnCallLog_Analz) 
// replace可以换作apoc.text.replace
set n.fnSym_fileName=replace(n.fnSym_fileName, '/fridaAnlzAp/cgsecurity--testdisk/src/', '') 
// return n
```

利用 cytoscape 可视化 neo4j中的 V_FnCallLog_Analz、E_P2S


https://apps.cytoscape.org/apps/cytoscapeneo4jplugin


https://apps.cytoscape.org/apps/yfileslayoutalgorithms


```cypher
MATCH (v1:V_FnCallLog_Analz) - [e:E_P2S] -> (v2:V_FnCallLog_Analz) return v1,e,v2
```


###  yFiles Orgnatic Layout

[cytoscape__testdisk_qphotorec/Group_Attributes_Layout__fnSym_fileName.cys](http://giteaz:3000/frida_analyze_app_src/analyze_by_graph/src/branch/main/visual/cytoscape__testdisk_qphotorec/Group_Attributes_Layout__fnSym_fileName.cys)



Style  选择 "BiPAX"

1.  Style 下的 "Fill Color" 被 字段deepth  离散映射 

     人工选的不同颜色


2.  Style 下的 "Heigth" 被 字段deepth 离散映射 

     人工选的不同数值， 字段deepth值  与 "Heigth" 成 反比


3.  Style 下的 "Width" 被 字段width 离散映射 

     人工选的不同数值， 字段width值  与 "Width" 成 正比


4.  Style 下的 "Label" 被 字段fnSym_name  "Passthrough Mapping" 



入口main函数最矮, 叶子较高

函数内容中调用函数次数越多的越宽



![cytoscape__testdisk_qphotorec/yFiles_Orgnatic_Layout.png](http://giteaz:3000/frida_analyze_app_src/analyze_by_graph/raw/branch/main/visual/cytoscape__testdisk_qphotorec/yFiles_Orgnatic_Layout.png)


###  "Group Attributes Layout --> fnSym_fileName"


Style  选择 "default black"

1.  Style 下的 "Size" 被 字段width "Passthrough Mapping" 



[cytoscape__testdisk_qphotorec/yFiles_Orgnatic_Layout.cys](http://giteaz:3000/frida_analyze_app_src/analyze_by_graph/src/branch/main/visual/cytoscape__testdisk_qphotorec/yFiles_Orgnatic_Layout.cys)



![cytoscape__testdisk_qphotorec/Group_Attributes_Layout__fnSym_fileName.png](http://giteaz:3000/frida_analyze_app_src/analyze_by_graph/raw/branch/main/visual/cytoscape__testdisk_qphotorec/Group_Attributes_Layout__fnSym_fileName.png)