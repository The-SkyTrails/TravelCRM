import requests


# def fetch_recording_urls_and_dates():
#     url = "https://api-smartflo.tatateleservices.com/v1/call/records?destination=918318187374&direction=outbound"

#     headers = {
#         "accept": "application/json",
#         "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIzNjM3MDgiLCJpc3MiOiJodHRwczovL2Nsb3VkcGhvbmUudGF0YXRlbGVzZXJ2aWNlcy5jb20vdG9rZW4vZ2VuZXJhdGUiLCJpYXQiOjE3MDIyNzE2NzAsImV4cCI6MjAwMjI3MTY3MCwibmJmIjoxNzAyMjcxNjcwLCJqdGkiOiJCa0xPV05hcVNNVkZabm4wIn0.w76qiqkkFZpcb9sjIg_J9MG__iw7m0yZ-rlAoOGKab4"
#     }

#     response = requests.get(url, headers=headers)
#     data = response.json() if response.status_code == 200 else {}
#     return data



def fetch_recording_urls_and_dates():
    url = "https://api-smartflo.tatateleservices.com/v1/call/records?destination=918318187374&direction=outbound"

    headers = {
        "accept": "application/json",
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIzNjM3MDgiLCJpc3MiOiJodHRwczovL2Nsb3VkcGhvbmUudGF0YXRlbGVzZXJ2aWNlcy5jb20vdG9rZW4vZ2VuZXJhdGUiLCJpYXQiOjE3MDIyNzE2NzAsImV4cCI6MjAwMjI3MTY3MCwibmJmIjoxNzAyMjcxNjcwLCJqdGkiOiJCa0xPV05hcVNNVkZabm4wIn0.w76qiqkkFZpcb9sjIg_J9MG__iw7m0yZ-rlAoOGKab4"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise error for HTTP errors (4xx, 5xx)

        if response.text.strip():  # Ensure response is not empty
            return response.json()
        else:
            print("API Response is empty")
            return {}  # Return empty dictionary if response is empty

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {}  # Return empty dictionary if request fails

    except ValueError as e:
        print(f"JSON Decode Error: {e}")
        print(f"Response Content: {response.text}")  # Debugging purpose
        return {}  # Return empty dictionary if JSON decoding fails

def LeadWiseCallRecords(destination):
    url = f"https://api-smartflo.tatateleservices.com/v1/call/records?destination={destination}&direction=outbound"

    headers = {
        "accept": "application/json",
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIzNjM3MDgiLCJpc3MiOiJodHRwczovL2Nsb3VkcGhvbmUudGF0YXRlbGVzZXJ2aWNlcy5jb20vdG9rZW4vZ2VuZXJhdGUiLCJpYXQiOjE3MDIyNzE2NzAsImV4cCI6MjAwMjI3MTY3MCwibmJmIjoxNzAyMjcxNjcwLCJqdGkiOiJCa0xPV05hcVNNVkZabm4wIn0.w76qiqkkFZpcb9sjIg_J9MG__iw7m0yZ-rlAoOGKab4"
    }

    response = requests.get(url, headers=headers)
    data = response.json() if response.status_code == 200 else {}
    return data
