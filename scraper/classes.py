from enum import Enum
import json


class Site(json.JSONEncoder):
    def __init__(self, url, site):
        super().__init__()
        self.url = url
        self.site = site
        self.days = []

    def default(self, obj):
        if (isinstance(obj, Site)):
            return obj.__dict__


class SiteType(Enum):
    MENSA = "mensa"
    FORSCHUNGSZENTRUM = "forschungszentrum"


class SiteDay(json.JSONEncoder):
    def __init__(self, weekday, date):
        super().__init__()
        self.weekday = weekday
        self.date = date
        self.menus = []

    def default(self, obj):
        if (isinstance(obj, SiteDay)):
            return obj.__dict__


class MenuItem(json.JSONEncoder):
    def __init__(self, title, description):
        super().__init__()
        self.title = title
        self.description = description

    def default(self, obj):
        if (isinstance(obj, MenuItem)):
            return obj.__dict__
