import json
import ssl
import urllib.request


data = {}

myurl = "https://d20ac7f5.ngrok.io/security_test"

req = urllib.request.Request(myurl)
req.add_header('Content-Type', 'application/json; charset=utf-8')
jsondata= json.dumps(data)
json_bytes = jsondata.encode('utf-8')
req.add_header('Content-Length', len(json_bytes))

context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

response = urllib.request.urlopen(req, json_bytes, context=context)
print(response)

