class Site:
    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.days = {}


class SiteDay:
    def __init__(self, name):
        self.name = name
        self.menus = []


class MenuItem:
    def __init__(self, title, description):
        self.title = title
        self.description = description
