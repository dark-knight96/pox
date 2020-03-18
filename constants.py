PRIMARY_TABLE = "layer2"
WHERE_REQ_KEY = "wherevalues"
LAYER_KEY = "layer"
FIELDS = "fields"
tableFields= {
"layer2" : ["RULE_ID", "SOURCE_ADDRESS", "DEST_ADDRESS", "SRC_PORT", "DEST_PORT", "L4PROTO"]
}
primarykeys = {
    "layer2": "RULE_ID"
}
OTYPE= "oType"
INSERT = "INSERT"
UPDATE = "UPDATE"
DELETE = "DELETE"
SRC_PORT = "SRC_PORT"
DEST_PORT = "DEST_PORT"
PROTO="L4PROTO"
PORT = "ports"
SOURCE_ADDRESS = "SOURCE_ADDRESS"
DEST_ADDRESS = "DEST_ADDRESS"
protoCodes = {"IPV4": 0x800, "TCP": 6}


