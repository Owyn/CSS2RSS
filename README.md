# CSS2RSS
scrapper post-process script for RSSGuard ( https://github.com/martinrotter/rssguard )

## Arguments - each is a CSS selector ( https://www.w3schools.com/cssref/css_selectors.asp ): 
1) item
2) item title (optional - else would use all the text from item as title)
3) item description (optional - else would use all the text from item as title)
4) item link (optional - else would use 1st found link in the item (or the item itself if it's a link))
5) item title 2nd part (optional (or if static main title \ multilink option is enabled), else just title, e.g. title is "Batman" and 2nd part is "chapter 94")

## Options for arguments:
* for `1) item` - `@` at start - enables searching for multiple links inside the found item, e.g. one `div` item and multiple `a` links inside it and you want it as separate feed items
* for `1) title` , `5) item title 2nd part` and `3) item description` - `!` at start - makes it a static specified value (after the !), e.g. `"!my title"`, if you make 1st part of the title fixed then 2nd part title addon would get auto-enabled and it would use text inside the found link as the 2nd part (unless you specify what to use manually as the 5th argument)

## Notes: 
- `1) item` is searched in the whole document and the rest is searched inside the `item` document node (but you can make the `item` point right at the `a` hyperlink - it will be used by default)
- use `~` as the whole argument (for arguments after `1) item` to let the script decide what to do (default action) - e.g. use 1st found link inside the item, use whole text inside the item as the description etc (not actually an option, but rather a format for the argument line), e.g. `python css2rss.py div.class ~ span.description` (here link's text will be used as the title by default action but description is manually specified)
- use space ` ` as the separator for arguments if they contain no spaces themselves, else (if they do) also enclose such arguments into double-brackets `"`, e.g. `python css2rss.py div.class "div.subclass > h1.title" span.description` (btw, you can also enclose arguments without any spaces into brackets if you'd like)
- if no item is found - a feed item would be generated with the html dump of the whole page so you could see what could be wrong (e.g. - cloudflare block page)

## Limitations:  
- If you are using a **NoWebEngine** version of the RSSGuard (like I am), then no javaScripts would run on scrapped pages, so sites which populate their content with javaScripts wouldn't be able to get scrapped, instead their starting version (what you'd see in `right click -> view page source`) would get scrapped.
    - You could try to get the needed content from other pages of the site, e.g. - main page, releases page or even the search page - one of these pages could be static and not constructed using javaScripts

# Installation

1) Have Python ( https://www.python.org/downloads/ ) installed (and added to PATH during install)  

    1.2. Have Python Soup ( https://www.crummy.com/software/BeautifulSoup/ ) installed (Win+R -> cmd -> enter -> `pip install beautifulsoup4`) 

2) Put css2rss.py into your `data4` folder (so you can call the script with just `python css2rss.py`, else you'd need to specify full path to the `.py` file)

![data4](https://user-images.githubusercontent.com/1309656/162590050-0c6d4d9d-4c57-4123-9959-06a83f0af61b.jpg)

# Examples

 ## *  
- a simple link makeover into an rss feed (right-clicked a link -> inspect element -> use its CSS selector):  

url: `https://www.foxnews.com/media`  
script: `python css2rss.py ".title > a"` (link `a` right inside an element with `title` class
![](https://user-images.githubusercontent.com/1309656/162590533-dcc261f4-3a24-4c59-9e24-60d312a4e3ec.jpg)
![](https://user-images.githubusercontent.com/1309656/162590684-c452b64f-7916-43e1-b440-3889b2d6a82c.jpg)
![](https://user-images.githubusercontent.com/1309656/162590622-66bf2f9e-e2cb-4434-a377-3ebdcc573f20.jpg)

 ## *  
- the reason for implementing static titles  

url: `https://kumascans.com/manga/sokushi-cheat-ga-saikyou-sugite-isekai-no-yatsura-ga-marude-aite-ni-naranai-n-desu-ga/`  
script: `python css2rss.py ".eph-num > a" "!Sokushi Cheat" ".chapterdate" ~ ".chapternum"`

![](https://user-images.githubusercontent.com/1309656/162590790-1995cd7e-ea6f-41b5-a24c-cb669de851d2.jpg)
![](https://user-images.githubusercontent.com/1309656/162590821-d3388846-fb47-41e4-866a-5aaa3754d022.jpg)

 ## *  
- the reason for implementing searching multiple links inside one item  

url: `https://www.asurascans.com/`  
script: `python css2rss.py "@.uta" "h4" img "li > a" "li > a"`

![](https://user-images.githubusercontent.com/1309656/162590919-4374ba05-9c1f-4f39-b27c-f723d4afda1f.jpg)
![](https://user-images.githubusercontent.com/1309656/162590934-4c28c614-7548-4048-b147-b7a5b036a842.jpg)

 ## *  
url: `https://reader.kireicake.com/`  
script: `python css2rss.py @.group a[href*='/series/'] .meta_r ".element > .title a" ".element > .title a"`

![](https://user-images.githubusercontent.com/1309656/162591038-3664255c-8e8b-4065-b0a9-a0d2eb4977c7.jpg)
![](https://user-images.githubusercontent.com/1309656/162591089-6951e712-384f-4109-8c57-1caa05ac49f6.jpg)

 ## *  
url: `https://reaperscans.com/home1/` or url: `https://immortalupdates.com/` (same website design)  
script: `python css2rss.py "@div.manga" ".post-title" "img" ".btn-link" ".btn-link"`

 ## *  
- the workaround to scrap sites which give out their contents via javaScripts  

url: `https://manhuaus.com/?s=Wo+Wei+Xie+Di&post_type=wp-manga&post_type=wp-manga`  
script: `python css2rss.py ".latest-chap a" "!I'm an Evil God"`  
