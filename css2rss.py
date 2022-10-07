# CSS2RSS
# input html file must be provided in stdin
# arguments: item, item title, item description, item link, item title 2nd part

import json
import sys
from bs4 import BeautifulSoup

def css_to_rss(item, depth):
  find_links_near = False
  tLink = None
  if not(bDefault_link) and (link_l := len(tLink := item.select(sys.argv[4]))) > depth:
    tLink = tLink[depth]
    item_link = tLink['href']
    if bMulti_enabled and depth+1 < link_l:
      find_links_near = True
  else:
    if item.name == "a": #item itself is a link
      tLink = item
      item_link = item['href']
    else: # use 1st link found
      tLink = item.find("a")
      if(tLink):
        item_link = tLink['href']
      else: # we found something else without a link
        global found_items_bad_n
        found_items_bad_n += 1
        return

  main_title = ""
  if bFixed_main_title:
    main_title = sys.argv[2]
  elif bEval_main_title:
      main_title = eval("tLink."+sys.argv[2]).text
  elif not(bDefault_main_title) and (mt_l := len(main_title := item.select(sys.argv[2]))) != 0:
    main_title = main_title[depth if mt_l > depth else 0].text # not sure if we should look for more main titles?
  else:
    main_title = tLink.text # use the link's text
    #main_title = item.text # use all the text inside - bad idea

  addon_title = ""
  if bFixed_addon_title:
      addon_title = sys.argv[5]
  elif not(bDefault_addon_title):
    if bEval_addon_title:
      addon_title = eval("tLink."+sys.argv[5]).text # lets just use "tLink" as an anchor instead of making ppl care about "[depth]"
    elif len(addon_title := item.select(sys.argv[5])) > depth:
      addon_title = addon_title[depth].text
    else:
      addon_title = tLink.text
  elif bFixed_main_title or bMulti_enabled: # enable addon title by default for these options
    addon_title = tLink.text
  #raise(ValueError(addon_title)) # lets see what we've found?

  item_title = main_title + (" - " if addon_title != "" else "") + addon_title

  if bComment_fixed:
    item_description = str(sys.argv[3])
  elif not(bDefault_comment) and (desc_l := len(tDescr := item.select(sys.argv[3]))) != 0:
    item_description = str(tDescr[depth if desc_l > depth else 0]) # keep html, also use 1st found if none further
    #item_description = item_description.replace('>', '');
    #item_description = item_description.replace('<', '');
  else:
    item_description = str(item) # use everything inside found item

  items.append("{{\"title\": {title}, \"content_html\": {html}, \"url\": {url}}}".format(
      title=json.dumps(item_title),
      html=json.dumps(item_description),
      url=json.dumps(item_link)))

  if find_links_near:
    global found_items_n
    found_items_n += 1
    css_to_rss(item, depth+1)

#from urllib.request import Request, urlopen
#url="https://en.wikivoyage.org/wiki/Main_Page"
#req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
#web_byte = urlopen(req).read()
#input_data = web_byte.decode('utf-8')

sys.stdin.reconfigure(encoding='utf-8')
input_data = sys.stdin.read()

soup = BeautifulSoup(input_data, 'html.parser')
items = list()

# options: ! - fixed result text, @ - look for multiple links inside one item, ~ - do default action, $ - eval code
if sys.argv[1][0] == '@':
  sys.argv[1] = sys.argv[1][1:]
  bMulti_enabled = True
else:
  bMulti_enabled = False

bDefault_main_title = False
bFixed_main_title = False
bEval_main_title = False
if len(sys.argv) > 2:
  if sys.argv[2][0] == '!':
    sys.argv[2] = sys.argv[2][1:]
    bFixed_main_title = True
  elif sys.argv[2][0] == '$':
    sys.argv[2] = sys.argv[2][1:]
    bEval_main_title = True
  elif sys.argv[2] == '' or sys.argv[2][0] == '~':
    bDefault_main_title = True
else:
  bDefault_main_title = True

bDefault_addon_title = False
bFixed_addon_title = False
bEval_addon_title = False
if len(sys.argv) > 5:
  if sys.argv[5][0] == '!':
    sys.argv[5] = sys.argv[5][1:]
    bFixed_addon_title = True
  elif len(sys.argv) > 5 and sys.argv[5][0] == '$':
    sys.argv[5] = sys.argv[5][1:]
    bEval_addon_title = True
  elif sys.argv[5] == '' or sys.argv[5][0] == '~':
    bDefault_addon_title = True
else:
  bDefault_addon_title = True

bDefault_comment = False
bComment_fixed = False
if len(sys.argv) > 3:
  if sys.argv[3][0] == '!':
    sys.argv[3] = sys.argv[3][1:]
    bComment_fixed = True
  elif sys.argv[3] == '' or sys.argv[3][0] == '~':
    bDefault_comment = True
else:
  bDefault_comment = True

if len(sys.argv) > 4:
  if sys.argv[4] == '' or sys.argv[4][0] == '~':
    bDefault_link = True
  else:
    bDefault_link = False
else:
  bDefault_link = True
# end options

found_items = soup.select(sys.argv[1])
found_items_n = len(found_items)
found_items_bad_n = 0
if found_items_n != 0:
  for item in found_items:
    css_to_rss(item, 0)
  json_feed = "{{\"title\": {title}, \"description\": {description}, \"items\": [{items}]}}"
  json_feed = json_feed.format(title = json.dumps(soup.title.text), description = json.dumps("Script found "+str(found_items_n)+" items") if found_items_bad_n == 0 else json.dumps("Script found "+str(found_items_n)+" items, " + str(found_items_bad_n) + " bad items with no link"), items = ", ".join(items))
else:
  items.append("{{\"title\": {title}, \"content_html\": {html}, \"url\": {url}}}".format(
    title=(json.dumps("ERROR page: " + soup.title.text) if soup.title else json.dumps("ERROR page:")),
    html=json.dumps(soup.prettify()),
    url=json.dumps("")))
  json_feed = "{{\"title\": {title}, \"description\": {description}, \"items\": [{items}]}}"
  json_feed = json_feed.format(title = (json.dumps("ERROR: " + soup.title.text) if soup.title else json.dumps("ERROR")), description = json.dumps("Error: - CSS selector found no items"), items = ", ".join(items))

print(json_feed)

