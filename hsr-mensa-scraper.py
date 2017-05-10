import logging
import requests
from bs4 import BeautifulSoup


class Site:
    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.days = {}


class SiteDay:
    def __init__(self, name):
        self.name = name
        self.menus = []


class MenuItem:
    def __init__(self, title, description):
        self.title = title
        self.description = description


def extract_day_elements(day, element):
    return element.find('div', {'id': 'menu-plan-tab' + str(day)})


def extract_menu_item(element):
    return element.findAll('div', {'class': 'menu-item'})


def extract_menu_title(element):
    return element.find('h2', {'class': 'menu-title'}).contents[0]


def extract_menu_description(element):
    return element.find('p', {'class': 'menu-description'}).contents[0]


def scrap_HSR_site(site):
    logging.info("Loading site " + site.url)
    request = requests.get(site.url)
    data = request.text
    soup = BeautifulSoup(data, "html.parser")

    for i in range(1, 6):
        todayElements = extract_day_elements(i, soup)
        if todayElements is not None:
            today = SiteDay('Day ' + str(i))
            for singleElement in extract_menu_item(todayElements):
                menuItem = MenuItem(
                    extract_menu_title(singleElement),
                    extract_menu_description(singleElement)
                )
                today.menus.append(menuItem)
            site.days[i] = today


def print_menu(sites):
    for site in sites:
        print('=== Menu for Site ' + site.name + ' ===')
        for day in site.days.values():
            print('== ' + day.name + ' ==')
            for menu in day.menus:
                print(menu.title + ': ' + menu.description)


def main():
    logging.basicConfig(level=logging.INFO)
    sites = [
        Site('http://hochschule-rapperswil.sv-restaurant.ch/de/menuplan/mensa/', 'Mensa'),
        Site('http://hochschule-rapperswil.sv-restaurant.ch/de/menuplan/forschungszentrum/', 'Forschungszentrum')
    ]

    for site in sites:
        scrap_HSR_site(site)
    print_menu(sites)


if __name__ == "__main__":
    main()
