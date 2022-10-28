from bs4 import BeautifulSoup
import requests
import unicodedata
from html import unescape
import re
import json


def get_schedule(as_object = True):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }


    uri = "https://schedule.nspu.ru/group_index.php?dep=5"
    page = requests.get(uri, headers)
    soup = BeautifulSoup(page.content, "html.parser")

    uri = soup.select_one("a:-soup-contains('3.022.2.21')")["href"]
    page = requests.get(f"https://schedule.nspu.ru/{uri}", headers)
    soup = BeautifulSoup(page.content, "lxml")


    last_change = soup.select('small:-soup-contains("Последнее изменение расписания")')[0]
    last_change = last_change.text.split("-")[1].strip()


    soup = soup.select("table.rasp_table")
    for i in soup:
        #if i.find_all(text="Знаменатель" or i.find_all(text="Числитель")):
        if ("Числитель" in str(i)):
            new_soup = i
            break

    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    new_soup = unicodedata.normalize("NFKC", unescape(new_soup.text.replace("\r", "")))


    split_string = re.split(r"Понедельник|Вторник|Среда|Четверг|Пятница|Суббота", new_soup)
    split_string = split_string[1::]


    schedule = {}
    for day in days:
        schedule[day] = {}


    for day_num, i in enumerate(split_string):

        lessons = re.split(r"[0-2]?[0-9]*:[0-6][0-9]-[0-2]?[0-9]*:[0-6][0-9]", i)
        lesson_starts = re.findall(r"[0-2]?[0-9]*:[0-6][0-9]-[0-2]?[0-9]*:[0-6][0-9]", i)
        temp_lessons = []
        for i in lessons:
            if i.isspace() or len(i) == 0:
                pass
            else:
                i = i.strip().split(";")
                temp_lessons.append(i)
        lessons = temp_lessons.copy()
        del temp_lessons
        #print(lessons)
        #print(lesson_starts)
        #print()

        for time, lesson in zip(lesson_starts, lessons):
            schedule[days[day_num]][time] = lesson
        schedule["last_update"] = last_change


    if as_object:
        return schedule
    else:
        with open("timetable.json", "w") as f:
            json.dump(schedule, f, indent=4, ensure_ascii=False)
        return True