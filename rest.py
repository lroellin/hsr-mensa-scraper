from flask import Flask
from flask_restful import Resource, Api, fields, marshal_with, abort
import datetime
import calendar
from scraper import classes
from scraper import scraper

app = Flask('hsr-mensa-scraper')

api = Api(app)

MenuItem_fields = {
    'title': fields.String,
    'description': fields.String
}

SiteDay_fields = {
    'weekday': fields.String,
    'date': fields.String,
    'menus': fields.List(fields.Nested(MenuItem_fields))
}

Site_fields = {
    'site': fields.String,
    'days': fields.List(fields.Nested(SiteDay_fields))
}

weekday_dict = {
    'mon': 'Mo',
    'tue': 'Di',
    'wed': 'Mi',
    'thu': 'Do',
    'fri': 'Fr'
}


def check_weekday(weekday):
    if weekday not in weekday_dict:
        abort(406, description='Invalid weekday')


def check_site(site):
    if site not in classes.SiteType.__members__:
        abort(406, description='Invalid sitename')


def get_today():
    weekdaynumber = datetime.datetime.today().weekday()
    if weekdaynumber >= 4:
        weekdaynumber = 4
    weekday = calendar.day_abbr[weekdaynumber]
    return weekday.lower()


class SingleSite(Resource):
    def __init__(self, sites):
        self.sites = sites

    @marshal_with(Site_fields)
    def get(self, sitename):
        check_site(sitename)
        for site in self.sites:
            if site.site.value == sitename:
                return site
        abort(404, description="This site was not found")


class AllSites(Resource):
    def __init__(self, sites):
        self.sites = sites

    @marshal_with(Site_fields, envelope='sites')
    def get(self):
        return self.sites


class SingleSiteSingleDay(Resource):
    def __init__(self, sites):
        self.sites = sites

    @marshal_with(Site_fields)
    def get(self, sitename, weekday):
        check_site(sitename)
        if weekday == 'today':
            weekday = get_today()
        check_weekday(weekday)
        german_weekday = weekday_dict[weekday]
        for site in self.sites:
            if site.site.value == sitename:
                for day in site.days:
                    if day.weekday == german_weekday:
                        returnSite = classes.Site(site.url, site.site)
                        returnSite.days.append(day)
                        return returnSite
                abort(404, description="No menu for this day!")
        abort(404, description="This site was not found")


class AllSiteSingleDay(Resource):
    def __init__(self, sites):
        self.sites = sites

    @marshal_with(Site_fields, envelope='sites')
    def get(self, weekday):
        returnSites = []
        if weekday == 'today':
            weekday = get_today()
        check_weekday(weekday)
        german_weekday = weekday_dict[weekday]
        for site in self.sites:
            for day in site.days:
                if day.weekday == german_weekday:
                    returnSite = classes.Site(site.url, site.site)
                    returnSite.days.append(day)
                    returnSites.append(returnSite)
        if returnSites:
            return returnSites
        else:
            abort(404, description="No menu for this day!")


def main():
    sites = [
        classes.Site('http://hochschule-rapperswil.sv-restaurant.ch/de/menuplan/mensa/', classes.SiteType.MENSA),
        classes.Site('http://hochschule-rapperswil.sv-restaurant.ch/de/menuplan/forschungszentrum/',
                     classes.SiteType.FORSCHUNGSZENTRUM)
    ]

    for site in sites:
        scraper.scrap_site(site)

    api.add_resource(SingleSite, '/site/<string:sitename>', resource_class_kwargs={'sites': sites})
    api.add_resource(AllSites, '/site/all', resource_class_kwargs={'sites': sites})
    api.add_resource(SingleSiteSingleDay, '/site/<string:sitename>/days/<string:weekday>',
                     resource_class_kwargs={'sites': sites})
    api.add_resource(AllSiteSingleDay, '/site/all/days/<string:weekday>',
                     resource_class_kwargs={'sites': sites})

    app.run(debug=True)


if __name__ == "__main__":
    main()
