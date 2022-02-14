# CSS2RSS
scrapper post-process script for RSSGuard ( https://github.com/martinrotter/rssguard )

arguments - each is a CSS selector ( https://www.w3schools.com/cssref/css_selectors.asp ): 
1) item
2) item title (optional - else would use all the text from item as title)
3) item description (optional - else would use all the text from item as title)
4) item link (optional - else would use 1st found link in the item (or the item itself if it's a link))
5) item title 2nd part (optional, else just title, e.g. title is "Batman" and 2nd part is "chapter 94")

note: - `item` is searched in the whole document and everything else is searched inside the `item` document node

if no item would be found - a feed item would be generated with the html dump of the whole page so you could see what could be wrong (e.g. - cloudflare block page)


![image](https://user-images.githubusercontent.com/1309656/153844051-206dfff7-559d-4cec-aa46-d66f3f12b2cd.png)

![image](https://user-images.githubusercontent.com/1309656/153844254-eb1b6d38-e418-4346-af9d-1fd31fbf152b.png)


# Installation

1) Have Python ( https://www.python.org/downloads/ ) installed (and added to PATH during install)

2) Put css2rss.py into your `data4` folder (so you can call the script with just `python css2rss.py`, else you'd need to specify full path to the `.py` file)

![image](https://user-images.githubusercontent.com/1309656/153845026-cdc439e4-1b75-4715-bfbe-188139fc0ed4.png)
