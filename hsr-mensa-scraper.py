from scraper import classes
from scraper import scraper


def print_menu(sites):
    for site in sites:
        print('=== Menu for Site ' + site.name.value + ' ===')
        for weekday in ['Mo', 'Di', 'Mi', 'Do', 'Fr']:
            print('== ' + weekday + ' ==')
            if weekday in site.days:
                day = site.days[weekday]
                for menu in day.menus:
                    print(menu.title + ': ' + menu.description)
            else:
                print('(no menu')


def main():
    sites = [
        classes.Site('http://hochschule-rapperswil.sv-restaurant.ch/de/menuplan/mensa/', classes.SiteType.MENSA),
        classes.Site('http://hochschule-rapperswil.sv-restaurant.ch/de/menuplan/forschungszentrum/',
                     classes.SiteType.FORSCHUNGSZENTRUM)
    ]

    for site in sites:
        scraper.scrap_site(site)
    print_menu(sites)


if __name__ == "__main__":
    main()
