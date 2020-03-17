import constants

def convertToDict(data, keys):
    result = []
    for record in data:
        temp = {}
        for key in keys:
            keyIndex = keys.index(key)
            temp[key] = str(record[keyIndex])
        result.append(temp)
    # print "The processed data is:"
    # print result
    return result

def getTable(layer):
    if layer == "layer2":
        return constants.PRIMARY_TABLE

def checkForFields(request, fieldList):
    for field in fieldList:
        if field not in request:
            return field
    return 1

def unformattedDict(data):
    temp = {}
    for key in data.keys():
        temp[str(key)] = str(data[key])
    return temp

def generateErrorStringFromMeta(field):
    if field == constants.LAYER_KEY:
        return "Layer information is missing"
    elif field == constants.FIELDS:
        return "Fields list for query construction is missing"

def extractAddress(rule):
    addr = []
    for key in rule.keys():
        if key != constants.OTYPE and key != constants.PROTO and key != constants.PORT:
            addr.append(str(rule[key]))
    return addr

