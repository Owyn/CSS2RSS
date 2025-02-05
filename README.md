# CSS2RSS
scrapper post-process script for RSSGuard ( https://github.com/martinrotter/rssguard )

## Arguments - each is a CSS selector ( https://www.w3schools.com/cssref/css_selectors.asp ): 
1) item
2) item title (optional - else would use link's text as title)
3) item description (optional - else would use all the text from item as description)
4) item link (optional - else would use 1st found link in the item (or the item itself if it's a link))
5) item title 2nd part (optional (or if static main title \ multilink option is enabled), else just title, e.g. title is "Batman" and 2nd part is "chapter 94")
6) item date (optional, else it'd all be "just now") - aim this selector either at text nodes (e.g. `span`) or elements (`a`, `img`) with `title` or `alt` containing the Date (e.g. "New!" flashing image badges you get the Date when hovering over)

## Options for arguments:
* for `1) item` - `@` at start - enables searching for multiple links inside the found item, e.g. one `div` item and multiple `a` links inside it and you want it as separate feed items
* for everything after `1) item` - `~` as the whole argument - to let the script decide what to do (default action) - e.g. use 1st found link inside the item, use whole text inside the item as the description etc (not actually an option, but rather a format for the argument line), e.g. `python css2rss.py div.itemclass ~ span.description` (here link's inner text (2nd argument) will be used as the title by default action but description is being looked for (3rd argument))
* for `2) title` , `5) item title 2nd part` and `3) item description` - `!` at start - makes it a static specified value (after the !), e.g. `"!my title"`, if you make 1st part of the title fixed then 2nd part title addon would get auto-enabled and it would use text inside the found link as the 2nd part (unless you specify what to use manually as the 5th argument)
* for everything (even for the `1) item` - `$` at start - executes (via `eval()`) a python code expression instead of using CSS selectors, the return value of that expression will be used for that item e.g. `$found_link.find('img')['alt']` would return `alt` text from an `img` element inside found link, see https://www.crummy.com/software/BeautifulSoup/bs4/doc/ for things you can do with the soup - e.g. go one level up (to the parent element) or to the next element - or select elements CSS selectors can't select, or anything you can do with Python - see examples section below
* for `6) date` - `?` at start - tells the parser that you're expecting an Americal format of date - "Month/Day/Year"

## Notes: 
- `1) item` is searched in the whole document and the rest is searched inside the `item` document node (but you can make the `item` point right at the `a` hyperlink - it will be used by default)

- use space ` ` as the separator for arguments if they contain no spaces themselves, else (if they do) also enclose such arguments into quotation marks `"`, e.g. `python css2rss.py div.class "div.subclass > h1.title" span.description` (btw, you can also enclose arguments without any spaces into brackets if you'd like)
**Warning**: starting from RSSGuard v4.5.2 which supports single quotation marks as well `'` you have to either use single quotation marks instead `'` to enclose arguments to pass them as is or escape backslashes and double-quotes with backslashes, e.g. `python css2rss.py "\\:argument starting with\\:"` or `python css2rss.py '\:argument starting with\:'`
- if no item is found - a feed item would be generated with the html dump of the whole page so you could see what could be wrong (e.g. - cloudflare block page)
- content you need to log-in first to see is available
    - scrapper uses cookies of RSSGuard, so if you login into a website using built-in browser of RSSGuard - scrapper would be able to access that content as well to scrape it into a feed

## Limitations:  
- No javaScripts would run on scrapped pages, so sites which populate their content with javaScripts wouldn't be able to get scrapped, instead their starting version (what you'd see in `right click -> view page source`) would get scrapped.
    - You could try to get the needed content from other pages of the site, e.g. - main page, releases page or even the search page - one of these pages could be static and not constructed using javaScripts

# Installation

1) Have Python 3+ or newer ( https://www.python.org/downloads/ ) installed (and added to PATH during install)  

    1.2. Have Python Soup ( https://www.crummy.com/software/BeautifulSoup/ ) installed (Win+R -> cmd -> enter -> `pip install beautifulsoup4`)  
    1.3. (optional) If you'd like to parse Dates for articles - Have Maya ( https://github.com/timofurrer/maya/ ) installed (Righ click the Start menu -> run powershell as administrator -> cmd -> `pip install maya`)  

3) Put css2rss.py into your `data4` folder (so you can call the script with just `python css2rss.py`, else you'd need to specify full path to the `.py` file)

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
- the reason for implementing eval expressions for titles (since CSS selectors can't select text nodes outside any tags) 

url: `https://reaperscans.com/`  
script: `python css2rss.py "@div.space-y-4:first-of-type div.relative.bg-white" "p.font-medium" "img" "a.border" "$found_ink.contents[0].text"` (it was just `$contents[0]` previously as seen on the screenshot but later more freedom was given so now you have to write the full code)

![image](https://user-images.githubusercontent.com/1309656/194601286-7c7b399a-7561-4274-9444-89508dd51681.png)
![image](https://user-images.githubusercontent.com/1309656/194601403-578c9550-785e-44bd-98d7-88c50f785a5d.png)


 ## *  
url: `https://reader.kireicake.com/`  
script: `python css2rss.py @.group a[href*='/series/'] .meta_r ".element > .title a" ".element > .title a"`

![](https://user-images.githubusercontent.com/1309656/162591038-3664255c-8e8b-4065-b0a9-a0d2eb4977c7.jpg)
![](https://user-images.githubusercontent.com/1309656/162591089-6951e712-384f-4109-8c57-1caa05ac49f6.jpg)


 ## *  
 - example for parsing Dates for articles, here it uses OR in the css selector and it looks for either `a` element (the "New!" badge) with date inside its tooltip (`title` or `alt`) **OR** for a `span` element without any child nodes (both these elements are of class `.post-on`
 
url: `https://drakescans.com/`  
script: `python css2rss.py  "@.page-item-detail" ".post-title a" "img" "span.chapter > a" ~ ".post-on > a,.post-on:not(:has(*))"`

![](https://github.com/Owyn/CSS2RSS/assets/1309656/692796e0-8caa-4b1b-ac05-2be60388aa28)
![](https://github.com/Owyn/CSS2RSS/assets/1309656/55220446-4c22-498a-9bb7-1c27294996bb)


 ## *  
- the workaround to scrap sites which give out their contents via javaScripts (the workaround is to find a static page - right-click -> view page source - and see if your text is originally there - that means it's static and not given out later via JS) 

url: `https://manhuaus.com/?s=Wo+Wei+Xie+Di&post_type=wp-manga&post_type=wp-manga`  
script: `python css2rss.py ".latest-chap a" "!I'm an Evil God"`  
