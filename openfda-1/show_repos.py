import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()
print(repos_raw)
repos = json.loads(repos_raw)


print("The id of the first repository is",repos['results'][0]['id'])
print("The purpose of the first repository is",repos['results'][0]['purpose'])
print("The manufacturer name of the first repository is",repos['results'][0]['openfda']['manufacturer_name'])