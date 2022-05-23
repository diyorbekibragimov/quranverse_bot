import requests

URL = "https://api.quran.com/api/v4/verses/by_key/1:2?language=ru&words=true"

r = requests.get(url=URL)

data = r.json()
words = data['verse']['words']
arr = []
for e in words:
    w = e['translation']['text']
    arr.append(w)

string = ",".join(arr)
print(arr)

def get_translations():
    url = "https://api.quran.com/api/v4/resources/translations"
    r = requests.get(url=url)
    data = r.json()
    translations = data["translations"]
    for t in translations:
        if t["language_name"] == "russian":
            print(t)