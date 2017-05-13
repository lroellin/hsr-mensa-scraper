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

sites = []


def check_weekday(weekday):
    if weekday not in weekday_dict:
        abort(406, description='Invalid weekday')


def check_site(site):
    if site not in ['mensa', 'forschungszentrum']:
        abort(406, description='Invalid sitename')


def get_today():
    weekdaynumber = datetime.datetime.today().weekday()
    if weekdaynumber >= 4:
        weekdaynumber = 4
    weekday = calendar.day_abbr[weekdaynumber]
    return weekday.lower()


def update_sites():
    global lastUpdate
    global sites
    if lastUpdate < datetime.datetime.now() - datetime.timedelta(minutes=1):
        sites = [
            classes.Site('http://hochschule-rapperswil.sv-restaurant.ch/de/menuplan/mensa/', classes.SiteType.MENSA),
            classes.Site('http://hochschule-rapperswil.sv-restaurant.ch/de/menuplan/forschungszentrum/',
                         classes.SiteType.FORSCHUNGSZENTRUM)
        ]
        for site in sites:
            scraper.scrap_site(site)
            if len(site.days) < 1:
                abort(503,
                      description='There are no upcoming days on the website (normal on a weekend). '
                                  'If a manual check proves otherwise, please file an issue at github.com/lroellin/hsr-mensa-scraper. '
                                  'URL: ' + site.url)
        print('Updating sites...')
        lastUpdate = datetime.datetime.now()


class SingleSite(Resource):
    @marshal_with(Site_fields)
    def get(self, sitename):
        update_sites()
        check_site(sitename)
        for site in sites:
            if site.site.value == sitename:
                return site
        abort(404, description="This site was not found")


class AllSites(Resource):
    @marshal_with(Site_fields, envelope='sites')
    def get(self):
        update_sites()
        return sites


class SingleSiteSingleDay(Resource):
    @marshal_with(Site_fields)
    def get(self, sitename, weekday):
        update_sites()
        check_site(sitename)
        if weekday == 'today':
            weekday = get_today()
        check_weekday(weekday)
        german_weekday = weekday_dict[weekday]
        for site in sites:
            if site.site.value == sitename:
                for day in site.days:
                    if day.weekday == german_weekday:
                        returnSite = classes.Site(site.url, site.site)
                        returnSite.days.append(day)
                        return returnSite
                abort(404, description="No menu for this day!")
        abort(404, description="This site was not found")


class AllSiteSingleDay(Resource):
    @marshal_with(Site_fields, envelope='sites')
    def get(self, weekday):
        update_sites()
        returnSites = []
        if weekday == 'today':
            weekday = get_today()
        check_weekday(weekday)
        german_weekday = weekday_dict[weekday]
        for site in sites:
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
    global lastUpdate
    lastUpdate = datetime.datetime.fromtimestamp(0)

    api.add_resource(SingleSite, '/site/<string:sitename>')
    api.add_resource(AllSites, '/site/all')
    api.add_resource(SingleSiteSingleDay, '/site/<string:sitename>/days/<string:weekday>')
    api.add_resource(AllSiteSingleDay, '/site/all/days/<string:weekday>')

    app.run()


if __name__ == "__main__":
    main()
