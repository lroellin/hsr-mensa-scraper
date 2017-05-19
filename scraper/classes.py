from enum import Enum
import json


class Site():
    def __init__(self, url, site):
        super().__init__()
        self.url = url
        self.site = site
        self.days = []


class SiteType(Enum):
    MENSA = "mensa"
    FORSCHUNGSZENTRUM = "forschungszentrum"


class SiteDay():
    def __init__(self, weekday, date):
        super().__init__()
        self.weekday = weekday
        self.date = date
        self.menus = []


class MenuItem():
    def __init__(self, title, description):
        super().__init__()
        self.title = title
        self.description = description
