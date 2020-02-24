from mysql import connector
import enum

class Concatnator(enum.Enum):
    AND = 1
    OR = 2

connection= connector.connect(host="localhost", user="root", database="Network_security")

def getCusror():
    return connection.cursor()

def checkForTypeErrors(data):
    if type(data) == list:
        for val in data:
            for d in val.keys():
                v = val[d]
                if type(v) == list:
                    for li in v:
                        if type(li) != str:
                            return -1
                elif type(v) != str:
                    return -1
    else:
        for d in data.keys():
            val = data[d]
            if type(val) != str:
                return -1
    return 1

def insertRecord(tableName, data):
    checkVal = checkForTypeErrors(data)
    if checkVal == -1:
        print "Values should be of type str"
        return -1
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
        else:
            print "Record cannot be inserted"
            return -1
    except Exception as e:
        print e
        print "Error in generating insert query"
        return -1

def fetchAllRecords(tableName, concatnator = None, whereValues = None):
    try:
        if whereValues != None:
            whereString = constructWhere(whereValues, concatnator)
            print whereString
            sqlquery = "SELECT * FROM " + tableName + " " + whereString + ";"
        else:
            sqlquery = "SELECT * FROM " + tableName + ";"
        cursor = getCusror()
        print sqlquery
        cursor.execute(sqlquery)
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
        cursor = getCusror()
        cursor.execute(sqlquery)
        records = cursor.fetchone()
        return records
    except Exception as e:
        print e
        return -1

def constructWhere(data, concatnator):
    """
    :param values: dictionary of key and value pairs
    :return: where string add-on for sql statement
    """
    if checkForTypeErrors(data) == -1:
        return -1
    else:
        whereStatement = "WHERE "
        concat = ""
        if concatnator == Concatnator.AND:
            concatString = "AND"
        else:
            concatString = "OR"
        for val in data:
            for key in val.keys():
                value = val[key]
                # print value
                # print type(value)
                if type(value) == list:
                    tempString = ""
                    minconcat = "OR"
                    for ml in value:
                        if value.index(ml) == len(value) - 1:
                            tempString = tempString + " " + key + "='" + ml + "'"
                        else:
                            tempString = tempString + " " + key + "='" + ml + "'" + minconcat + " "
                    print tempString
                    whereStatement = whereStatement + " " + tempString
                    print "final"
                    print whereStatement
                else:
                    v = str(val[key])
                    whereStatement = whereStatement + " " + str(key) + "='" + v + "'"
                if concatnator != None and data.index(val) != len(data) - 1:
                    whereStatement = whereStatement + " " + concatString + " "
    print "The generated where statement is:" + whereStatement
    return whereStatement

if __name__ == "__main__":
    print fetchAllRecords("layer2", concatnator=Concatnator.AND,whereValues=[{"SWITCH_ID":["1", "2"]}, {"SOURCE_ADDRESS":"00:00:00:01"}])



