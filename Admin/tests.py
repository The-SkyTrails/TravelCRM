# from django.test import TestCase

# # Create your tests here.

# # get payment list 
# import requests

# url = "https://sandbox.cashfree.com/pg/links/1c89fe10-eaf4-4f59-8f79-b8145beeb94a"

# headers = {
#     "accept": "application/json",
#     "x-api-version": "2023-08-01",
#     "x-client-id": "17792263f8ad3b41a90673b52f229771",
#     "x-client-secret": "00f09ad3074140b18466ebbb092f8e6066917028"
# }

# response = requests.get(url, headers=headers)

# print(response.json())




import requests


url = "https://api-smartflo.tatateleservices.com/v1/call/records?destination=918318187374&direction=outbound"

headers = {
    "accept": "application/json",
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIzNjM3MDgiLCJpc3MiOiJodHRwczovL2Nsb3VkcGhvbmUudGF0YXRlbGVzZXJ2aWNlcy5jb20vdG9rZW4vZ2VuZXJhdGUiLCJpYXQiOjE3MDIyNzE2NzAsImV4cCI6MjAwMjI3MTY3MCwibmJmIjoxNzAyMjcxNjcwLCJqdGkiOiJCa0xPV05hcVNNVkZabm4wIn0.w76qiqkkFZpcb9sjIg_J9MG__iw7m0yZ-rlAoOGKab4"
}

response = requests.get(url, headers=headers)

# print(response.text)

