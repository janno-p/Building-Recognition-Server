from google.appengine.ext import ndb


def app_key():
    return ndb.Key('Application', 'Building Recognition')


class User(ndb.Model):
    username = ndb.StringProperty(indexed=True)


class BuildingTag(ndb.Model):
    username = ndb.StringProperty(indexed=True)
    building = ndb.IntegerProperty(indexed=True)
    name = ndb.StringProperty()
