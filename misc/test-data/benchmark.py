import csv
import time
import requests
import sys

LIGHT = 500
FULL = 4000

test = LIGHT
try:
    if sys.argv[1] == "full":
        test = FULL
except:
    pass

url = "http://0.0.0.0:8000/api/v1/bookings"

headers = {
    "content-type": "application/json",
    "cache-control": "no-cache",
    "postman-token": "29a846ef-a9e2-7422-071b-30b98ebc2ed4",
}


global_array = []
with open("bookings.csv", "rt") as f:
    reader = csv.DictReader(f)
    temp = 0
    for row in reader:
        global_array.append(str(row).replace("'", '"'))
        temp += 1
        if temp == test:
            break

a = time.localtime()

for booking in global_array:
    response = requests.request("POST", url, data=booking, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Status code returned {response.status_code}")

# import pdb;pdb.set_trace()
a = time.mktime(time.localtime()) - time.mktime(a)
print(f"Took {a} seconds for {test} requests")
