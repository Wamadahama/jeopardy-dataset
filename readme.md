# Jeopardy dataset

Dataset containing all recorded jeopardy games on the ![j-archive](http://www.j-archive.com) webiste. The associated script will check if there are new episodes and add it to the `jeopardy_dataset.csv` file. There are some nulls due to lack of information on the website. The csv is encoded in utf-8.

## Files 
* jeopardy_dataset.csv  - Latest dataset scraped from the j-archive
* jeopardy_dataset.info - metadata, contains the last epsiode id scraped from the site
* generate_dataset.py   - scrapes all games from j-archive

## Fields
* Category
* Value
* Order - The order that the question was selected during the game 
* Question
* Answer 

## Usage
Requires `BeautifulSoup4`
```
$ python generate_dataset.py 
```

## TODO
* Final jeopardy
* command line arguments for the scraper
* ~~Write to info file~~
* date field 

## Reducing scraping time 
* ~persistent HTTP connection~ 
* multi threading?

