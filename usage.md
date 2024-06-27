## 使用手册

###   1. 准备 fridaLog 文件

以java的fridaLog为例子

```shell
fridaLogLink=/gain/frida-out/PureNow.log ; \
fridaLogReal=/fridaAnlzAp/frida_js/InterceptFnSym-java.log ; \
unlink $fridaLogLink ; \
ln -s $fridaLogReal $fridaLogLink ; \
ls -lh $fridaLogLink
```

### (例) 查找openjdk-24(java)的fridaLog中调用次数大于1万次的函数们


行尾的续行符 不是必须的， 只是为了方便，    当你整体复制 在终端下执行后,  按上箭头 获得的历史命令 将是 在单行 ， 而不是分散在几行，这样方便

#### 2. fridaLog转sqlite3 (查找fridaLog中调用次数大于1万的函数们)

```shell
source /fridaAnlzAp/analyze_by_graph/_pythonpath_disableBuffered.sh

#做完 fridaLog转sqlite3 后， 不做 sqlite3转neo4j, 但要求 neo4j实例 得在运行
envVar__analyze_by_graph__fridaLog_to_sqlite3_only=True python fridaLog-sqlite3-neo4j/_main_fridaLog-sqlite3-neo4j.py 2>&1 | tee fridaLog-sqlite3-java.log
```


### (例) 一键正常使用 (fridaLog转sqlite3转neo4j 、 neo4j遍历器算法 、初步可视化)

```shell
bash /fridaAnlzAp/analyze_by_graph/_main.sh
```

[_main.sh](http://giteaz:3000/frida_analyze_app_src/analyze_by_graph/src/branch/release/_main.sh)


### (例) 分步正常使用 

#### 0. 前置
```shell
source /fridaAnlzAp/analyze_by_graph/_pythonpath_disableBuffered.sh
cd /fridaAnlzAp/analyze_by_graph/
```

#### 1. fridaLog转sqlite3转neo4j

```shell
PYTHONPATH="$_PYTHONPATH__fridaLog_to_sqlite3_to_neo4j" python fridaLog-sqlite3-neo4j/_main_fridaLog-sqlite3-neo4j.py 2>&1 | tee fridaLog-sqlite3-neo4j.log
```

#### 2. neo4j遍历器算法

```shell
PYTHONPATH="$_PYTHONPATH__neo4j_traverse" python  neo4j_traverse_bz/_main_neo4j_traverse_bz.py 2>&1 | tee _main_neo4j_traverse_bz.log
```

#### 3. 初步可视化

```shell
PYTHONPATH="$_PYTHONPATH__basic_visual_main" python  visual/visual_main.py
```
