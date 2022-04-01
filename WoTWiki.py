import random
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from tqdm.asyncio import tqdm
from aiohttp import ClientSession
import asyncio

BaseURL = "https://wot.fandom.com"
URL = "https://wot.fandom.com/wiki/Rand_al%27Thor"

months = ["Taisham", "Jumara", "Saban", "Aine ", "Adar ", "Saven", "Amadaine", "Tammaz", "Maigdhal", "Choren", "Shaldine", "Nesan", "Danu ",
          "January", "February", "March", "April", "May ", "June ", "July ", "August ", "September", "October", "November", "December"]

done = False

async def TableToMarkdown(table):
    table = table.find_all("tr")
    markdownTable = ""
    header = True

    for row in table:
        if(row.find("table")):
            continue
        else:
            for collumn in row:
                if(collumn.name == "th" or collumn.name == "td"):
                    markdownTable += '|'
                    collText = await ElementToMarkdown(collumn)
                    markdownTable += collText.replace("\n", "")
            markdownTable += '|\n'
        if(header):
            markdownTable += "|-|-|\n"
            header = False

    return markdownTable


async def HtmlToMarkdown(element):
    markdown = ""
    global done
    if done:
        return ""

    if element == None:
        return ""
    else:
        for child in element:
            if done:
                return markdown
            result = await ElementToMarkdown(child)
            markdown += result
    return markdown


async def ElementToMarkdown(element):
    global done

    if element.name == None:
        try:
            return element.text
        except:
            if type(element) == NavigableString:
                return element
            else:
                return ""
    elif element.name == 'a':
        try:
            if element['class'][0] == "external" or element['class'][0] == "extiw" or element['class'][0] == "image":
                return ""
        except KeyError:
            pass  # or some other fallback action
        return await LinkToMarkdown(element)
    elif element.name == 'b':
        return f"**{element.text}**"
    elif element.name == 'th':
        return f"**{element.text}**"
    elif element.name == 'em':
        return f"*{element.text}*"
    elif element.name == 'i':
        return f"*{element.text}*"
    elif element.name == 'ul':
        paige = await HtmlToMarkdown(element)
        return paige
    elif element.name == 'li':
        paige = await HtmlToMarkdown(element)
        return paige
    elif element.name == 'td':
        paige = await HtmlToMarkdown(element)
        return paige
    elif element.name == 'h3':
        paige = await HtmlToMarkdown(element)
        return "### " + paige
    elif element.name == 'h3':
        paige = await HtmlToMarkdown(element)
        return "#### " + paige
    elif element.name == 'h2':
        try:
            if element.text == "Notes[edit]":
                done = True
                return ""
        except KeyError:
            pass  # or some other fallback action
        paige = await HtmlToMarkdown(element)
        return "## " + paige
    elif element.name == 'span':
        try:
            if element['class'][0] == "mw-editsection":
                return ""
        except KeyError:
            pass  # or some other fallback action
        paige = await HtmlToMarkdown(element)
        return paige
    elif element.name == 'p':
        paige = await HtmlToMarkdown(element)
        return paige
    elif element.name == 'div':
        try:
            if element['class'][0] == "notice quality quality-partial stub":
                return ""
        except KeyError:
            pass  # or some other fallback action
        paige = await HtmlToMarkdown(element)
        return paige
    elif element.name == 'table':
        paige = await TableToMarkdown(element)
        return paige
    elif element.name == 'blockquote':
        mark_return = await HtmlToMarkdown(element.p)
        blockquote = ">" +  mark_return.replace("\n", "")
        blockquote = str(blockquote) + "\n"
        if len(element.contents) > 1:
            blockquote += "\-" + element.contents[1].text.replace("—", "")
            blockquote = str(blockquote) + "\n"
        return blockquote
    else:
        return ""

wikiQueue = [URL,"https://wot.fandom.com/wiki/Perrin_Aybara"]
wikiDone = []

async def LinkToMarkdown(a):

    global wikiQueue
    global wikiDone

    # Get reference link
    ref = a.get('href')
    ref = str(ref)

    # If unnecessary page
    if "File:" in ref or "Artists" in ref or "#" in ref or ":" in ref or "wikipedia" in ref:
        return a.text

    # If wiki page
    if "wiki" in ref:
        if BaseURL + ref not in wikiQueue:
            if BaseURL + ref not in wikiDone:
                wikiQueue.append(BaseURL + ref)
        title = ref.replace("/wiki/", "").replace("_", " ").replace("%27", "'")

        # Convert to obsidian format
        if any(title.startswith(x) for x in months) or title.endswith(" NE") or ("/Chapter" in title):
            return f"{a.text}"
        elif title == a.text:
            return f"[[{title}]]"
        else:
            return f"[[{title}|{a.text}]]"

    return ""

async def find_categories(doc):

    return_cat = []
    
    # If categories exists
    element = doc.find("ul", {"class": "categories"})
    if element != None:
        # Find all categories
        categories = element.find_all("li", {"class": "category normal"})
        if len(categories) > 0:
            # Add them to list
            for category in categories:
                return_cat.append(category.text.strip().replace(" ",""))
    
    return return_cat

async def procc_page(wikiPage):

    # Get page
    async with ClientSession() as session:
        async with session.get(wikiPage) as resp:
            HTMLpage = await resp.text()
    
    # Parse with BeautifulSoup
    doc = BeautifulSoup(HTMLpage, "html.parser")
    content = doc.find(class_="mw-parser-output")

    # Stop if no content
    if content is None:
        return True, wikiPage
    
    # Find title by firstHeading
    title = doc.find(id="firstHeading").text

    # Stop if unnecessary page
    if any([x in title for x in ["File:", "Artists", "#", "/", ":", "wikipedia", "Chapter"]]):
        return True, wikiPage

    # Try to get tags and page
    try:
        wiki_tags = await find_categories(doc)
        page = await HtmlToMarkdown(content)
        page += "\n\n" + wikiPage
    except Exception as e:
        print(title,e)
    
    # Stop if it's a date
    if any([title.strip().startswith(x) for x in months]):
        return True, wikiPage
    else:
        # Write to file
        with open("Randland\{}.md".format(title.strip()), "w", encoding="utf-8") as f:

            # Write tags if exists
            if len(wiki_tags) > 0:
                f.write("---\n")
                f.write("tags: [{}]\n".format(", ".join(wiki_tags)))
                f.write("---\n")
            # Write page
            f.write(page)

    return False, wikiPage

async def main():
    
    global wikiQueue
    global wikiDone
    global done

    ## Init progress-bar
    tq_elem = tqdm(total=2)
    pages_done = 0
    
    ## While queue not empty
    while len(wikiQueue) > 0:

        # Arrange processing queue
        process_queue = []
        for _ in range(min(len(wikiQueue),10)):
            process_queue.append(wikiQueue.pop(0))

        # Process
        for future in asyncio.as_completed(map(procc_page, process_queue), timeout=60):
            is_empty, wikiPage = await future

            # If it was not empty
            if not is_empty:

                # Add to done
                wikiDone.append(wikiPage)
                done = False

                # Increase progress
                pages_done += 1
                tq_elem.update(1)
                tq_elem.total = pages_done + len(wikiQueue)

asyncio.run(main())