from time import sleep
from requests import get, post, delete

IP_ADDRESS = "http://192.168.1.111:8080"
base_url = f"{IP_ADDRESS}/ccapi/ver100"

# Check connection with API
res = get(f"{IP_ADDRESS}/ccapi")
print(f"API connection - status code: {res.status_code}")

# Take a picture
res = post(f"{base_url}/shooting/control/shutterbutton", json={"af": True})
print(f"Take a picture - status code: {res.status_code}")

# Get urls of pictures on the device
img_dir_url = f"{base_url}/contents/sd/100CANON"
res = get(img_dir_url)

# Wait for picture to save in the memory
counter = 0

while res.status_code != 200:
    sleep(0.1)
    if counter > 20:
        raise RuntimeError("Cannot get urls")
    res = get(img_dir_url)
    counter += 1

sleep(0.5)

res = get(img_dir_url)
print(f"Get urls - status code: {res.status_code}")

urls = res.json()["url"]

# Get pictures and then delete them
for i, url in enumerate(urls):
    res = get(url)

    with open(f"img_{i}.jpeg", mode="wb") as f:
        f.write(res.content)

    delete(url)


