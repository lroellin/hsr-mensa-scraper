import logging
import requests
from scraper import classes
from scraper import extract
from bs4 import BeautifulSoup

def format_date(weekday, date):
    return weekday + ', ' + date;


def scrap_site(site):
    logging.info('Loading site ' + site.name)
    request = requests.get(site.url)
    data = BeautifulSoup(request.text, "html.parser")
    daysElements = extract.extract_weekdays_elements(data)

    for day in range(1, 6):
        logging.info('Scraping day number: ' + str(day))
        menu_elements = extract.extract_menu_day_elements(day, data)
        day_elements = extract.extract_single_day(day, daysElements)
        if menu_elements is not None and day_elements is not None:
            weekday = extract.extract_weekday(day_elements)
            today = classes.SiteDay(
                format_date(extract.extract_weekday(day_elements), extract.extract_date(day_elements)))
            logging.info('Current weekday: ' + today.name)
            for menu_element in extract.extract_menu_item(menu_elements):
                menuItem = classes.MenuItem(
                    extract.extract_menu_title(menu_element),
                    extract.extract_menu_description(menu_element)
                )
                logging.info('Found menu item ' + menuItem.title)
                today.menus.append(menuItem)
            logging.debug('Adding day ' + today.name)
            site.days[weekday] = today