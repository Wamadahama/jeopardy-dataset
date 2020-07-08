import requests 
import re
import itertools
import math
import pprint as p 
import csv
from bs4 import BeautifulSoup

BASE_URL = "http://www.j-archive.com/"
SEASON_LIST_URL = BASE_URL + "listseasons.php"
GAME_PAGE_URL = BASE_URL + "showgame.php?game_id=" # game_id is iterable 

DATASET_FILE =  "jeopardy_dataset.csv"
METADATA_FILE = "jeopardy_dataset.info"


def get_page(url):
    return requests.get(url).text

def get_latest_game_id():
    season_list = BeautifulSoup(get_page(SEASON_LIST_URL), 'html.parser')
    latest_season = BeautifulSoup(get_page(BASE_URL + season_list.find_all('tr')[0].a['href']), 'html.parser')
    latest_show = latest_season.find_all('tr')[0]
    last_id = latest_show.a['href'].split("?")[1].split("=")[1]
    return last_id

def read_metadata():
    with open(METADATA_FILE, "r") as f:
        text = f.read()
        lines = text.split("\n")
        if len(lines) <= 1:
            return 0, ""
        else:
            return lines[1].split(" ")[0], lines[1].split(" ")[1 ]


# maybe do a single episode_to_csv function
def episodes_to_csv(tuple_set):
    with open(DATASET_FILE, 'w', newline='') as dataset_file:
        writer = csv.writer(dataset_file, delimiter=',')
        writer.writerow(["Category", "Value", "Order", "Question", "Answer"])
        for tpl in tuple_set:
            writer.writerow(tpl)
            

def scrape_table(table_dom):

    if table_dom is None:
        return []

    categories = [rnd.text for rnd in table_dom.select(".category .category_name")]
    values =     [val.text for val in table_dom.find_all(class_=re.compile("clue_value*"))]
    orders =     [order.text for order in table_dom.select(".clue_header .clue_order_number")]
    questions =  [clue_text.text for clue_text in table_dom.select(".clue .clue_text")]

    category_count = math.ceil(len(values) / len(categories))
    categories_full =  itertools.repeat(categories, category_count)
    categories_full = itertools.chain(*categories_full)

    # Answers are inside onclick events : 
    #onmouseover="toggle('clue_J_2_1', 'clue_J_2_1_stuck', '<em class=&quot;correct_response&quot;><i>Misery</i></em><br /><br /><table width=&quot;100%&quot;><tr><td class=&quot;right&quot;>Dan</td></tr></table>')"

    answers = []
    loc = 0 # need track where we are so we can add nulls to missing fields  
    for answer in table_dom.select('.clue'):
        if answer.div is not None:
            html_text = answer.div["onmouseover"].split(',')[2]
            temp_answer = BeautifulSoup(html_text, 'html.parser')
            if temp_answer.em is None: # no answer
                answers.append("") 
            else:
                answers.append(temp_answer.em.text)
        else:
            answers.append("")
            values.insert(loc, "")
            orders.insert(loc, "")
            questions.insert(loc, "")
        loc +=1

    return list(zip(categories_full, values, orders, questions, answers))

def scrape_episode(id):
    # id = jeopardy_round
    first_round = BeautifulSoup(get_page(GAME_PAGE_URL + str(id)), 'html.parser').find(id='jeopardy_round')

    if first_round is None:
        return []

    first_round = scrape_table(first_round.table)

    second_round = BeautifulSoup(get_page(GAME_PAGE_URL + str(id)), 'html.parser').find(id = 'double_jeopardy_round')

    if second_round is None:
        return [] 

    second_round = scrape_table(second_round.table)

    final_set = sorted(list(itertools.chain(*[first_round, second_round])),key = lambda x: x[0])
    return final_set

def scrape_all(latest_id = 0, dataset_file = DATASET_FILE, metadata_file = METADATA_FILE):
    print("Starting j-archive scrape, latest game id = {}".format(latest_id))

    episodes = []
    for i in range(1, latest_id):
        print("\r Scraping {} [{}/{}]".format(GAME_PAGE_URL + str(i) , str(i), str(latest_id)), end="")
        episodes.append(scrape_episode(i))

    episodes_to_csv(list(itertools.chain(*episodes)))

def main():
    last_id, _ = read_metadata()
    latest_id = int(get_latest_game_id())
    if last_id == latest_id:
        print("No new episodes to scrape")
        return 
    else:
        scrape_all(latest_id)


main()
