"""
script expects productType.zip file in the local directory for all the devices to update.
"""
import json
import re
import time
import subprocess
from pyadb import ADB
from CastleTestUtils.RivieraUtils.rivieraCommunication import ADBCommunication
from CastleTestUtils.RivieraUtils.rivieraUtils import RivieraUtils
from CastleTestUtils.LoggerUtils.CastleLogger import get_logger
LOGGER = get_logger(__name__)

def update_multiple_devices():
    productType = "professor"
    zipfile = "professor.zip"
    devices_list = adb.get_devices()
    adb_object = ADBCommunication()
    devices_list = adb_object.getDeviceIDs()
    LOGGER.info("The devices connected are: %s:", devices_list) 
    product_dict = {}
    cmd = "cat /persist/mfg_data.json"
    for device in devices_list:
        adb_obj = ADBCommunication()
        adb_obj.setCommunicationDetail(device=device)
        response = (adb_obj.executeCommand(command =cmd))
        LOGGER.info("response is: %s ", response)
        response = json.loads(response)
        product_dict[device] = [response["productType"],response["productType"]+".zip"]
        zipfile = response["productType"]+".zip"
        command = ["python2.7","-m","CastleTestUtils.SoftwareUpdateUtils.BonjourUpdateScripts.pushup",                 
                     "--device",device,"--zipfile",zipfile]  
        subprocess.call(command)

def  factory_default_updated_devices():
     devices_list = adb.get_devices()
     adb_object = ADBCommunication()
     devices_list = adb_object.getDeviceIDs()
     delay = 120
     length = len(devices_list)
     time.sleep(length*delay)
     for device in devices_list:
         adb_obj = ADBCommunication()
         adb_obj.setCommunicationDetail(device=device)
         cmd = "/opt/Bose/bin/factory_default"
         adb_obj.executeCommand(command=cmd)
         LOGGER.info("factory_reset device : %s ", device)
                         
if __name__ == "__main__":
   update_multiple_devices()
   factory_default_updated_devices()
