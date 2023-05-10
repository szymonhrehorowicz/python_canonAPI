from requests import get, post, delete
from time import sleep

IP_ADRESS = "http://192.168.1.111:8080"
base_url = f"{IP_ADRESS}/ccapi/ver100"

# Sprawdzenie polaczenia z API
response = get(f"{IP_ADRESS}/ccapi")
print(response.status_code)

# Shoot
response = post(f"{base_url}/shooting/control/shutterbutton",  json={'af': True})
print(response.status_code)

# Get img
img_dir_url = f"{base_url}/contents/sd/100CANON"
counter = 0

response = get(img_dir_url)
while response.status_code != 200:
    sleep(0.1)
    if counter > 20:
        raise RuntimeError('Cannot get urls')
    
    response = get(img_dir_url)
    counter += 1

sleep(0.5)

response = get(img_dir_url)
print(response.status_code)

urls = response.json()['url']

# get and del
for i, url in enumerate(urls):
    response = get(url)
    
    with open(f"image_{i}.jpeg", mode="wb") as f:
        f.write(response.content)
        
     delete(url)
    
