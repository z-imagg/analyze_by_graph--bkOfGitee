from neo4j import GraphDatabase, RoutingControl
from neo4j import Driver

#neo4j 计算函数调用日志节点 深度
def calc_deepth(driver:Driver):
    pass


def _main():
    URI = "neo4j://localhost:7687"
    AUTH = ("neo4j", "123456")
    NEO4J_DB="neo4j"


    driver:Driver=GraphDatabase.driver(URI, auth=AUTH)
    assert isinstance(driver, Driver) == True

    try:
        calc_deepth(driver)
    except (Exception,) as  err:
        import traceback
        traceback.print_exception(err)
    finally:
        #关闭neo4j的连接
        driver.close() 


if __name__=="__main__":
    _main()