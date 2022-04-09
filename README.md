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


# Installation

1) Have Python ( https://www.python.org/downloads/ ) installed (and added to PATH during install)

2) Put css2rss.py into your `data4` folder (so you can call the script with just `python css2rss.py`, else you'd need to specify full path to the `.py` file)

![data4](https://user-images.githubusercontent.com/1309656/162590050-0c6d4d9d-4c57-4123-9959-06a83f0af61b.jpg)
