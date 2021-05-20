from config import DbCfg
import mysql.connector
from mysql.connector import pooling



# connect to MySQL databases
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name = 'MySQLPool',
        pool_size = 5,
        host = DbCfg.host,
        user = DbCfg.usr,
        password = DbCfg.pwd,
        database = DbCfg.db
 )


##### functions #####

def get_attractions_data(num_per_page, start_point, keyword):
    sitedb = connection_pool.get_connection()
    cursor = sitedb.cursor()
    if not keyword:
        query = f'SELECT * FROM attractions LIMIT {start_point},{num_per_page}'
        cursor.execute(query)
        results = cursor.fetchall() 
        
    else:
        keyword_query_condition = f'''
        WHERE name LIKE "%{keyword}%" 
        OR category LIKE "%{keyword}%" 
        OR description LIKE "%{keyword}%" 
        OR address LIKE "%{keyword}%" 
        OR mrt LIKE "%{keyword}%" 
        '''
        keyword_query = f'SELECT * FROM attractions {keyword_query_condition}  LIMIT {start_point},{num_per_page}'
        cursor.execute(keyword_query)
        results = cursor.fetchall()
    
    sitedb.close()
    return results


def get_attractions_count(keyword):
    sitedb = connection_pool.get_connection()
    cursor = sitedb.cursor()
    
    if not keyword:
        count_query = 'SELECT COUNT(*) FROM attractions'
        cursor.execute(count_query)
        result_count = cursor.fetchone()[0]
    
    else:
        keyword_query_condition = f'''
        WHERE name LIKE "%{keyword}%" 
        OR category LIKE "%{keyword}%" 
        OR description LIKE "%{keyword}%" 
        OR address LIKE "%{keyword}%" 
        OR mrt LIKE "%{keyword}%" 
        '''
        count_query = f'SELECT COUNT(*) FROM attractions {keyword_query_condition}'
        cursor.execute(count_query)
        result_count = cursor.fetchone()[0]   
    
    sitedb.close()
    return result_count 


def get_attraction_by_id(id):
    sitedb = connection_pool.get_connection()
    cursor = sitedb.cursor()

    id_query = f'SELECT * FROM attractions WHERE id={id}'
    cursor.execute(id_query)
    result = cursor.fetchone()
    
    sitedb.close()
    return result
    