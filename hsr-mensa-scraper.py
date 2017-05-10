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


def extract_menu_day_elements(day, element):
    return element.find('div', {'id': 'menu-plan-tab' + str(day)})


def extract_menu_item(element):
    return element.findAll('div', {'class': 'menu-item'})


def extract_menu_title(element):
    return element.find('h2', {'class': 'menu-title'}).contents[0]


def extract_menu_description(element):
    return element.find('p', {'class': 'menu-description'}).contents[0]


def extract_weekdays_elements(element):
    return element.find('div', {'class': 'day-nav'})


def extract_single_day(day, element):
    return element.find('label', {'for': 'mp-tab' + str(day)})

def extract_weekday(element):
    return element.find('span', {'class': 'day'}).contents[0]

def extract_date(element):
    return element.find('span', {'class': 'date'}).contents[0]


def scrap_site(site):
    logging.info("Loading site " + site.url)
    request = requests.get(site.url)
    data = BeautifulSoup(request.text, "html.parser")
    daysElements = extract_weekdays_elements(data)

    for day in range(1, 6):
        menu_elements = extract_menu_day_elements(day, data)
        day_elements = extract_single_day(day, daysElements)
        if menu_elements is not None and day_elements is not None:

            today = SiteDay(extract_weekday(day_elements) + ", " + extract_date(day_elements))
            for menu_element in extract_menu_item(menu_elements):
                menuItem = MenuItem(
                    extract_menu_title(menu_element),
                    extract_menu_description(menu_element)
                )
                today.menus.append(menuItem)
            site.days[day] = today


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
        scrap_site(site)
    print_menu(sites)


if __name__ == "__main__":
    main()
