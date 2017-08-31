def extract_menu_day_elements(day, parent_element):
    return parent_element.find('div', {'id': 'menu-plan-tab' + str(day)})


def extract_menu_item(parent_element):
    return parent_element.findAll('div', {'class': 'menu-item'})


def extract_menu_title(parent_element):
    menu_title = parent_element.find('h2', {'class': 'menu-title'}).get_text()
    menu_title = menu_title.replace(u'\xAD', u'')
    return menu_title


def extract_menu_description(parent_element):
    menu_description = parent_element.find('p', {'class': 'menu-description'}).get_text()
    menu_description = menu_description.replace(u'\xAD', u'')
    return menu_description


def extract_weekdays_elements(parent_element):
    return parent_element.find('div', {'class': 'day-nav'})


def extract_single_day(day, parent_element):
    return parent_element.find('label', {'for': 'mp-tab' + str(day)})


def extract_weekday(parent_element):
    return parent_element.find('span', {'class': 'day'}).contents[0]


def extract_date(parent_element):
    return parent_element.find('span', {'class': 'date'}).contents[0]
