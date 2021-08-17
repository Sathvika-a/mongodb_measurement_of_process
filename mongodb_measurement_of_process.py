#!/usr/bin/python

import sys
import time
import json
import requests
import subprocess
import os
import argparse
from requests.auth import HTTPDigestAuth


PYTHON_MAJOR_VERSION = sys.version_info[0]

if PYTHON_MAJOR_VERSION == 3:
    import urllib
    import urllib.request as connector
elif PYTHON_MAJOR_VERSION == 2:
    import urllib2 as connector

plugin_version = 1

heartbeat_required = "true"

resultjson={}

metric_units={
    "NETWORK_BYTES_IN":"byte",
    "NETWORK_BYTES_OUT":"byte",
    "LOGICAL_SIZE":"byte"
}


group_id="6080fc32b449622900b6612e"
host="cluster0-shard-00-02.bcgaj.mongodb.net"
port="27017"
public_key = 'jifqsfrc'
private_key = '80d11231-0482-4387-8107-ea0336380452'


def metrics_collector():
    resultjson={}
    try:
        url = "https://cloud.mongodb.com/api/atlas/v1.0/groups/"+group_id+"/processes/"+host+":"+port+"/measurements?granularity=PT5M&period=PT5M&pretty=true" 
        data=json.loads((requests.get(url, auth=HTTPDigestAuth(public_key, private_key)).content))
        new_data = {}
        new_data["groupId"]=data["groupId"]
        new_data["hostId"]=data["hostId"]
        new_data["start"]=data["start"]
        new_data["end"]=data["end"]
        new_data["CONNECTIONS"] = data["measurements"][0]["dataPoints"][0]["value"]
        new_data["NETWORK_BYTES_IN"]=data["measurements"][1]["dataPoints"][0]["value"]
        new_data["NETWORK_BYTES_OUT"]=data["measurements"][2]["dataPoints"][0]["value"]
        new_data["NETWORK_NUM_REQUESTS"]=data["measurements"][3]["dataPoints"][0]["value"]
        new_data["OPCOUNTER_CMD"]=data["measurements"][4]["dataPoints"][0]["value"]
        new_data["OPCOUNTER_QUERY"]=data["measurements"][5]["dataPoints"][0]["value"]
        new_data["OPCOUNTER_UPDATE"]=data["measurements"][6]["dataPoints"][0]["value"]
        new_data["OPCOUNTER_DELETE"]=data["measurements"][7]["dataPoints"][0]["value"]
        new_data["OPCOUNTER_GETMORE"]=data["measurements"][8]["dataPoints"][0]["value"]
        new_data["OPCOUNTER_INSERT"]=data["measurements"][9]["dataPoints"][0]["value"]
        new_data["LOGICAL_SIZE"]=data["measurements"][10]["dataPoints"][0]["value"]
        

        
        return new_data

        
        
    
        
        
    except Exception as e:
        resultjson["msg"]=str(e)
        resultjson["status"]=0
    return resultjson




if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--group_id',help="group ID of mongodb_measurement_of_processes",type=str)
    parser.add_argument('--host',help="host name for mongodb_measurement_of_processes",type=str)
    parser.add_argument('--port',help="port name for mongodb_measurement_of_processes",type=str)
    parser.add_argument('--public_key',help="public key of mongodb_measurement_of_processes",type=str)
    parser.add_argument('--private_key',help="Private key for mongodb_measurement_of_processes",type=str)
    args=parser.parse_args()
	
    if args.group_id:
        group_id=args.group_id
    if args.host:
        host=args.host
    if args.port:
        port=args.port
    if args.public_key:
        public_key=args.public_key
    if args.private_key:
        private_key=args.private_key    
    resultjson=metrics_collector() 
    resultjson['plugin_version'] = plugin_version
    resultjson['heartbeat_required'] = heartbeat_required
    resultjson['units'] = metric_units
print(json.dumps(resultjson, indent=4, sort_keys=True))
