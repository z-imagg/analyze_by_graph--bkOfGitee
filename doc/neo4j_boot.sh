#!/usr/bin/env bash

#【描述】 neo4j启动脚本  
#【依赖】  脚本neo4j_linux_dl_install.sh 
#【术语】 
#【返回类型说明】  
#【备注】  此脚本环境变量与 脚本neo4j_linux_dl_install.sh 有重复

shopt -s expand_aliases



export JAVA_HOME=/app/zulu11.70.15-ca-jdk11.0.22-linux_x64

export NEO4J_HOME=/app/neo4j-community-4.4.32

export PATH=$PATH:$NEO4J_HOME/bin:$JAVA_HOME/bin


neo4j version #neo4j 4.4.32


neo4j start


echo """
#http://10.0.4.220:7474/browser/
#默认用户名密码 neo4j/123456
#web端修改密码, 输入命令 ':server change-password'
"""


#关闭图形化界面, 进入 多用户文本界面  #systemctl set-default multi-user.target   #reboot
#关闭多用户文本界面, 进入 图形化界面  #systemctl set-default graphical.target

