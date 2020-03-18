from flask import Flask
from flask import jsonify, make_response
import utilmethods as um
import sqlmanager as sql
import constants as con
from flask import request
from sqlmanager import Concatnator
from Sender import sendToServer
import constants
from sqlmanager import operationType
import utilmethods

app = Flask(__name__)

@app.route("/")
def index():
    result = {"data":"Hello world"}
    if sendToServer(result) == 1:
        return make_response(jsonify(result), 200)
    else:
        return make_response(jsonify(({"error": "Data cannot be sent to the server"})), 400)

@app.route("/fetchAllRules", methods=['POST'])
def fetchAllRules():
    if not request.json:
        return make_response(jsonify({"error": "Request structure needs to be a json"}))
    else:
        whereValues = None
        tableName = None
        concatnator = None
        if con.LAYER_KEY not in request.json:
            return make_response(jsonify({"error": "Layer information missing"}), 400)
        else:
            tableName = um.getTable(request.json.get(con.LAYER_KEY))
        if con.WHERE_REQ_KEY in request.json:
            whereValues = request.json.get(con.WHERE_REQ_KEY)
            concatnator = Concatnator.AND
        records = sql.fetchAllRecords(tableName, concatnator = concatnator, whereValues=whereValues)
        if records == -1:
            return make_response(jsonify({"error": "Data cannot be retrieved from the database"}), 500)
        else:
            return make_response(jsonify(um.convertToDict(records, con.tableFields.get(tableName))), 200)


@app.route("/addRule", methods = ["POST"])
def addRule():
    if not request.json:
        return make_response(jsonify({"error":"Request needs to be a json"}), 400)
    else:
        if con.LAYER_KEY not in request.json:
            return make_response(jsonify({"error": "Layer information missing"}), 400)
        else:
            result = sql.insertRecord(con.PRIMARY_TABLE, request.json.get(con.FIELDS))
            if result ==-1:
                return make_response(jsonify({"error": "New Rule cannot be inserted"}), 500)
            elif result ==1:
                fields = utilmethods.unformattedDict(request.json.get(con.FIELDS))
                fields[constants.OTYPE] = operationType[constants.INSERT]
                sendToServer(fields)
                return make_response(jsonify({"message": "Rule inserted successfully"}), 200)

@app.route("/deleteRule", methods= ["POST"])
def deleteRule():
    if not request.json:
        return make_response(jsonify({"error": "Request structure needs to be a json."}), 400)
    else:
        checkFields = um.checkForFields(request.json, [con.LAYER_KEY])
        if  checkFields != 1:
            return make_response(jsonify({"error": um.generateErrorStringFromMeta(checkFields)}), 200)
        else:
            whereValues = None
            if request.json.get(con.WHERE_REQ_KEY):
                whereValues = request.json.get(con.WHERE_REQ_KEY)
            matchRecord = sql.fetchFirstRow(um.getTable(request.json.get(constants.LAYER_KEY)), whereValues = whereValues, concatnator= Concatnator.AND)
            if matchRecord == None:
                return make_response(jsonify({"message": "No matching record found"}), 500)

            result = sql.deleteRecord(um.getTable(request.json.get(con.LAYER_KEY)), whereValues = whereValues, concatnator=Concatnator.AND)
            if result == 1:
                fields = utilmethods.getUnformattedDictFromTuple(matchRecord, constants.tableFields.get(um.getTable(request.json.get(constants.LAYER_KEY))))
                fields[constants.OTYPE] = operationType[constants.DELETE]
                sendToServer(fields)
                return make_response(jsonify({"message": "Record has been successfully deleted."}), 200)
            else:
                return make_response(jsonify({"message": "Record cannot be deleted."}), 500)

@app.route("/updateRule", methods = ["POST"])
def updateRule():
    #Update has to be done using the primary key which set in the where value
    if not request.json:
        return make_response(jsonify({"error": "Request structure needs to be a json."}))
    else:
        checkFields = um.checkForFields(request.json, [con.LAYER_KEY, con.FIELDS])
        if checkFields != 1:
            return make_response(jsonify({"error": um.generateErrorStringFromMeta(checkFields)}))
        else:
            whereValues = None
            if request.json.get(con.WHERE_REQ_KEY):
                whereValues = request.json.get(con.WHERE_REQ_KEY)
            layer = request.json.get(con.LAYER_KEY)
            setValues = request.json.get(con.FIELDS)

            matchedRecord = sql.fetchFirstRow(um.getTable(layer), whereValues=whereValues, concatnator=Concatnator.AND)
            if matchedRecord == None:
                return make_response(jsonify({"message": "No matched record is found"}))
            result = sql.updateRecord(um.getTable(layer), setData=setValues, whereValues= whereValues, concatnator=Concatnator.AND)
            if result >= 1:
                deleteRule = utilmethods.getUnformattedDictFromTuple(matchedRecord, constants.tableFields.get(
                    um.getTable(request.json.get(constants.LAYER_KEY))))
                deleteRule[constants.OTYPE] = operationType[constants.DELETE]
                sendToServer(deleteRule)

                fields = utilmethods.unformattedDict(request.json.get(con.FIELDS))
                fields[constants.OTYPE] = operationType[constants.UPDATE]
                sendToServer(fields)

                return make_response(jsonify({"message": str(result) + " record has been updated" if result ==1 else " records have been updated."}), 200)
            else:
                return make_response(jsonify({"error": "Record cannot be updated."}), 500)


if __name__=="__main__":
    app.run(debug=True, host="localhost")
