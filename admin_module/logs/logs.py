import time
import calendar
import datetime

current_GMT = time.gmtime()
time_stamp = calendar.timegm(current_GMT)
logJson = {
        "ProjectName": "TMSPinInspection",
        "ModuleName": "TMSApp",
        "UniqueValue": "",
        "Host": "10.10.1.45",
        "Port": "8001",
        "ProcessId": str(time_stamp),
        "ParentProcessTag": "",
        "SelfProcessTag": "",
        "TechnicalModuleName": "Django",
        "LogType": "ApplicationLog",
        "Tag": "",
        "Endpoint": "",
        "LogLevel": "Info",
        "Message": "",
        "Timestamp": str(time_stamp)
}

