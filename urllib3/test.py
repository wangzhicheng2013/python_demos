import urllib3
import json
http = urllib3.PoolManager(timeout = 3)
r = http.request('GET', 'https://www.baidu.com')
print r.status
print r.data
data = { 'attribute':'value' }
encode_data = json.dumps(data).encode('utf-8')
print encode_data
r = http.request('POST', 'http://httpbin.org/post', body = encode_data, headers = {'Content-Type':'application/json'})
print r.status
