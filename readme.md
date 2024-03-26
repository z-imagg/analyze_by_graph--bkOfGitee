
不再手工搭建 jupyter pyspark环境 、 jupyeter scala_spark 环境

转而 使用 docker镜像，比如 ```jupyter/pyspark-notebook:2023-05-30```, https://github.com/jupyter/docker-stacks.git 


```cat /etc/docker/daemon.json ```
```json
{
  "registry-mirrors": ["https://fe2ajwut.mirror.aliyuncs.com"]
}
```


不要加前缀quay.io ，即不要写为  ```quay.io/jupyter/pyspark-notebook:2023-05-30```，否则 国内 pull不了, 因为 他已经在  https://hub.docker.com/layers/jupyter/pyspark-notebook/latest/images/sha256-7d0b19de594978b8c0541194d91e29abba40e20aa124873bcf5e9cda2fe037f7?context=explore



```docker run -p 10000:8888  jupyter/pyspark-notebook:2023-05-30```，  输出 访问 jupyter 的url地址， 将其中8888换成10000, 形如  http://127.0.0.1:10000/lab?token=... 