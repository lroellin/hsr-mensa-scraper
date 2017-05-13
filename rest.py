from flask import Flask
from flask_restful import Resource, Api, fields, marshal_with, abort, request
import datetime
import calendar
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from scraper import classes
from scraper import scraper

application = Flask('hsr-mensa-scraper')

api = Api(application)

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
    logging.info("last update: " + str(lastUpdate))
    if lastUpdate < datetime.datetime.now() - datetime.timedelta(hours=1):
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
        logging.info("Updating sites")
        lastUpdate = datetime.datetime.now()
    else:
        logging.info('No need to update')


class SingleSite(Resource):
    @marshal_with(Site_fields)
    def get(self, sitename):
        logging.info('Request for Single site, sitename: ' + sitename)
        update_sites()
        check_site(sitename)
        for site in sites:
            if site.site.value == sitename:
                return site
        abort(404, description="This site was not found")


class AllSites(Resource):
    @marshal_with(Site_fields, envelope='sites')
    def get(self):
        logging.info('Request for All sites')
        update_sites()
        return sites


class SingleSiteSingleDay(Resource):
    @marshal_with(Site_fields)
    def get(self, sitename, weekday):
        logging.info('Request for Single Site Single Day, sitename: ' + sitename + ', weekday: ' + weekday)
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
        logging.info('Request for All Sites Single Day, weekday: ' + weekday)
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
    filename = "logs/access.log"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    fileHandler = TimedRotatingFileHandler(filename, when='midnight', backupCount=365)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s: %(message)s',
                        datefmt='%m-%d (%a) %H:%M:%S',
                        handlers=[fileHandler]
                        )
    global lastUpdate
    lastUpdate = datetime.datetime.fromtimestamp(0)

    api.add_resource(AllSites, '/sites/all')
    api.add_resource(AllSiteSingleDay, '/sites/all/days/<string:weekday>')
    api.add_resource(SingleSite, '/sites/<string:sitename>')
    api.add_resource(SingleSiteSingleDay, '/sites/<string:sitename>/days/<string:weekday>')

    application.run(debug=True, host='0.0.0.0', port=5000)

@application.errorhandler(404)
def page_not_found(error):
    return 'This route does not exist {}'.format(request.url), 404

if __name__ == "__main__":
    main()
