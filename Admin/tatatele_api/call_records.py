import requests

def fetch_recording_urls_and_dates():
    url = "https://api-smartflo.tatateleservices.com/v1/call/records"
    headers = {
        "accept": "application/json",
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIzNjM3MDgiLCJpc3MiOiJodHRwczovL2Nsb3VkcGhvbmUudGF0YXRlbGVzZXJ2aWNlcy5jb20vdG9rZW4vZ2VuZXJhdGUiLCJpYXQiOjE3MDIyNzE2NzAsImV4cCI6MjAwMjI3MTY3MCwibmJmIjoxNzAyMjcxNjcwLCJqdGkiOiJCa0xPV05hcVNNVkZabm4wIn0.w76qiqkkFZpcb9sjIg_J9MG__iw7m0yZ-rlAoOGKab4"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        recording_urls_and_dates = [
            {
                'recording_url': result.get('recording_url'),
                'date': result.get('date')
            } 
            for result in data.get('results', [])
        ]
        return recording_urls_and_dates
    else:
        return []
