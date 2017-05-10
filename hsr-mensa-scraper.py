import logging
from scraper import classes
from scraper import scraper


def print_menu(sites):
    for site in sites:
        print('=== Menu for Site ' + site.name + ' ===')
        for weekday in ['Mo', 'Di', 'Mi', 'Do', 'Fr']:
            print('== ' + weekday + ' ==')
            if weekday in site.days:
                day = site.days[weekday]
                for menu in day.menus:
                    print(menu.title + ': ' + menu.description)
            else:
                print('(no menu')


def main():
    logging.basicConfig(level=logging.INFO)
    sites = [
        classes.Site('http://hochschule-rapperswil.sv-restaurant.ch/de/menuplan/mensa/', 'Mensa'),
        classes.Site('http://hochschule-rapperswil.sv-restaurant.ch/de/menuplan/forschungszentrum/',
                     'Forschungszentrum')
    ]

    for site in sites:
        scraper.scrap_site(site)
    print_menu(sites)


if __name__ == "__main__":
    main()
