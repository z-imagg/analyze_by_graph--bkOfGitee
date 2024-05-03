#!/bin/bash

sudo mkdir /app/pack && sudo chown z.z /app/pack 

# cytoscape-3.10.2需要的jdk17
md5_cytoscape='bb826d2598b6ceaaae56a6c938f2030e  zulu17.48.15-ca-jdk17.0.10-linux_x64.tar.gz'
( cd /app/pack && echo "$md5_cytoscape" | md5sum --check ;) || wget https://cdn.azul.com/zulu/bin/zulu17.48.15-ca-jdk17.0.10-linux_x64.tar.gz --output-document=/app/pack/zulu17.48.15-ca-jdk17.0.10-linux_x64.tar.gz
#github下的文件 通常国内下载很慢,  需要人工打开浏览器并爬墙下载 zulu17.48.15-ca-jdk17.0.10-linux_x64.tar.gz 并放到目录/app/pack/下
#若javac文件不存在 ，则解包
[[ ! -f /app/zulu17.48.15-ca-jdk17.0.10-linux_x64/bin/javac ]] && tar -zxf /app/pack/zulu17.48.15-ca-jdk17.0.10-linux_x64.tar.gz -C /app/

# cytoscape-3.10.2
md5_cytoscape='a6b5638319b301bd25e0e6987b3e35fd  cytoscape-unix-3.10.2.tar.gz'
( cd /app/pack && echo "$md5_cytoscape" | md5sum --check ;) || wget https://github.com/cytoscape/cytoscape/releases/download/3.10.2/cytoscape-unix-3.10.2.tar.gz --output-document=/app/pack/cytoscape-unix-3.10.2.tar.gz
#若cytoscape.sh文件不存在 ，则解包
[[ ! -f /app/cytoscape-unix-3.10.2/cytoscape.sh ]] && tar -zxf /app/pack/cytoscape-unix-3.10.2.tar.gz -C /app/

