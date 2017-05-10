import logging
import requests
from bs4 import BeautifulSoup


class Sites:
    def __init__(self, url, name):
        self.url = url
        self.name = name

class MenuItem:
    def __init__(self, title, description):
        self.title = title
        self.description = description

def main():
    logging.basicConfig(level=logging.INFO)
    sites = [
        Sites('http://hochschule-rapperswil.sv-restaurant.ch/de/menuplan/mensa/', 'Mensa'),
        Sites('http://hochschule-rapperswil.sv-restaurant.ch/de/menuplan/forschungszentrum/', 'Forschungszentrum')
    ]

    for site in sites:
        logging.info("Loading site " + site.url)
        request = requests.get(site.url)
        data = request.text
        soup = BeautifulSoup(data, "html.parser")

        todayElements = soup.find('div', {'id': 'menu-plan-tab1'})
        for singleElement in todayElements.findAll('div', {'class': 'menu-item'}):
            print(singleElement.find('h2', {'class': 'menu-title'}).contents[0])
            print(singleElement.find('p', {'class': 'menu-description'}).contents[0])


if __name__ == "__main__":
    main()
