import logging
import requests
from bs4 import BeautifulSoup

class Sites:
    def __init__(self, url, name):
        self.url = url
        self.name = name

def main():
    logging.basicConfig(level=logging.INFO)
    sites = [
        Sites('http://hochschule-rapperswil.sv-restaurant.ch/de/menuplan/mensa/', 'Mensa'),
        Sites('http://hochschule-rapperswil.sv-restaurant.ch/de/menuplan/forschungszentrum/', 'Forschungszentrum')
    ]

    for site in sites:
        logging.info("Loading site " + site.url)
        request = requests.get(site.url)



if __name__ == "__main__":
    main()