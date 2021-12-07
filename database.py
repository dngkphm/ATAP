'''
This file handles SQLite commands for a SQLite DB

Largely borrowed/inspired by resilientDB SQLite structure

Protocol are as follows:
1) Open database connection with openDB()
2) Choose table from the databse with selectTable()
3) Modify values in the table
4) close the connection with closeDB()

Tables follow a key,value pair marked with a unique txnID for logging reversion
'''

import sqlite3
MAX_CHAR = 10000

class DataBase:
#private:
    db = None   #SQLite database connection
    
    #gathers data from the query. Useful for checking for empty tables or logging data
    class _query_data:
        data = None   #key,[value] pairs for the data
        cmd = ""        #query command (GET,PUT,etc)
        arraysize = 100 #limit result size from executing query
        def getData(self):
            return self.data
        def setData(self,results:list):
            self.data = results
        def clearData(self):
            self.data = list()
        def setOP(self,op:str):
            self.cmd = op
        def getOP(self):
            return self.cmd
        def __repr__(self):
            items = ""
            if self.data == None:
                items = ""
            if type(self.data) == list:
                for item in self.getData():
                    items += str(item)
            if type(self.data) == str:
                items += self.data
            return "QR: "+items
    qResults = _query_data()

    def __del__(self):
        if self.db != None:
            self.db.close()
        self.qResults.clearData()

    def __repr__(self):
        con = sqlite3.connect(self._dbname)
        curs = con.cursor()
        tables = ""
        try:
            #FOR COMMAND IF CANNOT FIND "sqlite_master", REPLACE WITH "sqlite_schema"
            command = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
            curs.execute(command)
            self.qResults.setData(curs.fetchall())
        except sqlite3.Error as err:
            print("[SQLiteErr]\n{}".format(err))
        tables += str(self.qResults.getData()) + '\n'

        values = ""
        for tableName in self._tables:
            values += tableName + ":\n"
            try:
                command = "SELECT * FROM "+tableName+";"
                curs.execute(command)
                values += str(curs.fetchall())+'\n'
            except:
                print("[SQLiteErr]\n{}".format(err))
        con.close()
        return "Database \""+self._dbname+"\"\n"+tables+values
        
    
#protected:
    _dbname = ""    #name of the database
    tableName = ""  #name of the recently used table
    _tables = None  #directory of tables
    #C++ Callback method replaced with cursor fetchall()

#public
    '''for executing SQL queries
        @input: name of the database, a string SQL query, the query's transaction ID
    '''
    def executeQuery(self,dbname:str,command:str,txnID:str):
        dbConnect = sqlite3.connect(dbname)
        #check for valid sql command
        if not sqlite3.complete_statement(command):
            return -1

        #execute query
        curs = dbConnect.cursor()
        self.qResults.setOP("Execute")
        try:
            curs.executescript(command)
        except sqlite3.Error as err:
            print("[SQLiteERR]\nUnable to execute query: {}".format(err[:MAX_CHAR]))
            return -1
        #close the connection and return exit result
        dbConnect.close()
        return 0

    '''Creates a database with name "db" if does not exist.
      Otherwise open existing database with name
      @input:   name of the database, query's ID (opt)
      @output:  returns the Database Connection and sets the Database.db
    '''
    def openDB(self,dbname:str="db",txnID:str=""):
        dbname = dbname[:MAX_CHAR]
        dbConnect = None
        try:
            dbConnect = sqlite3.connect(dbname)
        except socket.error as e:
            print("[SQLiteErr]\nCan't open database \"{}\"\n".format(dbname))
            return -1
        print("[SQLiteOK]\nOpened \"{}\" db connection\n".format(dbname))
        self._dbname = dbname
        self.db = dbConnect
        return 0
    
    '''closes the current database connection'''
    def closeDB(self):
        if self.db == None:
            return
        self.db.close()
        print("[SQLiteOK]:\nClosing connection to \"{}\"\n".format(self._dbname))
        self._dbname = ""
        self.db = None

    '''updates the table'''
    def updateTable(self,txnID:str=""):
        self.db.commit()

    '''adds table to list of tables in database'''
    def addTable(self,name:str):
        if self._tables == None:
            self._tables = list()
        self._tables.append(name)

    '''creates a table in db
      follows resilientDB's key,value pair for easier table integration
      @input: name of the table, default "main"
    '''
    def createTable(self,table:str="main",txnID:str=""):
        table = table[:MAX_CHAR]
        command = "CREATE TABLE IF NOT EXISTS " + table + "("\
                                                                      "KEY      CHAR(64) PRIMARY KEY    NOT NULL,"\
                                                                      "VALUE    TEXT                    NOT NULL);"
        cursor = self.db.cursor()

        try:
            cursor.execute(command)
        except sqlite3.Error as err:
            print("[SQLiteERR]\nFailed to create table \"{}\": {}\n".format(table,err))
            return 1
        self.tableName = table
        self.addTable(table)
        print("[SQLiteOK]\nCreated table \"{}\"\n".format(table))
        return 0

    '''selects a table in db
    @input: name of the table
    '''
    def selectTable(self,table:str,txnID:str=""):
        table = table[:MAX_CHAR]
        command = "SELECT name FROM sqlite_master WHERE type='table' AND name='" + table + "';"
        cursor = self.db.cursor()
        self.qResults.setOP("SelectTable")
        try:
            cursor.execute(command)
        except sqlite3.Error as err:
            print("[SQLiteERR]\nCould not select table \"{}\": {}\n".format(table,err))
            return -1
        
        #if query results are empty (no table), create the table
        self.qResults.setData(cursor.fetchall())
        if len(self.qResults.getData()) == 0:
            self.createTable(table)
            print("[SQLiteOK]\nCreated table \"{}\" in database \"{}\"".format(table,self._dbname))
        self.tableName = table
        return 0

    '''drops table in db
    @input: name of the table
    '''
    def dropTable(self,table:str,txnID:str=""):
        table = table[:MAX_CHAR]
        command = "DROP TABLE IF EXISTS " + table + ";"
        cursor = self.db.cursor()
        try:
            cursor.execute(command)
        except sqlite3.Error as err:
            #in the case of dependency violations (not likely)
            print("[SQLiteERR]\nCould not drop table \"{}\": {}\n".format(table,err))
            return 1
        for name in self._tables:
            if name == table:
                self._tables.remove(name)
        self.tableName = ""
        return 0

    '''modifying table values in database
    '''
    def insertValue(self,key:str,value:str,txnID:str=""):
        command = ""
        self.qResults.setOP("PUT")

        prev = self.selectValue(key)
        #If the value to be inserted is the same, just return
        if value == prev:
            return prev

        if len(prev) >= 1: #if the same, just replace the value, else insert key,value pair
          #print("Updating the value")
          command = "UPDATE " + self.tableName + " set VALUE = '" + value + "' where KEY = '" + key + "';"
        else:
          #print("Inserting the value")
          command = "INSERT INTO " + self.tableName + " (KEY, VALUE) VALUES('" + key + "', '" + value + "');"

        cursor = self.db.cursor()
        try:
            cursor.execute(command)
        except sqlite3.Error as err:
            print("[SQLiteERR]\nfailed PUT\t\"{}\": {}}\n".format(command,err))
            return -1
        return 0

    '''retrieves values from the table in the database
    @input: takes a key pair to retrieve its value
    @output:  returns the retrieved value
    '''
    def selectValue(self,key:str,txnID:str=""):
        self.qResults.setOP("GET")
        value = None

        command = "SELECT KEY, VALUE FROM " + self.tableName + " WHERE KEY = '" + key + "';"
        cursor = self.db.cursor()
        try:
            cursor.execute(command)
        except sqlite3.Error as err:
            print("[SQLiteERR]\nGET\t\"{}\": {}\n".format(command,err))
            return -1
        
        results = cursor.fetchall()
        if results != None or len(results) >= 1:
            value = results
        return value

    '''removes the key value pair from the table in the database
    @input: key pair
    '''
    def deleteValue(self,key:str,txnID:str=""):
        command = "DELETE FROM "+self.tableName+" WHERE KEY = '" + key + "';"
        cursor = self.db.cursor()
        cursor.execute(command)

        self.qResults.setOP("DEL")
        results = cursor.fetchall() #get true/false result
        if results == None:
            print("[SQLiteOK]\nNo value to delete from table \"{}\"\n".format(table))
        return 0


''' FOR TESTING PURPOSES '''
def main():
    db = DataBase()
    dbName = "db"
    db.openDB(dbName)
    tableName = "workers"

    db.createTable(tableName)
    db.insertValue("914","David")
    db.insertValue("915","Alberto")
    db.insertValue("916","Bryan")
    db.insertValue("918","Tommy")
    db.updateTable()

    print(db)

    print(db.selectValue("901"))
    print(db.selectValue("914"))
    print(db.selectValue("918"))
    db.deleteValue("914")
    print(db.selectValue("914"))

    tableName = "artists"
    db.createTable(tableName)
    db.insertValue("RL Grime","EDM")
    db.insertValue("The NBHD","AltRock")
    db.insertValue("Big Sean","Rap")
    db.updateTable()

    print(db)
    print("break")

    db.selectTable("workers")
    db.dropTable("artists")

    print(db)
    
    db.closeDB()
    del db
    return 0
