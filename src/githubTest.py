from ensurepip import version
import requests
import json

url = "https://api.github.com/repos/cityofaustin/TagTool/releases"
versionNumber = "1.5.0"

response = requests.get(url)
responseJson = response.json()
responseDict = responseJson[0]
githubVer = str(responseDict["tag_name"])
if versionNumber != githubVer:
    print("Versions don't match!")
else:
    print("Versions match :)")