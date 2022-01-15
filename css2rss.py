# CSS2RSS
# input html file must be provided in stdin
# arguments: item, item title, item description, item link

import json
import sys
#import urllib.request
#from html.parser import HTMLParser
from bs4 import BeautifulSoup

sys.stdin.reconfigure(encoding='utf-8')
input_data = sys.stdin.read()
#input_data = urllib.request.urlopen("https://en.wikivoyage.org/wiki/Main_Page") # if you want to do the web-request as well
soup = BeautifulSoup(input_data, 'html.parser')

json_feed = "{{\"title\": {title}, \"icon\": {icon}, \"items\": [{items}]}}"
items = list()

for item in soup.select(sys.argv[1]):
  if len(sys.argv) > 2 and sys.argv[2] != '':
    item_title = json.dumps(item.select(sys.argv[2])[0].text)
  else:
    item_title = item.text

  #print(item_title)

  if len(sys.argv) > 3 and sys.argv[3] != '':
    item_description = json.dumps(str(item.select(sys.argv[3])[0])) # keep html
  else:
    item_description = item

  #print(item_description)

  if len(sys.argv) > 4 and sys.argv[4] != '':
    item_link = json.dumps(item.select(sys.argv[4])[0]['href'])
  else:
    item_link = json.dumps(item.find("a")['href']) # 1st link

  #print(item_link)

  items.append("{{\"title\": {title}, \"content_html\": {html}, \"url\": {url}}}".format(
    title=item_title,
    html=item_description,
    url=item_link,
    date=json.dumps("2020-12-31T08:00:00")))

icon = soup.select('link[rel*=icon]')
if len(icon):
  json_feed = json_feed.format(title = json.dumps(soup.title.text), icon = json.dumps(icon[0]['href']), items = ", ".join(items))
else:
  json_feed = json_feed.format(title = json.dumps(soup.title.text), items = ", ".join(items))

print(json_feed)

