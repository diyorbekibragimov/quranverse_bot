import requests
from config import BASE_URL as base
from config import verses_per_page, chapters_per_page

def get_verse(key, language="en"):
    translation = 0 # for now = undefined
    if language == "en":
        translation = 22 # Yusuf Ali - id=22
    elif language == "ru":
        translation = 45 # Russian Translation (Elmir Kuliev) - id=45
    url = base + f"/verses/by_key/{key}?language={language}&words=true&translations={translation}"
    r = requests.get(url=url)
    data = r.json()
    verse = data["verse"]["translations"][0]["text"]
    return verse

def get_list_of_chapters(page_number, language="en"):
    """
        There can be only 8 pages because 114 (all chapters) / 15 (number of displayed chapters per page) ~= 8 pages
    """
    url = base + f"/chapters?language={language}"
    r = requests.get(url=url)
    data = r.json()

    start = chapters_per_page*(page_number-1)
    chapters = data["chapters"][start:(page_number*chapters_per_page)]
    context = ""

    for chapter in chapters:
        number = chapter["id"]
        name = chapter["name_simple"]
        translated_name = chapter["translated_name"]["name"]
        verses = chapter["verses_count"]
        context += f"<b>{number}.</b> {name} | {translated_name} ({verses})\n"

    return context

def get_chapter_name(chapter_id, language="en"):
    translation = 0 # for now = undefined
    if language == "en":
        translation = 22 # Yusuf Ali - id=22
    elif language == "ru":
        translation = 45 # Russian Translation (Elmir Kuliev) - id=45
    url = base + f"/chapters/{chapter_id}?language={language}"
    r = requests.get(url=url)
    data = r.json()
    name_simple = data["chapter"]["name_simple"]
    name_arabic = data["chapter"]["name_arabic"]
    context = f"<b>{name_simple} | {name_arabic}</b>"
    return context

def get_chapter(chapter_id, page_number, language="en"):
    translation = 0 # for now = undefined
    if language == "en":
        translation = 22 # Yusuf Ali - id=22
    elif language == "ru":
        translation = 45 # Russian Translation (Elmir Kuliev) - id=45

    url = base + f"/verses/by_chapter/{chapter_id}?language={language}&words=true&page={page_number}&per_page={verses_per_page}&translations={translation}"
    r = requests.get(url=url)
    data = r.json()
    verses = data["verses"]
    chapter_name = get_chapter_name(chapter_id, language)
    context = f"{chapter_name}\n\n"
    for i in range(verses_per_page):
        try:
            context += f"<b>{verses_per_page*(page_number-1)+i+1}.</b> {verses[i]['translations'][0]['text']}\n"
        except:
            break

    return context

def get_number_of_pages(chapter_number):
    url = base + f"/chapters/{chapter_number}"
    r = requests.get(url=url)
    data = r.json()
    chapter = data["chapter"]
    verses_count = int(chapter['verses_count'])
    pages_count = verses_count // verses_per_page
    return pages_count + 1