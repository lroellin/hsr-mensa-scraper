import calendar
import datetime
import logging
import os
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, redirect
from flask_restful import Resource, Api, fields, marshal_with, abort, output_json
from flask_compress import Compress

from scraper import classes
from scraper import scraper


class UnicodeApi(Api):
    """
    from here: https://github.com/flask-restful/flask-restful/issues/552
    """

    def __init__(self, *args, **kwargs):
        super(UnicodeApi, self).__init__(*args, **kwargs)
        self.app.config['RESTFUL_JSON'] = {
            'ensure_ascii': False
        }
        self.representations = {
            'application/json; charset=utf-8': output_json
        }


application = Flask('hsr-mensa-scraper')
Compress(application)

api = UnicodeApi(application)

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
            # noinspection PyBroadException
            try:
                scraper.scrap_site(site)
            except:
                abort(503,
                      description='Uh-oh, scraping broke'
                                  'Please file an issue at github.com/lroellin/hsr-mensa-scaper')

            if len(site.days) < 1:
                abort(503,
                      description='There are no upcoming days on the website (normal on a weekend). '
                                  'If a manual check proves otherwise, please file an issue '
                                  'at github.com/lroellin/hsr-mensa-scraper. '
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
                        return_site = classes.Site(site.url, site.site)
                        return_site.days.append(day)
                        return return_site
                abort(404, description="No menu for this day!")


class AllSiteSingleDay(Resource):
    @marshal_with(Site_fields, envelope='sites')
    def get(self, weekday):
        logging.info('Request for All Sites Single Day, weekday: ' + weekday)
        update_sites()
        return_sites = []
        if weekday == 'today':
            weekday = get_today()
        check_weekday(weekday)
        german_weekday = weekday_dict[weekday]
        for site in sites:
            for day in site.days:
                if day.weekday == german_weekday:
                    return_site = classes.Site(site.url, site.site)
                    return_site.days.append(day)
                    return_sites.append(return_site)
        if return_sites:
            return return_sites
        else:
            abort(404, description="No menu for this day!")


@application.route('/')
def hello():
    return redirect("http://www.dreami.ch/hsr-mensa-scraper/", code=302)


def main():
    application.run(debug=True, host='0.0.0.0', port=5000)


filename = "logs/access.log"
os.makedirs(os.path.dirname(filename), exist_ok=True)
fileHandler = TimedRotatingFileHandler(filename, when='midnight', backupCount=365)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(message)s',
                    datefmt='%m-%d (%a) %H:%M:%S',
                    handlers=[fileHandler]
                    )

lastUpdate = datetime.datetime.fromtimestamp(0)

VERSION_1 = '/v1'
ALL_SITES = '/sites/all'
SINGLE_SITE = '/sites/<string:sitename>'
SINGLE_DAY = '/days/<string:weekday>'

# noinspection PyTypeChecker
api.add_resource(AllSites, VERSION_1 + ALL_SITES)
# noinspection PyTypeChecker
api.add_resource(AllSiteSingleDay, VERSION_1 + ALL_SITES + SINGLE_DAY)
# noinspection PyTypeChecker
api.add_resource(SingleSite, VERSION_1 + SINGLE_SITE)
# noinspection PyTypeChecker
api.add_resource(SingleSiteSingleDay, VERSION_1 + SINGLE_SITE + SINGLE_DAY)

if __name__ == "__main__":
    main()
