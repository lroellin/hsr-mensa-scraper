def extract_menu_day_elements(day, parentElement):
    return parentElement.find('div', {'id': 'menu-plan-tab' + str(day)})


def extract_menu_item(parentElement):
    return parentElement.findAll('div', {'class': 'menu-item'})


def extract_menu_title(parentElement):
    menu_title = parentElement.find('h2', {'class': 'menu-title'}).get_text()
    menu_title = menu_title.replace(u'\xAD', u'')
    return menu_title


def extract_menu_description(parentElement):
    menu_description = parentElement.find('p', {'class': 'menu-description'}).get_text()
    menu_description = menu_description.replace(u'\xAD', u'')
    return menu_description


def extract_weekdays_elements(parentElement):
    return parentElement.find('div', {'class': 'day-nav'})


def extract_single_day(day, parentElement):
    return parentElement.find('label', {'for': 'mp-tab' + str(day)})


def extract_weekday(parentElement):
    return parentElement.find('span', {'class': 'day'}).contents[0]


def extract_date(parentElement):
    return parentElement.find('span', {'class': 'date'}).contents[0]