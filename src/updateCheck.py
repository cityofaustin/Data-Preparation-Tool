import requests
import json

def checkUpdates(verNum: str):
    url = "https://api.github.com/repos/cityofaustin/Data-Preparation-Tool/releases"

    try:
        response = requests.get(url)
        responseJson = response.json()
        responseDict = responseJson[0]
        ghVer = str(responseDict["tag_name"])
        if verNum != ghVer:
            return False
        else:
            return True
    except:
        return True