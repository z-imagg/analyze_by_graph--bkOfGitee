
## 使用手册

行尾的续行符 不是必须的， 只是为了方便，    当你整体复制 在终端下执行后,  按上箭头 获得的历史命令 将是 在单行 ， 而不是分散在几行，这样方便


###   0. 准备项目py环境

miniconda激活环境、pip安装项目目录下的requirements.txt依赖

```shell

#以source 加载依赖脚本
#_condaEnvActivate_pipInstallRequirements == miniconda激活环境、pip安装项目目录下的requirements.txt依赖

source /app/bash-simplify/condaEnvActivate_pipInstallRequirements.sh ; \
_CondaHome=/app/Miniconda3-py310_22.11.1-1 ; \
_PrjHome=/fridaAnlzAp/analyze_by_graph  ; \
_condaEnvActivate_pipInstallRequirements  $_CondaHome  $_PrjHome  ; \
_CondaBin=$_CondaHome/bin ; \
_CondaPy=$_CondaBin/python
```

###   1. 准备 fridaLog 文件

以java的fridaLog为例子

```shell
fridaLogLink=/gain/frida-out/PureNow.log ; \
fridaLogReal=/fridaAnlzAp/frida_js/InterceptFnSym-java.log ; \
unlink $fridaLogLink ; \
ln -s $fridaLogReal $fridaLogLink ; \
ls -lh $fridaLogLink
```

### (例2A) 查找fridaLog中调用次数大于1万次的函数们

诉求：  查找openjdk-24(java)的fridaLog中调用次数大于1万次的函数们， 从而 方便开发者 修改 frida_js脚本 屏蔽掉这些 频繁调用函数 ， 以 迫使 openjdk-24(java) 更快运行完  且 产生的 fridaLog更小

实现过程是 : fridaLog转sqlite3 、sqlite3中查询调用次数大于1万的函数们

 

```shell
source /fridaAnlzAp/analyze_by_graph/_pythonpath_disableBuffered.sh

#做完 fridaLog转sqlite3 后， 不做 sqlite3转neo4j, 但要求 neo4j实例 得在运行
envVar__analyze_by_graph__fridaLog_to_sqlite3_only=True $_CondaPy fridaLog-sqlite3-neo4j/_main_fridaLog-sqlite3-neo4j.py 2>&1 | tee fridaLog-sqlite3-java.log
```


### (例2B) 一键正常使用
 
 一键 执行 **fridaLog转sqlite3转neo4j 、 neo4j遍历器算法 、初步可视化**

```shell
bash /fridaAnlzAp/analyze_by_graph/_main.sh
```

[_main.sh](http://giteaz:3000/frida_analyze_app_src/analyze_by_graph/src/branch/release/_main.sh)


### (例2C) 分步正常使用 

#### 2C.0、 前置
```shell
source /fridaAnlzAp/analyze_by_graph/_pythonpath_disableBuffered.sh
cd /fridaAnlzAp/analyze_by_graph/
```

#### 2C.1、 fridaLog转sqlite3转neo4j

```shell
PYTHONPATH="$_PYTHONPATH__fridaLog_to_sqlite3_to_neo4j" $_CondaPy fridaLog-sqlite3-neo4j/_main_fridaLog-sqlite3-neo4j.py 2>&1 | tee fridaLog-sqlite3-neo4j.log
```

#### 2C.2、 neo4j遍历器算法

```shell
PYTHONPATH="$_PYTHONPATH__neo4j_traverse" $_CondaPy  neo4j_traverse_bz/_main_neo4j_traverse_bz.py 2>&1 | tee _main_neo4j_traverse_bz.log
```

#### 2C.3、 初步可视化

```shell
PYTHONPATH="$_PYTHONPATH__basic_visual_main" $_CondaPy  visual/visual_main.py
```
