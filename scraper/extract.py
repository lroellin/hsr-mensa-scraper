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