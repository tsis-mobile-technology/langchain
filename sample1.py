import requests
from bs4 import BeautifulSoup

def get_weather():
   url = "https://wttr.in/Seoul?format=3"
   headers = {
      "User-Agent": "curl/7.64.1",
      "Content-Type":"text/html; charset=utf-8"
}
   resp = requests.get(url, headers=headers)
   soup = BeautifulSoup(resp.content, "lxml")
   print("Current weather in Seoul:\n\n{}".format(str(soup)))

get_weather()