from django.test import TestCase

# Create your tests here.

# get payment list 
import requests

url = "https://sandbox.cashfree.com/pg/links/1c89fe10-eaf4-4f59-8f79-b8145beeb94a"

headers = {
    "accept": "application/json",
    "x-api-version": "2023-08-01",
    "x-client-id": "17792263f8ad3b41a90673b52f229771",
    "x-client-secret": "00f09ad3074140b18466ebbb092f8e6066917028"
}

response = requests.get(url, headers=headers)

print(response.json())



