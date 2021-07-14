import requests

guest_id = 1
event_id = 1
url = f'http://127.0.0.1:5000/rsvp/{event_id}/{guest_id}'
data = {'value': 'n'}
response = requests.post(url, data=data)
print(response)
