# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "beautifulsoup4",
#     "maya",
# ]
# ///
# CSS2RSS
# input html file must be provided in stdin
# arguments: item, item title, item description, item link, item title 2nd part, item date

import json
import sys
import datetime
from bs4 import BeautifulSoup

def css_to_rss(item, depth):
  find_links_near = False
  found_link = None
  if (not(bDefault_link) and sys.argv[4][0] == '!'):
    item_link = sys.argv[4][1:]
    #found_link = item #for the default description - maybe bad idea?
    if bMulti_enabled and not(bDefault_main_title) and (depth+1 < len(item.select(sys.argv[2]))): # lets count found main titles then if the link is static?
      find_links_near = True
  elif aEval[4]:
    found_link = eval(sys.argv[4])
    if isinstance(found_link, list) == True:
      if (link_l := len(found_link)) > depth:
        if bMulti_enabled and depth+1 < link_l:
          find_links_near = True
        found_link = found_link[depth]
        item_link = found_link['href']
    else:
      item_link = found_link['href']
  elif not(bDefault_link) and (link_l := len(found_link := item.select(sys.argv[4]))) > depth:
    found_link = found_link[depth]
    item_link = found_link['href']
    if bMulti_enabled and depth+1 < link_l:
      find_links_near = True
  else:
    if item.name == "a": #item itself is a link
      found_link = item
      item_link = item['href']
    else: # use 1st link found
      if bDefault_link:
        found_link = item.find("a")
        if found_link:
          item_link = found_link['href']
      if not(found_link): # we found something else without a link or we specified a link to find so we don't want 1st found link anymore
        global found_items_bad_n
        found_items_bad_n += 1
        return
  
  if bFixed_main_title:
    main_title = sys.argv[2]
  elif aEval[2]:
    main_title = eval(sys.argv[2]) # add .text at the end of your eval selector yourself if it's a html element
    if isinstance(main_title, list) == True:
      main_title = main_title[depth if len(main_title) > depth else 0]
  elif not(bDefault_main_title) and (mt_l := len(main_title := item.select(sys.argv[2]))) != 0:
    main_title = main_title[depth if mt_l > depth else 0].text # not sure if we should look for more main titles?
  elif found_link:
    main_title = found_link.text # use the link's text
    #main_title = item.text # use all the text inside - bad idea
  else:
    main_title = ""
    #raise(ValueError("Title & Link were not found - can't do anything now, please adjust your Title selector: " + sys.argv[2]))
    global found_items_bad_t
    found_items_bad_t += 1
    return
      
  if bFixed_addon_title:
    addon_title = sys.argv[5]
  elif not(bDefault_addon_title):
    if aEval[5]:
      addon_title = eval(sys.argv[5]) # add .text at the end of your eval selector yourself if it's a html element
      if isinstance(addon_title, list) == True:
        addon_title = addon_title[depth] # we need all the addon titles
    elif len(addon_title := item.select(sys.argv[5])) > depth:
      addon_title = addon_title[depth].text
    else:
      addon_title = found_link.text
  elif bFixed_main_title or (bMulti_enabled and found_link): # enable addon title by default for these options
    addon_title = found_link.text
  else:
    addon_title = ""
  #raise(ValueError(addon_title)) # lets see what we've found?
  
  item_title = main_title + (" - " if addon_title != "" else "") + addon_title
  
  if bComment_fixed:
    item_description = sys.argv[3]
  elif aEval[3]:
    item_description = eval(sys.argv[3])
    if isinstance(item_description, list) == True:
      item_description = item_description[depth if len(item_description) > depth else 0]
  elif not(bDefault_comment) and (desc_l := len(tDescr := item.select(sys.argv[3]))) != 0:
    item_description = str(tDescr[depth if desc_l > depth else 0]) # keep html, also use 1st found if none further
    #item_description = item_description.replace('<', '≤').replace('&', '＆') # don't keep html
  else:
    item_description = str(item) # use everything inside found item

  item_date = ""
  DateCurEl = ""
  if bFind_date:
    if ((tDate := eval(sys.argv[6])) if aEval[6] else (date_l := len(tDate := item.select(sys.argv[6])))) != 0:
      if aEval[6]:
        if isinstance(tDate, list) == False:
          DateCurEl = tDate
        else:
          date_l = len(tDate)
      
      if DateCurEl == "":
        if date_l > depth:
          DateCurEl = tDate[depth]
        else:
          DateCurEl = "no Date element found for THIS item (there are less date elements found than total items)"
      
      if type(DateCurEl) == str:
        item_date = DateCurEl
      else:
        item_date = (DateCurEl['datetime'] if DateCurEl.has_attr('datetime') else DateCurEl['alt'] if DateCurEl.has_attr('alt') else DateCurEl['title'] if DateCurEl.has_attr('title') else "") or DateCurEl.text
      try:
        item_date = maya.parse(item_date, get_localzone().key, bNotAmerican_Date).datetime().isoformat()
      except: # BaseException:
        try:
          item_date = maya.when(item_date, get_localzone().key).datetime().isoformat()
        except: # ValueError:
          #ok what now? do we error everything or say that the feed is fully invalid when just the date is invalid?
          item_description += "\n<br>CSS2RSS: Date '"+item_date+"' from element '"+str(DateCurEl).replace('<', '≤').replace('&', '＆')+"' could not be parsed for this entry, please adjust your CSS selector: " + sys.argv[6].replace('<', '≤').replace('&', '＆')
          global found_items_w_bad_dates
          found_items_w_bad_dates += 1
          item_date = ""
    else:
      global found_items_wo_dates
      found_items_wo_dates += 1
  
  items.append("{{\"title\": {title}, \"content_html\": {html}, \"url\": {url}, \"date_published\": {date}}}".format(
      title=json.dumps(item_title),
      html=json.dumps(item_description),
      url=json.dumps(item_link),
      date=json.dumps(item_date)))

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

aEval = [False] * 7
i = 1
while i < len(sys.argv):
  if sys.argv[i][0] == '$':
    sys.argv[i] = sys.argv[i][1:] # cut $
    aEval[i] = True
  i += 1

bDefault_main_title = False
bFixed_main_title = False
if len(sys.argv) > 2:
  if sys.argv[2] == '' or sys.argv[2][0] == '~':
    bDefault_main_title = True
  elif sys.argv[2][0] == '!':
    sys.argv[2] = sys.argv[2][1:]
    bFixed_main_title = True
else:
  bDefault_main_title = True

bDefault_addon_title = False
bFixed_addon_title = False
bEval_addon_title = False
if len(sys.argv) > 5:
  if sys.argv[5] == '' or sys.argv[5][0] == '~':
    bDefault_addon_title = True
  elif sys.argv[5][0] == '!':
    sys.argv[5] = sys.argv[5][1:]
    bFixed_addon_title = True
  elif len(sys.argv) > 5 and sys.argv[5][0] == '$':
    sys.argv[5] = sys.argv[5][1:]
    bEval_addon_title = True
else:
  bDefault_addon_title = True

bDefault_comment = False
bComment_fixed = False
if len(sys.argv) > 3:
  if sys.argv[3] == '' or sys.argv[3][0] == '~':
    bDefault_comment = True
  elif sys.argv[3][0] == '!':
    sys.argv[3] = sys.argv[3][1:]
    bComment_fixed = True
else:
  bDefault_comment = True

if len(sys.argv) > 4:
  if sys.argv[4] == '' or sys.argv[4][0] == '~':
    bDefault_link = True
  else:
    bDefault_link = False
else:
  bDefault_link = True

bFind_date = False
bNotAmerican_Date = True
if len(sys.argv) > 6:
  if sys.argv[6] != '' and sys.argv[6][0] != '~':
    bFind_date = True
    try:
      import maya
      from tzlocal import get_localzone
    except BaseException as e:
      raise(SystemExit("Couldn't import Maya module to parse time, have you installed it? error: ", e))
    if sys.argv[6][0] == '?':
      sys.argv[6] = sys.argv[6][1:]
      bNotAmerican_Date = False

# end options

if aEval[1]:
  item_selector = eval(sys.argv[1])
else:
  item_selector = sys.argv[1]
found_items = soup.select(item_selector)
found_items_n = len(found_items)
found_items_bad_n = 0
found_items_bad_t = 0
found_items_wo_dates = 0
found_items_w_bad_dates = 0

jsonfeed_version = "https://jsonfeed.org/version/1.1"
description_addon = ""
if found_items_n != 0:
  for item in found_items:
    css_to_rss(item, 0)
  if found_items_bad_n != 0:
    description_addon += ", Found items with NO Link: " + str(found_items_bad_n)
  if found_items_bad_t != 0:
    description_addon += ", Found items with NO Title: " + str(found_items_bad_t)
  if found_items_wo_dates != 0:
    description_addon += ", Found no Date item for: " + str(found_items_wo_dates)
  if found_items_w_bad_dates != 0:
    description_addon += ", Failed to parse Dates for: " + str(found_items_w_bad_dates)
  json_feed = "{{\"version\": {version}, \"title\": {title}, \"description\": {description}, \"items\": [{items}]}}"
  json_feed = json_feed.format(version = json.dumps(jsonfeed_version), title = json.dumps(soup.title.text), description = json.dumps("Script found "+str(found_items_n)+" items"+description_addon), items = ", ".join(items))
else:
  raise(SystemExit("CSS selector found no items - is the content generated with JavaScript? - Or did the website change its structure?"))
  items.append("{{\"title\": {title}, \"content_html\": {html}, \"url\": {url}}}".format(
    title=json.dumps("ERROR page @ " + str(datetime.datetime.now()) + (" - " + soup.title.text) if soup.title else ""),
    html=json.dumps(soup.prettify()),
    url=json.dumps("")))
  json_feed = "{{\"version\": {version}, \"title\": {title}, \"description\": {description}, \"items\": [{items}]}}"
  json_feed = json_feed.format(version = json.dumps(jsonfeed_version), title = (json.dumps("ERROR: " + soup.title.text) if soup.title else json.dumps("ERROR")), description = json.dumps("Error: - CSS selector found no items"), items = ", ".join(items))

print(json_feed)
