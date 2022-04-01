# WoTWikiScraper
This is a webscraper for the [Wheel of Time Fandom Wiki](https://wot.fandom.com/wiki/A_beginning). Main purpose is to scrape the pages and convert them to a format that [Obsidian.md](https://obsidian.md/) can read and visualize as a network.

Inspired by the [Malthemester](https://github.com/Malthemester)'s webscraper, modified for fandom and added parallelization.

Original code: https://github.com/Malthemester/CoppermindScraper

## Reddit Posts
- WoT Fandom post: https://www.reddit.com/r/WoT/comments/ttzlve/wheel_of_time_connection_graph_fandom_wiki
- Coppermind post: https://www.reddit.com/r/Cosmere/comments/tku1a3/visualization_of_the_coppermind_wiki_all

## Requirements
- Python 3.x
- [tqdm](https://github.com/tqdm/tqdm) - progress bar
- [aiohttp](https://github.com/aio-libs/aiohttp) - async requests

## Use
Existing files:
- Export `Randland.7z`, it includes scraped and Obsidian-ready files.

To scrape and preapare from scratch:
- `WotWiki.py`: Main script. Scrapes the fandom given an initial page.
- `clear_tags.py`: Creates a taglist and filters some unnecessary ones for better visualization.
- `count_links.py`: Counts the number of links between pages (3,325 pages and 50,860 links)

## Visualization
You may wish to do some manual cleaning before starting, though `clear_tags.py` script should be enough for most cases. Obsidian is used for all visualization purposes.

Obsidian graph settings:
- Filters
  - Existing files only: True
  - Orphans: False
- Forces
  - Center force: 0.5
  - Repel force: 10
  - Link force: 1
  - Link distance: 250
