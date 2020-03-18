from mysql import connector
import enum
import mysqlInfo as sqlInfo

class Concatnator(enum.Enum):
    AND = 1
    OR = 2

#As enum to int is not possible in python 2.7
operationType = {
    "INSERT":1,
    "UPDATE":2,
    "DELETE":3
}

connection= connector.connect(host=sqlInfo.host, user=sqlInfo.user, database=sqlInfo.database)

def getCusror():
    return connection.cursor(buffered=True)

# def checkForTypeErrors(data):
#     if type(data) == list:
#         for val in data:
#             for d in val.keys():
#                 v = val[d]
#                 print "v"
#                 print type(v)
#                 if type(v) == list:
#                     for li in v:
#                         if type(li) != str:
#                             return -1
#                 elif type(v) != str:
#                     return -1
#     else:
#         for d in data.keys():
#             val = data[d]
#             if type(val) != str:
#                 return -1
#     return 1

def insertRecord(tableName, data):
    try:
        insertString = "INSERT INTO " + tableName + " ("
        for key in data.keys():
            if data.keys().index(key) == len(data.keys()) - 1:
                insertString = insertString + key + ")"
            else:
                insertString = insertString + key + ", "

        insertString = insertString + " VALUES ("
        for value in data.values():
            if data.values().index(value) == len(data.values()) - 1:
                insertString = insertString + "%s)"
            else:
                insertString = insertString + " %s, "
        insertString = insertString + ";"
        print "The sql query is:"
        print insertString
        cursor = getCusror()
        cursor.execute(insertString, data.values())
        connection.commit()
        if cursor.rowcount == 1:
            print "Record inserted!!"
            return 1
        else:
            print "Record cannot be inserted"
            return -1
    except Exception as e:
        print e
        print "Error in generating insert query"
        return -1

def fetchAllRecords(tableName, concatnator = None, whereValues = None):
    print tableName
    try:
        if whereValues != None:
            whereString = constructWhere(whereValues, concatnator)
            sqlquery = "SELECT * FROM " + tableName + " " + whereString + ";"
        else:
            sqlquery = "SELECT * FROM " + tableName + ";"
        print sqlquery
        cursor = queryExecutor(sqlquery)
        if type(cursor) == tuple:
            raise Exception(cursor[1])
        else:
            records = cursor.fetchall()
            return records
    except Exception as e:
        print e
        return -1

def fetchFirstRow(tableName, concatnator = None, whereValues = None):
    try:
        if whereValues != None:
            whereString = constructWhere(whereValues, concatnator)
            sqlquery = "SELECT * FROM " + tableName + " " + whereString + ";"
        else:
            sqlquery = "SELECT * FROM " + tableName + ";"
        cursor = queryExecutor(sqlquery)
        if type(cursor) == tuple:
            raise Exception(cursor[1])
        else:
            records = cursor.fetchone()
            return records
    except Exception as e:
        print e
        return -1

def updateRecord(tableName, setData, whereValues, concatnator):
    """
    :param tableName: Name of the table where the value needs to be updated
    :param data: key value pairs of field vs data to be updated
    :param whereValues: list of key value pairs for where clause.
    :return: string (sql query)
    """
    updateString = "UPDATE " + tableName + " SET "
    whereString = constructWhere(whereValues, concatnator)

    for key in setData.keys():
        if setData.keys().index(key) == len(setData.keys()) - 1:
            updateString = updateString + str(key) + "='" + str(setData[key]) + "' "
        else:
            updateString = updateString + str(key) + "='" + str(setData[key]) + "', "
    updateString = updateString + whereString + ";"
    print "Update query is"
    print updateString

    try:
        result = queryExecutor(updateString)
        if type(result) == tuple:
            raise(Exception(result[1]))
        else:
            if result.rowcount == 1:
                print "Record has been successfully updated."
            elif result.rowcount > 1:
                print "More than one record has been updated."
            return result.rowcount
    except Exception as e:
        print e
        print "Record update failed."
        return -1

def deleteRecord(tableName, whereValues, concatnator):
    """
    :param tableName: Name of the table from where the record needs to be deleted.
    :param whereValues: Values for the clause
    :param concatnator: concatnator for where clause.
    :return: delete sql statement with the given values
    """
    deleteQuery = "DELETE FROM " + tableName + " "
    whereString = constructWhere(whereValues, concatnator)
    deleteQuery = deleteQuery + whereString
    deleteQuery = deleteQuery + ";"
    print "The delete query is "
    print deleteQuery
    result = queryExecutor(deleteQuery)
    if type(result) == tuple:
        if result[0] == -1:
            print result[1]
            return result[0]
        else:
            if result[0].rowCount == 1:
                print "Record deleted successfully"
                return 1
    else:
        return result.rowcount

def queryExecutor(sqlStatement):
    try:
        cursor = getCusror()
        cursor.execute(sqlStatement)
        connection.commit()
        return cursor
    except Exception as e:
        return -1, e

def constructWhere(data, concatnator):
    """
    :param values: dictionary of key and value pairs
    :return: where string add-on for sql statement
    """
    whereStatement = "WHERE "
    concat = ""
    if concatnator == Concatnator.AND:
        concatString = "AND"
    else:
        concatString = "OR"
    for val in data:
        for key in val.keys():
            value = val[key]
            print value
            print type(value)
            if type(value) == list:
                tempString = ""
                minconcat = "OR"
                for ml in value:
                    if value.index(ml) == len(value) - 1:
                        tempString = tempString + " " + str(key) + "='" + str(ml) + "'"
                    else:
                        tempString = tempString + " " + str(key) + "='" + str(ml) + "'" + minconcat + " "
                print tempString
                whereStatement = whereStatement + " " + tempString
            else:
                v = str(val[key])
                whereStatement = whereStatement + " " + str(key) + "='" + v + "'"
            if concatnator != None and data.index(val) != len(data) - 1:
                whereStatement = whereStatement + " " + concatString + " "
            print "The generated where statement is:" + whereStatement
            return whereStatement

if __name__ == "__main__":
    print fetchAllRecords("layer2", concatnator=None, whereValues= None)
    # #print deleteRecord("layer2", concatnator=None, whereValues=[{"DEST_ADDRESS":"00:00:00:00:00:03"}],)
    # # print insertRecord("layer2", data={"RULE_ID": "3", "SOURCE_ADDRESS": "00:00:00:00:00:01",
    # #                                    "DEST_ADDRESS": "00:00:00:00:00:02"})

