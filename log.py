'''
Handles transactions to the nodes
'''

from pathlib import Path
import CONFIG

class LogFile:
    file_path = ""
    length = 0

    def __init__(self,name=CONFIG.LOG_DB_DIR,path=CONFIG.LOG_DIR):
        self.file_path = path+name

    #create a file if it does not exist yet
    def setPath(self,path):
        file = Path(path)
        if not file.is_file():
            with open(file,'w') as f:
                return

    '''
    Gets all transactions from the start to end (or specified otherwise)
    Get exact transaction, end = 0
    Get range of transactions, end >= start
    Get all of transactions from start, end = -1
    '''
    def fetch_log(self,start,end=0):
        result = []
        if start >= self.length or end >= self.length:
            return list()
        
        with open(self.file_path,'r') as log_file:
            line_num = 0
            text = ""
            while line_num < start:
                text = log_file.readline()
                line_num += 1

            #if no end specified
            if end == 0 or start==end:
                result.append(log_file.readline())
            #from start to end of file
            if end == -1:
                while text:
                    text = log_file.readline()
                    result.append(text)
                    line_num += 1
            #within range of start to end
            if end > start:
                while line_num <= end:
                    result.append(log_file.readline())
                    line_num += 1
        return result

    '''
    Write message into the log
    '''
    def write_log(self,txn):
        assert type(txn) is str
        with open(self.file_path,'a') as log_file:
            log_file.write(txn)
            self.length += 1

    def _clear(self):
        with open(self.file_path,'w') as log_file:
            log_file.write('')
            self.length = 0
