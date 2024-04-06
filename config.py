#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】  
#【返回类型说明】  
#【备注】 


from neo4j_db_basic import Neo4J_DB_Entity


neo4jDB_default= Neo4J_DB_Entity(URI="neo4j://localhost:7687", AUTH_user="neo4j", AUTH_pass="123456", DB_NAME="neo4j")