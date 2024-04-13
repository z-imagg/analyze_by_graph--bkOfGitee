#!/usr/bin/env bash

#【术语】  
#【返回类型说明】  
#【备注】  

shopt -s expand_aliases

cd /app/

S=/app/Miniconda3-py310_22.11.1-1/bin/activate

[ -f $S ] && { echo "已安装$S;退出代码0" && exit 0 ;}


sudo apt install axel -y

F=Miniconda3-py310_22.11.1-1-Linux-x86_64.sh
md5sum_txt='e01420f221a7c4c6cde57d8ae61d24b5  Miniconda3-py310_22.11.1-1-Linux-x86_64.sh' 

{ echo "$md5sum_txt" | md5sum --check ;} || axel -n 8 https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-py310_22.11.1-1-Linux-x86_64.sh

bash $F


