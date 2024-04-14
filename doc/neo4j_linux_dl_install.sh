#!/usr/bin/env bash

#【术语】  
#【返回类型说明】  
#【备注】  

shopt -s expand_aliases

#重启本地下载服务
# { kill -9 $(ps auxf | grep python3 | grep 2111 | awk '{print $2}')  && sleep 1 ;}  ;  ( cd /app/pack/ && python3 -m http.server 2111 & )

LocFDlSvr="http://172.17.0.1:2111"

cd /app/

F_neo4j=neo4j-community-4.4.32-unix.tar.gz
#https://neo4j.com/deployment-center/
md5_neo4j="a88d5de65332d9a5acbe131f60893b55  $F_neo4j"
#    优先从本地文件下载服务下载 ，其次才从外网文件下载
{ echo "$md5_neo4j" | md5sum --check ;} ||  { curl ${LocFDlSvr} &&   wget --output-document=$F_neo4j ${LocFDlSvr}/$F_neo4j ;} ||  axel -n 8 --output=$F_neo4j https://neo4j.com/artifact.php?name=neo4j-community-4.4.32-unix.tar.gz

#通过 docker镜像 'neo4j:4.4.32-community' 知道 其用的jdk11
F_jdk11=zulu11.70.15-ca-jdk11.0.22-linux_x64.tar.gz
md5_jdk11="f13d179f8e1428a3f0f135a42b9fa75b  $F_jdk11"
#    优先从本地文件下载服务下载 ，其次才从外网文件下载
{ echo "$md5_jdk11" | md5sum --check ;} ||  { curl ${LocFDlSvr} &&   wget --output-document=$F_jdk11 ${LocFDlSvr}/$F_jdk11 ;} || axel -n 8 --output=$F_jdk11 https://cdn.azul.com/zulu/bin/zulu11.70.15-ca-jdk11.0.22-linux_x64.tar.gz

export JAVA_HOME=/app/zulu11.70.15-ca-jdk11.0.22-linux_x64
tar -zxf $F_jdk11 -C "$(dirname  $JAVA_HOME)"

export NEO4J_HOME=/app/neo4j-community-4.4.32
tar -zxf $F_neo4j  -C "$(dirname  $NEO4J_HOME)"
#tar -zxf $F_neo4j  -C /app

export PATH=$PATH:$NEO4J_HOME/bin:$JAVA_HOME/bin

neo4j --help
# console start   stop    restart status  version help 

neo4j version #neo4j 4.4.32

F_cfg=/app/neo4j-community-4.4.32/conf/neo4j.conf
grep dbms.default_listen_address $F_cfg
grep dbms.memory $F_cfg
cp -v $F_cfg "${F_cfg}_$(date +%s)"
#修改 neo4j 监听地址为0.0.0.0
sed -i  "s/#dbms.default_listen_address=0.0.0.0/dbms.default_listen_address=0.0.0.0/g"  $F_cfg
#修改 neo4j 线程数目为 4 
sed -i  's/#dbms.threads.worker_count=/dbms.threads.worker_count=4/'   $F_cfg

#neo4j安装apoc插件
F_apocAllJar_fullPath=/app/neo4j-community-4.4.32/plugins/apoc-4.4.0.26-all.jar
F_apocAllJar=/app/neo4j-community-4.4.32/plugins/apoc-4.4.0.26-all.jar
md5_apocAllJar="5a42a32e12432632124acd682382c91d  $F_apocAllJar_fullPath"
#    优先从本地文件下载服务下载 ，其次才从外网文件下载
{ echo "$md5_apocAllJar" | md5sum --check ;} ||  { curl ${LocFDlSvr} &&   wget --output-document=$F_apocAllJar_fullPath ${LocFDlSvr}/$F_apocAllJar ;} || wget --output-document=$F_apocAllJar_fullPath    https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/4.4.0.26/apoc-4.4.0.26-all.jar


#neo4j重启
# neo4j restart

#neo4j状态
# neo4j status

#启动neo4j
neo4j start


#http://10.0.4.220:7474/browser/
#neo4j-community-4.4.32默认用户名密码 neo4j/neo4j
#web端修改密码, 输入命令 ':server change-password'



#关闭图形化界面, 进入 多用户文本界面  #systemctl set-default multi-user.target   #reboot
#关闭多用户文本界面, 进入 图形化界面  #systemctl set-default graphical.target

