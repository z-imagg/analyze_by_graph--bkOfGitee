#!/usr/bin/env bash

#【术语】  
#【返回类型说明】  
#【备注】  

shopt -s expand_aliases

cd /app/

F_neo4j=neo4j-community-4.4.32-unix.tar.gz
#https://neo4j.com/deployment-center/
md5_neo4j='a88d5de65332d9a5acbe131f60893b55  neo4j-community-4.4.32-unix.tar.gz'
{ echo "$md5_neo4j" | md5sum --check ;} || axel -n 8 --output=$F_neo4j https://neo4j.com/artifact.php?name=neo4j-community-4.4.32-unix.tar.gz

#通过 docker镜像 'neo4j:4.4.32-community' 知道 其用的jdk11
F_jdk11=zulu11.70.15-ca-jdk11.0.22-linux_x64.tar.gz
md5_jdk11='f13d179f8e1428a3f0f135a42b9fa75b  zulu11.70.15-ca-jdk11.0.22-linux_x64.tar.gz'
{ echo "$md5_jdk11" | md5sum --check ;} || axel -n 8 --output=$F_jdk11 https://cdn.azul.com/zulu/bin/zulu11.70.15-ca-jdk11.0.22-linux_x64.tar.gz

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
sed -i  "s/#dbms.default_listen_address=0.0.0.0/dbms.default_listen_address=0.0.0.0/g"  $F_cfg

neo4j start


#http://10.0.4.220:7474/browser/
#默认用户名密码 neo4j/neoj4
#web端修改密码, 输入命令 ':server change-password'



#关闭图形化界面, 进入 多用户文本界面  #systemctl set-default multi-user.target   #reboot
#关闭多用户文本界面, 进入 图形化界面  #systemctl set-default graphical.target

