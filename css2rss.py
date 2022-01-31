# CSS2RSS
# input html file must be provided in stdin
# arguments: item, item title, item description, item link

import json
import sys
from bs4 import BeautifulSoup

#from urllib.request import Request, urlopen
#url="https://en.wikivoyage.org/wiki/Main_Page"
#req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
#web_byte = urlopen(req).read()
#input_data = web_byte.decode('utf-8')

sys.stdin.reconfigure(encoding='utf-8')
input_data = sys.stdin.read()

soup = BeautifulSoup(input_data, 'html.parser')
items = list()
found_items = soup.select(sys.argv[1])

if len(found_items) != 0:
  for item in found_items:
    #print(item)

    if len(sys.argv) > 2 and sys.argv[2] != '':
      if len(sys.argv) > 5 and sys.argv[5] != '':
        item_title = json.dumps(item.select(sys.argv[2])[0].text + " - " + item.select(sys.argv[5])[0].text)
      else:
        item_title = json.dumps(item.select(sys.argv[2])[0].text)
    else:
      item_title = json.dumps(item.text) # use all the text inside

    #print(item_title)

    if len(sys.argv) > 3 and sys.argv[3] != '':
      item_description = json.dumps(str(item.select(sys.argv[3])[0])) # keep html
    else:
      item_description = json.dumps(str(item))

    #print(item_description)

    if len(sys.argv) > 4 and sys.argv[4] != '':
      item_link = json.dumps(item.select(sys.argv[4])[0]['href'])
    else:
      item_link = json.dumps(item['href']) if item.name == "a" else json.dumps(item.find("a")['href']) # 1st link or the item itself if it is a link

    #print(item_link)

    items.append("{{\"title\": {title}, \"content_html\": {html}, \"url\": {url}}}".format(
      title=item_title,
      html=item_description,
      url=item_link,
      date=json.dumps("2020-12-31T08:00:00")))

    #icon = soup.select('link[rel*=icon]')
    #if len(icon):
    #  json_feed = "{{\"title\": {title}, \"icon\": {icon}, \"items\": [{items}]}}"
    #  json_feed = json_feed.format(title = json.dumps(soup.title.text), icon = json.dumps(icon[0]['href']), items = ", ".join(items))
    #else:
    json_feed = "{{\"title\": {title}, \"description\": {description}, \"items\": [{items}]}}"
    json_feed = json_feed.format(title = json.dumps(soup.title.text), description = json.dumps("Script found "+str(len(found_items))+" items"), items = ", ".join(items))
else:
  items.append("{{\"title\": {title}, \"content_html\": {html}, \"url\": {url}}}".format(
    title=(json.dumps("ERROR page: " + soup.title.text) if soup.title else json.dumps("ERROR page:")),
    html=json.dumps(str(soup.select(":root")[0])),
    url=json.dumps(""),
    date=json.dumps("2020-12-31T08:00:00")))
  json_feed = "{{\"title\": {title}, \"description\": {description}, \"items\": [{items}]}}"
  json_feed = json_feed.format(title = (json.dumps("ERROR: " + soup.title.text) if soup.title else json.dumps("ERROR")), description = json.dumps("Error: - CSS selector found no items"), items = ", ".join(items))

print(json_feed)

