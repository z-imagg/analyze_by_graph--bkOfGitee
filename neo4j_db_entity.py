#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Neo4J_DB_Entity:
    def __init__(self,URI:str,AUTH_user:str,AUTH_pass:str,DB_NAME:str) -> None:
        """
        URI = "neo4j://localhost:7687"
        AUTH = ("neo4j", "123456")
        DB_NAME = "neo4j"
        """
        self.URI:str = URI
        self.AUTH_user:str = AUTH_user
        self.AUTH_pass:str = AUTH_pass
        self.DB_NAME:str=DB_NAME
        return
