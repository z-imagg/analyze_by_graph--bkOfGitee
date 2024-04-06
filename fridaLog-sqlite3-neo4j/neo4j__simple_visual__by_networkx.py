#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【标题】 简易可视化neo4j图（以networkx）
#【术语】 
#【备注】 
#【术语】 

## 简易可视化neo4j图（以networkx）

# networkx在边上 显示neo4j的关系名 ，支持多个关系名，多个关系名写在同一个networkx边上, 获得关系名字列表的简单写法

import neo4j
from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt

#### 只可视化前TopN即30个边

TopN=30

#### 可视化方法

def neo2jPath_to_networkxG(sess:neo4j.Session):
    G = nx.MultiGraph()
    records= sess.run(
f"""MATCH (n)-[r]->(m)
RETURN n, r, m LIMIT {TopN}""",
        # database_=NEO4J_DB, routing_=RoutingControl.READ,
    )
    for record in records:
        srcV=record['n']['fnSym_address']
        dstV=record['m']['fnSym_address']
        relation_type = record['r'].type
        # print("neo4j中的关系名字为",relation_type)
        G.add_node(srcV)
        G.add_node(dstV)
        G.add_edge(srcV,dstV,E_FnEL=relation_type)
    return G

#### 可视化
# 前面已经建立过了neo4j连接，这里不再建立
# driver= GraphDatabase.driver(URI, auth=AUTH)

def neo4j_visual__by_networkx(sess:neo4j.Session):
    G=neo2jPath_to_networkxG(sess)

    pos = nx.spring_layout(G)  
    plt.figure(figsize=(10, 8))

    nx.draw_networkx_nodes(G, pos, node_size=800, node_color='skyblue')
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)

    edge_labels = {(u, v): [d['E_FnEL'] for k, d in G[u][v].items()] for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("visual neo4j graph by networkx")
    plt.show()

#### 关闭neo4j连接
# driver.close()


#### 调试写法
#边列表，简陋
# G.edges()
#边列表，完备
# G.edges(keys=True, data=True)
#获取关系名字ReltnName列表
# [  ( f"{u},{v}", G[u][v].items() ) for u, v in G.edges()]
#### 错误写法
#错误写法，只获取到了最后一个关系名字ReltnName
# {(u, v): d['E_FnEL']  for u, v, k, d in G.edges(keys=True, data=True)}

## 此notebook结束时刻


