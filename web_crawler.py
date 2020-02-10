import requests
from bs4 import BeautifulSoup
import time

wiki_domain = 'https://en.wikipedia.org'
user_input = input('What topic would you like to start from?\n')
starting_page = wiki_domain + '/wiki/' + user_input.replace(' ', '_')
list_of_pages = [starting_page]

def find_first_link(current_page):
    first_link = ''
    response = requests.get(current_page)
    response_text = response.text
    soup = BeautifulSoup(response_text, 'html.parser')
    content_div = soup.find(class_='mw-parser-output')
    for any_tag in content_div.find_all('p', recursive=False):
        if any_tag.find('a', recursive=False):
            first_link = any_tag.find('a', recursive=False).get('href')
            first_link = wiki_domain + first_link
            break
    return first_link

def continue_crawl(search_history, target_url, max_steps=25):
    if search_history[-1] == target_url:
        print(search_history[-1])
        print("We've arrived at our desired destination")
        return False
    elif search_history[-1] in search_history[:-1]:
        print("We're in a loop")
        return False
    elif len(search_history) > max_steps:
        print("I'm tired of searching")
        return False
    else:
        return True

while continue_crawl(list_of_pages, 'https://en.wikipedia.org/wiki/Science', 20):
    print(list_of_pages[-1])
    first_link = find_first_link(list_of_pages[-1])
    list_of_pages.append(first_link)
    time.sleep(2)
