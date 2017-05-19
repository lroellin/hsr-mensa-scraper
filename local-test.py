from scraper import classes
from scraper import scraper


def print_menu(sites):
    for site in sites:
        print('=== Menu for Site ' + site.site.value + ' ===')
        for day in site.days:
            print('== Menu for Day ' + day.weekday)
            for menu in day.menus:
                print(menu.title)
                print(menu.description)




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
