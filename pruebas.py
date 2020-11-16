import requests
import json

email = 'A01566153@itesm.mx'
password = 'ascp'

url = 'https://api.backendless.com/9176FE65-2FB5-2B00-FFED-BEB6A480BC00/0397420A-AA65-4BA2-9A1F-D4C9583099C8/users/login'
data = {'login':email, 'password':password}
headers = {'content-type': 'application/json'}

x = requests.post(url, data = json.dumps(data), headers = headers)

print(x.text)

j = json.loads(x.text)
objid = j['objectId']
token = j['user-token']
print("\tObjectID: " + objid)
print("\tToken: " + token)

# request ip for other user
other_email = 'A01566153@itesm.mx'
url = 'https://api.backendless.com/9176FE65-2FB5-2B00-FFED-BEB6A480BC00/0397420A-AA65-4BA2-9A1F-D4C9583099C8/data/Users?where=email%3D%27' + other_email + '%27'
headers = {'content-type': 'application/json', 'user-token':token}
x = requests.get(url, headers = headers)

print(x.text)

j = json.loads(x.text)
other_ip = j[0]['last_ip']
print("\tOther IP: " +  other_ip)