# Deploy the fine-tuned model
import json
import os
import requests

fine_tuned_model = "gpt-35-turbo-0125.ft-9f7d681a3f264f2d8767a3711061ee6c"

token= os.getenv("eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkwxS2ZLRklfam5YYndXYzIyeFp4dzFzVUhIMCIsImtpZCI6IkwxS2ZLRklfam5YYndXYzIyeFp4dzFzVUhIMCJ9.eyJhdWQiOiJodHRwczovL21hbmFnZW1lbnQuY29yZS53aW5kb3dzLm5ldC8iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9jNjMyOGRjMy1hZmRmLTQwY2UtODQ2ZC0zMjZlZWFkODZkNDkvIiwiaWF0IjoxNzE0NzI2MDkxLCJuYmYiOjE3MTQ3MjYwOTEsImV4cCI6MTcxNDczMTIzOCwiYWNyIjoiMSIsImFpbyI6IkFUUUF5LzhXQUFBQW5uUVdVZXZ2YVZkaW9MVGR1cERTZjVjcERNNUtkNFVpaEdoZmFTQlJpcTN6dk9jM1pCUDlGRkswYTYrTUZDWEgiLCJhbXIiOlsicHdkIiwicnNhIl0sImFwcGlkIjoiYjY3N2MyOTAtY2Y0Yi00YThlLWE2MGUtOTFiYTY1MGE0YWJlIiwiYXBwaWRhY3IiOiIwIiwiZGV2aWNlaWQiOiJlZDIwYThjYy0zN2RmLTRiY2EtYWVlYi1kYmEzNTZmMzU1NWEiLCJmYW1pbHlfbmFtZSI6IkJBTFpBTk8iLCJnaXZlbl9uYW1lIjoiTklDT0xBIiwiZ3JvdXBzIjpbImE3YTVmOTMwLTEzNGEtNDQ3ZC1hMWNjLWI5Yjk0NjAyYTEwZSJdLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiIzNy4xNjIuNTUuOTciLCJuYW1lIjoiQkFMWkFOTyBOSUNPTEEiLCJvaWQiOiIwNjMyOTc0MC0zY2JjLTQyOWUtOWQyNC02ZDM5MDQ5MTdhNmUiLCJvbnByZW1fc2lkIjoiUy0xLTUtMjEtMjYxMjQxNDMxLTI3ODQ3NjgyNDAtMTEwNjM2NjcxNi00ODUyMCIsInB1aWQiOiIxMDAzMjAwMTgwQjg2QjhBIiwicmgiOiIwLkFTQUF3NDB5eHQtdnprQ0ViVEp1NnRodFNVWklmM2tBdXRkUHVrUGF3ZmoyTUJQa0FGSS4iLCJzY3AiOiJ1c2VyX2ltcGVyc29uYXRpb24iLCJzdWIiOiJNbzhWdEpUaTVFV2FWWF85V3ZwTFhvdGRlMEhoQXEwZDNxaTVnSUpMRjNNIiwidGlkIjoiYzYzMjhkYzMtYWZkZi00MGNlLTg0NmQtMzI2ZWVhZDg2ZDQ5IiwidW5pcXVlX25hbWUiOiJuLmJhbHphbm8yQHN0dWRlbnRpLnVuaWJhLml0IiwidXBuIjoibi5iYWx6YW5vMkBzdHVkZW50aS51bmliYS5pdCIsInV0aSI6InQ0bkRZM2YtS2t5Ym1CY3FHOHFTQUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdLCJ4bXNfdGNkdCI6MTQzMzc1NTUwM30.NYC31vMAn-pUi3OXHpofwckIL1foejbo0zfvjJWfn5zu8l8l34QrqaXQycwCKy_JtjcQqwuTSJwMN04RTq1QixKJdEVzQZi42XQmOZzMhV5AHcFxNqtHjILg_Z9R-xe1q4Oqx7LNi3ufYgCkwQCI7OviTZqWL-gGX6n7AxBi70o9VLgvCjkDJytnOyXtABIopw_1ve8XYjxtrSatg5K_eTO_BF09ETjAaUxMC-GVOCH3qFiO_ZDSKsxsbk_4DN4rZxzk1gHB9c07Sc-ENRdANLV0zRQvdUNDwhYgSLH5_on9II7E7hri4T-1a_fWO05qwh3BmhI_mCqwl94BM4A-yw")
resource_group = "cti-fine-tuned"
subscription = "19fab229-9b43-4d88-8401-3f01a29c8287"
resource_name = "cti-gpt-fine-tuned"
model_deployment_name ="gpt-35-turbo-ft-cti" # custom deployment name that you will use to reference the model when making inference calls.

deploy_params = {'api-version': "2023-05-01"}
deploy_headers = {'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json'}

deploy_data = {
    "sku": {"name": "standard", "capacity": 1},
    "properties": {
        "model": {
            "format": "OpenAI",
            "name": fine_tuned_model, #retrieve this value from the previous call, it will look like gpt-35-turbo-0613.ft-b044a9d3cf9c4228b5d393567f693b83
            "version": "1"
        }
    }
}
deploy_data = json.dumps(deploy_data)

request_url = f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/{resource_group}/providers/Microsoft.CognitiveServices/accounts/{resource_name}/deployments/{model_deployment_name}'

print('Creating a new deployment...')

r = requests.put(request_url, params=deploy_params, headers=deploy_headers, data=deploy_data)

print(r)
print(r.reason)
print(r.json())