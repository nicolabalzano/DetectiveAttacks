


url = 'http://127.0.0.1:8080/api/cvwelib/api/get_cwe'

response = requests.get(f'{url}?keywordSearchCWE=xss')
 
print(response.text