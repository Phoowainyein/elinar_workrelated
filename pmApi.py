from urllib import response
import requests
from requests.structures import CaseInsensitiveDict
from urllib3.exceptions import InsecureRequestWarning
import time

#disable warning in terminal
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

url = "https://10.100.4.12/incomingrest/login"
#Auth 
headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"
headers["Authorization"] = "Basic aW50ZXJmYWNlVXNlcjpld2YyMWRqaW9ld240MjM4NDk1eWRk"
data = {"username":"interfaceUser","password":"ewf21djioewn4238495ydd"}

#uploading files
myurl = 'https://10.100.4.12/incomingrest/documents/sendtoai'
#files = {'file': open('case1_part1-part-1.pdf', 'rb')}
files = [('file', open('Document Cloud/case1-part-1-pg1-14.pdf', 'rb')), ('file', open('Document Cloud/case1-part-2-pg15-27.pdf', 'rb')),('file', open('Document Cloud/case1-part-3-pg28-41.pdf', 'rb'))]

def login(url,headers,data):
        try:
            #I had ssl certification error and I had to set verify as False 
            response = requests.post(url, headers=headers,data=data,verify=False)
            #response = requests.post(myurl, files=files,verify=False)
            return response.text
        except requests.exceptions.HTTPError as errh:
            return "Failed request :",errh
        except requests.exceptions.ConnectionError as errc:
            return "Failed request :",errc
        except requests.exceptions.Timeout as errt:
            return "Failed request :",errt
        except requests.exceptions.RequestException as err:
            return "Failed request :",err

auth_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiaW50ZXJmYWNlVXNlciJ9.sdxzHGeZz-AvGKlGeTE084rOWaXjjInmxTu6FHH9PBE"

def sendToAI(auth_token,files):
    try:
        hed = {'destination': 'CONTAINER','Authorization': 'Bearer ' + auth_token}
        response = requests.post(myurl,files=files, headers=hed,verify=False)
        return response.json()
    except requests.exceptions.HTTPError as errh:
            return "Failed request :",errh
    except requests.exceptions.ConnectionError as errc:
        return "Failed request :",errc
    except requests.exceptions.Timeout as errt:
        return "Failed request :",errt
    except requests.exceptions.RequestException as err:
        return "Failed request :",err

def storeFileID(fileIdjson):
    with open("filesId.txt","a") as myFile:
        myFile.write("\n")
        myFile.write(str(fileIdjson))

def pollrequest():
    
    
if __name__=='__main__':
    print(login(url,headers,data))
    print(sendToAI(auth_token))
    fileIdjson=sendToAI(auth_token)
    storeFileID(fileIdjson)
    time.sleep(90)
    # print("Poll Id")
    hed_ = {'Authorization': 'Bearer ' + auth_token,'fileId': '0e172ffb-722f-4b24-bdeb-1da3727c4cd8'}
    json=sendToAI(auth_token)
    #json=  {'fileId': '0e172ffb-722f-4b24-bdeb-1da3727c4cd8'}
    # pollId='https://10.100.4.12/results/collect/poll/{}'
    # response = requests.post(pollId, headers=hed_,json=json,verify=False)
    print(response.text)
    print(response.status_code)
    url = "https://10.100.4.12/results/collect/poll/{}"
    #payload={'fileId': '16b04b67-eda7-4813-9f25-3d44a5ea8b9b'}
    response = requests.request("POST", url, headers=hed_,verify=False)
    print(response.text)
    




#headers["destination"]= "CONTAINER"
#headers["Token"] = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiaW50ZXJmYWNlVXNlciJ9.sdxzHGeZz-AvGKlGeTE084rOWaXjjInmxTu6FHH9PBE"
# def uploadFile(myurl,files):
#     response = requests.post(myurl, headers=headers,files=files,verify=False)
#     return response.raise_for_status(),response.status_code,response.text