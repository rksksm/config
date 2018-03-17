from flask import Flask, request
from healthcheck import HealthCheck, EnvironmentDump
from flask_cors import CORS
from pymongo import MongoClient
import bson.json_util
import json


app = Flask(__name__)
CORS(app)

health = HealthCheck()
client = MongoClient("mongodb://localhost:27017")
db = client.userConfig
def addition_works():
    if 1 + 1 == 2:
        return True, "addition works"

STATUS200 = {"status_code":200,"data": None}

@app.route('/')
def health_check():
    health.add_check(addition_works)
    return health.run()

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        try:
            configuration = request.json
            filter = {"tenant": configuration["tenant"], "integration_type": configuration["integration_type"]}
            if db.config.find_one(filter) == None:
                db.config.insert_one(configuration)
                STATUS200["data"] = "inserted"
                return json.dumps(STATUS200)
            # else statement is for merging the new configuration with existing one
            else:
                configurationList = []
                response = db.config.find_one(filter, {"_id": 0})
                configurationList.append(response["configuration"])
                configurationList.append(configuration["configuration"])
                configuration["configuration"] = configurationList
                db.config.replace_one(filter, configuration)
                STATUS200["data"] = "updated"
                return json.dumps(STATUS200)

            # else statement is for replacing the new configuration with existing one

            # else:
            #     db.config.replace_one(filter, configuration)
            #     return "updated"
        except NameError as e:
            STATUS200["data"] = 'Name Error : '+ str(e)
            return json.dumps(STATUS200)
        except ValueError as e:
            STATUS200["data"] = 'Value Error : '+ str(e)
            return json.dumps(STATUS200)
        except KeyError as e:
            msg = 'Missing Parameter : ' + str(e) + ' is Missing'
            STATUS200["data"] = 'Key Error : '+ msg
            return json.dumps(STATUS200)
        except TypeError as e:
            STATUS200["data"] = 'Type Error:'+ str(e)
            return json.dumps(STATUS200)
        except Exception as ex:
            STATUS200["data"] = ex
            return json.dumps(STATUS200)
    else:
        try:
            filter = {"tenant":request.args["tenant"], "integration_type":request.args["integration_type"]}
            response = db.config.find_one(filter, { "_id": 0, "tenant":0, "integration_type":0})
            if response == None:
                STATUS200["data"] = "No such record exists"
                return json.dumps(STATUS200)
            else:

                STATUS200["data"] = response
                return bson.json_util.dumps(STATUS200)
        except NameError as e:
            STATUS200["data"] = 'Name Error : '+ str(e)
            return json.dumps(STATUS200)
        except ValueError as e:
            STATUS200["data"] = 'Value Error : '+ str(e)
            return json.dumps(STATUS200)
        except KeyError as e:
            msg = 'Missing Parameter : ' + str(e) + ' is Missing'
            STATUS200["data"] = 'Key Error : ' + msg
            return json.dumps(STATUS200)
        except TypeError as e:
            STATUS200["data"] = 'Type Error:'+ str(e)
            return json.dumps(STATUS200)
        except Exception as ex:
            STATUS200["data"] = ex
            return json.dumps(STATUS200)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)