from enum import Enum

class Site(object):
    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.days = {}

class SiteType(Enum):
    MENSA = "Mensa"
    FORSCHUNGSZENTRUM = "Forschungszentrum"

class SiteDay(object):
    def __init__(self, name):
        self.name = name
        self.menus = []


class MenuItem(object):
    def __init__(self, title, description):
        self.title = title
        self.description = description
