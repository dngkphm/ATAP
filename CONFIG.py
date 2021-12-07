'''
Contains DEF global variables as well as pre-sets for running the nodes
'''


#DEBUGGING
REPR_ALLOWED = False

#THREADS
THREAD_NUM_QUERY = 1
THREAD_NUM_TXN = 1

#PACKET
MSG_MAX_LIMIT = 512
MSG_DELIM_OPEN = "/<"
MSG_DELIM_CLOSE = "/>"
PACK_MAX_LIMIT = 1024
PACK_DELIM_OPEN = "//<"
PACK_DELIM_CLOSE = "//>"
PACK_DELIM_SEP = "//"

#LOGGING
LOG_DIR = "./logging/"
LOG_DB_DIR = "sql_db.txt"

#CONNECTION
CONNECT_IP_DEFAULT = "127.0.0.1"
CONNECT_PORT_DEFAULT = 8080
PING_MAX_LIMIT = 500
PING_MAX_CONNECTION = 10
CONNECT_ENCODE_DEFAULT = 'utf-8'



#METHODS
'''floor divide a by b and round up
'''
def upFlDiv(a:int,b:int)->int:
    qA = a/b
    qT = a//b
    if qT < qA:
        return qT+1
    return qT
