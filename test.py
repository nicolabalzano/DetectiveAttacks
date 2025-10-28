import requests
import json



url = 'http://127.0.0.1:8080/api/cvwelib/api/get_cwe'

response = requests.get(f'{url}?keywordSearchCWE=xss&keywordExactMatch')
 
print(response.text)
"""dict_= json.loads(response.text)

print(dict_[0]['id'])
print("-----------------------------------------------------")
print(dict_[1] ['id'])
print("-----------------------------------------------------")
print(dict_[2]  ['id'])"""
